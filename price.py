import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
from scrape import save_sp500
import pickle

def get_yahoo_data(reload_sp500=False):
    if reload_sp500:
        tickers=save_sp500()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers=pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start=dt.datetime(2000,1,1)
    end=dt.datetime(2017,1,1)
    print (len(tickers))
    for ticker in tickers:
        print (ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                df=web.DataReader(ticker,'yahoo',start,end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except:
                pass
        else:
            print ('{} already exists'.format(ticker))

# get_yahoo_data(reload_sp500=False)

def compile_data():
    with open("sp500tickers.pickle","rb") as f:
        tickers=pickle.load(f)
    
    main_df=pd.DataFrame()
    for i,t in enumerate(tickers):
        try:
            df=pd.read_csv('stock_dfs/{}.csv'.format(t))
        except:
            continue
        df.set_index('Date',inplace=True)
        df.rename(columns={'Adj Close':t},inplace=True)
        df.drop(['Open','High','Low','Close','Volume'],axis=1,inplace=True)
        

        if main_df.empty:
            main_df=df
        else:
            main_df=main_df.join(df,how='outer')

        if i%10==0:
            print (i)
    print(main_df.head())
    main_df.to_csv('sp500_joined.csv')

compile_data()

