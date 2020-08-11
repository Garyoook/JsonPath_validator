import codecs
import json

import requests


def download(appcode):
    outputPath = '/Users/yg9418/Downloads/Seeklane 测试/JsonPath_validator/jsons'

    # 拉取data.json
    html = requests.get("http://test.seeklane.com/location/getConfig?appCode=" + appcode)
    mapPath = json.loads(html.text)['data']['mapPath']
    mapdata = requests.get("http://test.seeklane.com" + mapPath + 'data.json')
    print("http://test.seeklane.com" + mapPath + 'data.json')
    data = json.loads(mapdata.text)
    text = json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ': '))
    fs = codecs.open(outputPath + '/' + appcode + '.json', 'w', encoding='utf-8')
    fs.write(text)
    fs.close()