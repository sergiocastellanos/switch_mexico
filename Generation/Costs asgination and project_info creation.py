
# coding: utf-8

# In[24]:

import pandas as pd 
import numpy as np
df1=pd.read_csv("data/PowerPlants.csv",header=0,index_col=0)
df2=pd.read_csv("data/TechCostsSergio.tab",sep="\t",header=0,index_col=0)
df2=df2[df2['investment_period']==2020]
df2=df2.drop(['investment_period','source','Unnamed: 6'],axis=1)
#selecting only the generating plants of interest. See report for more details.
df1=df1.loc[df1['being_built'].isin([a for a in list(set(df1['being_built'].tolist())) if a  not in ['generic_project','optimization']])]

# In[25]:

for index in df1.index.tolist():
    for name in ['fixed_o_m','variable_o_m','overnight_cost']:
        df1.loc[index,name]=df2.loc[df1.loc[index,'gen_tech'],"g_"+name]

#adjusting outage rates from percentages to fractions
df1['scheduled_outage_rate']=df1['scheduled_outage_rate']/100
df1['forced_outage_rate']=df1['forced_outage_rate']/100
#adding a value for plants that are units of bigger plants
names=df1.index.tolist()
temp=pd.DataFrame(columns=df1.columns)
for index,row in df1.iterrows():
    if any(x[0]=='u' and len(x)==2 for x in index.split("_")):
        #print index
        #print x
        #print "unidad {0} de {1}".format(x[1],index.replace("_"+x,""))
        temp=temp.append(row)
        temp.loc[index,'real_name']=index.replace(index[index.index('_u'):index.index('_u')+3],"")
    else: 
        temp=temp.append(row)
        temp.loc[index,'real_name']=index

# In[26]:

#export data
temp.index.name='project_name'
temp.to_csv('data/PowerPlantsWithCosts.csv')

'''
# In[27]:

#selecting columns that we need for project_info:
cols=["proj_gen_tech","proj_load_zone","proj_variable_o_m","proj_full_load_heat_rate","proj_forced_outage_rate","proj_scheduled_outage_rate","proj_dbid","proj_capacity_limit_mw"]
df3=pd.DataFrame(index=df1.index.tolist())
for name in cols:
    for index in df3.index.tolist():
        df3.loc[index,name]=df1.loc[index,name[5:]]
df3.index.name='PROJECT'
df3
df3.to_csv('../Main Tabs/project_info_trial.tab',sep="\t")

'''
# In[28]:
'''
#creation of variable_capacity_factors tab.
df4=pd.read_csv("../Main Tabs/timepoints.tab",sep="\t")
df5=pd.DataFrame(index=pd.MultiIndex.from_product([df3[df3['proj_gen_tech'].isin(['wind','solar'])].index.tolist(),df4['timepoint_id'].tolist()]))         
df5.to_csv('../Main Tabs/variable_capacity_factors_trial.tab',sep="\t")

'''
# In[ ]:



