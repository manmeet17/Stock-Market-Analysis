import numpy as np
import pandas as pd
import pickle
from collections import Counter

def process_data(ticker):
    days=7
    df=pd.read_csv('sp500_joined.csv',index_col=0)
    tickers=df.columns.values
    df.fillna(0,inplace=True)
    
    # Percent Change
    for i in range(1,days+1):
        df['{}_{}d'.format(ticker,i)]=(df[ticker].shift(-i)-df[ticker])/df[ticker]
    df.fillna(0,inplace=True)

    return tickers,df

def buy_sell_hold(*args):
    cols=[c for c in args]
    req=0.02
    for col in cols:
        if col>req:
            return 1
        if col<-req:
            return -1
    return 0

def extract_feature(ticker):
    tickers, df=process_data(ticker)
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold,df['{}_1d'.format(ticker)],
                                                            df['{}_2d'.format(ticker)],
                                                            df['{}_3d'.format(ticker)],
                                                            df['{}_4d'.format(ticker)],
                                                            df['{}_5d'.format(ticker)],
                                                            df['{}_6d'.format(ticker)],
                                                            df['{}_7d'.format(ticker)]
                                                            ))

    vals=df['{}_target'.format(ticker)].values
    str_vals=[str(i) for i in vals]
    print('Data Spread:',Counter(str_vals))

    df.fillna(0,inplace=True)
    df=df.replace([np.inf,-np.inf],np.nan)
    df.dropna(inplace=True)

    df_vals=df[[ticker for ticker in tickers]].pct_change()
    df_vals=df_vals.replace([np.inf,-np.inf],0)
    df_vals.fillna(0,inplace=True)
    print (df_vals)

    X=df_vals.values
    y=df['{}_target'.format(ticker)].values

    return X,y,df

(extract_feature('AMZN'))
