#!/usr/bin/env python
# coding: utf-8

# In[14]:


import numpy as np
import pandas as pd


# In[15]:


#busca balancetes de receitas de 2017
url = "http://dados.tce.rs.gov.br/dados/municipal/balancete-receita/2018.csv.zip"
df1 = pd.read_csv('receitas_2018-1.csv', header=0, sep=';',decimal=",",thousands=".")


# In[16]:


df1.head()


# In[18]:


import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly.io as pio
import plotly.offline as offline

pio.renderers.default = "browser"

df = df1
# condicoes para extinção dos municipios
# df = df1[df1['HABITANTES'] <= 5000]
# df = df[df['PercPropria'] < 10]


bubble_size = []
hover_text = []

# Create figure
fig = go.Figure()

for index, row in df.iterrows():
    hover_text.append(('Município: {Municipio}<br>'+
                      'Receita Total: {ReceitaTotal}<br>'+
                      'População: {HABITANTES}<br>'+
                      'Receita Própria: {ReceitaPropria}<br>'+
                      '% Receita Própria: {PercPropria}').format(Municipio=row['Município'],
                                                                 ReceitaTotal="{:,.2f}".format(row['ReceitaTotal']),
                                                                 HABITANTES="{:,.2f}".format(row['HABITANTES']),
                                                                 ReceitaPropria="{:,.2f}".format(row['ReceitaPropria']),
                                                                 PercPropria="{:.2%}".format(row['PercPropria']/100)).format())
    bubble_size.append(row['ReceitaTotal'])
    
df['text'] = hover_text
df['size'] = bubble_size
sizeref = 2.*max(df['size'])/(100**2)


fig.add_trace(go.Scatter(
       x=df['HABITANTES'], y=df['PercPropria'],
       name='Porto', 
       text=df['text'],
       marker_size=df['size'] 
       ))



# Tune marker appearance and layout
fig.update_traces(mode='markers', marker=dict(sizemode='area', color=df['PercPropria'],
                                              sizeref=sizeref, line_width=2,showscale=True))


fig.update_layout(
    title='% Receita Própria x População',
    xaxis=dict(
        title='População',
        gridcolor='white',
        type='log',
        gridwidth=2,
    ),
    yaxis=dict(
        title='% Receita Própria',
        gridcolor='white',
#        type='log',
        gridwidth=2,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
)
## offline.plot(fig, filename = 'X:\DCF\CGEX\misc\Grafico PopulaçãoXReceitaPropria\ReceitaXPopulacao.html', auto_open=False)
fig.show()    
#df.head()    
    


# In[42]:


df.count()


# In[60]:


df = df.sort_values('HABITANTES')


# In[61]:


df


# In[80]:


'{:,}'.format(1234567890)


# In[ ]:




