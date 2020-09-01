import json
import os
import sys

from termcolor import colored
import jsonpath
import download_jsondata


# main函数在本文件最下方
#
#


def validate(data, m, n):
    return (m, n) in data


# # 生成一个Array，其含有valid "h" 的mapdata的index
# def generate_valid_data_h(json_obj):
#     valid_data_hs = []
#     len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
#     for i in range(len0):
#         len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
#         for j in range(len1):
#             objType = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")
#             # print(objType)
#             if not objType:
#                 pass
#             elif objType[0] == 'Extruded' or 'Shape':
#                 valid_data_hs.append((i, j))
#     return valid_data_hs


# 生成一个Array，其含有valid "color" 的mapdata的index
def generate_valid_data_color(json_obj):
    valid_data_colors = []
    len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(len0):
        len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(len1):
            objType = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")
            if not objType:
                objType = ''
            type = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")[0]
            # print(objType)
            # print(type)
            if objType == 'Shape' and type == 'Polygon':
                valid_data_colors.append((i, j))
    return valid_data_colors


# # 生成一个Array，其含有valid "src" 的mapdata的index
# def generate_valid_data_src(json_obj):
#     valid_data_srcs = []
#     len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
#     for i in range(len0):
#         len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
#         for j in range(len1):
#             type = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")[0]
#             # print(type)
#             if type == 'Object':
#                 valid_data_srcs.append((i, j))
#     return valid_data_srcs


def generate_valid_poitype_indices(json_obj):
    poitype_indices = []
    len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(len0):
        len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(len1):
            poitype = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".poitype")
            if poitype:
                poitype_indices.append(poitype[0])
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
def generate_jsonObj_from_file(inputfile):
    # inputfile = sys.argv[1]
    inputfile = 'duodong/' + inputfile + '.json'
    file0 = open(inputfile, 'r', encoding='UTF-8')
    lines = file0.readlines()
    jsonArr = []
    for line in lines:
        jsonArr.append(line)
    jsonStr = ''.join(jsonArr)
    json_obj = json.loads(jsonStr)
    file0.close()
    return json_obj


