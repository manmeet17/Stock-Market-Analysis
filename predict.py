import numpy as np
import pandas as pd
import pickle
from collections import Counter
from sklearn import svm,neighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier


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
    req=0.028
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
    # print (df_vals)

    X=df_vals.values
    y=df['{}_target'.format(ticker)].values

    return X,y,df

def ml(ticker):
    X,y,df=extract_feature(ticker)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25)
    # clf=neighbors.KNeighborsClassifier()
    clf=VotingClassifier([('lsvc',svm.LinearSVC()),('knn',neighbors.KNeighborsClassifier()),('rfor',RandomForestClassifier())])

    clf.fit(X_train,y_train)
    confidence=clf.score(X_test,y_test)
    pre=clf.predict(X_test)
    print('Predicted Values:',Counter(pre))
    print("Accuracy:",confidence)
    return confidence,Counter(pre)

def find(obj):
    sorted_list=sorted(obj.items(),key=lambda x:x[1])
    val=sorted_list[-1][0]
    if val==0:
        return "Hold"
    if val==1:
        return "Buy"
    return "Sell"


def get_companies():
    df=pd.read_csv('sp500_joined.csv',index_col=0)
    final=pd.DataFrame(columns=["Company","Stocks"])
    companies=df.columns.values
    for c in companies[15:25]:
        print ("Company Ticker:",c)
        con,pre=ml(c)
        final=final.append({'Company':c,"Stocks":find(pre)},ignore_index=True)
        print("\n\n")
    print (final.head())
    final.to_csv('predictions.csv')

get_companies()
