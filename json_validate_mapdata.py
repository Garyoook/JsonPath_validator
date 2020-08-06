import json
import sys
import jsonpath


def validate(data, m, n):
    return (m, n) in data


# 生成一个Array，其含有valid "h" 的mapdata的index
def generate_valid_data_h(json_obj):
    valid_data_hs = []
    len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(len0):
        len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(len1):
            objType = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")[0]
            # print(objType)
            if objType == 'Extruded':
                valid_data_hs.append((i, j))
    return valid_data_hs


# 生成一个Array，其含有valid "color" 的mapdata的index
def generate_valid_data_color(json_obj):
    valid_data_colors = []
    len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(len0):
        len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(len1):
            objType = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")[0]
            type = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")[0]
            # print(objType)
            # print(type)
            if objType == 'Shape' and type == 'Polygon':
                valid_data_colors.append((i, j))
    return valid_data_colors


# 生成一个Array，其含有valid "src" 的mapdata的index
def generate_valid_data_src(json_obj):
    valid_data_srcs = []
    len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(len0):
        len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(len1):
            type = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")[0]
            # print(type)
            if type == 'Object':
                valid_data_srcs.append((i, j))
    return valid_data_srcs


# 从Json文件中获取json)_obj，传入给main用来验证。
def generate_jsonObj_from_file():
    inputfile = sys.argv[1]
    file0 = open(inputfile, 'r')
    lines = file0.readlines()
    jsonArr = []
    for line in lines:
        jsonArr.append(line)
    jsonStr = ''.join(jsonArr)
    json_obj = json.loads(jsonStr)
    file0.close()
    return json_obj


if __name__ == '__main__':
    json_obj = generate_jsonObj_from_file()
    valid_data_h = generate_valid_data_h(json_obj)
    valid_data_color = generate_valid_data_color(json_obj)
    valid_data_src = generate_valid_data_src(json_obj)

    # print(len(jsonpath.jsonpath(json_obj, "$.mapdata.0.15.data.features[*]")))
    # print(jsonpath.jsonpath(json_obj, "$.mapdata.0.15.data.features[1].properties.h"))

    # 外面i，j循环了mapdata中的"data"部分，
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            lenk = len(jsonpath.jsonpath(json_obj, "$.mapdata.0.15.data.features[*]"))
            for k in range(lenk):
                map = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                        ".data.features[" + str(k) + "].properties.map")
                if map:
                    result = True
                    error_msg = []
                    name = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                             ".data.features[" + str(k) + "].properties.name")
                    if name == False:
                        result = False
                        error_msg.append(
                            'ERROR: missing \"name\" at mapdata/{}/{}/data/features[{}]/properties/'.format(i, j, k))
                    print("found \"map\" value {} and \"name\" {} at"
                          " mapdata/{}/{}/data/features[{}]/properties/lpos! \nvalidating... {}\n{}\n"
                          .format(map, name, i, j, k, result, error_msg))

                # 当data中的feature包含"h"时， k循环了每一个具有"h"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                lpos = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                         ".data.features[" + str(k) + "].properties.lpos")
                if lpos:
                    result = True
                    error_msg = []
                    len_lpos = len(lpos[0])
                    name = ''
                    name2 = ''

                    if len_lpos == 1:
                        name = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                                 ".data.features[" + str(k) + "].properties.name")
                        if name == False:
                            result = False
                            error_msg.append(
                                'ERROR: missing \"name\" at mapdata/{}/{}/data/features[{}]/properties/'.format(i, j,
                                                                                                                k))
                        else:
                            error_msg = ''
                    elif len_lpos > 1:
                        name2 = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                                  ".data.features[" + str(k) + "].properties.name2")
                        if name2 == False:
                            result = False
                            error_msg.append(
                                'ERROR: missing \"name2\" at mapdata/{}/{}/data/features[{}]/properties/'.format(i, j,
                                                                                                                 k))
                        else:
                            error_msg = ''

                    print("found \"lpos\" value {} and \"name\" {} \"name2\" {} at"
                          " mapdata/{}/{}/data/features[{}]/properties/lpos! \nvalidating... {}\n{}\n"
                          .format(lpos, name, name2, i, j, k, result, error_msg))

                # 当data中的feature包含"h"时， k循环了每一个具有"h"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                h = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                      ".data.features[" + str(k) + "].properties.h")
                if h:
                    print("found \"h\" value {} at mapdata/{}/{}/data/features[{}]/properties/h! \nvalidating... {}\n"
                          .format(h, i, j, k, validate(valid_data_h, i, j)))

                # 当data中的feature包含"color"时， k循环了每一个具有"color"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                color = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                          ".data.features[" + str(k) + "].properties.color")
                if color:
                    print("found \"color\" value {} at mapdata/{}/{}/data/features[{}]/properties/color!"
                          " \nvalidating... {}\n".format(color, i, j, k, validate(valid_data_color, i, j)))

                # 当data中的feature包含"src"时， k循环了每一个具有"src"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                src = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                        ".data.features[" + str(k) + "].properties.src")
                if src:
                    ydir = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                             ".data.features[" + str(k) + "].properties.ydir")
                    xw = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                           ".data.features[" + str(k) + "].properties.xw")
                    error_msg = []
                    result = validate(valid_data_src, i, j)
                    if ydir == False:
                        result = False
                        error_msg.append(
                            'ERROR: missing \"ydir\" at mapdata/{}/{}/data/features[{}]/properties/'.format(i, j, k))
                    else:
                        error_msg = ''

                    if xw == False:
                        result = False
                        error_msg.append(
                            'ERROR: missing \"xw\" at mapdata/{}/{}/data/features[{}]/properties/'.format(i, j, k))
                    else:
                        error_msg = ''

                    print(
                        "found \"src\" value {} at mapdata/{}/{}/data/features[{}]/properties/src! \nvalidating... {}\n{}\n"
                            .format(src, i, j, k, result, error_msg))
