**Map Data Validator (JsonSchema + JsonPath)**

Read this to get help with how to use `jsonSchema_validate_mapdata.jar`, `jsonSchema_validator.py` and `jsonPath_validate_mapdata.py`.
And how to run integrated validation `validate_all.py`.

`jsonSchema_validate_mapdata.jar`: 
This jar file is packaged from java to report all errors found in the target mapdata json file.
you can give 1 or 2 arguments to this jar file:
e.g: run  in terminal :
`jsonSchema_validate_mapdata.jar target.json`  
to validate the map data file 'taget.json" using default map schema.
Or, you can run :
`jsonSchema_validate_mapdata.jar target.json your_schrma.json` 
to validate with your own schema.



`jsonSchema_validator.py`: 
this py file is another tool to check errors with json schema using python. However, this can only report one error at a time.
Usage: run  in terminal `:
jsonSchema_validator.py target.json schema.json`



`jsonPath_validate_mapdata.py`:
This file is to validate mapdata using JsonPath, which is a powerful validation to the content and relationships between properties of map data.
Rules are specified inside this file.
Usage: run in terminal: 
`jsonPath_validate_mapdata target.json` 
to validate the target mapdata with yout rules in jsonPath.



`validate_all.py`:
This file is to run both `jsonSchema_validate_mapdata.jar` and `jsonPath_validate_mapdata.py`, to check both validations at the same time.
Usage: tun in terminal:
`validate_all.py target.json`
to validate this mapdata file using both json schema and jsonPath.