#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
pd.set_option('mode.chained_assignment',None)


# In[2]:


import plotly.graph_objects as go
import plotly.io as pio
import plotly.offline as offline
pio.renderers.default = "browser"


# In[3]:


url = "http://ti.saude.rs.gov.br/covid19/download/20200609.csv"
df =  pd.read_csv('dados.csv', header=0, sep=';',decimal=",",thousands=".",encoding="cp1252",infer_datetime_format=True)


# In[4]:


df.count()


# In[5]:


# dataframe para dados de Porto Alegre
dfPOA = df
#dfPOA = df[df['COD_IBGE'] == 431490]
dfPOA = dfPOA[['COD_IBGE','MUNICIPIO','DATA_CONFIRMACAO','DATA_SINTOMAS','DATA_EVOLUCAO','EVOLUCAO']]
dfPOA['DATA_CONFIRMACAO'] =pd.to_datetime(dfPOA.DATA_CONFIRMACAO,format='%d/%m/%y')
dfPOA['DATA_SINTOMAS'] =pd.to_datetime(dfPOA.DATA_SINTOMAS,format='%d/%m/%y')
dfPOA.sort_values(by='DATA_CONFIRMACAO',ascending=True)


# In[6]:


# dataframe para obitos
dfObitos = dfPOA[dfPOA['EVOLUCAO']=='OBITO']
dfObitos = dfObitos[['DATA_EVOLUCAO','EVOLUCAO']]
dfObitos['DATA_EVOLUCAO'] =pd.to_datetime(dfObitos.DATA_EVOLUCAO,format='%d/%m/%y')
dfObitos.sort_values(by='DATA_EVOLUCAO',ascending=True)
dfObitos = dfObitos.rename(columns={'DATA_EVOLUCAO':'Date','EVOLUCAO':'TOT_DIA'})
dfObitos = dfObitos.groupby(['Date']).count()
dfObitos['TOT_OBITOS'] = dfObitos.cumsum()
dfObitos = dfObitos.reset_index()
dfObitos


# In[7]:


# dataframe para dados com data de sintomas
dfDtConf = dfPOA[['DATA_CONFIRMACAO','COD_IBGE']]
dfDtConf = dfDtConf.rename(columns={'DATA_CONFIRMACAO':'Date','COD_IBGE':'TOT_DIA'})
dfDtConf = dfDtConf.groupby(['Date']).count()


# In[8]:


# acumulados por data de confirmacao
dfDtConf['TOT_CONF'] = dfDtConf.cumsum()
dfDtConf = dfDtConf.reset_index()
dfDtConf


# In[9]:


# dataframe para dados com data de sintomas
dfDtSint = dfPOA[['DATA_SINTOMAS','COD_IBGE']]
dfDtSint = dfDtSint.rename(columns={'DATA_SINTOMAS':'Date','COD_IBGE':'TOT_DIA'})
dfDtSint = dfDtSint.groupby(['Date']).count()


# In[10]:


# acumulados por data de sintomas
dfDtSint['TOT_SINT'] = dfDtSint.cumsum()
#dfDtSint = dfDtSint.drop(['TOT_DIA'],axis=1)
dfDtSint = dfDtSint.reset_index()
dfDtSint


# In[11]:


# Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=dfDtConf['Date'],y=dfDtConf['TOT_CONF'],
                    mode='lines',
                    name='casos acumulados por data de confirmação'))
fig.add_trace(go.Scatter(x=dfDtSint['Date'],y=dfDtSint['TOT_SINT'],
                     mode='lines',
                     name='casos acumulados por data de sintomas'))
fig.add_trace(go.Scatter(x=dfObitos['Date'],y=dfObitos['TOT_OBITOS'],
                      mode='lines',
                      name='óbitos acumulados por data'))
fig.add_trace(go.Bar(x=dfDtConf['Date'],y=dfDtConf['TOT_DIA'],name="conf/dia"))
fig.update_layout(title_text='data confimação, data dos sintomas e confirmados por dia')
fig.show()


# In[12]:


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=dfObitos['Date'],y=dfObitos['TOT_OBITOS'],
                      mode='lines',
                      name='óbitos acumulados por data'))
fig1.add_trace(go.Bar(x=dfObitos['Date'],y=dfObitos['TOT_DIA'],name="óbitos/dia"))
fig1.update_layout(title_text='óbitos acumulados e por dia')
fig1.show()


# In[ ]:




