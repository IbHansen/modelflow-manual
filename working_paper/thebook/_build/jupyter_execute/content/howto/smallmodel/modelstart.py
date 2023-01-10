#!/usr/bin/env python
# coding: utf-8

# 
# # Create a small model from scratch and save it
# 
# **Modelflow can manage models but it can't estimate equations**. There are many different estimation programs around, each with certain  capabilities. 
# 
# In this notebook a small model estimated in Eviews is created in modelflow and solved. 

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import pandas as pd


# In[3]:


from  modelmacrograb import GrabMacroModel
from modelclass import model
model.widescreen()


# In[4]:


import modeljupytermagic  # to activate %%dataframe


# ## Load the  national account data 
# Using a jupyter magic command (something starting with %%) defined in modeljupytermagic

# In[5]:


get_ipython().run_cell_magic('dataframe', 'smalldata start=2011', 'Y CPV I G X M YDISC\n2011 1562682. 1320302. 373938.8 131272.0 121715.0 444232.2 59686.22\n2012 1632040. 1360376. 381170.2 128860.1 146292.9 457745.7 73087.14\n2013 1689572. 1396402. 414556.8 124254.9 165234.6 522447.7 111572.0\n2014 1791141. 1438904. 466473.0 138532.7 194705.5 632207.9 184733.1\n2015 1862357. 1476067. 536416.7 154466.9 199214.9 692794.8 188986.9\n2016 1870424. 1537410. 570679.5 135990.5 164738.9 714625.6 176230.0\n2017 2038337. 1549515. 702407.5 165119.3 179327.0 916469.9 358437.5\n2018 2193706. 1645118. 785371.4 168506.8 193124.7 1090956. 492542.0\n2019 2339741. 1737872. 874480.5 180872.4 203830.6 1154398. 497084.1\n2020 2295808. 1802824. 843961.1 192010.8 171282.5 978064.9 263794.1\n2021 2327410. 1846635. 866899.3 211728.7 140302.8 1009072. 270916.5\n2022 2402827. 1914157. 941428.0 240255.2 152623.9 1127119. 281482.2\n2023 2536741. 2007600. 1060909. 252761.7 179968.7 1260336. 295838.0\n2024 2715810. 2151422. 1205927. 278364.4 199108.6 1414850. 295837.8\n2025 2924763. 2300322. 1359892. 307746.9 220190.6 1559226. 295837.8\n2026 3140827. 2444181. 1512696. 337450.3 242638.9 1691977. 295837.8\n2027 3335992. 2552411. 1652032. 363373.5 266225.5 1793888. 295837.8\n2028 3528125. 2635657. 1787782. 388431.1 290729.5 1870312. 295837.8\n2029 3729062. 2714120. 1927845. 414569.4 316021.6 1939332. 295837.8\n2030 3945452. 2802550. 2076752. 441658.4 342117.3 2013464. 295837.8\n')


# ### Now we got a pandas dataframe with the values

# In[6]:


smalldata


# ## Specify  a (small demo) model 

# Consumption
# Lets make consumption a function of GDP (a proxy for incomes) and just to be fancy we will do it an error correction format.
# 
# **Long run equation**
# 
# $ CPV_t= \alpha + \beta * Y_t +\eta_t $
# 
# In error correction format:
# 
# $ \Delta cpv_t = - \gamma *(cpv_{t-1}- y_{t-1} - \beta_2 ) + \Delta y_t $ where lowercase variables preprsent the logarithm of the original variable
# 
# For this model we assume that CPV, G, I, M can be specified in the same format.
# 
# So we have these **stochastic equations**: 
# 
# ```
#  dlog(cpv)= -gamma_cpv*(log(cpv(-1))-log(y(-1)) - beta_cpv)+beta2_cpv*dlog(y)
# 
#  dlog(g)=-gamma_g*(log(g(-1))-log(y(-1)) - beta_g)+beta2_g*dlog(y)
# 
#  dlog(i)=-gamma_i*(log(i(-1))-log(y(-1)-g(-1)) - beta_i)+beta2_i*dlog(y) 
#  
#  dlog(m)=-gamma_m*(log(m(-1))-log(gde(-1)) - beta_m)+beta2_m*dlog(gde)
#  
# ```
# 
#  
#  In addition we have **two identities**:  
# ``` 
#  y=cpv+i+g+x-m+ydisc
#  
#  gde=cpv+i+g
# ```
# 

