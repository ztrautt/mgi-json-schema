var cordra = require('cordra');
var cordraUtil = require('cordraUtil');
var config = require('/cordra/schemas/Config');
var schema = require('/cordra/schemas/MaterialProperty.schema.json');

exports.beforeSchemaValidation = beforeSchemaValidation;
exports.objectForIndexing = objectForIndexing;
exports.onObjectResolution = onObjectResolution;

function beforeSchemaValidation(object, context) {
    if (!object.content['@id']) object.content['@id'] = "";
    object = config.staticMethods.getJSONLD(object, schema)
    delete object.content.metadata;
    return object;
}

function objectForIndexing(object, context) {
    object.content.metadata = object.metadata;
    return object;
}

function onObjectResolution(object, context) {
    object.content.metadata = object.metadata;
    return object;
}

