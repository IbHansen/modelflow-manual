#!/usr/bin/env python
# coding: utf-8

# # Onboard all models  defined in .wf1 files
# This notebook takes all .wf1 workfile from the folder wfs\ and transform the models  it to a modelflow model.<br>
# 
# The overall process is performed in a Dataclass named:**GrapWfModel**<br> 
# Close study of this class can be rewarding, but is outside the need of most users.<br>
# The overall structure is: Onboard all model defined in a .wf1 file
# 
# The overall structure is:
# 
# Eviews is started and the wf1 file is loaded
# Some transformations are performed on data.
# The model is unlinked
# The workspace is saved as a wf2 file. Same name with _modelflow appended
# Eviews is closed
# The wf2 file is read as a json file.
# Relevant objects are extracted.
# The MFMSA variable is extracted, to be saved in the dumpfile.
# The equations are transformed and normalized to modelflow format and classified into identities and stochastic
# Stochastic equations are enriched by add_factor and fixing terms (dummy + fixing value)
# For Stochastic equations new fitted variables are generated - without add add_factors and dummies.
# A model to generate fitted variables is created
# A model to generate add_factors is created.
# A model encompassing the original equations, the model for fitted variables and for add_factors is created.
# The data series and scalars are shoveled into a Pandas dataframe
# Some special series are generated as the expression can not be incorporated into modelflow model specifications
# The model for fitted values is simulated in the specified timespan
# The model for add_factors is simulated in the timespan set in MFMSA
# The data descriptions are extracted into a dictionary.
# Data descriptions for dummies, fixed values, fitted values and add_factors are derived.
# Now we have a model and a dataframe with all variables which are needed. b The GrapWfModel instance in general keeps most of the steps so the developer can inspect the the different steps.
# 
# The GrapWfModel instance in general keeps most of the steps so the developer can inspect the the different steps.  
# 

# - Eviews has to be installed 
# - pyevies has to be installed 
# 

# In[1]:


from pathlib import Path

from modelclass import model 
from modelgrabwf2 import GrabWfModel
model.widescreen()
model.scroll_off()
latex=1


# In[2]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# ## List potential files
# The workfiles are located in the ```wfs``` folder. <br>
# The [pathlib.Path](https://docs.python.org/3/library/pathlib.html) class is used to find all wf1 files

# In[3]:


filedict = {f.stem[:3].lower():f for f in Path('wfs').glob('*.wf1')}
for modelname,filename in filedict.items():
    print(f'The model and date for {modelname} is located in this workfile:{filename}')


# ## Model specific transformations 
# Not all Eviews equations has a direct counterpart in modelflow.<br>
# To handle that two types of transformations can be provided for a specific model. 
# - **eviews_run_lines** which specifies a list of Eviews command lines to be run. Typical to make some transformation of data. 
# - **country_trans** which specifies a list of replacements to be done to the Eviews formulas before they are processed. 
# 
# As a convention the variables like this \<modelname>_eviews_run_lines and <modelname>_trans

# In[4]:


pak_trans = lambda input : input.replace('- 01*D(','-1*D(')   

ago_trans = lambda  input : input.replace('@MEAN(AGOBNCABFUNDCD/AGONYGDPMKTPCD,"2000 2020")','MEAN_AGOBNCABFUNDCD_DIV_AGONYGDPMKTPCD') 
ago_eviews_run_lines = ['smpl @ALL','series MEAN_AGOBNCABFUNDCD_DIV_AGONYGDPMKTPCD = @MEAN(AGOBNCABFUNDCD/AGONYGDPMKTPCD,"2000 2020")']

mda_trans = lambda input: input.replace('_MDAsbbrev.@coef(2)','_MDASBBREV_at_COEF_2')         
mda_eviews_run_lines = ['Scalar _MDASBBREV_at_COEF_2 = _MDASBBREV.@COEF(+2)']


# ## Transform all wf1 files in the folder

# In[5]:


allmodels = {modelname: 
     GrabWfModel(filename, 
                        eviews_run_lines= globals().get(f'{modelname}_eviews_run_lines',[]),
                        country_trans    =   globals().get(f'{modelname}_trans'   ,lambda x : x[:]),
                        make_fitted = True,        # make equatios for fitted values of stocastic equations 
                        do_add_factor_calc=True,   # Calculate the add factors which makes the stocastic equations match    
                        fit_start = 2000,          # Start of calculation of fittet model in baseline (to have some historic values) 
                        fit_end   = None,           # end of calc for fittted model, if None taken from mdmfsa options  
                        disable_progress =True
                        ) 
                  for modelname,filename in filedict.items()}


# ## Check all the models 

# In[6]:


for modelname,cmodel in allmodels.items():
    cmodel.test_model(cmodel.start,cmodel.end,maxerr=100,tol=1,showall=0)   # tol determins the max acceptable absolute difference 


# ## Run the models 
# Some models need a different alfa (dampening factor in Gauss iterations) in order to solve. 

# In[7]:


alfadict={'ago':0.7}


# In[8]:


for modelname,cmodel in allmodels.items():
    _ = cmodel.mmodel(cmodel.base_input,alfa=alfadict.get(modelname,1.0))
    cmodel.mmodel.modeldump(f'modelflowdumps/{modelname}.pcim')  
    print(f'{modelname} run and saved')


# In[9]:


get_ipython().system('dir modelflowdumps\\')


# ## Make some names in the namespace

# In[10]:


for modelname,cmodel in allmodels.items():
    thismodel = f'm{modelname}'
    thisbaseline = f'{modelname}_baseline'
    thiscmodel = f'{modelname}_cmodel'
    globals()[thismodel] = cmodel.mmodel
    globals()[thisbaseline]= cmodel.base_input 
    globals()[thiscmodel]= cmodel
    print(f'{thismodel}, {thisbaseline} and {thiscmodel} has been created')    


# In[11]:


thissilent = 1
_ = mago(ago_baseline,silent=thissilent,alfa=0.7)
_ = mmda(mda_baseline,silent=thissilent)
_ = mpak(pak_baseline,silent=thissilent)
_ = mper(per_baseline,silent=thissilent)


# ## From here testing - will be deleted 

# ## Lets create a list of all variable names

# In[12]:


allvar = [varname for cmodel  in allmodels.values() for varname in cmodel.mmodel.allvar.keys()]


# In[13]:


allvar = [varname for thismodel in [mago,mmda,mpak,mper] for varname in thismodel.allvar.keys()]


# In[14]:


allvar_dict  = {varname:cmodel.mmodel.var_description[varname] for cmodel  in allmodels.values() for varname in cmodel.mmodel.allvar.keys()}


# In[15]:


len(allvar)


# In[16]:


import fnmatch


# In[17]:


fnmatch.filter(allvar, '*NECONGOVTCN')


# In[18]:


len(set(allvar))


# In[19]:


def getnames(pat,allvar=allvar,allvar_dict=allvar_dict):
    selected = [(varname,allvar_dict[varname]) for varname in fnmatch.filter(allvar_dict.keys(), pat)]
    print(*selected,sep='\n')


# ### Government consumption

# In[20]:


getnames('*NECONGOVTCN')


# ### Government investment 

# In[21]:


getnames('*NEGDIFGOVCN')


# In[22]:


getnames('*LMEMPTOTLCN*')


# In[23]:


getnames('*GGEXPWAGECN*')


# In[24]:


mpak.PAKBXFSTREMTCD.frml


# In[25]:


mpak.PAKGGEXPGNFSCN.frml


# In[26]:


###  mpak.modeldash('PAKNECONGOVTCN',jupyter=1)


# In[27]:


allmodels['pak'].all_frml_dict['PAKGGEXPGNFSCN']


# In[28]:


allmodels['ago'].all_frml_dict['AGONECONGOVTCN']


# In[29]:


allmodels['pak'].mmodel

