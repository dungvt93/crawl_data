import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def load_data(file_name, sequence_length=10):
    close = []
    volume = []
    cap = []

    with open(file_name,'r') as f:
        reader = csv.reader(f)
        # skip header
        next(reader)
        for row in reader:
            if len(row) != 0 and is_number(row[4]) and is_number(row[5]) and is_number(row[6]):
                close.append([row[4]])
                volume.append([row[5]])
                cap.append([row[6]])

    # reversed data time stamp
    close=close[::-1]
    volume=volume[::-1]
    cap=cap[::-1]

    #norm data
    volume = np.array(volume).astype(float)
    scaler_vol = MinMaxScaler()
    volume = scaler_vol.fit_transform(volume)

    cap = np.array(cap).astype(float)
    scaler_cap = MinMaxScaler()
    cap = scaler_cap.fit_transform(cap)

    close = np.array(close).astype(float)
    scaler_close = MinMaxScaler()
    close = scaler_close.fit_transform(close)

    # concat data to shape (None,3)
    data_origin = np.concatenate([close,volume,cap],1)

    #group data to shape (None,sequence_length+1,3)
    data = []
    for i in range(len(close) - sequence_length ):
        data.append(data_origin[i: i + sequence_length + 1])
        # data.append([close[i: i + sequence_length + 1],volume[i: i + sequence_length + 1],cap[i: i + sequence_length + 1]])

    reshaped_data = np.array(data).astype('float64')
    return reshaped_data,[scaler_vol,scaler_cap,scaler_close]

def generate_train_data(file_name, sequence_length=10,split = 0.8):
    reshaped_data, scaler = load_data(file_name,sequence_length)
    # np.random.shuffle(reshaped_data)

    # get sequence_length data of each  element
    x = reshaped_data[:,:-1]
    # get end of close_price data of each element
    y = reshaped_data[:, 0, -1]

    split_boundary = int(reshaped_data.shape[0] * split)
    train_x = x[: split_boundary]
    test_x = x[split_boundary:]

    train_y = y[: split_boundary]
    test_y = y[split_boundary:]
    return train_x, train_y, test_x, test_y, scaler

def build_model():
    # input_dim是输入的train_x的最后一个维度，train_x的维度为(n_samples, time_steps, input_dim)
    model = Sequential()
    model.add(LSTM(50,input_shape=(None,3), return_sequences=True))
    print(model.layers)
    model.add(LSTM(100, return_sequences=False))
    model.add(Dense(output_dim=1))
    model.add(Activation('linear'))

    model.compile(loss='mse', optimizer='rmsprop')
    model.summary()
    return model

def train_model(train_x, train_y, test_x, test_y):
    model = build_model()

    try:
        model.fit(train_x, train_y, batch_size=512, nb_epoch=30, validation_split=0.1)
        predict = model.predict(test_x)
        predict = np.reshape(predict, (predict.size, ))
    except KeyboardInterrupt:
        print(predict)
        print(test_y)
    # print(predict)
    # print(test_y)
    # try:
    #     plt.figure(1)
    #     plt.plot(predict, 'r:')
    #     plt.plot(test_y, 'g-')
    #     plt.legend(['predict', 'true'])
    # except Exception as e:
    #     print(e)
    return predict, test_y, model


if __name__ == '__main__':

    train_x, train_y, test_x, test_y, scaler = generate_train_data('btc.csv',20)
    train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1],3))
    test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1],3))
    predict_y, test_y, model = train_model(train_x, train_y, test_x, test_y)
    predict_y = scaler[-1].inverse_transform([[i] for i in predict_y])
    test_y = scaler[-1].inverse_transform([[i] for i in test_y])
    # fig2 = plt.figure(2)
    # plt.plot(predict_y, 'g:')
    # plt.plot(test_y, 'r-')
    # plt.show()

    input, scaler= load_data('btc.csv',20)
    # print(input)
    # print(input[-1][-1][0])
    # print(scaler[-1].inverse_transform([[input[-1][-1][0]]]))
    # exit()
    y = [[input[-1][-1][0]]]
    input = [input[-1][1:]]
    input = np.reshape(input,(1,20,3))
    predict = model.predict(input)
    predict = scaler[-1].inverse_transform(predict)
    y = scaler[-1].inverse_transform(y)
    print(predict)
    print(y)