def validate_poitype(json_obj):
    print(
        '------------ validating \'mapdata.图层属性.poitype的值必须是poitype.fuseMap中的一个键\'... ------------------------------------------------')
    # validating poitype...
    poitype_indices = generate_valid_poitype_indices(json_obj)
    poitype_result = True
    counter_total = counter_succ = counter_fail = 0
    for i in range(len(poitype_indices)):
        poitype = jsonpath.jsonpath(json_obj, "$.poitype.fuseMap[" + str(poitype_indices[i]) + "]")
        if not poitype:
            poitype_result = False
            counter_fail += 1
            counter_total += 1
            print(colored('cannot find poitype number {} in poitype/fusemap, {}'
                          .format(poitype_indices[i], poitype_result), 'red'))
        else:
            poitype_result = True
            counter_succ += 1
            counter_total += 1
            # print('validated poitype number {}, matched with poitype/fuseMap/{}, {}'.format(poitype_indices[i], i,
            #                                                                                 poitype_result))
    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def validate_ctype(json_obj):
    global i
    print(
        '------------ validating \'mapdata.图层属性.ctype的值必须是poitype.colorMap中的一个键\'... ------------------------------------------------')
    # validating ctype...
    ctype_list = generate_valid_ctype(json_obj)
    counter_total = counter_succ = counter_fail = 0
    for i in range(len(ctype_list)):
        ctype = jsonpath.jsonpath(json_obj, "$.poitype.colorMap[" + str(ctype_list[i]) + "]")
        if not ctype:
            ctype_result = False
            counter_fail += 1
            counter_total += 1
            print(colored('cannot find ctype {}, in keys of poitype/colorMap/{}, {}'
                          .format(ctype_list[i], i, ctype_result), 'red'))
        else:
            ctype_result = True
            counter_succ += 1
            counter_total += 1
            # print('validated ctype {}, matched with poitype/colorMap/{}, {}'.format(ctype_list[i], i, ctype_result))
    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def validate_type(json_obj):
    global leni, i, lenj, j, result, error_msg, objType
    print('------------ validating type = \'Object\' -> objType = \'Extruded\' ------------------------------------')
    # 外面i，j循环了mapdata中的"data"部分，
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    counter_total = counter_succ = counter_fail = 0
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
                        counter_fail += 1
                        counter_total += 1
                        error_msg.append('ERROR: missing \"objType\" at mapinfo/')
                    else:
                        error_msg = ''
                        counter_succ += 1
                        counter_total += 1

                    if result:
                        a = 0 # 无意义 只用作填充
                        # print("found \"type\" value {} and \"objType\" \"{}\" at mapdata/{}/{}/"
                        #       "texture! validating... {} {}".format(type, objType, i, j, result, error_msg))
                    else:
                        print(colored("found \"type\" value {} and \"objType\" \"{}\" at mapdata/{}/{}/"
                                      "texture! validating... {} {}".format(type, objType, i, j, result,
                                                                            '\n' + str(error_msg)), 'red'))
    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def validate_ground(json_obj):
    global leni, i, lenj, j, result, error_msg, objType
    print('------------ validating ground = 1 -> objType = \'Extruded\' ------------------------------------')
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    counter_total = counter_succ = counter_fail = 0
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):  # properties of mapdata is validated here:
            # validating ground = 1 -> objType = 'Extruded'
            ground = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".ground")
            if ground:
                if ground[0] == 1:
                    result = True
                    error_msg = []
                    objType = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")
                    if not objType or objType[0] != 'Extruded':
                        result = False
                        counter_fail += 1
                        counter_total += 1
                        error_msg.append("ERROR: incorrect \"objType\" {} at mapdata.".format(objType)
                                         + str(i) + "." + str(j) + ".objType")
                    else:
                        error_msg = ''
                        counter_succ += 1
                        counter_total += 1

                    if result:
                        a = 0
                        # print("found \"ground\" value {} and \"objType\" \"{}\" at mapdata/{}/{}/texture! "
                        #       "validating... {} {}".format(ground, objType[0], i, j, result, error_msg))
                    else:
                        print(
                            colored("found \"ground\" value {} and an incorrect \"objType\" at mapdata/{}/{}/texture! "
                                    "validating... {} {}".format(ground, i, j, result, ('\n' + str(error_msg))), 'red'))
    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def validate_texture(json_obj):
    global leni, i, lenj, j, result, error_msg
    print('------------ validating 如果mapdata.图层属性.texture 存在且不为空, '
          '则 mapinfo.texturesroot不能为空t... ------------------------------------')
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    counter_total = counter_succ = counter_fail = 0
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
                    counter_fail += 1
                    counter_total += 1
                    error_msg.append(
                        'ERROR: missing \"texturesroot\" at mapinfo/')
                else:
                    error_msg = ''
                    counter_succ += 1
                    counter_total += 1

                if result:
                    a = 0
                    # print("found \"texture\" value {} at mapdata/{}/{}/texture! and \"texturesroot\" {} at"
                    #       " mapinfo/texturesroot! validating... {} {}"
                    #       .format(texture, i, j, texturesroot, result, error_msg))
                else:
                    print(colored("found \"texture\" value {} at mapdata/{}/{}/texture! and \"texturesroot\" {} at"
                                  " mapinfo/texturesroot! validating... {} {}"
                                  .format(texture, i, j, texturesroot, result, ('\n' + str(error_msg))), 'red'))
    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def validate_src(json_obj):
    global leni, i, lenj, j, lenk, k, error_msg, result
    # loop for src validation:
    print('------------ validating src存在时，ydir与xw同时存在且有值&type为Object ------------------------------------------------')
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    counter_total = counter_succ = counter_fail = 0
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            # properties of mapdata/data/features is checked here:
            type = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")

            feature_content = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".data.features[*]")
            if feature_content:
                lenk = len(feature_content)
            else:
                lenk = 0
            for k in range(lenk):
                # 当data中的feature包含"src"时， k循环了每一个具有"src"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                src = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                        ".data.features[" + str(k) + "].properties.src")
                if src:
                    if src[0] == '':
                        break
                    ydir = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                             ".data.features[" + str(k) + "].properties.ydir")
                    xw = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                           ".data.features[" + str(k) + "].properties.xw")
                    error_msg = []
                    result = True
                    if ydir == False:
                        result = False
                        error_msg.append(
                            'ERROR: missing \"ydir\" at mapdata/{}/{}/data/features[{}]/properties/'
                                .format(i, j, k))
                        counter_fail += 1
                        counter_total += 1

                        if xw == False:
                            result = False
                            counter_fail += 1
                            counter_total += 1
                            error_msg.append(
                                'ERROR: missing \"xw\" at mapdata/{}/{}/data/features[{}]/properties/'
                                    .format(i, j, k))
                        else:
                            type = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")[0]
                            if type == 'Object':
                                counter_succ += 1
                                counter_total += 1
                            else:
                                result = False
                                counter_fail += 1
                                counter_total += 1
                                error_msg.append(
                                    'ERROR: missing \"xw\" at mapdata/{}/{}/data/features[{}]/properties/'
                                        .format(i, j, k))

                    else:
                        if xw == False:
                            result = False
                            counter_fail += 1
                            counter_total += 1
                            error_msg.append(
                                'ERROR: missing \"xw\" at mapdata/{}/{}/data/features[{}]/properties/'
                                    .format(i, j, k))
                        else:
                            type = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")[0]
                            if type == 'Object':
                                error_msg = ''
                                counter_succ += 1
                                counter_total += 1
                            else:
                                result = False
                                counter_fail += 1
                                counter_total += 1
                                error_msg.append(
                                    'ERROR: missing \"xw\" at mapdata/{}/{}/data/features[{}]/properties/'
                                        .format(i, j, k))

                    if result:
                        a = 0
                        # print(
                        #     "found \"src\" value {} at mapdata/{}/{}/data/features[{}]/properties/src! validating... {} {}"
                        #         .format(src, i, j, k, result, error_msg))
                    else:
                        print(colored(
                            "found \"src\" value {} at mapdata/{}/{}/data/features[{}]/properties/src! validating... {} {}"
                                .format(src, i, j, k, result, ('\n' + str(error_msg))), 'red'))
    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def validate_h(json_obj):
    global leni, i, lenj, j, lenk, k
    # loop for validating h:
    print('------------ validating h存在时objType为Extruded ------------------------------------------------')
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    counter_total = counter_succ = counter_fail = 0
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            # properties of mapdata/data/features is checked here:

            objType = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")

            feature_content = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".data.features[*]")
            if feature_content:
                lenk = len(feature_content)
            else:
                lenk = 0
            for k in range(lenk):
                # 当data中的feature包含"h"时， k循环了每一个具有"h"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                h = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".data.features[" + str(
                    k) + "].properties.h")
                if h:
                    result = True
                    error_msg = []
                    if objType:
                        if objType[0] != 'Extruded' and objType[0] != 'Shape':
                            result = False
                            error_msg.append(
                                'ERROR: Wrong objtype at mapdata/{}/{}/, expected: \'Extruded\' or \'Shape\''
                                'but got: {}'.format(i, j, objType[0]))
                        else:
                            error_msg = ''
                    else:
                        result = False
                        error_msg.append('ERROR: objType not found')

                    if result:
                        counter_succ += 1
                        counter_total += 1
                        # print(
                        #     "found \"h\" value {} and objType {} at mapdata/{}/{}/data/features[{}]/properties/h! validating... {} {}"
                        #         .format(h, objType, i, j, k, result, error_msg))
                    else:
                        counter_fail += 1
                        counter_total += 1
                        print(colored(
                            "found \"h\" value {} at mapdata/{}/{}/data/features[{}]/properties/h! validating... {} {}"
                                .format(h, i, j, k, result, ('\n' + str(error_msg))), 'red'))

    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def validate_color(json_obj):
    global leni, i, lenj, j, lenk, k, result
    # loop for validating color
    print('------------ validating color存在，则当前mapdata层的type为polygon ------------------------------------')
    valid_data_color = generate_valid_data_color(json_obj)
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    counter_total = counter_succ = counter_fail = 0
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            # properties of mapdata/data/features is checked here:
            feature_content = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".data.features[*]")
            if feature_content:
                lenk = len(feature_content)
            else:
                lenk = 0
            for k in range(lenk):
                # 当data中的feature包含"color"时， k循环了每一个具有"color"的"feature"， 并检查了所在"mapdata"层是否符合规定。

                color = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                          ".data.features[" + str(k) + "].properties.color")
                if color:
                    result = True
                    error_msg = []

                    objType = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".objType")
                    if not objType:
                        result = False
                        error_msg.append("ERROR: objType not found at mapdata." + str(i) + "." + str(j) + ".objTyp")

                    type = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".type")
                    if not type:
                        result = False
                        error_msg.append("ERROR: type not found at mapdata." + str(i) + "." + str(j) + ".type")

                    if (objType[0] != 'Shape' or type[0] != 'Polygon'):
                        result = False
                        error_msg.append('ERROR: please check: incorrect objType {} or type {}'.format(objType, type))

                    if result:
                        counter_succ += 1
                        counter_total += 1
                        # print("found \"color\" value {} at mapdata/{}/{}/data/features[{}]/properties/color!"
                        #       " validating... {} {}".format(color, i, j, k, result, error_msg))
                    else:
                        counter_fail += 1
                        counter_total += 1
                        print(colored("found \"color\" value {} at mapdata/{}/{}/data/features[{}]/properties/color!"
                                      " validating... {} {}".format(color, i, j, k, result, ('\n' + str(error_msg))),
                                      'red'))

    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def validata_map(json_obj):
    global leni, i, lenj, j, lenk, k, result, error_msg, name
    # loop for validating mapcode:
    print('------------ validating mapcode非空，则name非空 ------------------------------------------------')
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    counter_total = counter_succ = counter_fail = 0
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            # properties of mapdata/data/features is checked here:
            feature_content = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".data.features[*]")
            if feature_content:
                lenk = len(feature_content)
            else:
                lenk = 0
            for k in range(lenk):
                # 当data中的feature包含"mapcode"时， k循环了每一个具有"mapcode"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                mapcode = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                            ".data.features[" + str(k) + "].properties.mapcode")
                if mapcode:
                    result = True
                    error_msg = []
                    name = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                             ".data.features[" + str(k) + "].properties.name")
                    if name == False:
                        result = False
                        counter_fail += 1
                        counter_total += 1
                        error_msg.append(
                            'ERROR: missing \"name\" at mapdata/{}/{}/data/features[{}]/properties/'.format(i, j,
                                                                                                            k))
                    else:
                        result = True
                        error_msg = ''
                        counter_succ += 1
                        counter_total += 1

                    if result:
                        a = 0
                        # print(
                        #     "found \"mapcode\" value {} and \"name\" {} at mapdata/{}/{}/data/features[{}]/properties/"
                        #     "lpos! validating... {} {}".format(mapcode, name, i, j, k, result, error_msg))
                    else:
                        print(colored(
                            "found \"mapcode\" value {} and \"name\" {} at mapdata/{}/{}/data/features[{}]/properties/"
                            "lpos! validating... {} {}".format(mapcode, name, i, j, k, result, ('\n' + str(error_msg))
                                                               ), 'red'))
    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def validate_lpos(json_obj):
    global leni, i, lenj, j, lenk, k, result, error_msg, name
    # loop for validating lpos:
    print('------------ validating lpos -> name/name2 ------------------------------------------------')
    leni = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    counter_total = counter_succ = counter_fail = 0
    for i in range(leni):
        lenj = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(lenj):
            # properties of mapdata/data/features is checked here:
            feature_content = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".data.features[*]")
            if feature_content:
                lenk = len(feature_content)
            else:
                lenk = 0
            for k in range(lenk):
                # 当data中的feature包含"lpos"时， k循环了每一个具有"lpos"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                lpos = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                         ".data.features[" + str(k) + "].properties.lpos")
                if lpos:
                    if (lpos[0] == ''):
                        break
                    result = True
                    error_msg = []
                    len_lpos = 0
                    if isinstance(lpos[0], str):
                        lpos_arr = json.loads(lpos[0])
                    else:
                        len_lpos = len(lpos[0])
                    name = ''
                    name2 = ''
                    if len_lpos == 1:
                        name = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                                 ".data.features[" + str(k) + "].properties.name")
                        if name == False:
                            result = False
                            counter_fail += 1
                            counter_total += 1
                            error_msg.append(
                                'ERROR: missing \"name\" at mapdata/{}/{}/data/features[{}]/properties/'.format(i, j,
                                                                                                                k))
                        else:
                            error_msg = ''
                            counter_succ += 1
                            counter_total += 1
                    elif len_lpos > 1:
                        name2 = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                                  ".data.features[" + str(k) + "].properties.name2")
                        if name2 == False:
                            result = False
                            counter_fail += 1
                            counter_total += 1
                            error_msg.append(
                                'ERROR: missing \"name2\" at mapdata/{}/{}/data/features[{}]/properties/'.format(i, j,
                                                                                                                 k))
                        else:
                            error_msg = ''
                            counter_succ += 1
                            counter_total += 1

                    if result:
                        a = 0
                        # print("found \"lpos\" value {} and \"name\" {} \"name2\" {} at"
                        #       " mapdata/{}/{}/data/features[{}]/properties/lpos! validating... {} {}"
                        #       .format(lpos, name, name2, i, j, k, result, error_msg))
                    else:
                        print(colored(
                            "found \"lpos\" value {} and \"name\" {} \"name2\" {} at"
                            " mapdata/{}/{}/data/features[{}]/properties/lpos! validating... {} {}"
                                .format(lpos, name, name2, i, j, k, result, ('\n' + str(error_msg))), 'red'))

    print(
        '------------ in poitype test: {} violation found, Test passed ({}/{}) ------------------------------------\n'.format(
            counter_fail, counter_succ, counter_total))


