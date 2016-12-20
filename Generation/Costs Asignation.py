
# coding: utf-8

# In[27]:

import pandas as pd 
import numpy as np
df1=pd.read_csv("data/PowerPlants.csv",header=0,index_col=0)
df2=pd.read_csv("data/TechCosts.csv",header=0,index_col=0)
def nearest_value(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]
def lis(x):
    if isinstance(x,list): return np.asarray(x)
    else: return np.asarray([x])
#selecting only the generating plants of interest. See report for more details.
df1=df1.loc[df1['being_built'].isin([a for a in list(set(df1['being_built'].tolist())) if a  not in ['generic_project','optimization']])]


# In[40]:

for i in df1.index.tolist():
    #setting auxiliary dataframe for plant gen_tech info
    df3=df2.loc[df1.loc[i,'gen_tech'],:]
    #iterating over the costs
    for name in ['fixed_o_m','variable_o_m','overnight_cost']:
        #selecting the costs according to the capacity and technology of the plant
        #try and except due to error with length of dataframe']
        try: a=df3.loc[df3['capacity_mw']==nearest_value(lis(df2.loc[df1.loc[i,'gen_tech'],'capacity_mw'].tolist()),df1.loc[i,'capacity_limit_mw'].astype('float'))]
        except KeyError: a=df3
        df1.loc[i,name]=float(a[name])


# In[41]:

#export data
df1.to_csv('data/PowerPlantsWithCosts.csv')


# In[ ]:




# In[ ]:




# In[ ]:



