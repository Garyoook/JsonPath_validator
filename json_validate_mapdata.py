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


def generate_valid_poitype_indices(json_obj):
    poitype_indices = []
    len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(len0):
        len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(len1):
            poitype_indices.append(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".poitype")[0])
    return poitype_indices


def generate_valid_ctype(json_obj):
    ctypes = []
    len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(len0):
        len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(len1):
            ctypes.append(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".ctype")[0])
    return ctypes


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


def validate_poitype(json_obj):
    global i
    # validating poitype...
    poitype_indices = generate_valid_poitype_indices(json_obj)
    poitype_result = True
    for i in range(len(poitype_indices)):
        poitype = jsonpath.jsonpath(json_obj, "$.poitype.fuseMap[" + str(poitype_indices[i]) + "]")
        if not poitype:
            poitype_result = False
        else:
            poitype_result = True
        print('validated poitype number {}, matched with poitype/fuseMap/{}, {}'.format(poitype_indices[i], i,
                                                                                        poitype_result))
    print('\n')


def validate_ctype(json_obj):
    global i
    # validating ctype...
    ctype_list = generate_valid_ctype(json_obj)
    ctype_result = True
    for i in range(len(ctype_list)):
        ctype = jsonpath.jsonpath(json_obj, "$.poitype.colorMap[" + str(ctype_list[i]) + "]")
        if not ctype:
            ctype_result = False
        else:
            ctype_result = True
        print('validated ctype {}, matched with poitype/colorMap/{}, {}'.format(ctype_list[i], i, ctype_result))
    print('\n')


if __name__ == '__main__':
    json_obj = generate_jsonObj_from_file()
    valid_data_h = generate_valid_data_h(json_obj)
    valid_data_color = generate_valid_data_color(json_obj)
    valid_data_src = generate_valid_data_src(json_obj)

    validate_poitype(json_obj)

    validate_ctype(json_obj)

    # 外面i，j循环了mapdata中的"data"部分，
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):  # properties of mapdata is validated here:
            # validating type = 'Object' -> objType = 'Extruded'
            type = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")
            if type:
                if (type[0] == 'Object'):
                    result = True
                    error_msg = []
                    objType = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")[0]
                    if objType != 'Extruded':
                        result = False
                        error_msg.append('ERROR: missing \"objType\" at mapinfo/')
                    else:
                        error_msg = ''
                    print(
                        "found \"type\" value {} and \"objType\" \"{}\" at mapdata/{}/{}/texture! validating... {} {}"
                            .format(type, objType, i, j, result, error_msg))
    print('\n')

    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):  # properties of mapdata is validated here:
            # validate ground -> objType
            ground = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".ground")
            if ground:
                if (ground[0] == 1):
                    result = True
                    error_msg = []
                    objType = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")[0]
                    if objType != 'Extruded':
                        result = False
                        error_msg.append('ERROR: missing \"objType\" at mapinfo/')
                    else:
                        error_msg = ''
                    print(
                        "found \"ground\" value {} and \"objType\" \"{}\" at mapdata/{}/{}/texture! validating... {} {}"
                            .format(ground, objType, i, j, result, error_msg))
    print('\n')

    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):  # properties of mapdata is validated here:
            # validating texture...
            texture = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".texture")
            if texture:
                result = True
                error_msg = []
                texturesroot = jsonpath.jsonpath(json_obj, "$.mapinfo.texturesroot")
                if texturesroot == False:
                    result = False
                    error_msg.append(
                        'ERROR: missing \"texturesroot\" at mapinfo/')
                else:
                    error_msg = ''
                print("found \"texture\" value {} at mapdata/{}/{}/texture! and \"texturesroot\" {} at"
                      " mapinfo/texturesroot! validating... {} {}"
                      .format(texture, i, j, texturesroot, result, error_msg))
    print('\n')

    # loop for src validation:
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            # properties of mapdata/data/features is checked here:
            lenk = len(jsonpath.jsonpath(json_obj, "$.mapdata.0.15.data.features[*]"))
            for k in range(lenk):
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
                            'ERROR: missing \"ydir\" at mapdata/{}/{}/data/features[{}]/properties/'
                                .format(i, j, k))
                    else:
                        error_msg = ''

                    if xw == False:
                        result = False
                        error_msg.append(
                            'ERROR: missing \"xw\" at mapdata/{}/{}/data/features[{}]/properties/'
                                .format(i, j, k))
                    else:
                        error_msg = ''
                    print(
                        "found \"src\" value {} at mapdata/{}/{}/data/features[{}]/properties/src! validating... {} {}"
                            .format(src, i, j, k, result, error_msg))
    print('\n')

    # loop for validating h:
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            # properties of mapdata/data/features is checked here:
            lenk = len(jsonpath.jsonpath(json_obj, "$.mapdata.0.15.data.features[*]"))
            for k in range(lenk):
                # 当data中的feature包含"h"时， k循环了每一个具有"h"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                h = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                      ".data.features[" + str(k) + "].properties.h")
                if h:
                    print("found \"h\" value {} at mapdata/{}/{}/data/features[{}]/properties/h! validating... {}"
                          .format(h, i, j, k, validate(valid_data_h, i, j)))

                # 当data中的feature包含"color"时， k循环了每一个具有"color"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                color = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                          ".data.features[" + str(k) + "].properties.color")
                if color:
                    print("found \"color\" value {} at mapdata/{}/{}/data/features[{}]/properties/color!"
                          " validating... {}\n".format(color, i, j, k, validate(valid_data_color, i, j)))
    print('\n')

    # loop for validating map:
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            # properties of mapdata/data/features is checked here:
            lenk = len(jsonpath.jsonpath(json_obj, "$.mapdata.0.15.data.features[*]"))
            for k in range(lenk):
                # 当data中的feature包含"map"时， k循环了每一个具有"map"的"feature"， 并检查了所在"mapdata"层是否符合规定。
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
                            'ERROR: missing \"name\" at mapdata/{}/{}/data/features[{}]/properties/'.format(i, j,
                                                                                                            k))
                    print("found \"map\" value {} and \"name\" {} at"
                          " mapdata/{}/{}/data/features[{}]/properties/lpos! validating... {} {}"
                          .format(map, name, i, j, k, result, error_msg))
    print('\n')

    # loop for validating lpos:
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            # properties of mapdata/data/features is checked here:
            lenk = len(jsonpath.jsonpath(json_obj, "$.mapdata.0.15.data.features[*]"))
            for k in range(lenk):
                # 当data中的feature包含"lpos"时， k循环了每一个具有"lpos"的"feature"， 并检查了所在"mapdata"层是否符合规定。
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
                          " mapdata/{}/{}/data/features[{}]/properties/lpos! validating... {} {}"
                          .format(lpos, name, name2, i, j, k, result, error_msg))