def recursively_check(json_obj):
    mapcode_list = []
    len0 = len(jsonpath.jsonpath(json_obj, "$.mapdata.*"))
    for i in range(len0):
        len1 = len(jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + ".*"))
        for j in range(len1):
            feature_content = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) + ".data.features[*]")
            if feature_content:
                lenk = len(feature_content)
            else:
                lenk = 0
            for k in range(lenk):
                # 当data中的feature包含"src"时， k循环了每一个具有"src"的"feature"， 并检查了所在"mapdata"层是否符合规定。
                mapcode = jsonpath.jsonpath(json_obj, "$.mapdata." + str(i) + "." + str(j) +
                                            ".data.features[" + str(k) + "].properties.mapcode")
                if mapcode:
                    mapcode_list.append(mapcode[0])

    for mapcode in mapcode_list:
        recursivly_validate(mapcode)


def recursivly_validate(appcode):

    # appcode = '1273874511682342914'
    download_jsondata.download(appcode)
    json_obj = generate_jsonObj_from_file(appcode)

    map_name = jsonpath.jsonpath(json_obj, "$.mapinfo.name")[0]
    print(colored('---------------------------------- ' + map_name  + ' ------------------------------------------------------------------------------------', 'yellow'))

    print(colored('\nSchema validation:', 'yellow'))
    os.system('java -jar jsonSchema_validate_mapdata.jar ' + 'duodong/' + appcode + '.json')


    print(colored('\njsonPath validation:', 'yellow'))

    # map_name = download_jsondata.download(appcode)
    # json_obj = generate_jsonObj_from_file('jsons/' + map_name + '.json')
    # json_obj = generate_jsonObj_from_file(sys.argv[1])
    validate_poitype(json_obj)
    validate_ctype(json_obj)
    validate_type(json_obj)
    validate_ground(json_obj)
    validate_texture(json_obj)
    validate_src(json_obj)
    validate_h(json_obj)
    validate_color(json_obj)
    validata_map(json_obj)
    validate_lpos(json_obj)


def validate_first_item(mapcode_path):
    json_obj = generate_jsonObj_from_file(mapcode_path)

    map_name = jsonpath.jsonpath(json_obj, "$.mapinfo.name")[0]
    print(colored(
        '---------------------------------- ' + map_name + ' ------------------------------------------------------------------------------------',
        'yellow'))

    print(colored('\njsonPath validation:', 'yellow'))

    # map_name = download_jsondata.download(appcode)
    # json_obj = generate_jsonObj_from_file('jsons/' + map_name + '.json')
    # json_obj = generate_jsonObj_from_file(sys.argv[1])
    validate_poitype(json_obj)
    validate_ctype(json_obj)
    validate_type(json_obj)
    validate_ground(json_obj)
    validate_texture(json_obj)
    validate_src(json_obj)
    validate_h(json_obj)
    validate_color(json_obj)
    validata_map(json_obj)
    validate_lpos(json_obj)
    # recursively check submaps:
    recursively_check(json_obj)


if __name__ == '__main__':
    validate_first_item(sys.argv[1])

    print(colored('Completed.', 'yellow'))
