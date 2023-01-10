#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# 
# # Create an experiment, simulate it and access results 
# 
# This notebook shows how to make a single simple experiment 
# 
# 1. Loading a pre-existing model in Modelflow
# 2. Creating an experimet by updating some variables
# 3. Simulating the model
# 4. Visualizing the results 
# 
# This Notebook uses a  model for Pakistan described here: {cite:author}`Burns2021`

# ## Imports
# 
# Modelflow's modelclass includes most of the methods needed to manage a model in Modelflow.

# In[2]:


from modelclass import model 
#model.widescreen()
#model.scroll_off()


# In[3]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# ## Load a pre-existing model, data and descriptions 
# The file `pak.pcim` contains a dump of model equations, dataframe, simulation options and variable descriptions. The file has been created when onboarding the model. 
# Examples can be found [here](../../onboard/eviews/onboard%20one%20model%20from%20%20wf1.html#onboard-a-model-defined-in-a-wf1-file)

# In[4]:


mpak,baseline = model.modelload('../../models/pak.pcim',alfa=0.7,run=1)


# ## Create an experiment
# The variable ```mpak``` contains the model instance and the variable   ```baseline``` contains the pandas dataframe with all series. 
# 
# We want to make an experiment where these variables: PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER are updated.
# 
# The  variables contains tax rates for CO2 emission from different sources. The descriptions can be retrieved like this: 

# :::{margin} **Variable descriptions**
# Are contained in the variable '''mpak.var_description''' 
# which is a dictionary
# :::

# In[5]:


for variable in ['PAKGGREVCO2CER', 'PAKGGREVCO2GER', 'PAKGGREVCO2OER']:
    print(variable,':',mpak.var_description[variable])
    


# In[6]:


extra_description = {'PAKNYGDPMKTPKN': 'GDP',
 'PAKNECONPRVTKN': 'Consumption',
 'PAKNEGDIFTOTKN': 'Investment',
 'PAKNEEXPGNFSKN': 'Exports',
 'PAKNEIMPGNFSKN': 'Import',
 'PAKLMUNRTOTLCN': 'Unemployment rate',
 'PAKGGDBTTOTLCN_': 'Debt (%GDP)',
 'PAKCCEMISCO2TKN': 'Total emissions from fossil fuels',
 'PAKCCEMISCO2CKN': 'Emissions from Coal',
 'PAKCCEMISCO2OKN': 'Emissions from Oil',
 'PAKCCEMISCO2GKN': 'Emissions from Natural Gas',
 'PAKGGREVTOTLCN': 'Fiscal revenues',
 'PAKWDL': 'Working days lost due to pollution'}
mpak.set_var_description({**mpak.var_description,**extra_description})


# # Update 
# In order to update series in a pandas dataframe, one can use the pandas functions.

# In[7]:


alternative_pd = baseline.copy()
alternative_pd.loc[2023:2100,['PAKGGREVCO2CER','PAKGGREVCO2GER', 'PAKGGREVCO2OER']] = 29 


# However modelflow contains some functions which has been designed to make updating economic series parsimonious and effective.
# 
# ```dataframe.upd``` creates a new dataframe where the tree tax variables are updated. You will find more [here](../update/model%20update.ipynb)

# In[8]:


alternative  =  baseline.upd("<2023 2100> PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER = 29")


# ## Run the model with all the scenarios

# In[9]:


result = mpak(alternative,2020,2100) # simulates the model 


# ## Access results 
# 
# Now we have two dataframes with results ```baseline``` and ```result```. These dataframes can be manipulated and visualized
# with the tools provided by the **pandas** library and other like **Matplotlib** and **Plotly**. However to make things easy the first and
# latest simulation result is also in the mpak object:
# 
# - **mpak.basedf**: Dataframe with the values for baseline
# - **mpak.lastdf**: Dataframe with the values for alternative  
# 
# 

# ### An overview of GDP

# In[10]:


with mpak.set_smpl(2020,2023):   # set smpl in the indented block
    mpak.PAKNYGDPMKTPKN.show


# ### Look at selected variables with the [] operator 
# If you want to look at multiple variables the index [] operator can be used to select the variables to analyze/visualize. Here only a few operations will be shown. There is more [here](index-operator)

# In[11]:


mpak['PAKNYGDPMKTPKN PAKNECONGOVTKN PAKNEGDIFTOTKN PAKNEIMPGNFSKN PAKCCEMISCO2TKN']


# In[ ]:




