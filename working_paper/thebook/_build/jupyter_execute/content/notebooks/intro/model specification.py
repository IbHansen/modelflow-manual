#!/usr/bin/env python
# coding: utf-8

# # Specification of models (introduction) 
# 
# Modelflow was started in order to build transparent and agile models and in order to be able to recycle and connect a broad range of models from different sources. 
# 
# For these reasons it should be possible to onboard models from different sources and it should be possible to specify a model in a parsimonious and expressive way. This allows focus  on the economic content without entanglement from implementation and housekeeping details. 
# 
# For this purpose specification of a model typical **flows**  through several phases (hence the flow in modelflow). 
# 
# Which *initial phases* the model specification flows through depend on the nature and origin of the model at hand. Python has a rich set of string manipulation functions which allows different processing in these phases. Some more advanced examples for instance [onboarding a Eviews model](../../howto/onboard/eviews/onboard%20one%20model%20from%20%20wf1.ipynb) is given in the onboarding section of this manual.  
# 
# The *last phase* is always the model specification in **The Basic Business logic language**. From this specification the model is  transpiled by a python function like this [python solution code for Solow model](solow-python-code)
# which is needed for both the Gauss and the Newton type solution methods [python solution code](solution-methods). 

# :::{figure-md} markdown-fig
# <img src="onboarding.png" alt="fishy" class="bg-primary mb-1" width="700px">
# 
# Flow from model specification to python solver
# :::

# The Basic Business Logic Language which is used for specification of models in ModelFlow can trace its origins to the [TSP program](https://en.wikipedia.org/wiki/TSP_(econometrics_software)) which was installed in the UNIVAC mainframe in RECKU - the computer center of University of Copenhagen in the 70's (and a lot of other mainframes used for model worK). It looks to some extend like model specification in packages used for simulation of macroeconomic models like  [Eviews], Gekko, PCIM, Dynare, Aremos or TROLL.

# ## Specify equations in Basic business logic language. 
# Each equation $f_i$ in a model is specified as:
# 
# 
# ```
# FRML <options> <left hand side> = <right hand side> $
# ```
# 
# Each formula ends with a \$.
# 
# The ```<left hand side>``` should not contain transformations. Lags or leads can not be specified at the left hand side of $=$. 
# 
# 
# Time $t$ is implicit in the equations which means that a $var$ at time $t$ written as ```var```, while $var_{t-1}$ is written as ```var(-1)```. ModelFlow is case-insensitive. Everything is eventually transformed into upper case.
# 
# The ```<right hand side>``` can contain variables, operators, functions and variables. ModelFlow comes with a number of built-in functions. In addition python functions can be supplied when a model is created.
# 
# A variable is a timeseries which for contains a numbers or Python objects. This paper is mostly concerned with variables containing numbers (scalars). 
# 
# Operators:
# 
# Standard: ```= + - * / ** ( ) @ ```
# 
# Comparison: ```>= <= == !=```  \# evaluates to 0 if false, 1 if true
# 
# Special: ```$ > < , . [  ] ``` \# used in different python constructions.
# 
# In addition a number of pre-defined functions can be used and should be avoided as variable names. 

# In[1]:


# This inputcell is hidden
import modelpattern
print(' '.join(modelpattern.funkname))


# If formulas (equations) can be separated by linebreak, frml and \$ don't need to be specified. 
# 
# Equation options  which are enclosed in ´´´<>``` are used to control differed aspects both of the text processing of equations and of the solving. Use of equation options will be provided later. 
# 
# ## Specify equations in (Macro) Business logic language. 
# 
# Models should be specified in a domain specific language which matches the problem at hand and which lend itself to short and expressive specification. The focus should be on the business logic and not on the housekeeping which is necessary for the solving algorithms.  
# 
# Stress test models should for instance be able to handle many bank and sectors without repeating text. Also the language should be able to handle common model constructs like: DLOG(var) = $(log(var_t)-log(var_{t-1}))$ or DIF(var) = $(var_t-var_{t-1})$ on both sides of =, inclusion of factors, possibility of fixing endogenous variables and more. 
# 
# So on top of the **Business logic language**. there is a **Macro Business Logic language**. The primary goal of this is to allow (conditional) looping and normalization of formulas. More no this later on.
# 
# ### Advanced, Tupels and matrices.
# 
# The left hand side can be a Python [tuple](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences) that matches the ```<right hand side>```. 
# 
# Also Pandas Dataframes can also contain python objects. This means that a variable can also be a matrix. This makes it possible to create a broader range of models - input output, bank contagion and optimizing models - in Modelflow. However there are also limitations to solving methods and output has to be taken special care of. In this manual it is therefor assumed that a variable is a timeserie of numbers. 

# In[ ]:




