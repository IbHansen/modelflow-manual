#!/usr/bin/env python
# coding: utf-8

# # Fixing the value of variables 
# Provided a model has been specified to allow this it is possible to fix the values of some endogenous variable. This can be 
# useful in many situations. Also when a variable is fixed a matching add factor is calculated. This keeps the result unchanged 
# when the fixing is lifted and the marginal properties of the model is preserved. 

# ## Import the model class
# This class incorporates most of the methods used to manage a model. 

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import pandas as pd
from modelclass import model 
import modelwidget as mw
model.widescreen()
model.scroll_off()


# ## Load a pre-existing model, data and descriptions 
# The file `pak.pcim` contains a dump of model equations, dataframe, simulation options and variable descriptions. The file was created separately. 
# 
# The modelload method returns an instance ```mpak``` of the ```model``` class, and a dataframe ```result``` that holds the baseline run. 

# In[3]:


mpak,result = model.modelload('../../models/pak.pcim',run=1,silent=1)


# ## How to fix the values for variables
# 
# The equation for a fixable variable should like this: 
# >frml <z,exo> VAR  = (expression)*(1-VAR_D) + VAR_X * VAR_D
# 
# Each endogenous variable which has an _D variable and _X variable can be fixed
#  
# _D=1 means that the variable is to be fixed and 
# 
# _X holds the value to which it should be fixed
# 
# In the pak model all stocastic equations are fixable.

# ### .fix(dataframe,variable pattern, start,end) Returns a dataframe where variables matching pattern are fixed
# 
# The code fixes the values for some variables by setting the _X variable to the current value, and _D variable to 1 in the timespan \[start,end].

# In[4]:


var_to_be_fixed = 'PAKGGEXPCAPTCN PAKGGEXPGNFSCN PAKGGEXPOTHRCN PAKGGEXPTRNSCN'
fix_df = mpak.fix(result,var_to_be_fixed,2021,2100)


# ## Now run the model with the new dataframe

# In[5]:


_ = mpak(fix_df,silent=1,keep=f'Baseline') # _ is just a  name, the dataframe is not going to be used 


# In[6]:


alternative  =  fix_df.upd("<2023 2100> PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER = 29")


# In[7]:


_ = mpak(alternative,silent=1,keep=f'Tax = 29',alfa = 0.5)


# In[8]:


with mpak.set_smpl(2020,2030):
    display(mpak['PAKNYGDPMKTPKN'])


# ### .fix_inf() Show relevant variables for each fixed variables
# To make it short we only show the first 4 years  

# In[9]:


with mpak.set_smpl(2021,2024):
    mpak.fix_inf()


# ### The result match the result before exogenizing, as it should 
# Numbers below show the difference in pct betwen the solution whitout and with fixing
# 
# The difference is small and OK 

# In[10]:


with mpak.keepswitch(True):
    mpak.keep_plot('PAKNYGDPMKTPKN',diffpct=1,dec=7)


# ## Dump the model and solution for later use

# In[11]:


mpak.modeldump('../../models/pak_exogenized.pcim')


# ## More advanced information
# The model instance (here mpak) maintain properties related to the fixing of values.

# ### List of potential and actual fixed variables
# The model instance (here mpak) maintain properties related to the fixing of values.
# 
# |Variable type|Variable name suffix|Lists for all fixable variables|List of fixed variables|
# |:--|:--|:--|:--|    
# Endogenous|  |.fix_endo|.fix_endo_fixed
# Dummy|_D|.fix_dummy|.fix_dummy_fixed
# Fixed value|_X|.fix_value|.fix_value_fixed
# Add factor|_A|.fix_add_factor|.fix_add_factor_fixed

# #### LIst of all fixable variables for this model 

# In[12]:


all_fix_var =[vars for vars in zip(mpak.fix_dummy,mpak.fix_value,mpak.fix_add_factor)]
fix_names = pd.DataFrame(all_fix_var,columns=['Dummy','Fixed value','Add factor'],index=mpak.fix_endo)
mw.htmlwidget_df(mpak,fix_names).show


# :::{note}
# **Dataframes with strings and zip**
# 
# Pandas dataframes are very versatile. Here the dataframe is filled not with scalars but with strings. 
# 
# Also the zip function is used to combine lists. [More here](https://docs.python.org/3/library/functions.html#zip)
# :::

# #### List of fixed variables

# In[13]:


fixed_fix_var =[vars for vars in 
                 zip(mpak.fix_dummy_fixed,mpak.fix_value_fixed,mpak.fix_add_factor_fixed)]
fixed_names = pd.DataFrame(fixed_fix_var,columns=['Dummy','Fixed value','Add factor'],index=mpak.fix_endo_fixed)
mw.htmlwidget_df(mpak,fixed_names).show


# #### Is there a model (.calc_add_factor_model) available  to calculate the add factors corresponding to the fixed values

# In[14]:


mpak.split_calc_add_factor


# #### Show the equations for the .calc_add_factor_model
# Here only 3 are displayed. Delete the [:3] and all equations will be displayed.

# In[15]:


mpak.calc_add_factor_model.equations.split('$')[:3]


# In[ ]:




