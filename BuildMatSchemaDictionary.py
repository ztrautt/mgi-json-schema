#!/usr/bin/env python

import json
from MatVocabUtils import *

with open('mat-schema-extended.json','r') as f:
    data = json.loads(f.read())

graph_dict = dict()

for item in data["@graph"]:
    graph_dict[item["@id"]] = item

for k,v in graph_dict.items():
    check_dict_wrap_list(v,"rdfs:subClassOf")
    check_dict_wrap_list(v,"schema:domainIncludes")
    check_dict_wrap_list(v,"schema:rangeIncludes")
    check_dict_wrap_list(v,"mat:domainIncludes")
    check_dict_wrap_list(v,"mat:rangeIncludes")

for k,v in graph_dict.items():
    if v["@type"] == "rdfs:Class":
        v["propertiesInclude"] = []

for k,v in graph_dict.items():
    if "schema:domainIncludes" in v:
        for item in v["schema:domainIncludes"]:
            graph_dict[item["@id"]]["propertiesInclude"].append({"@id":v["@id"]})

dictionary = dict()
dictionary["$schema"] = "http://json-schema.org/draft-07/schema#"
dictionary["$defs"] = dict()
defs = dictionary["$defs"]

defs["Date"] = {"title":"Date","type":"string","format":"date"}
defs["Boolean"] = {"title":"Boolean","type":"boolean"}
defs["DateTime"] = {"title":"DateTime","type":"string","format":"date-time"}
defs["Time"] = {"title":"Time","type":"string","format":"time"}
defs["Number"] = {"title":"Number","type":"number"}
defs["Float"] = {"title":"Float","type":"number"}
defs["Integer"] = {"title":"Integer","type":"number"}
defs["Text"] = {"title":"Text","type":"string"}
defs["ObjectLink"] = {
    "type":"object",
    "title": "ObjectLink",
    "properties":{
        "@type":{
            "title":"@type",
            "type":"string"},
            "@id":{"title":"@id","type":"string"}
            }
    }

skip_list = ["DataType"]

for k,v in graph_dict.items():
    label = None
    rdfType = v['@type']
    if "rdfs:label" in v:
        if isinstance(v["rdfs:label"], str):
            label = v["rdfs:label"]
        if isinstance(v["rdfs:label"], dict):
            label = v["rdfs:label"]["@value"]
        #print(label)
    else:
        print("no label in:",v)

    if label in defs.keys():
        continue

    if label in skip_list:
        continue

    if rdfType == "rdf:Property":
        if "schema:rangeIncludes" not in v:
            continue
        
        anyOfList = list()
        anyOfList.append({"$ref": "#/$defs/ObjectLink"})
        for rangeItem in v["schema:rangeIncludes"]:
            className = rangeItem["@id"].split(":")[1]
            anyOfList.append({"$ref": "#/$defs/"+className})
        
        defs[label] = {
            "oneOf":[
                {
                    "anyOf":anyOfList
                },
                {
                    "type": "array",
                    "items": {
                        "anyOf":anyOfList
                        }
                }
            ]
        }
    
    if rdfType == "rdfs:Class":
        numClassProperties = len(v["propertiesInclude"])
        if "rdfs:subClassOf" in v.keys():
            defs[label] = {"allOf": []}

            for parentClass in v["rdfs:subClassOf"]:
                parentLabel = parentClass["@id"].replace("schema:","")
                if parentLabel in skip_list:
                    continue
                defs[label]["allOf"].append({"$ref": "#/$defs/"+parentLabel})
            
            if numClassProperties > 0:
                classProperties = dict()
                classProperties["type"] = "object"
                classProperties["properties"] = dict()
                for pi in v["propertiesInclude"]:
                    pi_label = pi["@id"].split(":")[1]
                    classProperties["properties"][pi_label] = {"$ref": "#/$defs/"+pi_label}
                defs[label]["allOf"].append(classProperties)

        else:
            if numClassProperties > 0:
                defs[label] = dict()
                defs[label]["type"] = "object"
                defs[label]["properties"] = dict()
                properties = defs[label]["properties"]
                for pi in v["propertiesInclude"]:
                    pi_label = pi["@id"].split(":")[1]
                    properties[pi_label] = {"$ref": "#/$defs/"+pi_label}

with open('mat-dictionary.json','w') as f:
    json.dump(dictionary, f, sort_keys=True, indent=4)