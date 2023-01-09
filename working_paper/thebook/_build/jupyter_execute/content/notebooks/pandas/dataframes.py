#!/usr/bin/env python
# coding: utf-8

# # Introduction to Pandas dataframes
# 
# Modelflow is built on top of the Pandas library. Pandas is the Swiss knife of data science and can perform an impressing array of tasks.
# 
# This tutorial is a very short introduction to how pandas dataframes are used with Modelflow.
# 
# For more info on pandas:
# 
# [Pandas homepage](https://pandas.pydata.org/)
# 
# [Pandas community tutorials](https://pandas.pydata.org/pandas-docs/stable/getting_started/tutorials.html)
# 

# ## Import the pandas library
# The convention is, that pandas is imported as pd 

# In[1]:


import pandas as pd 


# ## What is a dataframe
# 
# A dataframe is a two-dimensional data structure with named rows and columns </span>
# 
# Creating a dataframe can be done in many ways. Here we are creating a Dataframe from a dictionary and  assigning a list of years as the index.

# In[2]:


df = pd.DataFrame({'B': [1,1,1,1],'C':[1,2,3,6],'E':[4,4,4,4]},index=[2018,2019,2020,2021])
df 


# In modelflow each column is a  time serie for an economic variable. So in this dataframe A, B and C are economic time series. 
# 
# In this manual all variables will be timeseries scalars (numbers). <br>
# However for more advanced use a variable can also be a timeserie of matrices or vectors.  

# ## Attributes
# 
# Lets take a look at some of the most important attributes of a dataframe.
# 
# To learn more check out the [official pandas website](https://pandas.pydata.org/docs/reference/frame.html).

# ```{margin} Python object properties
# A python object such as ```df``` has properties and methods.<br> 
# They are accessed by the . operator
# ```

# ### .columns, column names
# .columns gives you the names of the columns in the dataframe.

# In[3]:


df.columns


# The dataframe df has 3 columns. 

# ### Column names in  Modelflow 
# ```{margin} Modelflow variable names
# Many python Objects are legal as column names in a dataframe, but not as variable names (column names)  in modelflow
# ```
# The columns have names.<br>In A dataframe column names can be many different python objects. So for instance 123.4  is a legal column name. That would make construction of models very impossible. 
#  <br>To facilitate construction of models modelflow a column name has to be a  string and start with a letter or _  and followed by letters, underscore or digits.<br>
# **All letters in column names should be upper case.**  
# 
#  - ```IB``` is legal 
#  - ```ib``` is illegal 
#  - ```42ANSVER``` is illegal 
#  - ```_HORSE1``` is legal 
#  - ```AVERY_LONG_VAIABLE_NAME_WHIS_IS_LEGAL``` is legal

# ### .index and time dimensions in Modelflow

# The row names are called .index. For yearly models a list of integers like in ```df``` is fine.<br>
# Pandas has a number of data types for different date and time objects. They can all be used for models with other frequencies.<br>However be aware that plots will not necessary be working well with all index names. 
# 
# When modelflow uses a lagged variable like ```A(-1)``` It will take the value from the row above the current row. No matter if the index is an integer, a year, quarter or a millisecond. The same goes for leads ```A(+1)```  That will be the value in the next row. 

# In[4]:


df.index


# <span style='color:Blue'> Freya comment: So what is the take away here? Is this about naming indexes? Or what instance of time is? The user can define this, no? If its a timeserie based on rows (based on whatever time frame that spans) or something else?</span>
# 
# 

# ### .eval() evalueation expressions 
# With this method expressions can be evaluated and new columns created.  

# In[5]:


df.eval('''X = B*C
           THE_ANSWER = 42''')


# However, .eval cannot handle lagged variables and no systems of equations. Modelflow can! 

# ### .loc[] when slicing a dataframe

# #### .loc[row,column] A single element

# In[6]:


df.loc[2019,'C']


# #### .loc[:,column] A single column

# In[7]:


df.loc[:,'C']


# #### .loc[row,:] A single row 

# In[8]:


df.loc[2019,:]


# ####  .loc[:,[names...]] Several columns

# In[9]:


df.loc[:,['B','C']]


# #### .loc[] Slices of the dataframe can also be assigned values 
# This can be very handy when updating scenarios.<br>
# 

# In[10]:


df.loc[2019,'C'] = 42
df


# ```{warning}
# The dimensions on the right hand side of = and the left hand side should match. That is: either the dimensions should be the same, or the right hand side should be broadcasted into the left hand slice.
# A link [here](https://jakevdp.github.io/PythonDataScienceHandbook/02.05-computation-on-arrays-broadcasting.html)
# ```

# <span style='color:Blue'> Freya comment: I would delete this. </span> 
# 
# <span style='color:Blue'> ib comment: Det er en warning label i jupyter book .  </span> 
# 
# this is hidden 

# In[ ]:




