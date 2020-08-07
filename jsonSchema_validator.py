import json
from json_validate_mapdata import generate_jsonObj_from_file
from jsonschema import validate

schema = generate_jsonObj_from_file("Schema.json")

sample = generate_jsonObj_from_file("failure.json")

validate(instance=sample, schema= schema)

