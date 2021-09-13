#!/usr/bin/env python
# coding: utf-8

import os
import json
import requests
import numpy as np
import copy

# Collect all schemas

def readJSON(fp):
    with open(fp, 'r') as f:
        return json.load(f)

jsonSchemas = {j['title']: j for j in [readJSON(fp) for fp in os.listdir('.') if fp[-5:]=='.json']}

allRefs = set()

for name, schema in jsonSchemas.items():
    currRefs = [ref for ref in schema['allOf'] if '$ref' in ref.keys()]
    
    for ref in currRefs:
        allRefs.add(ref['$ref'].split('/')[-1])
        

def updateLists(v1, v2):
    if not isinstance(v1, list):
        return v2
    if not isinstance(v2, list):
        return v2
    
    for v2i in v2:
        v1.append(v2i)
    
    return list(np.unique(v1))


def updateDicts(d1, d2):
    for k, v in d2.items():
        d1[k] = updateLists(d1.get(k), v)
        
        
def collapseListOfDicts(v):
    w = dict()
    
    for vi in v:
        k = vi["@id"]
        if k in w:
            updateDicts(w[k], vi)
        else:
            w[k] = vi
            
    return list(w.values())


inSchemaOrg = lambda name: requests.get(f'https://schema.org/{name}').status_code == 200

loc_main = "{0}.json".format
loc_def = "definition-schemas/{0}.json".format

# RDF Schema Template
# [
#     {
#         @id: mat:...,
#         @type: rdfs:Class OR rdfs:Property,
#         rdfs:label: ...,
#         rdfs:subClassOf: ...,
#         schema:domainIncludes: {
#             @id: ...
#         },
#         schema:rangeIncludes: {
#             @id: ...
#         }
#     }
# ]

def dPath(d, path):
    for k in path.strip("/").split("/"):
        if d:
            d = d.get(k)
        
    return d

G_classes = []
G_properties = []

for c in sorted(list(allRefs)):
    print(c)
    
    classNode = {
        "@id": f"schema:{c}",
        "@type": "rdfs:Class",
        "rdfs:label": c
    }
    
    if not inSchemaOrg(c):
        classNode = {
            "@id": f"mat:{c}",
            "@type": "rdfs:Class",
            "rdfs:label": c
        }
        
    try:
        refs = [r for r in jsonSchemas[c]["allOf"] if "$ref" in r]
        refs = [r for r in refs if r["$ref"].split("/")[-1] not in ("CordraObjectID", c)]
        print(json.dumps(refs, indent=2))

    except:
        continue

    superClasses = []

    for r in refs:
        name = r["$ref"].split("/")[-1]

        if inSchemaOrg(name):
            superClasses.append(f"schema:{name}")
        else:
            superClasses.append(f"mat:{name}")

    classNode["rdfs:subClassOf"] = superClasses

    propertyNodes = []

    for ref in refs:
        className = ref["$ref"].split("/")[-1]
        
        with open(ref['$ref'].split("#")[0], "r") as f:
            data = json.load(f)
            data = dPath(data, ref["$ref"].split("#")[1])

        for pk, pv in data['properties'].items():
            
            propertyNode = {
                "@id": f"schema:{pk}",
                "@type": "rdfs:Property",
                "rdfs:label": pk,
                "schema:domainIncludes": [className]
            }

            if not inSchemaOrg(pk):
                propertyNode = {
                    "@id": f"mat:{pk}",
                    "@type": "rdfs:Property",
                    "rdfs:label": pk,
                    "schema:domainIncludes": [className]
                }
                
            if 'items' in pv:
                pv = pv.get('items')
            
            r = dPath(pv, 'cordra/type/handleReference/types')
            
            if r:
                propertyNode['schema:rangeIncludes'] = r
                
                
            
            propertyNodes.append(propertyNode)

    G_classes.append(classNode)

    for propertyNode in propertyNodes:
        G_properties.append(propertyNode)


G = copy.deepcopy(G_classes) + collapseListOfDicts(G_properties)



G_mat = [g for g in G if "mat:" in g["@id"]]


# Thing, CreativeWork rule
## If Thing and Creativework in a subclass of property, replace with CreativeWork
def removeThing(v):
    return list(filter(lambda vi: vi!="schema:Thing", v))

for d in G_mat:
    v = d.get("rdfs:subClassOf", [])
    if "schema:Thing" in v and "schema:CreativeWork" in v:
        d["rdfs:subClassOf"] = removeThing(v)
            
            
print(json.dumps(G_mat, indent=2))


matSchemas = {
    "@context": {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "schema": "https://schema.org/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "mat": "https://pages.nist.gov/material-schema/"
    },
    "@graph": G
}

with open("RDF/material-schema_auto.jsonld", "w+") as f:
    f.write(json.dumps(matSchemas, indent=2))