# ## The Equations

# Now these equations are written in modelflow format and letting the parameters start with c as it makes it more easy to translate estimates from eviews. 
# 
# Each equation can be prefixed by options enclosed in \<>.
# 
# |Option|meaning|
# |:--- |:---|
# |fixable|The variable can have its value fixed when simulating |
# |damp|When using Gauss-Seidle solution method the equation can be damped|
# |ident|This is an identity, used when we have to calculate the values |
# 
# The specification is a **string** object and assigned to a variable called: fsmallmodel. 
# 

# In[7]:


fsmallmodel = '''
<fixable, damp> dlog(cpv)= -c2_cpv*(log(cpv(-1))-log(y(-1)) -        c1_cpv)+c3_cpv*dlog(y)

<fixable, damp> dlog(g)  = -c2_g*  (log(g(-1))-  log(y(-1)) -        c1_g)  +c3_g*dlog(y)

<fixable, damp> dlog(i)  =    -c2_i*  (log(i(-1))-  log(y(-1)-g(-1)) - c1_i)   +c3_i*dlog(y) 
 
<fixable, damp> dlog(m) =     -c2_m*  (log(m(-1))-   log(gde(-1))    - c1_m)   +c3_m*dlog(gde)
 
<ident> y=cpv+i+g+x-m+ydisc 
 
<ident> gde=cpv+i+g

'''


# ## Convert the specification to modelflow
# The **specification** in itself can not be used for anything useful - it is just a string. The next step is to use the 
# specification to create an instance of the  **model class** which can solve the model. Instances of the ```model class``` wraps most of the capabilities of modelflow. Actually we will create a number  
# instances of model, as there are additional calculations to be done. So for this particular type of model another class: ***GrabMacroModel** is used to process the model specification. It will handle: 
# - Introducing add_factors 
# - Normalize equations 
# - Make equations fixable 
# - Generate equations for fitted values
# - Create model to calculate add factors 
# - Create model to calculate fitted values
# - Create model to calculate identities 
# 
# In the next cell it is shown how each equation flows trough several steps. 
# 
# |information|meaning|
# |:---|:---|
# |Frml name|The options provided|
# |Endo_var|The left hand side variable|
# |Original|The original specification|
# |Preprocessed|Some preprocessing like: dlog(x>) --> (log(x)-log(x(-1)))|
# |Normalized|Isolation of the endogenous variable on the left hand side|
# |Calc_add_factor |An equation for calculating addfactor which makes left and right hand side match|
# |Fitted|An equation which calculate the original equation without add factor and fixing |
# 
# 

# ## On normalization and enrichment of equations 

# In[8]:


from modelnormalize import normal 
normal('dlog(a) = dlog(b(-7)) ')


# In[9]:


normal('a = b',make_fixable=1,make_fitted=1,add_add_factor=1)


# In[10]:


thismodel = GrabMacroModel(fsmallmodel,modelname = 'Small demo model',make_fitted = True, debug = True)


# ## Get the model
# As a convention **m** is used as prefix for model objects.
# 
# So the model is called ```msmallmodel```

# In[11]:


msmallmodel = thismodel.mmodel


# ### Inject some variable descriptions. 
# A Python dictionary is used for storing variable descriptions. 

# In[12]:


descriptions = {
    'CPV'   : 'Private Consumption',
    'Y'     : 'GDP' ,
    'G'     : 'Government' ,
    'I'     : 'Investment',
    'GDE'   : 'Gross Domestic Expenditure',
    'X'     : 'Export',
    'M'     : 'Import',
    'YDISC' :  'Discrepance',
}
msmallmodel.set_var_description(msmallmodel.enrich_var_description(descriptions))


