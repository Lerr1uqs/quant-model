# import pandas_datareader as pdr
# from pandas_datareader import data, wb
import tushare as ts
from datetime import date
import numpy as np
import pandas as pd
import pdb

risk_free_return = 0.05
start = "2023 1 1"
end = "2024 1 26"
# # 赛轮轮胎 vs 上证指数
ticker1 = '601058'
ticker2  = "000001"

#Get stock data
stock1 = ts.get_hist_data(ticker1)
stock2 = ts.get_hist_data(ticker2)

# Resample for monthly data
# resample 是时间序列处理的方法
# return_s1 = stock1.resample('M').last()
# return_s2 = stock2.resample('M').last()

#Create a dataframe with the adjusted close
data = pd.DataFrame({
    'stock-close' : stock1['close'], 
    'market-close': stock2['close']
    }, 
    index=stock1.index
)

# Calc the stock and market retuens by computing log(n)/log(n-1)
# REF: https://www.zhihu.com/question/30113132
data[['stock-returns','market-returns']] = np.log(
    data[['stock-close', 'market-close']] / data[['stock-close', 'market-close']].shift(1)
)

#Drop null values
data = data.dropna();

#Generate covarience matrix
covmat = np.cov(data["stock-returns"], data["market-returns"])

#Calc beta from matrix
beta = covmat[0,1] / covmat[1,1]

print("Beta from formula: ", beta)

#Calc beta from regression
beta, alpha = np.polyfit(data["market-returns"], data["stock-returns"], deg=1)
print("Beta from regression: ", beta)

#Calc expected return
expected_return = risk_free_return + beta*(data["market-returns"].mean()*12-risk_free_return)
print("Expected Return: ",expected_return)

