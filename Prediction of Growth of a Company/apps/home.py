import streamlit as st
import numpy as np
import pandas as pd
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt

def app():
    st.title('Stock Forcasting')
    import matplotlib.pyplot as plt
    st.write('In this app, we will be building a model to predict Stock Price Index')
    

    start = '2010-01-01'
    end = '2022-06-07'
    X_test=[]
    y_test=[]

    user_input = st.text_input("Enter Stock Ticker", 'AAPL')
    df = data.DataReader(user_input , 'yahoo', start, end)

    st.subheader('Data From 2010 to 2022')
    st.write(df.tail())

    df1=df.reset_index()['Close']

#     st.subheader('Closing price vs Time chart')

#     ma100=df.Close.rolling(100).mean()
#     fig= plt.figure(figsize=(12,6))
#     plt.plot(df.Close)
#     st.pyplot(fig)

    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range=(0,1))
    df1=scaler.fit_transform(np.array(df1).reshape(-1,1))

    ##splitting dataset into train and test split
    training_size=int(len(df1)*0.65)
    test_size=len(df1)-training_size
    train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]

    training_size,test_size

    train_data

    import numpy
    # convert an array of values into a dataset matrix
    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-time_step-1):
            a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return numpy.array(dataX), numpy.array(dataY)
    #data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    #data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])
    time_step=100
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, ytest = create_dataset(test_data, time_step)


    #print(data_training.shape)
    #print(data_testing.shape)
    # reshape input to be [samples, time steps, features] which is required for LSTM
    X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
    X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

    # from sklearn.preprocessing import MinMaxScaler
    # scaler=MinMaxScaler(feature_range = (0,1))
    # data_training_array = scaler.fit_transform(data_training)

    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.layers import LSTM

    model=load_model('stock_forcast.h5')

    # past_100_days = data_training.tail(100)

    # final_df = past_100_days.append(data_testing, ignore_index= True)
    # input_data = scaler.fit_transform(final_df)

    # for i in range(100, input_data.shape[0]):
    #     X_test.append(input_data[i-100: i])
    #     y_test.append(input_data[i, 0])

    # x_test, y_test = np.array(x_test),np.array(y_test)
    # y_predicted = model.predict(x_test)
    train_predict=model.predict(X_train)
    test_predict=model.predict(X_test)

    train_predict=scaler.inverse_transform(train_predict)
    test_predict=scaler.inverse_transform(test_predict)

    ### Calculate RMSE performance metrics
    import math
    from sklearn.metrics import mean_squared_error
    st.write('RMSE Training:') 
    st.write(math.sqrt(mean_squared_error(y_train,train_predict)))

    ### Test Data RMSE
    st.write('RMSE Testing:')
    st.write(math.sqrt(mean_squared_error(ytest,test_predict)))

    # scaler=scaler.scale_
    # scale_factor = 1/scaler[0]
    # y_predicted = y_predicted *scale_factor
    # y_test = y_test * scale_factor

#     st.subheader('Actual vs Predicted')
#     ### Plotting 
#     fig2 = plt.figure(figsize=(12,6))
#     # shift train predictions for plotting
#     look_back=100
#     trainPredictPlot = numpy.empty_like(df1)
#     trainPredictPlot[:, :] = np.nan
#     trainPredictPlot[look_back:len(train_predict)+look_back, :] = train_predict
#     # shift test predictions for plotting
#     testPredictPlot = numpy.empty_like(df1)
#     testPredictPlot[:, :] = numpy.nan
#     testPredictPlot[len(train_predict)+(look_back*2)+1:len(df1)-1, :] = test_predict
#     # plot baseline and predictions
#     plt.plot(scaler.inverse_transform(df1))
#     plt.plot(trainPredictPlot)
#     plt.plot(testPredictPlot)
#     plt.legend(['Training Predictions', 'Training Observations','Validation Predictions'])
#     plt.show()
#     st.pyplot(fig2)

    # st.subheader('actual vs predicted')
    # fig3 = plt.figure(figsize=(12,6))
    # plt.plot(y_test, 'b', label = 'Orginal Price')
    # plt.plot(y_predicted, 'r',label='Predicted Price')
    # plt.xlabel('Time')
    # plt.ylabel('Price')
    # plt.legend()
    # plt.show()
    # st.pyplot(fig3)

    z=len(test_data)-500
    print(z)

    x_input=test_data[z:].reshape(1,-1)
    x_input.shape

    temp_input=list(x_input)
    temp_input=temp_input[0].tolist()

    # demonstrate prediction for next 10 days
    from numpy import array

    lst_output=[]
    n_steps=499
    i=0
    while(i<30):

        if(len(temp_input)>100):
            #print(temp_input)
            x_input=np.array(temp_input[1:])
            print("{} day input {}".format(i,x_input))
            x_input=x_input.reshape(1,-1)
            x_input = x_input.reshape((1, n_steps, 1))
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input=temp_input[1:]
            #print(temp_input)
            lst_output.extend(yhat.tolist())
            i=i+1
        else:
            x_input = x_input.reshape((1, n_steps,1))
            yhat = model.predict(x_input, verbose=0)
            print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i=i+1


    print(lst_output)

    day_new=np.arange(1,501)
    day_pred=np.arange(501,531)

    import matplotlib.pyplot as plt

    m=len(df1)-500

    print(scaler.inverse_transform(lst_output))

    st.subheader('Stock Price Forecast')
    fig3 = plt.figure(figsize=(12,6))
    plt.plot(day_new,scaler.inverse_transform(df1[m:]))
    plt.plot(day_pred,scaler.inverse_transform(lst_output))
    plt.legend(['Historical Stock Price', 'Future Stock Price'])
    plt.xlabel('Days')
    plt.ylabel('Price')
    st.pyplot(fig3)
    
    
#     score = model.score(X_test, ytest)
#     st.write('Accuracy:')
#     st.write(score)
    

#     st.subheader('actual vs predicted')
#     fig4 = plt.figure(figsize=(12,6))
#     df3=df1.tolist()
#     df3.extend(lst_output)
#     print(len(df3))
#     plt.plot(df3[3000:])
#     st.pyplot(fig4)

#     st.subheader('actual vs predicted')
#     fig5 = plt.figure(figsize=(12,6))
#     df3=scaler.inverse_transform(df3).tolist()
#     plt.plot(df3)
#     st.pyplot(fig5)