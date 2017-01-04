
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
df1=pd.read_csv('tables/CategorizedCounties.csv',index_col=0,header=0,usecols=[0,9])
df2=pd.read_csv('tables/balancing_areas.csv',index_col=0,header=0)
df3=pd.read_csv('../../Main Tabs/csv/lz_peak_loads_mid.csv',header=0,index_col=0)
df2=df2.drop('00-autoabasto_local',axis=0)


# In[2]:

df=pd.DataFrame(index=df2.index,columns=['cost_multipliers','existing_local_td',"local_td_annual_cost_per_mw"])
df['cost_multipliers']=1
"""we calculate the existing local td as the peak demand 
of that load area multiplied by a factor that compensates 
ditribution loses. 
This factor contemplates that 15% of the energy generated is lost 
during the transmission and distribution."""
for k in df.index.tolist():
    df.loc[k,'existing_local_td']=df3.loc[k,"peak_demand_mw"].iloc[0]*100/85
"""Now we must assign a distribution cost to each load zone
as a first aproach, we will asign the distribution cost of each load area
to the distribution cost of the county where the load area is located 
(for example, the distribution cost of '20-tamazunchale' 
is the distribution cost of the tamazunchale county).
This is not representative as a load area distributes electricity to 
much more counties that the county that gives name to it."""
    


# In[63]:

df1.loc["01-hermosillo"[3:],"distributioncost2 (millions of mxn)"]


# In[ ]:




# In[ ]:




# In[3]:

for k in  df.index.tolist():
    try: df.loc[k,'local_td_annual_cost_per_mw']=df1.loc[k[3:],"distributioncost2 (millions of mxn)"]
    except: pass
#manual correction for load zones whose name does not match any county
df.loc['03-obregon','local_td_annual_cost_per_mw']=df1.loc['cajeme',"distributioncost2 (millions of mxn)"]
df.loc['04-los_mochis','local_td_annual_cost_per_mw']=df1.loc['ahome',"distributioncost2 (millions of mxn)"]
df.loc['07-juarez','local_td_annual_cost_per_mw']=df1.iloc[235,0]
df.loc['08-moctezuma','local_td_annual_cost_per_mw']=df1.iloc[1926,0]
df.loc['11-laguna','local_td_annual_cost_per_mw']=df1.loc['torreon',"distributioncost2 (millions of mxn)"]
df.loc['12-rio_escondido','local_td_annual_cost_per_mw']=df1.loc['piedras_negras',"distributioncost2 (millions of mxn)"]
df.loc['15-matamoros','local_td_annual_cost_per_mw']=df1.iloc[1999,0]
df.loc['18-valles','local_td_annual_cost_per_mw']=df1.iloc[1825,0]
df.loc['19-huasteca','local_td_annual_cost_per_mw']=df1.iloc[2006,0]
df.loc['29-lazaro_cardenas','local_td_annual_cost_per_mw']=df1.iloc[833,0]
df.loc['31-central','local_td_annual_cost_per_mw']=df1.loc['coyoacan',"distributioncost2 (millions of mxn)"]
df.loc['32-poza_rica','local_td_annual_cost_per_mw']=df1.loc['poza_rica_de_hidalgo',"distributioncost2 (millions of mxn)"]
df.loc['35-acapulco','local_td_annual_cost_per_mw']=df1.loc['acapulco_de_juarez',"distributioncost2 (millions of mxn)"]
df.loc['36-temascal','local_td_annual_cost_per_mw']=df1.loc['oaxaca_de_juarez',"distributioncost2 (millions of mxn)"]
df.loc['39-grijalva','local_td_annual_cost_per_mw']=df1.loc['tuxtla_gutierrez',"distributioncost2 (millions of mxn)"]
df.loc['43-cancun','local_td_annual_cost_per_mw']=df1.iloc[1808,0]
df.loc['44-chetumal','local_td_annual_cost_per_mw']=df1.loc['othon_p._blanco',"distributioncost2 (millions of mxn)"]
df.loc['50-villa_constitucion','local_td_annual_cost_per_mw']=df1.loc['comondu',"distributioncost2 (millions of mxn)"]
df.loc['51-la_paz','local_td_annual_cost_per_mw']=df1.iloc[18,0]




# In[4]:

for k in  df.index.tolist():
    df.loc[k,'local_td_annual_cost_per_mw']=df.loc[k,'local_td_annual_cost_per_mw']*64820/df.loc[k,'existing_local_td']


# In[6]:

df.to_csv('../../Main Tabs/csv/load_zones.csv')
df.to_csv('../../Main Tabs/load_zones.tab',sep="\t")


# In[ ]:




# In[ ]:



