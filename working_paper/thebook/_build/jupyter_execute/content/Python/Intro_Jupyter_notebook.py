#!/usr/bin/env python
# coding: utf-8

# # Introduction to the Jupyter Notebook
# 

# ## Multiple ways to interact with Python
# * From the command line (simply type 'python' or 'ipython')
# * Plain text editor (e.g. Notepad++)
# * IDE (like  'Spyder' which is part of the Anaconda distribution but there are many)
# * Jupyter notebooks
# * And many more
# 
# **This manual is based on Jupyter**

# [The official Jupyter site](https://docs.jupyter.org/en/latest/) is a good starting point. But there are many good sites out there. 

# ## The idea of the notebook
# * Keep code and output close together (in "cells")
# * Great for documenting the analytical steps
# * ... and teaching 
# > The notebook format supports the idea of _replicability_: a scientific analysis should contain - in addition to the final output (text, graphs, tables) - all the computational steps needed to get from raw input data to the results.
# * A possible workflow:
# prototype code in the notebook and consolidate it into scripts later on

# ## Jupyter Notebook basics
# * Jupyter derives from **Ju**lia + **Pyt**hon + **R**
# * A separate Python process (a __'kernel'__) is started for each notebook 
#     * Can be seen as a open window in the background (do not close)
#     * Can be interrupted and restarted from the 'Kernel' menu
# * Multiple __cell types__, e.g. 'Code' and 'Markdown'
#     * Code is for executable Python code
#     * Markdown is for (formatted) text, e.g. descriptions of results
# * Cells can be in __two modes__
#     * Green vertical bar: 'Edit' mode
#     * Blue vertical bar: 'Select/copy' mode

# ### How to execute cells and display results
# Useful shortcuts: (see also "Help" => "Keyboard Shortcuts" or simply press keyboard icon in the toolbar)
# * **shift + ctrl**: run cell and stay in cell
# * **shift + enter**: run cell and jump to next cell
# 
# * Note that Notebook always prints last statement of a cell to screen. Except if the line ends in ';'
# * Can force print of other statement with "print" command for other lines

# In[1]:


x = 10
y = 45
y


# In[2]:


x = 10
print(x)
y = 20
y


# #### But no display when line ends in ;

# In[3]:


y = 20
y; 


# ### How to add, delete and move cells
# Toolbar
# * **+ button**: add a cell below
# * **scissors**: delete cell (can be undone from "Edit" tab)
# * **up- and down arrows**: move cells
# * **hold shift + click cells in left margin**: select multiple cells (vertical bar must be blue)

# ### Auto-complete and context-sensitive help
# * **tab**: autocomplete and  method selection
# * **double tab**: documention (double tab for full doc)

# ### LaTeX support
# Markdown mode includes LaTeX support.<br>
# Inline enclose the latex in ```$```:
# 
# An Equation: ```$y_t = \beta_0 + \beta_1 x_t + u_t\$``` will show like this:
# 
# An Equation: $y_t = \beta_0 + \beta_1 x_t + u_t$
# 
# Math blocks can be enclosed in ```$$```

# ## A few words on 'import' statements

# In[4]:


# Import and call a built-in module
import math
math.pi


# In[5]:


# Importing only part of a module's functionality
from math import pi, e, cos
pi


# In[6]:


# Use of aliases for modules
import math as M
M.pi


# In[7]:


# Conventions for some aliases
import numpy as np
import pandas as pd


# In[8]:


# Import the model class from modelflow
from modelclass import model 

