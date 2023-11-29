import numpy
import pandas as pd
import matplotlib.pyplot as plt
import numpy
import tensorflow as  tf
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')
# 创建数据集  将值数组转换为数据集矩阵，look_back是步长
root_dir=r'D:\gitdown'
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)  #X按照顺序取值
        dataY.append(dataset[i + look_back, 0]) #Y向后移动一位取值
    return numpy.array(dataX), numpy.array(dataY)

#预测数据控制
def process_num(num):
    if(num<=0):
        num=0
    else:
        num=numpy.floor(num)
    return num

#预测未来三天的数据
def predict_Three_days(model_dir,dataset,look_back=3):
    dataset = dataset.set_index(['日期'], drop=True)
    dataset = dataset.astype('float32')

    # 数据处理，归一化至0~1之间
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    train = dataset
    trainX, trainY = create_dataset(train, look_back)  # 三步预测
    # 调整输入数据的格式,数据重构为3D [samples, time steps, features]
    trainX = numpy.reshape(trainX, (trainX.shape[0], look_back, 1))  # （样本个数，1，输入的维度）
    # 模型加载
    model = tf.keras.models.load_model(model_dir)

    # 预测未来三天的数据
    finalX = numpy.reshape(train[-3:], (1, trainX.shape[1], 1))
    featruePredict1 = model.predict(finalX)
    # 将标准化数据转换为真实值

    finalx2=numpy.append(train[-2:],featruePredict1)
    featruePredict2=model.predict(numpy.reshape(finalx2,(1,trainX.shape[1],1)))

    finalx3=numpy.append(finalx2[-2:],featruePredict2)
    featruePredict3=model.predict(numpy.reshape(finalx3,(1,trainX.shape[1],1)))

    featruePredict1 = scaler.inverse_transform(featruePredict1)
    featruePredict2 = scaler.inverse_transform(featruePredict2)
    featruePredict3 = scaler.inverse_transform(featruePredict3)

    return process_num(featruePredict1.squeeze()),process_num(featruePredict2.squeeze()),process_num(featruePredict3.squeeze())
#读取工作表获取数据
def getData(dir,sheet):
    dataset = pd.read_excel(dir, sheet_name=sheet)
    return dataset