# ### The model equations
# Each equation has the form:
# >FRML \<[options]...> \<left hand variable> = \<right hand side expression>$
# 
# Equations with the option ```CALC_ADD_FACTOR``` specifies a separate model which can be used to calculate the add factors 
# which makes left hand side equals to the right hand side (without any fixing) 
# 
# So there are actually specified two models. 

# In[13]:


print(msmallmodel.equations)


# ### The model structure can be drawn
# Notice that mouseover shows additional information

# In[14]:


msmallmodel.drawmodel(size = (10,10))


# ### Only the endogenous variables

# In[15]:


msmallmodel.drawendo()


# ### The adjacendy matrix for the endogenous variables. 

# In[16]:


msmallmodel.plotadjacency();


# In[17]:


msmallmodel.endogene


# In[18]:


msmallmodel.exogene


# ## The Dataframe has to be enriched: 
# 
# - The the parameter values
# - Variables mentioned in the model, but not present in the dataframe 
# - Calculated variables from the model has to be calculated 
# - Add factors ensuring that the solution match the data has to be calculated. 

# ### The parameter values
# Modelflow is **not an estimation tool**. So we have to provide the estimated parameters. <br>
# This can be done in several way: 
#  - The parameters can be input into the equations. This can be automated.
#  - The parameters can be broadcast into a dataframe. Which is what we will do here.
#  
#  For this purpose a "magic" jupyter command will be used. It will create a dataframe with the right values: 
#  
# **Modelflow don't have a special datatype for parameters** so we just repeat the same value for all years 

# In[19]:


get_ipython().run_cell_magic('dataframe', 'parameters   periods=20 start=2011 melt t', '\n      c2      c1      c3 \ncpv   0.38 -0.11 0.02946\ng     0.3 -2.5974  1.332   \ni     0.027947 -0.515348 1.6967\nm     0.37  -1.57 5.0929 \n')


# In[20]:


baseline_first  = pd.concat([smalldata,parameters_melted],axis=1) # the original data plus the parameters 
baseline_first  = msmallmodel.insertModelVar(baseline_first) # to make sure all modelvariable are in the dataframe 
baseline_first.head().T # show the result, transposed


# ### Generate the variables defined by identities in the specification.
# The two variable Y and GDE are not in the original data, but are defined in identities. This can be 
# handled by modelflow. Identities are marked by the option  \<IDENT>.   
# 
# A model which can calculate the identities based on the option can be extracted from the model instance by ```.get_histmodel()```.
# 
# This small model is run for all years. 

# In[21]:


hist_smallmodel = msmallmodel.get_histmodel()


# In[22]:


print(hist_smallmodel.equations) # .equations shows the equations in this model 


# In[23]:


baseline = hist_smallmodel(baseline_first,silent=1) # run the model 


# In[24]:


baseline[['Y','GDE']].head()  # .head() returns the first 5 rows


# ### Generate the add factors which will ensure that the model result match the data
# If we run the model now the result might be far from the actual values. To take care of this we have to calculate the add factors which makes this happen. The model for doing that is imbedded in the model - remember the equations for this where prepared in an earlier step. 
# 
# The model is named ```.calc_add_factor_model()``` and run for the relevant years: 
# 
# In addition if a model to create fitted values is present it will also be run. 

# In[25]:


fitbaseline = msmallmodel.calc_add_factor_model(baseline,'2016','2030')
fitbaseline = thismodel.mfitmodel(fitbaseline)


# In[26]:


fitbaseline.loc['2014':'2020',].T


# ## Now all data is ready and the model can be simulated

# In[27]:


result = msmallmodel(fitbaseline,'2020','2030',silent=0,solver='sim',alfa=0.5)
msmallmodel.basedf = fitbaseline # To make comparasion possible. 


# ## The solution match the actual values
# So it is a starting point for scenario experiments

# In[28]:


msmallmodel['#endo'] 


# ## Dump the model and the data in a file to be used in the next episode 

# In[29]:


msmallmodel.modeldump('models/smallmodel.pcim')


# In[ ]:




