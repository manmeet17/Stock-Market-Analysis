from bs4 import BeautifulSoup
import pickle
import requests

def save_sp500():
    url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'lxml')
    table=soup.find("table",{'class':'wikitable sortable'})
    tickers=[]
    for row in table.findAll('tr')[1:]:
        ticker=row.findAll('td')[0].text
        tickers.append(ticker)
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    return tickers

save_sp500()