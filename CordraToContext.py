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

# Context Template
# [
#   {
#     "url": {
#       "@id": "schema:url",
#       "@type": "xsd:string"
#     }
#   }
# ]

def dPath(d, path):
    for k in path.strip("/").split("/"):
        if d:
            d = d.get(k)
        
    return d

G_classes = dict()
G_properties = dict()

for c in sorted(list(allRefs)):
    print(c)
    
    classNode = {
        "@id": f"schema:{c}"
    }
    
    if not inSchemaOrg(c):
        classNode = {
            "@id": f"mat:{c}"
        }
        
    G_classes[c] = classNode

    try:
        refs = [r for r in jsonSchemas[c]["allOf"] if "$ref" in r]
        refs = [r for r in refs if r["$ref"].split("/")[-1] not in ("CordraObjectID", c)]
        print(json.dumps(refs, indent=2))

    except:
        continue

    for ref in refs:
        
        with open(ref['$ref'].split("#")[0], "r") as f:
            data = json.load(f)
            data = dPath(data, ref["$ref"].split("#")[1])

        for pk, pv in data['properties'].items():
            
            propertyNode = {
                "@id": f"schema:{pk}"
            }

            if not inSchemaOrg(pk):
                propertyNode = {
                    "@id": f"mat:{pk}"
                }
                
            if 'items' in pv:
                pv = pv.get('items')
            
            # Check if reference
            r = dPath(pv, 'cordra/type/handleReference/types')
            
            if r:
                propertyNode['@type'] = "@id"
            elif ("url" in pk.lower()):
                propertyNode['@type'] = "schema:URL"
            elif ("date" in pk.lower()):
                propertyNode['@type'] = "xsd:date"
            elif (pv['type'] == 'string'):
                propertyNode['@type'] = "xsd:string"
            elif (pv['type'] == 'number'):
                propertyNode['@type'] = "xsd:decimal" 
            
            G_properties[pk] = propertyNode

    break


G = copy.deepcopy(G_classes) 
G.update(G_properties)


matContext = {
    "@context": {
        "mat": "https://pages.nist.gov/material-schema/",
        "mathub": "https://api.materialhub.org/objects/", 
        "schema": "http://schema.org/",
        "xsd": "https://www.w3.org/2001/XMLSchema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "broader": "skos:broader",
        "narrower": "skos:narrower",
        "related": "skos:related",
        "exactMatch": "skos:exactMatch",
        "closeMatch": "skos:closeMatch",
    }
}

matContext["@context"].update(G)

with open("context/matContext_auto.jsonld", "w+") as f:
    f.write(json.dumps(matContext, indent=2))




