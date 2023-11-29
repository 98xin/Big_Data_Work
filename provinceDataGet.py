import requests
import json
import pandas as pd


# 地区
areas = ['北京', '上海', '天津', '重庆', '澳门', '香港', '海南', '台湾', '河北', '山西',
    '山东', '江苏', '浙江', '安徽', '福建', '江西', '河南', '湖北', '湖南', '广东',
    '广西', '四川', '贵州', '云南', '陕西', '甘肃', '辽宁', '吉林', '黑龙江', '青海',
    '宁夏', '西藏', '新疆', '内蒙古']


# 获取某个省份的所有数据
def getProvinceData(results):
    provinceName = results["data"][0]["name"]
    trend = results["data"][0]["trend"]
    updateDate = trend["updateDate"]
    confirmAll = trend["list"][0]
    cure = trend["list"][1]
    die = trend["list"][2]
    confirmAdd = trend["list"][3]
    confirmAddNative = trend["list"][4]
    asymptomaticAdd = trend["list"][5]
    print(provinceName)
    # 获取3.1索引
    indexStart = 0
    if provinceName == "澳门" or provinceName == "香港" or provinceName == "台湾":
        indexStart = updateDate.index('3.14')
    else:
        indexStart = updateDate.index('3.1')

    updateDate = updateDate[indexStart:]
    confirmAll = confirmAll["data"][indexStart:]
    cure = cure["data"][indexStart:]
    die = die["data"][indexStart:]
    confirmAdd = confirmAdd["data"][indexStart:]
    confirmAddNative = confirmAddNative["data"][indexStart:]
    asymptomaticAdd = asymptomaticAdd["data"][indexStart:]
    return provinceName, updateDate, confirmAll, cure, die, confirmAdd, confirmAddNative, asymptomaticAdd


# 格式化数据
def formatData(dataLen):
    dataList = []
    for i in range(dataLen):
        dateTemp = updateDate[i]
        confirmAllTemp = confirmAll[i]
        cureTemp = cure[i]
        dieTemp = die[i]
        confirmAddTemp = confirmAdd[i]
        confirmAddNativeTemp = confirmAddNative[i]
        asymptomaticAddTemp = asymptomaticAdd[i]
        nowConfirm = confirmAllTemp-cureTemp-dieTemp
        dataList.append(
            [dateTemp, confirmAddTemp, confirmAddNativeTemp, asymptomaticAddTemp, confirmAllTemp, cureTemp, dieTemp, nowConfirm])
    # print(dataList)
    df = pd.DataFrame(dataList)
    df.columns = ["日期", "新增确诊", "新增本土", "新增无症状", "累计确诊", "累计治愈", "累计死亡", "现有确诊"]
    return df


if __name__ == '__main__':
    writer = pd.ExcelWriter(r'D:\pycharmCode\BigData\result\provinceData.xlsx')
    for area in areas:
        url = 'https://voice.baidu.com/newpneumonia/getv2?' \
              'from=mola-virus&stage=publish&target=trend&isCaseIn=1&' \
              'area={}&callback=jsonp_1652526814976_84234'.format(area)
        # url = 'https://voice.baidu.com/newpneumonia/getv2?from=mola-virus&stage=publish&target=trend&isCaseIn=1&area=%E8%BE%BD%E5%AE%81&callback=jsonp_1652526814976_84234'
        response = requests.get(url).text
        results = response[26:-2]
        results = json.loads(results)
        provinceName, updateDate, confirmAll, cure, die, confirmAdd, confirmAddNative, asymptomaticAdd = getProvinceData(results)
        # print(provinceName, updateDate, confirmAll, cure, die, confirmAdd, confirmAddNative, asymptomaticAdd)
        dataLen = len(updateDate)
        df = formatData(dataLen)
        print(df)
        # 输出到excel
        df.to_excel(writer, index=None, sheet_name=provinceName)
    # writer.save()
    writer.close()
