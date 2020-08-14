import sys

from jsonschema import validate

from jsonPath_validate_mapdata import generate_jsonObj_from_file

target = sys.argv[1]
schema = sys.argv[2]

sample = generate_jsonObj_from_file(target)
schema = generate_jsonObj_from_file(schema)


validate(instance=sample, schema= schema)

