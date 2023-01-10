#!/usr/bin/env python
# coding: utf-8

# (upd)=
# # Update, modifying series in a dataframe using modelflow
# Often when we are working with a model we will want to modify individual data points or series in a model (for example when doing a simulation, or if there is a data update to one or more series. 
# This can be done straight using pandas methods.

# However the **dataframe.upd** function in Modelflow simplifies this exercise.
# It gives the user a concise and expressive way to specify 
# typical updates of economic variables. 

# A line like: 
# >newdf = df.upd('the_answer = 42') 
# 
# will create a new dataframe based on the dataframe df where the variable ```THE_ANSWER``` has the value 42. 

# :::{danger}
# The df dataframe remains unchanged. The newdf contains the new updated values (and all non-updated variables from df.
# :::

# To make df.update useful you can also: 
#  - Perform different types of  updates
#  - Perform multiple updates each on a new line 
#  - Control the time for which the update has effect
#  - Use one input which is used for all time frames, or a input for each time 
#  - Keep the growth rate after the update time frame
#  - Display the results 

# **Types of update:** 
# 
# | Update to perform |Use this operator|
# | :- | :---|
#  Set a variable equal to the input| = 
#  Add the input to the input | + 
#  Set the variable to itself multiplied by the input | *
#  Set the variable to itself multiplied by (1+input/100) | %
#  Set the growth rate of the variable to the input | =growth
#  Set the growth rate of the variable to the current growth rate plus the input| +growth 
#  Set $\Delta = var_t - var_{t-1}$ of  the variable to the input| =diff

# ***Setting the time scope***
# 
# The update command takes a variety of mathematical operators ```=, +, \*, % =GROWTH, +GROWTH, =DIFF``` and applies them to data for the period set in the leading <>.
# 
#  - If **one date** is specified the operation is applied to a single point in time
#  - If **two dates**  are specifies the operation is applied over a period of time.
# 
# The time will persist until set next time. Useful to avoid visual noise if several variables are going to be updated for the same time period. 
# 
#  - To indicate the start of the dataframe use -0
#  - To indicate the end of the dataframe use -1
#  
# If no time is provided the dataframe start and end period will be used.  

# **Keep growth rates after the update time**
# 
# In a long projection it can sometime be useful to be able to update variables for which new information is available, but keep the growth rate the same as before the update  after the update time. 
# 
# For each *update line* it is governed 
# by the ```--keep_growth``` and ```--no_keep_growth``` option. 
# 
# For the *.update call* (which can contain many update lines) this is ruled by the ```keep_growth``` parameter. 
# The default value for ```keep_growth``` is ```False```. If ```keep_growth=True``` all lines will use the ```keep_growth```
# except lines with the --no_keep_growth option
# 
# Examples later.

# **Comments**
# 
# Everyting after a # until line end is regarded as a comment 

# ## Setting up the workspace

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import pandas as pd

from modelclass import model 
model.widescreen()
model.scroll_off()


# ## Create dataframe to update: 
# Now a pandas dataframe with one column and 6 rows are created. The column is has the name ```A``` and the rows have index 2020 to 2025.

# In[3]:


number_of_rows = 6 
df = pd.DataFrame(100,
       index=[2020+v for v in range(number_of_rows)], # create row index
       columns=['A'])                                 # create column name 
df


# 
# - ```pd.DataFrame``` creates a dataframe  [Description](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html#pandas.DataFrame)
# - ```[2020+v for v in range(number_of_rows)]``` defines a list comprehension which creates a list of the integers from 2020 to 2025 (see below for list comprehensions) 

# ## Use dataframe.loc to make a new variable
# ```.loc``` is used to access or set values in a dataframe based on row and column labels.

#  - [Description](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html)
#  - [Search](https://www.google.com/search?q=pandas+dataframe+loc&newwindow=1)

#  
#  A new series (a column) called B is set to 100
#  

# In[4]:


df.loc[:,'B' ] = 100.
df


# ## Use dataframe.upd()  to  modify a series in a dataframe or to add a series to a dataframe
# 
# Upd makes it much easier to create new series (compare the below, with the complicated pandas code above).

# ### = Setting value equal to input

# ####  Creates a new data series called c in the dataframe with values of 142 everywhere

# In[5]:


df2=df.upd('c = 142') 
df2


# #### Setting specific datapoints to specific values 
# In this example, upd uses the equals operator.  This indicates that the variable a should be set equal to the indicated values following the = operator (42 44 45 46 in this example). The dates enclosed in <> indicate the period over which the change should be applied.  
# 
# Either: 
#  - The number of data points provided must match the number of dates in the period, Or
#  - Only one data point is provided, it is applied to all dates in the period. 
# 
# If only one period is to be modified then it can be followed by just one date.

