#!/usr/bin/env python
# coding: utf-8

# (onboardone)=
# # Onboard a model defined in a .wf1 file
# This notebook takes a .wf1 workfile and transform  it to a modelflow model.<br>
# 
# The overall process is performed in a Dataclass named:**GrapWfModel**<br> 
# Close study of this class can be rewarding, but is outside the need of most users.<br>
# The overall structure is: 
#  1. Eviews is started and the wf1 file is loaded
#     -    Some transformations are performed on data.
#     -    The model is unlinked 
#     -    The workspace is saved as a wf2 file. Same name with ```_modelflow appended```
#  5. Eviews is closed 
#  6. The wf2 file is read as a json file. 
#  7. Relevant objects are extracted. 
#  7. The MFMSA variable is  extracted, to be saved in the dumpfile. 
#  8. The equations are transformed and normalized to modelflow format and classified into identities and stochastic
#  9. Stochastic equations are enriched by add_factor and fixing terms (dummy + fixing value)  
#  9. For Stochastic equations new fitted variables are generated - without add add_factors and dummies.  
#  9. A model to generate fitted variables is created  
#  9. A model to generate add_factors is created. 
#  9. A model encompassing the original equations, the model for fitted variables and for add_factors is created. 
#  9. The data series and scalars are shoveled into a Pandas dataframe 
#      - Some special series are generated as the expression can not be incorporated into modelflow model specifications
#      - The model for fitted values is simulated in the specified timespan
#      - The model for add_factors is simulated in the timespan set in MFMSA
#  10. The data descriptions are extracted into a dictionary. 
#     - Data descriptions for dummies, fixed values, fitted values and add_factors are derived. 
#  11. Now we have a model and a dataframe with all variables which are needed.
#  b
# The GrapWfModel instance in general keeps most of the steps so the developer can inspect the the different steps.  
# 

# ## Prerequisites  
# 
# - Eviews version 12 
# - The python library: ```pyevies```  
# 

# In[1]:


get_ipython().run_line_magic('matplotlib', 'Notebook')


# In[2]:


from pathlib import Path

from modelclass import model 
from modelgrabwf2 import GrabWfModel
model.widescreen()
model.scroll_off()


# In[3]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# ## Model specific transformations 
# Not all Eviews equations have a direct counterpart in modelflow.<br>
# To handle that two types of transformations can be provided for a specific model. 
# - **eviews_run_lines** which specifies a list of Eviews command lines to be run. Typical to make some transformation of data which is not possible in modelflow. 
# - **country_trans** which specifies a list of replacements to be done to the Eviews formulas before they are processed further. Typical to use the transformation mentioned above.  

# In[4]:


mda_eviews_run_lines = ['Scalar _MDASBBREV_at_COEF_2 = _MDASBBREV.@COEF(+2)']
mda_trans = lambda input: input.replace('_MDAsbbrev.@coef(2)','_MDASBBREV_at_COEF_2')   


# Another example 
ago_eviews_run_lines = ['smpl @ALL','series MEAN_AGOBNCABFUNDCD_DIV_AGONYGDPMKTPCD = @MEAN(AGOBNCABFUNDCD/AGONYGDPMKTPCD,"2000 2020")']
ago_trans = lambda  input : input.replace('@MEAN(AGOBNCABFUNDCD/AGONYGDPMKTPCD,"2000 2020")','MEAN_AGOBNCABFUNDCD_DIV_AGONYGDPMKTPCD') 


# ## Process the model

# In[5]:


all_about_mda = GrabWfModel(r'wfs\mdasoln.wf1', 
                  eviews_run_lines= mda_eviews_run_lines,
                  country_trans    =  mda_trans,
                    make_fitted = True,        # make equatios for fitted values of stocastic equations 
                    do_add_factor_calc=True,   # Calculate the add factors which makes the stocastic equations match    
                    fit_start = 2000,          # Start of calculation of fittet model in baseline (to have some historic values) 
                    fit_end   = None,           # end of calc for fittted model, if None taken from mdmfsa options  
                    disable_progress =True     # Better for jupyter book 
                           ) 


# In[ ]:





# ## Check if each equation on its own result in the values provided. 
# aka: residual check <br> 
# If they are not pretty close, something is very wrong. 

# In[6]:


all_about_mda.test_model(all_about_mda.start,all_about_mda.end,maxerr=100,tol=1,showall=0)   # tol determins the max acceptable absolute difference 


# ## Extract the model and the baseline
# **all_about_mda** has a lot of content including. 
# - .mmodel is the model instance
# - .base_input is the baseline where the add factors and the fitted values are calculated 

# In[7]:


mmda    = all_about_mda.mmodel       # the model instance  
baseline = all_about_mda.base_input


# ## Run the model 
# In order to achieve numerical stability Gauss-Seidle has to be dampened: alfa=0.7 makes sure that the solution does not explode. 
# The convergence criteria is tightend a lot. 

# In[8]:


res = mmda(all_about_mda.base_input,2016,2040,silent=1,alfa=1,ldumpvar=0)
mmda.basedf = all_about_mda.base_input


# ## And the simulation result is also fine. 
# Here the percent difference is displayed

# In[9]:


mmda['mdaGGEXPCAPTCN mdaNYGDPMKTPCN mdaGGDBTTOTLCN mdaBNCABFUNDCD']


# ## Look at a stochastic variable 
# Here the equations undergo more phases 

# In[10]:


all_about_mda.all_frml_dict['MDABFCAFCAPTCD'].fprint


# ## Look a all the modelflow frmls
# Notice after the "original" model the equations for the "fitted" values have been added. <br>
# Also in the end of the listing the specification of the model which calculates the add factors if a variable is fixed. When processing the equations the ```model``` class will process this this model separately and create a model instance 
# which is used to calculate add factors in case 

# In[11]:


print(mmda.equations)


# In[12]:


with mmda.set_smpl(2020,2023):
    print(mmda.mdaGGEXPCAPTCN.show)                        


# In[13]:


mmda.modeldump('test.pcim')


# In[14]:


get_ipython().system('dir *.pcim')


# In[ ]:




