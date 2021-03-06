import os
import sys
from termcolor import colored
import download_jsondata

inputfile = sys.argv[1]

print(colored(
    "\n-----------------------------------------------------------------------------------------\n----------------------------",
    'green')
      + " Initiatiing Schema Validation "
      + colored(
    "------------------------------------------------\n------------------------------------------------------------------------------------------\n",
    'green'))

appcode = sys.argv[1]
download_jsondata.download(appcode)
inputfile = 'duodong/' + appcode + '.json'


os.system("java -jar jsonSchema_validate_mapdata.jar " + inputfile)

print(colored(
    "\n------------------------------------------------------------------------------------------\n----------------------------",
    'green')
      + " Initiatiing JsonPath Validation "
      + colored(
    "------------------------------------------------\n------------------------------------------------------------------------------------------\n",
    'green'))
inputfile_mapname = inputfile.split('.')[0].split('/')[1]
os.system("python3 jsonPath_validate_mapdata.py " + inputfile_mapname)

print(colored(
    "\n------------------------------------------------------------------------------------------\n----------------------------",
    'green')
      + " End of Validation "
      + colored(
    "--------------------------------------------------------\n------------------------------------------------------------------------------------------\n",
    'green'))
