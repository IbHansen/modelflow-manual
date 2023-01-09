#!/usr/bin/env python
# coding: utf-8

# # Normalizing when onboarding  eviews models 
# When onboarding a model from Eviews the model flows through several phases. 
# In this notebook the normalization of equations is explored. 
# 
# In the normal function the equation is normalized. That is only one variable on the left hand side of the =. In addition the 
# the equation can be enriched by an add factor and a fixing construct. 
# 
# Also equations can be generated to calculate the add factor and a _fitted variable - meaning the value without fixing or add factor) 
# 
# First an equation is **preprocessed**. That is: diff ,dlog, pct_growth, movavg and the like is expanded.<br> 
# Then the equation is normalized. That is a variable (the endogenous variable) is isolated on the left hand side of the =. 
# 
# 

# In[1]:


from modelnormalize import normal


# In[2]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[3]:


normal('a/(b/c) = 3 ',make_fitted=1,add_add_factor=True)


# In[4]:


normal('dlog(a) = 3 ',make_fitted=1,add_add_factor=True)


# In[5]:


normal('a - b = 3 ',make_fitted=1,add_add_factor=True)


# In[6]:


normal('dlog(y)  = 3 * dlog(x+b) ',make_fitted=1)


# In[7]:


normal('x  = 3 ',add_add_factor=1)


# In[8]:


normal('pct_growth(x)  = pct_growth(y) ',make_fixable=0,add_add_factor=1)

