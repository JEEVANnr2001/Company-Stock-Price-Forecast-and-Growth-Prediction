import streamlit as st
import numpy as np
import pandas as pd
from sklearn import datasets
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st

import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression

def app():
    st.title('Total Assets Prediction')
    #!/usr/bin/env python
    # coding: utf-8

    # In[2]:


   

    uploaded_file = st.file_uploader('Choose a file')
    if uploaded_file is not None:
    #read csv
        df=pd.read_csv(uploaded_file)

    # uploadedFile = st.file_uploader(fileUploadLabel, type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    # user_input = st.text_input("Enter Stock Ticker", 'AAPL')
    # df = data.DataReader(user_input , 'yahoo', start, end)

    st.subheader('Data From 2010 to 2022')
    st.write(df.head())
    df.head()

    df['Quarter'] = df['Quarter'].map({
        'Q1': 0,
        'Q2': 1,
        'Q3': 2,
        'FY': 3
    })



    df['Date']=df['Year']+df['Quarter']*0.25
    #st.write(df['Date'])

    df.sort_values(["Date"], 
                        axis=0,
                        ascending=[True], 
                        inplace=True)

    #st.subheader('closing price vs time chart')

#     fig=plt.figure(figsize=(12,6))
#     plt.plot(df['Date'],df['TOTAL ASSET'])
#     st.pyplot(fig)

    data_training = df['TOTAL ASSET'].values.reshape(-1,1)
    data_testing = df['TOTAL ASSET'].values.reshape(-1,1)
    x_t=df[['Year','Quarter']]

#     st.write(x_t)
#     print(x_t)

    reg=LinearRegression()

    x_train=df['Date'].values.reshape(-1,1)
    x_test=df['Date'].values.reshape(-1,1)

    reg.fit(x_t,data_training)
    print(data_training.shape)
    print(data_testing.shape)


    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range = (0,1))
    data_training_array = scaler.fit_transform(data_training)


    pred=reg.predict(x_t)

    st.subheader('Total Asset Forecast')

#     fig2=plt.figure(figsize=(12,6))
#     plt.plot(df['Date'],pred)
#     #fig3=plt.figure(figsize=(12,6))
#     plt.plot(df['Date'],data_training)
#     st.pyplot(fig2)

    l=df['Date'].tolist()
    n=[]
    q=[]
    d=[]
    j=2021
    for i in range(0,10):
        if i%4==0:
            j+=1
        n=[]
        n.append(j)
        temp=j+(i%4)*0.25
        d.append(temp)
        n.append((i%4)*0.25)
        q.append(n)

    #q=pd.DataFrame(q)
    #q.values.reshape(-1,2)

    pred2=reg.predict(q)

    fig4=plt.figure(figsize=(12,6))

    plt.plot(df['Date'],data_training)
    plt.plot(df['Date'],pred)
    plt.plot(d,pred2)
    plt.legend(['Total Assets', 'Predicted Total Assets', 'Forecasted Total Assets'])
    plt.xlabel('Time')
    plt.ylabel('Total Assets(in 100 billion)')
    st.pyplot(fig4)



    print(q)


    # In[ ]:




