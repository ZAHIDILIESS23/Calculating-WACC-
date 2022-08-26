#!/usr/bin/env python
# coding: utf-8

# ## WACC:
# WACC=$k_{d}$*(1-TC)*(D/(D+E)+ke*(E/(D+E))\
# $k_{d}$:cost of debt\
# TC:tax effective rate\
# Ke:cost of equity
# 

# In[1]:


import pandas_datareader.data as web
import datetime
import requests


# ## the cost of debt
# $k_{d}$=RF+credit spread

# In[4]:


company='MSFT'
def interest_coverage_and_RF(company):
    IS=requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey=5440fa1b83055823728a35b8988f31eb').json()
    EBIT=IS[0]['ebitda']-IS[0]['depreciationAndAmortization']
    interest_expense=IS[0]['interestExpense']
    interest_coverage_ratio=EBIT/interest_expense
    # RF
    start=datetime.datetime(2019,7,10)
    end=datetime.datetime.today()
    Treasury=web.DataReader(['TB1YR'],'fred',start,end)
    RF=float(Treasury.iloc[-1])
    RF=RF/100
    print(RF,interest_coverage_ratio)
    return [RF,interest_coverage_ratio]
interest=interest_coverage_and_RF(company)
RF=interest[0]
interest_coverage_ratio=interest[1]
    


# In[8]:


def cost_of_debt(company,RF,interest_coverage_ratio):
    if interest_coverage_ratio>8.5:
        # Rating AAA
        credit_spread=0.0063
    if(interest_coverage_ratio>6.5)&(interest_coverage_ratio<=8.5):
        # Rating AA
        credit_spread=0.0078
    if(interest_coverage_ratio>5.5)&(interest_coverage_ratio<=6.5):
        # Rating A+
        credit_spread=0.0098
    if(interest_coverage_ratio>4.25)&(interest_coverage_ratio<=5.49):
        # Rating A
        credit_spread=0.0108
    if(interest_coverage_ratio>3)&(interest_coverage_ratio<=4.25):
        # Rating $A-
        credit_spread=0.0122
    if(interest_coverage_ratio>2.5)&(interest_coverage_ratio<=3):
        # Rating BBB
        credit_spread=0.0156
    if(interest_coverage_ratio>2.25)&(interest_coverage_ratio<=2.5):
        # Rating BB+
        credit_spread=0.02
    if(interest_coverage_ratio>2)&(interest_coverage_ratio<=2.25):
        # Rating BB
        credit_spread=0.0240
    if(interest_coverage_ratio>1.75)&(interest_coverage_ratio<=2):
        # Rating B+
        credit_spread=0.0351
    if(interest_coverage_ratio>1.5)&(interest_coverage_ratio<=1.75):
        # Rating B
        credit_spread=0.0421
    if(interest_coverage_ratio>1.25)&(interest_coverage_ratio<=1.5):
        # Rating B-
        credit_spread=0.0515
    if(interest_coverage_ratio>0.8)&(interest_coverage_ratio<=1.25):
        # Rating CCC
        credit_spread=0.0820
    if(interest_coverage_ratio>0.65)&(interest_coverage_ratio<=0.8):
        # Rating CC
        credit_spread=0.0864
    if(interest_coverage_ratio>0.2)&(interest_coverage_ratio<=0.65):
        # Rating C
        credit_spread=0.1134
    if(interest_coverage_ratio<=0.2):
        # Rating D
        credit_spread=0.1512
    cost_of_debt=RF+credit_spread
    print(cost_of_debt)
    return cost_of_debt
kd=cost_of_debt(company,RF,interest_coverage_ratio)
     
        
        
    
        
    


# ## calculating the cost of equity:

# In[13]:


def cost_of_equity(company):
    # RF
    start=datetime.datetime(2019,7,10)
    end=datetime.datetime.today()
    Treasury=web.DataReader(['TB1YR'],'fred',start,end)
    RF=float(Treasury.iloc[-1])
    RF=RF/100
    # BETA
    beta=requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{company}?apikey=5440fa1b83055823728a35b8988f31eb')
    beta=beta.json()
    beta=float(beta['profile']['beta'])
    # market return
    start=datetime.datetime(2019,7,10)
    end=datetime.datetime.today()
    SP500=web.DataReader(['SP500'],'fred',start,end)
    SP500yearlyreturn=(SP500['SP500'].iloc[-1]/SP500['SP500'].iloc[-252])-1
    cost_of_equity=RF+(beta*(SP500yearlyreturn-RF))
    print(cost_of_equity)
    return cost_of_equity
ke=cost_of_equity(company)
    


# # THE WACC

# In[22]:


def wacc(company):
    FR=requests.get(f'https://financialmodelingprep.com/api/v3/ratios//{company}?apikey=5440fa1b83055823728a35b8988f31eb').json()
    ETR=FR[0]['effectiveTaxRate']
    # capital structure
    BS=requests.get(f'https://fmpcloud.io/api/v3/balance-sheet-statement/{company}?limit=120&apikey=03143675d8f041d214b19231424e0527').json()
    debt_to=BS[0]['totalDebt']/(BS[0]['totalDebt']+BS[0]['totalStockholdersEquity'])
    equity_to=BS[0]['totalStockholdersEquity']/(BS[0]['totalDebt']+BS[0]['totalStockholdersEquity'])
    # WACC
    WACC=(kd*(1-ETR)*debt_to)+(ke*equity_to)
    print(WACC,equity_to,debt_to)
    return WACC
WACC=wacc(company)
print('WACC of' + company +'is'+str(WACC*100)+'%')


# In[18]:





# In[ ]:




