#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')


# 
# # One target one instrument with 3 instrument variables
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
import modelmf
model.widescreen()
model.scroll_off()


# In[3]:


import modelmf

from modelinvert import targets_instruments
from modelclass import model


# In[4]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# ## Load a pre-existing model, data and descriptions 
# The file `pak.pcim` contains a dump of model equations, dataframe, simulation options and variable descriptions. The file has been created when onboarding the model. 
# Examples can be found [here](../../onboard/eviews/onboard%20one%20model%20from%20%20wf1.html#onboard-a-model-defined-in-a-wf1-file)

# In[5]:


mpak,baseline = model.modelload('../../models/pak.pcim',alfa=0.7,run=1,ljit=0)


# ## Define targets and instruments
# In year 2100 we want to reduce the emission **PAKCCEMISCO2TKN** to a percent of the baseline (business as usual)
# 
# There is a tax rate for 3 different emission fuel types: 

# In[6]:


for variable in ['PAKGGREVCO2CER', 'PAKGGREVCO2GER', 'PAKGGREVCO2OER', ]:
    print(variable,':',mpak.var_description[variable])
    


# So the tax instrument consists of 3 variables. 

# In[7]:


target_var = ['PAKCCEMISCO2TKN']
instruments = [['PAKGGREVCO2CER','PAKGGREVCO2GER', 'PAKGGREVCO2OER']]


# ## Set the target reduction 

# In[8]:


reduction_percent = 30   # Input the desired reduction 


# In[9]:


bau_2100 =baseline.loc[2100,'PAKCCEMISCO2TKN']
bau_2022 = baseline.loc[2022,'PAKCCEMISCO2TKN']
bau_growth_rate = (bau_2100/bau_2022)**(1/(2100-2022))

target_2100 = baseline.loc[2100,'PAKCCEMISCO2TKN']*(1-reduction_percent/100)
target_growth_rate = (target_2100/bau_2022)**(1/(2100-2022))

print(f"Business as usual Emission value in 2100: {bau_2100:13,.0f}")
print(f"Business as usual Emission value in 2100: {target_2100:13,.0f}")
print(f"Business as usual growth rate in percent: {bau_growth_rate-1:13,.1%}")
print(f"Target growth rate in percent           : {target_growth_rate-1:13,.1%}")


# ## Create a dataframe with the target 

# In[10]:


target_before = baseline.loc[2022:,['PAKCCEMISCO2TKN']]     # Create dataframe with only the target variable 
# create a target dataframe with a projection of the target variable 
target = target_before.mfcalc(f'PAKCCEMISCO2TKN = PAKCCEMISCO2TKN(-1) * {target_growth_rate}',2023,2100 )


# ## Now solve the problem: 

# In[11]:


_ = mpak.invert(mpak.basedf,                  # Invert calls the target instrument device                   
                targets = target,                   
                instruments=instruments,
                DefaultImpuls=2,              # The default impulse instrument variables 
                defaultconv=2.0,              # Convergergence criteria for targets
                varimpulse=True,              # Only change the variable for current period
                nonlin=15,                    # If no convergence in 15 iteration recalculate jacobi 
                silent=1                      # Don't show iteration output (try 1 for showing)
                )


# ## Make a graph and decorate with a line and an annotation
# Also show the tax rate

# In[12]:


with mpak.set_smpl(2020,2100):    # change if you want another  timeframe 
    fig = mpak[f'PAKCCEMISCO2TKN' ].plot_alt(title='Pakistan')
    fig.axes[0].axhline( target_2100,
                                  xmin=0.6,
                                  xmax = 0.99,
                                  linewidth=3, 
                                  color='r', ls='dashed')

    fig.axes[0].annotate(f'BAU 2050 reduced by {reduction_percent}%', xy=(2050,target_2100 ))
    fig2 = mpak[f'PAKGGREVCO2CER' ].plot_alt(title=f'Pakistan'); 


# ### Look at selected variables with the [] operator 
# If you want to look at multiple variables the index [] operator can be used to select the variables to analyze/visualize. Here only a few operations will be shown. There is more [here](index-operator)

# In[13]:


mpak['PAKNYGDPMKTPKN PAKNECONGOVTKN PAKNEGDIFTOTKN PAKNEIMPGNFSKN PAKCCEMISCO2TKN']


# ## Now define instruments so they don't get the same shock. 
# Here the coal emission gets twice the shock as the two other. 

# In[14]:


new_instruments =[[('PAKGGREVCO2CER',10),
                   ('PAKGGREVCO2GER', 5),
                   ('PAKGGREVCO2OER',5)]]


_ = mpak.invert(mpak.basedf,targets = target,
                            instruments=new_instruments,
                          DefaultImpuls=1,
                                defaultconv=2.0,varimpulse=True,nonlin=15,silent=1)


# In[15]:


with mpak.set_smpl(2020,2100):    # change if you want another  timeframe 
    fig = mpak[f'PAKCCEMISCO2TKN' ].plot_alt(title='Pakistan')
    fig.axes[0].axhline( target_2100,
                                  xmin=0.6,
                                  xmax = 0.99,
                                  linewidth=3, 
                                  color='r', ls='dashed')

    fig.axes[0].annotate(f'BAU 2050 reduced by {reduction_percent}%', xy=(2050,target_2100*1.015 ))


# In[16]:


mpak['PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER' ]


# In[17]:


help(mpak.invert)


# In[18]:


import modelinvert
help(modelinvert.targets_instruments)


# In[ ]:




