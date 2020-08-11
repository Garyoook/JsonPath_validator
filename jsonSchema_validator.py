from jsonschema import validate

from json_validate_mapdata import generate_jsonObj_from_file

schema = generate_jsonObj_from_file("jsons/Schema.json")

sample = generate_jsonObj_from_file("jsons/szw.json")

validate(instance=sample, schema= schema)

