
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd


# In[8]:

df = pd.read_csv("RawTables/2016.csv",index_col=range(4),skiprows=range(4),header=0)
for s in range(2017,2031):
    a = pd.read_csv("RawTables/{0}.csv".format(s),index_col=range(4),skiprows=range(4),header=0)
    a.columns=df.columns.tolist()
    df=df.append(a) 
centraldata=pd.read_csv("RawTables/Central.csv",header=0,index_col=range(4))
df['31-Central']=centraldata
del centraldata
col1=[]
col2=[]
for i in df.columns.tolist():
    col1.append(int(i[0:2]))
for i in range(1,55):
    try: col2.append(df.columns.tolist()[col1.index(i)])
    except ValueError: pass
df=df[col2]
df=df.astype('float64')


# In[9]:

for a in range(2016,2031):
    for m in range(1,13):
        for d in df.xs([a,m,1],level=[0,1,3]).index.tolist():
            for h in range(1,25):
                su=df.xs([a,m,d,h])[['54-loreto','50-villa_constitucion','51-la_paz','52-los_cabos']].sum()
                lo = df.xs([a,m,d,h])['54-loreto']
                df.xs([a,m,d,h])['50-villa_constitucion']*=su/(su-lo)
                df.xs([a,m,d,h])['51-la_paz']*=su/(su-lo)
                df.xs([a,m,d,h])['52-los_cabos']*=su/(su-lo)
df=df.drop('54-loreto',axis=1)


# In[10]:

#asigment of 2% from the monterrey node to the tamazunchale node
tama=pd.DataFrame(index=df.index,columns=['20-tamazunchale'])
for a in range(2016,2031):
    for m in range(1,13):
        for d in df.xs([a,m,1],level=[0,1,3]).index.tolist():
            for h in range(1,25):
                tama.xs([a,m,d,h])['20-tamazunchale']=df.xs([a,m,d,h])['16-monterrey']*.04
                df.xs([a,m,d,h])['16-monterrey']*=.96
df.insert(19,'20-tamazunchale',tama['20-tamazunchale'])


# In[11]:

for i in range(2016,2031):
    df.xs([i],level=0).to_csv('OrganizedTables/{0}.csv'.format(i))


# In[7]:




# In[ ]:




# In[ ]:



