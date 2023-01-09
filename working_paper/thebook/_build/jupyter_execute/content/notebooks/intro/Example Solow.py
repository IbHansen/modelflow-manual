#!/usr/bin/env python
# coding: utf-8

# # Example Solow model 
# 
# 
# In this jupyter notebook we will specify, solve and analyse a simple Solow model in ModelFlow. 
#     

# In[1]:


if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb ipysheet  --no-dependencies ')
  incolab = True  
else:
  incolab = False 


# In[2]:


#Required packages
import pandas as pd

# Modelflow modules
from modelclass import model
   
#for publication 
latex=0
model.widescreen()


# 
# ## Specify the model 
# We start by defining the logic of the Solow model in the Business Logic Language.   
# 
# 

# :::{margin} **Business Logic Language**
# More on how to specify models [here](../intro/model%20specification.ipynb)
# :::

# In[3]:


fsolow = '''\
Income          = a  * Capital**alfa * Labor **(1-alfa) 
Consumption     = (1-saving_rate)  * Income 
Investment      = Income - Consumption   
diff(Capital)   = Investment-Depreciation_rate * Capital(-1)
diff(Labor)     = Labor_growth * Labor(-1)  
Capital_intensity = Capital/Labor 
'''


# ## Create a model class instance
# 
# After defining the Business Logic Language and storing it in the variable 'fsolow', we create a class instance called msolow. 

# In[4]:


msolow = model.from_eq(fsolow,modelname='Solow model')


# Above the equation for Capital and Labor on the left hand side of the = (equal to) consist of an expressing ```diff(Capital)``` and ```diff(Labor)```. **The equations are not normalized**. 
# 
# To solve a model in modelflow **all equations has to be normalized**. Meaning that the left hand side only consist of variables not expressions. So the function ```model.from_eq``` will normalize the equations as the first step before the model can be solved. 
# 
# In this case **first** ```diff(Capital)``` is transformed to $\Delta capital = capital-capital(-1)$. **Then** the lagged variables is moved to the right side of the =. 
#  The same goes for diff(labor).
#  
# So the normalized business language of the model now looks like:

# In[5]:


msolow.print_model


# ## Create some data 
# 
# To show what Modelflow can do, we create a Pandas dataframe with input data. And print the first 5 out of 300 observations.  

# In[6]:


N = 300  
df = pd.DataFrame({'LABOR':[100]*N,
                   'CAPITAL':[100]*N, 
                   'ALFA':[0.5]*N, 
                   'A': [1]*N, 
                   'DEPRECIATION_RATE': [0.05]*N, 
                   'LABOR_GROWTH': [0.01]*N, 
                   'SAVING_RATE':[0.05]*N})
df.head(2) #this prints out the first 5 rows of the dataframe


# ## Run the model 

# In[7]:


result = msolow(df,keep='Baseline') # The model is simulated for all years possible 
result.head(29)


# ## Create a scenario and run again 

# :::{margin} **dataframe.upd**
# When importing modelclass all pandas dataframes are enriched with a a handy way to create a new pandas dataframe with updated series. 
# 
# In this case df.upd will create a a new dataframe with updated LABOR_GROWTH 
# 
# For additional explanation look [here](../../howto/update/model%20update.ipynb)
# :::

# In[8]:


dfscenario = df.upd('LABOR_GROWTH + 0.002')  # create a new dataframe, increase LABOR_GROWTH by 0.002
scenario   = msolow(dfscenario,keep='Higher labor growth ') # simulate the model 


# ## Now the results are also embedded in msolow.  
# 
# 
#  - ```.basedf``` contains the first run of the model 
#  - ```.lastdf``` contains the last run of the model 
#  
#  Also in this case the keyword ```keep``` is used. This causes the results to be  stored in a dictionary ```msolow.keep_solutions```. This can be useful when comparing several scenarios. 
#  

# ## Inspect results  

# ### Using the [ ] operator 

# We can select the variables of interest with wildcards. This will operate the results stored in ```basedf``` and ```.lastdf```

# #### Look at variables starting with a C 

# In[9]:


msolow['#ENDO']


# #### Look at all endogenous variables

# In[10]:


msolow['labor*'].dif.plot() 


# ### Using the keept solutions 
# As mentioned above, because the keyword ```keep``` was used. The results are also stored in a dictionary. These data can 
# also be used for charting. 
# 
# The reason for placing the results in a dictionary is to enable comparison of many scenarios, not just the first and the last. 

# In[11]:


with msolow.set_smpl(1,30):
    msolow.keep_plot('income con*' ); 


# In[12]:


# msolow.modeldash('INCOME',jupyter=1)


# ## More advanced topics

# ### The logical stucture 
# Now the model has been analyzed, and the structure can be displayed.
# 
# You will find more on the logical structure [here](../../howto/structure/Logical_structure.ipynb)

# #### Model structure

# In[13]:


msolow.drawmodel( title="Model Structure", png=latex,size=(15,15))


# #### Adjacency matrix
# 
# Another way to illustrate the dependency graph is an adjacency matrix. 

# In[14]:


msolow.plotadjacency();


# The variables  ['INVESTMENT', 'CONSUMPTION', 'CAPITAL', 'INCOME'] in the red area are the core of the model and has to be solved as a system. 
# 
# LABOR is the prolog and can be calculated before the core is solved. While CAPITAL_INTENSE is the epilog which can be calculated after the core is solved. 
# 
# Many models comform to this pattern. And for solving purpose a model is divided into a prolog, core and an epilog. Even if the core is actually consistent of several strong components. 

# (solow-python-code)=
# ### The python function used to solve the model
# In order to solve the model Modelflow will generate a python function which implements the model. The user will hopeful  newer have to relate to the generated python code. **The point of modelflow is, that the user has to relate to the specification of the business logic, not the implementation in code**  

# In[15]:


print(msolow.make_los_text)


# In[ ]:




