#!/usr/bin/env python

import json
from MatVocabUtils import *

schema_graph_dict = get_schema_graph("https://schema.org/version/latest/schemaorg-current-https.jsonld")

mat_graph_dict = dict()

schema_classes = [
    "Action",
    "Boolean",
    "Collection",
    "Comment",
    "ComputerLanguage",
    "ConstraintNode",
    "CreativeWork",
    "DataCatalog",
    "DataDownload",
    "Dataset",
    "DataType",
    "Date",
    "DateTime",
    "DefinedTerm",
    "DefinedTermSet",
    "Duration",
    "Enumeration",
    "Float",
    "HowTo",
    "Intangible",
    "Integer",
    "ItemList",
    "ListItem",
    "MeasurementMethodEnum",
    "MeasurementTypeEnumeration",
    "MediaObject",
    "Number",
    "Observation",
    "Organization",
    "Person",
    "Place",
    "Product",
    "Project",
    "Property",
    "PropertyValue",
    "QualitativeValue",
    "QuantitativeValue",
    "Quantity",
    "SoftwareApplication",
    "SoftwareSourceCode",
    "StatisticalVariable",
    "StructuredValue",
    "Text",
    "Thing",
    "Time",
    "URL"
]

schema_properties = [
    "about",
    "accountablePerson",
    "address",
    "affiliation",
    "alternateName",
    "author",
    "brand",
    "citation",
    "collectionSize",
    "comment",
    "commentCount",
    "codeRepository",
    "constraintProperty",
    "contactPoint",
    "contentSize",
    "contentUrl",
    "contributor",
    "creator",
    "dataset",
    "dateCreated",
    "dateModified",
    "datePublished",
    "description",
    "distribution",
    "downloadUrl",
    "embedUrl",
    "encodingFormat",
    "estimatedCost",
    "exampleOfWork",
    "fileFormat",
    "funder",
    "hasDefinedTerm",
    "hasPart",
    "identifier",
    "image",
    "includedInDataCatalog",
    "inDefinedTermSet",
    "isBasedOn",
    "isPartOf",
    "item",
    "itemListElement",
    "keywords",
    "latitude",
    "learningResourceType",
    "license",
    "longitude",
    "marginOfError",
    "maintainer",
    "material",
    "materialExtent",
    "maxValue",
    "measurementDenominator",
    "measurementMethod",
    "measurementQualifier",
    "measurementTechnique",
    "member",
    "memberOf",
    "minValue",
    "name",
    "numConstraints",
    "numberOfItems",
    "observationAbout",
    "observationDate",
    "observationPeriod",
    "parentItem",
    "parentOrganization",
    "performTime",
    "populationType",
    "prepTime",
    "programmingLanguage",
    "provider",
    "propertyID",
    "publication",
    "publisher",
    "sameAs",
    "sha256",
    "statType",
    "step",
    "subjectOf",
    "subOrganization",
    "supply",
    "targetProduct",
    "telephone",
    "termCode",
    "text",
    "thumbnail",
    "thumbnailUrl",
    "tool",
    "totalTime",
    "uploadDate",
    "unitCode",
    "unitText",
    "url",
    "value",
    "valueReference",
    "variableMeasured",
    "workExample",
    "yield"
]

for schema_class in schema_classes:
    copy_class("schema:"+schema_class,schema_graph_dict,mat_graph_dict)

for schema_property in schema_properties:
    copy_property("schema:"+schema_property,schema_graph_dict,mat_graph_dict)

create_mat_class(
    mat_graph_dict,
    "Dataset",
    "An extended version of schema:Dataset for Materials Science and Engineering, which includes parameterControlled and conditionObserved.",
    [{"@id": "schema:Dataset"}]
)

create_mat_class(
    mat_graph_dict,
    "Experiment",
    "A grouping of datasets, materials, instrument, and other things that where used in a scientific procedure to test a hypothesis or reproduce previous results.",
    [{"@id": "mat:Dataset"}]
)

create_mat_class(
    mat_graph_dict,
    "Instrument",
    "An instrument in materials science and engineering may be a commercial off-the-shelf product or the one-off creation, which may also contain commercial off-the-shelf parts.",
    [{"@id": "schema:CreativeWork"},{"@id": "schema:Product"}]
)

create_mat_class(
    mat_graph_dict,
    "Material",
    "",
    [{"@id": "schema:CreativeWork"},{"@id": "schema:Product"}]
)

create_mat_class(
    mat_graph_dict,
    "PropertyValue",
    "An extended version of schema:PropertyValue for Materials Science and Engineering",
    [{"@id": "schema:PropertyValue"}]
)

create_mat_class(
    mat_graph_dict,
    "UnitOfMeasurement",
    "An extended version of schema:DefinedTerm for that allows for a unit of measurement to have an identifer and other relevant properties.",
    [{"@id": "schema:DefinedTerm"}]
)

create_mat_property(
    mat_graph_dict,
    "variableMeasured",
    "An extended version of schema:variableMeasured for Materials Science and Engineering",
    [{"@id":"mat:Dataset"},{"@id":"mat:PropertyValue"}],
    [{"@id":"mat:PropertyValue"},{"@id":"schema:DefinedTerm"}],
    None
)

create_mat_property(
    mat_graph_dict,
    "conditionObserved",
    "The conditionObserved property can indicate (repeated as necessary) the variables that are not controlled during the creation of a dataset but may impact the interpretation of the dataset.",
    [{"@id":"mat:Dataset"},{"@id":"mat:PropertyValue"}],
    [{"@id":"mat:PropertyValue"},{"@id":"schema:DefinedTerm"}],
    None
)

create_mat_property(
    mat_graph_dict,
    "parameterControlled",
    "The parameterControlled property can indicate (repeated as necessary) the variables that are controlled during the creation of a dataset that may impact the interpretation of the dataset.",
    [{"@id":"mat:Dataset"},{"@id":"mat:PropertyValue"}],
    [{"@id":"mat:PropertyValue"},{"@id":"schema:DefinedTerm"}],
    None
)

remove_undefined_nodes(mat_graph_dict)



mat_schema_extended = {
    "@context": {
        "schema": "https://schema.org/",
        "mat": "https://pages.nist.gov/material-schema/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "skos": "http://www.w3.org/2004/02/skos/core#"
    },
    "@graph": []
}

for k,v in mat_graph_dict.items():
    mat_schema_extended["@graph"].append(v)

with open('mat-schema-extended.json','w') as f:
    json.dump(mat_schema_extended, f, sort_keys=True, indent=4)





mat_schema = {
    "@context": {
        "schema": "https://schema.org/",
        "mat": "https://pages.nist.gov/material-schema/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "skos": "http://www.w3.org/2004/02/skos/core#"
    },
    "@graph": []
}

for k,v in mat_graph_dict.items():
    if "mat:" in v["@id"]:
        mat_schema["@graph"].append(v)

with open('mat-schema.json','w') as f:
    json.dump(mat_schema, f, sort_keys=True, indent=4)