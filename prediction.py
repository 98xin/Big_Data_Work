import pandas as pd
import warnings
import pyautogui
from utils import predict_Three_days,getData
warnings.filterwarnings('ignore')
import win32api

if __name__ == '__main__':
    # 加载数据
    while(1):
        print('*'*30)
        print("请输入相应指令：")
        print('1：获取全国疫情分布图')
        print('2：获取省份疫情统计')
        print('3：获取省份疫情预测结果')
        print('0:退出')
        print('*' * 30)
        income=int(input())
        pyautogui.hotkey("Alt","c")#清除run的输出信息，需要添加Alt+c快捷键到pycharm
        if(income==0):
            break;
        elif(income==1):
            win32api.ShellExecute(0,'open','.\\result\\China_map.html',"","",1)
            continue
        elif(income==2):
            province=input("请输入要查询的省份：")
            try:
                win32api.ShellExecute(0, 'open', '.\\result\\{}'.format(province)+".html", "", "", 1)
            except:
                print("没有查询到相应的省份信息！")
        elif(income==3):
            try:
                pro_vince=input("请输入要进行预测的省份：")
                dataset=getData(r'.\provinceData.xlsx',sheet=pro_vince)
                data_add_diagnosis=dataset[['日期','新增确诊']]
                data_add_asymptomatic=dataset[['日期','新增无症状']]
                data_acc_diagnosis=dataset[['日期','累计确诊']]
                data_acc_healing=dataset[['日期','累计治愈']]
                data_acc_dead=dataset[['日期','累计死亡']]
                print(r"{}--》未来三天预计新增确诊人数：".format(pro_vince),predict_Three_days("Model_for_Additional.ckpt",data_add_diagnosis))
                print(r"{}--》未来三天预计新增无症状人数：".format(pro_vince),predict_Three_days("Model_for_Additional.ckpt",data_add_asymptomatic))
                print(r"{}--》未来三天预计累计确诊人数：".format(pro_vince),predict_Three_days("Model_for_Acculative.ckpt",data_acc_diagnosis))
                print(r"{}--》未来三天预计累计治愈人数：".format(pro_vince),predict_Three_days("Model_for_Acculative.ckpt",data_acc_healing))
                print(r"{}--》未来三天预计累计死亡人数：".format(pro_vince),predict_Three_days("Model_for_Acculative.ckpt",data_acc_dead))
            except:
                print("预测过程出错！")



        else:
            print("您输入的指令有误，请重新输入（0-3）！")

