#!/usr/bin/env python
# coding: utf-8

# # Experiment: Export up  
# Take a small very small model and make some experiments 

# %load_ext autoreload   # To ensure code changes are implemented imidiatly 
# %autoreload 2

# In[1]:


import pandas as pd


# In[2]:


from modelclass import model
model.widescreen()


# ## Load the precooked model 
# This model was generated from scratch [here](modelstart.ipynb)

# In[3]:


msmallmodel,baseline = model.modelload('models/smallmodel.pcim',run=1,keep='Baseline',silent=1)


# ## Create new dataframe where the export is increased by 10 percent

# In[4]:


impuls_x_10pct = baseline.upd("<2024 2027> x % 10")


# In[5]:


impuls_x_5pct = baseline.upd("<2024 2027> x % 5")


# ## Simulate the model 

# In[6]:


result_x = msmallmodel(impuls_x_10pct,keep='Export increased by 10 percent',alfa=0.2,solver='newton',silent=1)


# In[7]:


_ = msmallmodel(impuls_x_5pct,keep='Export increased by 5 percent',alfa=0.2,solver='newton',silent=1)


# ## Display results 

# In[8]:


with msmallmodel.set_smpl('2020','2030'):
    display(msmallmodel['y cpv g x m gde' ]) 


# In[9]:


msmallmodel['y cpv g  m gde'].difpctlevel.rename().mul100.plot(sharey=True);


# In[10]:


try:
    
    if 1: 
        msmallmodel.modeldash('Y',jupyter=1,inline=0,dashport=5006)
    else:
        print(42)
except Exception as e:
    print(f"Can't run modeldash here")


# In[ ]:





# In[11]:


msmallmodel.keep_plot('y m c',diff=1,legend=1);


# In[12]:


msmallmodel.keep_viz('Y')


# ### The charts generated in the interactive widget are stored in a Dictionary
# So all the charts can be processed using the tools from Matplotlib 

# In[13]:


msmallmodel.keep_wiz_figs   # Which charts have been generated 


# In[14]:


yfig = msmallmodel.keep_wiz_figs['Y']  # Select one of the graphs 


# In[15]:


yfig.savefig('graph/GDP.pdf')   # Safe the graph as a pdf file 


# In[16]:


get_ipython().system('dir graph')


# In[17]:


display(yfig)


# ### The result  can be saved to an excel sheet 

# In[18]:


msmallmodel.lastdf.to_excel('smallmodel.xlsx')


# In[19]:


get_ipython().system('dir *.xlsx')


# In[ ]:




