#!/usr/bin/env python
# coding: utf-8

# #  Extend Pandas dataframes with ModelFLow capabilities. 
# This Jupyter notebook show how ModelFlow can extend pandas dataframes to run models. 

# :::{note}
# I would find a home for this which is more general concerning modelflow /Ib 
# 
# Modelflow is a library based on the needs of Economists in particular. Economists often work with time series and want to make calculations based on the time indexed values of a number of variables. 
# 
# For example we may say that 
# 
# $\hat p_t = \hat p^e_{t}+  \alpha * (Y_t/Y^{pot}_t -1) + \beta *  (\hat p_{t-1}- \hat p^e_{t-1})$
# 
# The inflation rate ($\hat p_t$) in time t is a function of expected inflation ($p^e_{t}$), the output gap $(Y_t/Y^{pot}_t -1)$ and the one period earlier difference between the inflation rate and expected inflation  $\hat p_{t-1}$
# 
# Or we may want to have a system of simultaneous equations that allow for circular references, such that 
# 
# $Y_t = C_t +I_t +G_t +X_t - M_t$ 
# 
# $C_t= f(Y_t)$
# 
# $I_t= f(Y_t)$
# 
# $M_t= f(C_t,I_t)$
# :::

# ## Imports

# In[1]:


#some stuff to make Jupyter notebooks run a bit more smoothly 
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import pandas as pd  # Python data science library
import modelmf       # Add useful features to pandas dataframes 
                     # using utlities initially developed for modelflow


# ## Set up experiment

# ### Create a  simple dataframe 
# 
# Create a Pandas dataframe with one column with the name A and 6 rows.
# 
# Set set the index to 2020 through 2026 and set the values of all the cells to 100. 
# 
# 
# - ```pd.DataFrame``` creates a dataframe  [Description](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html#pandas.DataFrame)
# - ```[2020+v for v in range(2020,2026)]``` defines a python list comprehension which creates a list of the integers from 2020 to 2025 

# In[3]:


df = pd.DataFrame(                                 # call the dataframe constructure 
    100.000,                                           # the values 
    index=[v for v in range(2020,2026)],           #index
    columns=['A']                                  # the column name 
                 )
df   # the result of the last statement is displayed in the output cell 


# ### Use  mfcalc to calculate a new column (series) as a function of the existing A column series
# X is a new column. Before it is calculated it is initialized to 0.0 for all years.

# In[4]:


df.mfcalc('x = x(-1) + a')


# :::{note}
# In the above example a  dataframe with the result is created and displayed, but the df dataframe did not change.  To have it change we would have had to assign it the result of the initial operation, as below.
# :::

# In[5]:


df


# In[6]:


df2=df.mfcalc('x = x(-1) + a') # Assign the result to df2
df2


# ### Recalculate A so  it grows by 2 percent
# 
# mfcalcs knows that it can not start to calculate in 2020 as there is no lagged variable. So it will start calculating in 2021 and leave the pre-existing value unchanged.

# In[7]:


res = df.mfcalc('a =  1.02 *  a(-1)')
res


# In[8]:


res.pct_change()*100 # to display the percent changes


# <span style='color:Blue'> ORIGINAL </span>
# 
# ### mfcalc does simple normalizations
# 
# Another way to set the growth rate of a variable by setting the difference in its natural logarithm.
# 
# Here  dlog(a) refers to the differene in the natural logarithm and is equal to the growth rate for the variable.
# >dlog(x) translates to  ($log(x_t)-log(x_{t-1}))$
# 
# In the current example dlog(a) is not defined for 2020 (there is no lagged value for 2019) so the 2020 value is left unchanged.
# 
# For 2021 2025 mfcalc normalizes the equation such that the systems solves for a:<br>
# $dlog(a)  = 0.02$ <br>
# $log(a)-log(a_{t-1}) = .02$<br>
# $log(a)=log(a_{t-1})+.02$ <br>
# $a = e^{log(a_{t-1})+0.02}$ <br>
# $a =a_{t-1}*e^{0.02}$
# 

# In[9]:


res = df.mfcalc('dlog( a) =  0.02',showeq=1)
res.pct_change()*100


# ### Using .diff ($\Delta$) with mfcalc

# In[10]:


res = df.mfcalc('diff(a) =  2') # Set delta to 2 
res.diff()                      # Display the delta 


# ### mfcalc with several equations and arguments
# In addition to a single equation multiple commands can be executed with one command.

# In[11]:


res = df.mfcalc('''
diff(a) =  2
x = a + 42 
''')

res

# use res.diff() to see the difference


# :::{warning}
# Take care. As the max lag is 1 the expressions will not be calculated for 2020. So A keeps its 
# value of 100 in 2020 and X is initialized to 0 before calculating. And then keeps the value of 0 
# for 2020, as 2020 is not calculated.  
# :::

# :::{note}
# Below, as in the example above we have zeroes for x prior to 2023 when the expressions are executed.
# 
# <mark> Ib, Is this  because you returns zeroes by default for a declared variable? As the command was not exected for the earlier period, NaNs for nissing might be more logical.</mark>
# 
# <mark> From Ib, Is this  because you returns zeroes by default for a declared variable? Yes. It will require some efford as some functionalities depend on this, for instance when equations are enriched with with add factors and exogenizing. 
# :::

# ### Setting a time frame with mfcalc.
# It can useful in some circumstances to limit the time frame for which the calculations are performed. By specifying a start date and end date enclosed in <> in a  line we can restrict the time period over which calculation is performed.
# 
# Below, as in the example above we have zeroes for x prior to 2023 when the expressions are executed.

# In[12]:


res = df.mfcalc('''
<2023 2025>
diff(a) =  2
x = a + 42 
''')

res.diff()

res


# ## .mfcalc usage
# .mfcalc can be a useful extension to dataframe.upd() when creating scenarios. Or just for simple and fast calculations. 
# 
# 