# In[6]:


df.upd("""
# Same number of values as years
<2021 2024> A = 42 44 45 46    # 4 years
<2020     > B = 200            # 1 year 
c = 500
""")


# ### Adding  the specified  values to all values in a range (the + operator)
# 
# NB: Here upd with the  + operator indicates that we are adding 42. 

# In[7]:


df.upd('''
# Or one number to all years in between start and end 
<2022 2024> B  +  42    # one value broadcast to 3 years 
''')


# ### Multiplying all values in a range by the specified values (the * operator)

# In[8]:


df.upd('''
# Same number of values as years
<2021 2023> A *  42 44 55
''')


# ### Increasing all  values in a range by a  specified percent amount (the % operator)
# In this example:
#  - A is increased by 42 and 44% over the range 2021 through 2022.
#  - B is increased by 10 percent in all years
#  - C, a new variable, is created and set to 100 for the whole range
#  - C is decreased by 12 percent over the range 2023 through 2025.

# In[9]:


df.upd('''
<2021 2022 > A %  42 44   
<-0 -1> B % 10            # all rows 
C = 100                   # all rows persist 
<2023 2025> C % -12       # now only fo 3 years 
''')


# ###  Set the percent growth rate to specified values (=GROWTH)

# In[10]:


res = df.upd('''
# Same number of values as years
<2021 2022> A =GROWTH  1 5  
<2020> c = 100 
<2021 2025> c =GROWTH 2 
''')
print(f'Dataframe:\n{res}\n\nGrowth:\n{res.pct_change()*100}\n') # Explained b


# :::{note}
# **Python constructs**<br>
# > print(f'Dataframe:\n{res}\n\nGrowth:\n{res.pct_change()*100}\n')
# 
# Uses
# 
# | Python construct |Explanation|Links
# | :- | :---| :---|
# |'\n'|A line break 
# |dataframe.pct_change|Percentage change between the current and a prior element.|[Description](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html) 
# |f'{varname} = ....'|A f-string, {expression} is replaced by the value of expression|[Search](https://www.google.com/search?q=python+f-string&newwindow=1)
# :::

# ### Add or subtract from the existing percent growth rate (+GROWTH operator) 

# In[11]:


res =df.upd('''
# Same number of values as years
<2021 2025> A =GROWTH  1  
# now we add values  to the growth rate, 
a +growth   2 3 4 5 6 
''')
print(f'Dataframe:\n{res}\n\nGrowth:\n{res.pct_change()*100}\n')


# ###  Set $\Delta = var_t - var_{t-1}$ to specified values (=diff operator) 

# In[12]:


df.upd('''
# Same number of values as years
< 2021 2022> A =diff  2 4   
# cv number to all years in between start and end 

<2020 > same = 100 
<2021 2025> same =diff  2  
''')


# ### Recall  that we have not overwritten df, so the df dataframe is unchanged.

# In[13]:


df


# ## .upd(,,,keep_growth)/--keep_growth, keep the growth rate in the years after the update
# 
# Before a series is updated the growth rate of the series is calculated. After a series has been updated, it is possible to use the saved growth rate to do an automatic update of the series from the end of the "proper" update period until the end of the dataframe. 
# 
# This allows to update variables for which new information is available, but keep the growth rate the same as before the update in the period after the update time.

# ###  First make a dataframe with some growth rate 

# In[14]:


res = df.upd('<2021 2025> a =growth 1 2 3 4 5')  
print(f'Dataframe:\n{res}\n\nGrowth:\n{res.pct_change()*100}\n')


# ### now update A in 2021 to 2023 to a new value, 
# and watch how values after 2023 are updated, so the gowth rate after the update is unchanged 

# In[15]:


res = df.upd('''
<2021 2025>  a =growth 1 2 3 4 5 
<2021 2023>  a = 120  --kg
''',lprint=0)
print(f'Dataframe:\n{res}\n\nGrowth:\n{res.pct_change()*100}\n')


# ### A more advanced example
# Where more advanced python is used 

# #### First create a string with update lines

# In[16]:


lines = '\n'.join(                               
 [f'''<2020     > {varname} = 100 
      <2021 2025> {varname} =growth 1 2 3 4 5'''
     for varname in 'c d e f'.split()])
print(lines) 


