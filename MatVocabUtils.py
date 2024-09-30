#!/usr/bin/env python

import requests

def check_dict_wrap_list(v,k):
    if k in v:
        if isinstance(v[k],list):
            None
        elif isinstance(v[k],dict):
            v[k] = [v[k]]
        else:
            print("type error")

def copy_class(id_,src_graph_dict,dest_graph_dict):
    dest_graph_dict[id_] = dict()
    dest_graph_dict[id_]["@id"] = id_
    #dest_graph_dict[id_]["@type"] = "rdfs:Class"

    try:
        dest_graph_dict[id_]["@type"] = src_graph_dict[id_]["@type"]
    except:
        print("problem with @type in", id_)

    try:
        dest_graph_dict[id_]["rdfs:label"] = src_graph_dict[id_]["rdfs:label"]
    except:
        print("problem with rdfs:label in", id_)

    try:
        dest_graph_dict[id_]["rdfs:comment"] = src_graph_dict[id_]["rdfs:comment"]
    except:
        print("problem with rdfs:comment in", id_)
    
    try:
        dest_graph_dict[id_]["rdfs:subClassOf"] = src_graph_dict[id_]["rdfs:subClassOf"]
    except:
        print("problem with rdfs:subClassOf in", id_)

    return None

def create_mat_class(dest_graph_dict,label,comment,subClassOf):
    id_ = "mat:"+label
    dest_graph_dict[id_] = dict()
    dest_graph_dict[id_]["@id"] = id_
    dest_graph_dict[id_]["@type"] = "rdfs:Class"
    dest_graph_dict[id_]["rdfs:label"] = label
    if comment:
        dest_graph_dict[id_]["rdfs:comment"] = comment
    if subClassOf:
        dest_graph_dict[id_]["rdfs:subClassOf"] = subClassOf
    return None

def copy_property(id_,src_graph_dict,dest_graph_dict):
    dest_graph_dict[id_] = dict()
    dest_graph_dict[id_]["@id"] = id_
    dest_graph_dict[id_]["@type"] = "rdf:Property"
    
    try:
        dest_graph_dict[id_]["rdfs:label"] = src_graph_dict[id_]["rdfs:label"]
    except:
        print("problem with rdfs:label in", id_)

    try:
        dest_graph_dict[id_]["rdfs:comment"] = src_graph_dict[id_]["rdfs:comment"]
    except:
        print("problem with rdfs:comment in", id_)
    
    try:
        dest_graph_dict[id_]["schema:domainIncludes"] = src_graph_dict[id_]["schema:domainIncludes"]
    except:
        print("problem with schema:domainIncludes in", id_)
    
    try:
        dest_graph_dict[id_]["schema:rangeIncludes"] = src_graph_dict[id_]["schema:rangeIncludes"]
    except:
        print("problem with schema:rangeIncludes in", id_)
    
    try:
        dest_graph_dict[id_]["rdfs:subPropertyOf"] = src_graph_dict[id_]["rdfs:subPropertyOf"]
    except:
        None

    return None

def create_mat_property(dest_graph_dict,label,comment,domainIncludes,rangeIncludes,subPropertyOf):
    id_ = "mat:"+label
    dest_graph_dict[id_] = dict()
    dest_graph_dict[id_]["@id"] = id_
    dest_graph_dict[id_]["@type"] = "rdf:Property"
    dest_graph_dict[id_]["rdfs:label"] = label
    if comment:
        dest_graph_dict[id_]["rdfs:comment"] = comment
    if domainIncludes:
        dest_graph_dict[id_]["schema:domainIncludes"] = domainIncludes
    if rangeIncludes:
        dest_graph_dict[id_]["schema:rangeIncludes"] = rangeIncludes
    if subPropertyOf:
        dest_graph_dict[id_]["rdfs:subPropertyOf"] = subPropertyOf
    return None

def remove_undefined_nodes(graph_dict):
    for k,v in graph_dict.items():
        check_dict_wrap_list(v,"rdfs:subClassOf")
        check_dict_wrap_list(v,"schema:domainIncludes")
        check_dict_wrap_list(v,"schema:rangeIncludes")
        check_dict_wrap_list(v,"rdfs:subPropertyOf")
    
    for k,v in graph_dict.items():
        if v["@type"] == "rdfs:Class":
            if "rdfs:subClassOf" in v:
                for parent_object in v["rdfs:subClassOf"]:
                    parent_name = parent_object["@id"]
                    if parent_name not in graph_dict:
                        print("Warning:",parent_name,"not found for",k)
        if v["@type"] == "rdf:Property":
            if "schema:domainIncludes" in v:
                new_list = list()
                for item in v["schema:domainIncludes"]:
                    item_name = item["@id"]
                    if item_name in graph_dict:
                        new_list.append(item)
                    else:
                        print("Removing", item_name, "from", k, "in domainIncludes")
                v["schema:domainIncludes"] = new_list
            if "schema:rangeIncludes" in v:
                new_list = list()
                for item in v["schema:rangeIncludes"]:
                    item_name = item["@id"]
                    if item_name in graph_dict:
                        new_list.append(item)
                    else:
                        print("Removing", item_name, "from", k,  "in rangeIncludes")
                v["schema:rangeIncludes"] = new_list
            if "rdfs:subPropertyOf" in v:
                for parent_object in v["rdfs:subPropertyOf"]:
                    parent_name = parent_object["@id"]
                    if parent_name not in graph_dict:
                        print("Warning:",parent_name,"not found for",k)
    return None

def get_schema_graph(url):
    graph = dict()
    r = requests.get(url)
    data = r.json()

    for item in data["@graph"]:
        graph[item["@id"]] = item


    for k,v in graph.items():
        check_dict_wrap_list(v,"rdfs:subClassOf")
        check_dict_wrap_list(v,"schema:domainIncludes")
        check_dict_wrap_list(v,"schema:rangeIncludes")
        check_dict_wrap_list(v,"rdfs:subPropertyOf")

    return graph