import json
import sys
import jsonpath

if __name__ == '__main__':
    inputfile = sys.argv[1]
    file0 = open(inputfile, 'r')
    lines = file0.readlines()
    jsonArr = []

    for line in lines:
        jsonArr.append(line)
    jsonStr = ''.join(jsonArr)
    json_obj = json.loads(jsonStr)

    file0.close()

    len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(len0):
        len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(len1):
            results0 = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")[0]
            print(str(i) + "/" + str(j) + ":")
            print(results0)
            results1 = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")[0]
            print(results1)
            print('\n')