# :::{note}
# ***Python constructs***
# 
# The creation of update lines involves a number of useful python constructs. A short 
# description:<br>
# 
# | Python construct |explanation|Google |
# | :- | :---| :---|
# |'a b'.split()|splits a string by ```blanks```into a list| [Search](https://www.google.com/search?q=python+split&newwindow=1)
# |'\n'.join()|Creates a string from a list of string separated by \n (linebreak)|[Search](https://www.google.com/search?q=python+string+join&newwindow=1)
# |f'{varname} = ....'|A f-string, {varname} is replaced by the value of varname|[Search](https://www.google.com/search?q=python+f-string&newwindow=1)
# |\[varname for varname in a_list] |List comprehension which creates an implicit loop|[Search](https://www.google.com/search?q=python+list+comprehension&newwindow=1)
# :::

# #### Use the update lines to update a dataframe

# In[17]:


dfnew = df.upd(lines)
dfnew


# #### Update the new dataframe and keep some of the growth rates
# ```keep_growth=True``` now all lines as default keep the growth rate
#  - c,d are updated in 2022 and 2023 and keep the growth rates afterwards
#  - e the --no_keep_growth in this line prevents the updating 2024-2025

# In[18]:


dfres = dfnew.upd('''
<2022 2023> c = 200 
<2022 2023> d = 300  
<2022 2023> e = 400  --no_keep_growth
''',keep_growth=True)
print(f'Dataframe:\n{dfres}\n\nGrowth:\n{dfres.pct_change()*100}\n')


# ### --kg can replace --keep_growth and --nkg can replace --non_keep_growth 
# Just to make typing more easy 
# 

# ## Update several variable in one line 
# Sometime there is a need to update several variable with the same value over the same time frame. To ease this case .update can accept several variables in one line

# In[19]:


df.upd('''
<2022 2024> h i j k =      40 
<2020>      p q r s =       1000
<2021 -1>   p q r s =growth 2     # -1 indicates the last year 
''')


# ## .upd(,,scale=\<number, default=1>) Scale the updates 
# When creating scenarios consistent of several updates it can be useful to be able to create 
# a number of scenarios based on one update but with different scale. For instance scale=0 is the baseline while scale=0.5 is a scenario half 
# the severity.  
# 
# In the example below the values of the dataframes are printed.<br>
# In a more realistic example  the ```print()``` below  would be changed to a call to a model instance, so the model would be simulated.  

# In[20]:


print(f'input dataframe: \n{df}\n\n')
for severity in [0,0.5,1]: 
    # First make a dataframe with some growth rate 
    res = df.upd('''
    <2021 2025>
    a =growth 1 2 3 4 5 
    b + 10
    ''',scale=severity)
    print(f'{severity=}\nDataframe:\n{res}\n\nGrowth:\n{res.pct_change()*100}\n\n')
    #  
    # Here the updated dataframe is only printet. 
    # A more realistic use case is to simulate a model like this: 
    # dummy_ = mpak(res,keep='Severity {serverity}')    # more realistic 


# ## .upd(,,lprint=True ) prints vaues the before and after update  
# When creating scenarios consistent of several updates it can be useful to be able to create 
# a number of scenarios based on one update but with different scale. For instance scale=0 is the baseline wile scale=0.5 is a scenario half 
# the severity.  

# In[21]:


df.upd('''
# Same number of values as years
<2021 2022> A *  42 44
''',lprint=1)


# ## .upd(,,create=True ) Requires the variable to exist  
# Until now .upd has created variables if they did not exist in the input dataframe.
# 
# To catch misspellings the parameter ```create``` can be set to False. 
# New variables will not be created, and an exception will be raised. 
# 
# Here Pythons exception handling is uses, so the notebook will continue to run the cells below. 

# In[22]:


try:
    xx = df.upd('''
    # Same number of values as years
    <2021 2022> Aa *  42 44
    ''',create=False)
    print(xx)
except Exception as inst:
    xx = None
    print(inst) 


# ## The call 

# def update(indf, updates, lprint=False,scale = 1.0,create=True,keep_growth=False,start='',end='')
# 
#     Args:
#             indf (DataFrame): input dataframe.
#             basis (string): lines with variable updates look below.
#             lprint (bool, optional): if True each update is printed  Defaults to False.
#             scale (float, optional): A multiplier used on all update input . Defaults to 1.0.
#             create (bool, optional): Creates a variables if not in the dataframe . Defaults to True.
#             keep_growth(bool, optional): Keep the growth rate after the update time frame. Defaults to False.
# 
#         Returns:
#             df (TYPE): the updated dataframe .
#             
#         A line in updates looks like this:     
#                
#         "<"[[start] end]">" <var....> <=|+|*|%|=growth|+growth|=diff> <value>...  [--keep_growth_rate|--no_keep_growth_rate]
# 
#         
#         
# 

# In[ ]:




