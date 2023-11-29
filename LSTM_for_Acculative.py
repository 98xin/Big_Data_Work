'''
    时间序列预测问题可以通过滑动窗口法转换为监督学习问题
'''

import numpy
import matplotlib.pyplot as plt
import pandas as pd
import math
import tensorflow as  tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')
from utils import create_dataset,root_dir
if __name__ == '__main__':
    # 加载数据
    dataset = pd.read_excel(r"{}\Big_Data_Work\Acculative.xlsx".format(root_dir))
    print("数据集长度：",len(dataset))
    #dataset = dataframe.values
    #print(dataset)
    # 将“日期”列转换为时间数据类型，并将“日期”列设置为Pandas的索引
    #dataset['日期'] = pd.to_datetime(dataset['日期'])
    dataset = dataset.set_index(['index'], drop=True)
    # 将整型变为float
    dataset = dataset.astype('float32')
    plt.plot(dataset)
    plt.show()

    #数据格式转换为监督学习，归一化数据，训练集和测试集划分
    # 数据处理，归一化至0~1之间
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    train=dataset
    # 构建监督学习型数据  创建测试集和训练集
    look_back = 3
    trainX, trainY = create_dataset(train, look_back)  # 三步预测
    print("转为监督学习，训练集数据长度：",len(trainX))
    print(trainX,trainY)

    # 调整输入数据的格式,数据重构为3D [samples, time steps, features]
    trainX = numpy.reshape(trainX, (trainX.shape[0], look_back, 1))  # （样本个数，1，输入的维度）
    # 创建LSTM神经网络模型
    model = Sequential()
    # 输入维度为1，时间窗的长度为1，隐含层神经元节点个数为120
    model.add(LSTM(4, input_shape=(trainX.shape[1], trainX.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=30, batch_size=1, verbose=2)

    # 打印模型
    model.summary()
    tf.keras.models.save_model(model,"Model_for_Acculative.ckpt")
    # 预测
    trainPredict = model.predict(trainX)

    # 反归一化，逆缩放预测值
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])

    # 计算误差 RMSE 计算均方根误差（标准差） 衡量观测值同真实值之间的偏差，RMSE越接近于0，说明模型选择和拟合更好，数据预测也越成功
    trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
    print('Train Score: %.2f RMSE' % (trainScore))


    #绘图
    trainPredictPlot = numpy.empty_like(dataset)
    trainPredictPlot[:, :] = numpy.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict

    plt.plot(scaler.inverse_transform(dataset))
    plt.plot(trainPredictPlot)
    plt.show()

    # 测试集对比折线图
    fig = plt.figure(figsize=(12, 10))
    plt.plot(trainY[0], label='observe')
    plt.plot([x for x in trainPredict[:, 0]], label='trained')
    plt.xlabel("date", fontsize=25)
    plt.ylabel("updateDate", fontsize=25)
    plt.legend(fontsize=25)
    plt.show()

    # 预测未来的数据
    # 测试数据的最后一个数据没有预测,这里补上
    finalX = numpy.reshape(train[-3:], (1, trainX.shape[1],1))
    #finalX = numpy.reshape(test[-3:], (1, testX.shape[1], 1))  #使用最后三个数据预测下一个数据
    # 预测得到标准化数据
    featruePredict = model.predict(finalX)
    # 将标准化数据转换为真实值
    featruePredict = scaler.inverse_transform(featruePredict)
    print('未来一天的累计确诊人数是: ', featruePredict)












