# The World Bank's MFMod Framework in Python with Modelflow - Using modelflow with World Bank models


# Using modelflow with World Bank models

# Using ```ModelFlow``` with World Bank models

The ```ModelFlow``` python package has been developed to solve a wide range of models, see the ModelFlow github [https://github.com/IbHansen/ModelFlow](https://github.com/IbHansen/ModelFlow) web site for working examples of the Solow Model, the United States' Federal REserve FRB/US model and others.

The package has been substantially expanded to include special features that enable it to work with World Bank models originally developed in EViews using the EViews Model Object for simulation. Although derived from these EViews models, the models available on the World Bank web site and through the mechanisms outlined below are **pure python** models and use `ModelFlow` and various python libraries for solution visualization and data management.

This section illustrates how to access these models (this Chapter). Subsequebnt chapters explain how: to load these ```ModelFlow``` models into the Anaconda environment on your computer andhow to explore various features of these models (Chapter 9); WB behavioural equations are designed and manipulated in `ModelFlow` (Chapter 10); how to perform a variety of simulations (Chapters 10,11 and 12) and how to extract results and compare results from your simulations (Chapter 13).

:class: tip

This chapter demonstrates how to access World Bank models that have been made publicly available using the `ModelFlow` python system.

- **Available Models**:
  - Access a range of pre-built World Bank models tailored for macroeconomic analysis.
  - Publicly available models can be loaded and customized in ModelFlow.

```python
#This is code to manage dependencies if the notebook is executed in the Google Colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

```python
# Prepare the notebook for use of ModelFlow 

# Jupyter magic command to improve the display of charts in the Notebook
%matplotlib inline

# Import Pandas 
import pandas as pd

# Import the model class from the modelclass module 
from modelclass import model 

# functions that improve rendering of ModelFlow outputs
model.widescreen()
model.scroll_off();
```

## Publicly available World Bank models for use with ModelFlow

Several World Bank macrostructural models are currently available for download and use with ModelFlow (more will be added over time). The available models include:

- Bolivia (Annual model)
- Croatia (Quarterly model)
- Iraq (Annual model)
- Nepal (Annual model with Climate features)
- Pakistan (Annual model with climate features)
- Turkiye (Annual model with climate features)

Each of these models has been developed as part of the outreach work of the World Bank.  The basic modeling framework of each of these models is outlined in {cite:t}`burns_world_2019` with  individual models having specific extensions reflecting features of the individual country and the questions for which the model was designed to respond.  The approach for the  models with climate features is laid out in {cite:t}`burns_climate_2021`, although several additional features are included in some of these models that have not yet been documented.

As additional models are released they will be made available using the mechanism described below.

## How to access the models the `.Worldbank_Models()` method

The World Bank models can be downloaded on to a user's computer using the `model.Worldbank_Models()` method, which downloads the models from the World Bank's GitHub repository at [https://github.com/worldbank/MFMod-ModelFlow](https://github.com/worldbank/MFMod-ModelFlow).

By default, the models are downloaded to a directory on the user's computer entitled `WorldbankModels` that is located just below the directory from which it is executed. The content of the downloaded folders will be displayed in a table of content, and the user can access the notebooks by clicking on them. 

```python
model.Worldbank_Models()
```

**Avaiable notebooks**

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

### WorldbankModels() Options

The `model.Worldbank_Models()` method includes several options, which affect the way the download of the models is executed.


#### The `destination`option

To change the directory to which the files are downloaded the `destination` parameter can be set (by default it points to `./WorldBankModels`).

`model.Worldbank_Models('./mydirectory')` (or equivalently `model.Worldbank_Models(destination='./mydirectory')`) would instead download the GitHub repository to a directory called mydirectory below the location from which the command was executed.  Note: For security reasons, the `destination` option will not accept a location that is above the directory from which it is executed.

#### The `silent` option

By default the `silent` option is set to True.  Setting it to False generates a more verbose indication of the directories and files downloaded and erased (of any).

#### Options controlling the treatment of existing files in the download directory

|option|default|Level of aggression|Action|
|:--|:--|:--|:--|
|replace|False|$\color{orange}{Medium}$| replace=True will replace any file in the local store that also exists on the World Bank github site with the version on the World Bank site. |
|replace|False|$\color{green}{Lowest}$| replace=False will not change or delete any files on the user's store.  Only files that exist on the World Bank web site (and not on the local copy) will be downloaded. |

To replace the all of the content first delete the destination directory (by default `./WorldBankModels`). <to do this use the operation system. 


#### Options to change the repository that is downloaded

It is possible to choose a repository other than the World Bank site to be downloaded, although the use case for this option is limited. A user that wishes to do this can specify the repository to be downloaded by setting the following options
|option|Default value|Explanation|
|:--|:--|:--|
|owner|WorldBank|Name of the owner of the github repository to be downloaded|
|repo_name|MFMod-ModelFlow| The name of the repository|
|branch|main| The branch to downloaded.|

## `.display_toc()` method

The `.display_toc()` method can be used to displays a list of the directories and files included in the subfolder to which the World Bank models were previously downloaded.

```python
model.display_toc(folder='WorldbankModels');
```

**Jupyter notebooks**

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

Help on the accessing World Bank models can be generated by using the `help()` function.

```python

help(model.Worldbank_Models)
```

```text
Help on function Worldbank_Models in module modelclass:

Worldbank_Models(owner: str = 'worldbank', repo_name: str = 'MFMod-ModelFlow', branch: str = 'main', destination='./WorldbankModels', go=True, silent=True, replace=False)
    Download an entire GitHub repository and extract it to a specified location.

    Parameters:
      owner: The owner of the GitHub repository.
      repo_name: The name of the repository.
      branch: The branch to download.
      destination: The local path where the repository should be extracted.
      go: display toc of notebooks
      silent: keep silent

    Returns:
      A message indicating whether the download was successful or not.
```

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

# Working with a World Bank Model under ModelFlow


The basic method for working with any model is the same. Indeed the initial steps followed here are the same as were followed during the preceding discussions of `ModelFlow` features.

Process:
1. Prepare the workspace
1. Load the model ModelFlow
2. Design some scenarios  
3. Simulate the model
4. Visualize the results 

## Prepare the work space

To use `ModelFlow` it must be installed as per the instructions in Chapter 3 (a one-time operation). The  the python environment into which `ModelFlow` was installed must be activated.  For users that installed `ModelFlow` according to the earlier instructions this can be achieved by executing `conda activate ModelFlow` in line with earlier instructions.

Once the python environment is activated, the `ModelFlow` and `pandas` packages must be imported into your workspace. Once this is done (accomplished by the code below), the user is ready to work with `ModelFlow`. 

:class: tip

This chapter provides practical guidance on using World Bank models within the ModelFlow framework. 

Key points include:

- **Setup and Preparation**:
  - Prepare the workspace by setting up the Python environment.
  - Load the model, associated data, and variable descriptions.

- **Model Exploration**:
  - Extract information about the model, including:
      - its equations
      - its variables
      - its structure
      - its data
  - Organize variables into groups for streamlined exploration and analysis.

- **Key Methods**:
  - Use ModelFlow’s built-in functions to query, modify, and analyze data.
  - Explore relationships between variables and their role in the model.

```python
# Prepare the notebook for use of ModelFlow 

# Jupyter magic command to improve the display of charts in the Notebook
%matplotlib inline

# Import pandas 
import pandas as pd

# Import the model class from the modelclass module 
from modelclass import model 

# functions that improve rendering of ModelFlow outputs
model.widescreen()
model.scroll_off();
```

## Load the model: Load a pre-existing model, data and descriptions 

To load a model use the ```model.modelload()``` method of ```ModelFlow```. In the example below, the model has been saved to the models folder located one level above the directory from which the `Jupyter Notebook` has been executed (but within the scope of `Jupyter` itself, i.e. below the directory from which the `Jupyter` system was launched.


### The `.modelload()` method

The command below

```
mpak,bline = model.modelload('../models/pak.pcim', alfa=0.7,run=1,keep= 'Baseline')
```
 
instantiates (creates an instance of) a `ModelFlow model` object using the model object (equiations and data) contained in the file `pak.pcim` and assigns it to the variable name `mpak`.

The ```run=1``` option executes the model and assigns the result of the model execution to the `DataFrame` ```bline```.  

The model is solved with the parameter alfa set to 0.7.  The $alfa \in (0,1)$ parameter determines the step size of the solution engine. The larger alfa the larger the step size. Larger step sizes solve faster, but may have trouble finding a unique solution.  Smaller step sizes take longer to solve but are more likely to find a unique solution.  Values of alfa=.7 work well for World Bank models.

The ```keep``` option instructs ```ModelFlow``` to maintain in the model object (```mpak```) the results of the initial scenario, assigning it the text name ```Baseline```.   As written, `modelload` returns both the model object `mpak`, but also a `DataFrame` ```bline``` that is assigned the results of the simulation.  This `DataFrame` is distinct from the one that is stored inside the `mpak` model object by the ```keep=``` command, although the data inside each of these `DataFrame`s will have the same numerical values. The `keep` option is described in more detail in the following chapter on scenarios.


If `ModelFlow` cannot find the file at the position indicated it will look for it in the global Model repository on line.

Upon return, the `modelload` command indicates the location from which the model was retrieved.  In this case, from the requested local file store.

```python
#Replace the path below with the location of the pak.pcim file (or some other world bank model file) on your computer
mpak,bline = model.modelload('../models/pak.pcim', \
                                alfa=0.7,run=1,keep= 'Baseline')
```

```text
Zipped file read:  ..\models\pak.pcim
```

### Extracting information about the model

The newly loaded python object  `mpak` is an instance of the model class and as such inherits the `methods` (functions) and `properties` (data) of that class. To learn about the model there are a variety of methods that can be used to extract information about the model and its data.

A World Bank model in `ModelFlow` contains a wide range of objects.

* variables  -- time series variables comprised of mnemonics and data
* dataframes -- data for each variable generated in  different simulations 
* groups     -- lists of variables
* equations  -- identities and behaviorals
* model      -- the model object itself

Extracting information about each of these objects is central to working with WBG models in `ModelFlow`.

The model object contains information about the model itself, its name, its structure (does it contain simultaneous equations or is it recursive), the number of variables it contains and the number that are exogenous and endogenous (have associated equations). Executing the unadorned name of a model object, i.e. `mpak` displays summary information about the model object.

```python
mpak
```

```text
<
Model name                              :                  PAK 
Model structure                         :         Simultaneous 
Number of variables                     :                  839 
Number of exogeneous  variables         :                  461 
Number of endogeneous variables         :                  378 
>
```

The model work space also has a time dimension, its sample period.  This can be retrieved and changed.

```python
mpak.current_per
```

```text
Index([2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027,
       2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035],
      dtype='int64')
```

Here the model is currently set up to solve over the period 2016 through 2030.  That period can be changed assuming, as is the case with the Pakistan model, that additional data are available.

### Information about variables 

The model object `mpak` contains lists of all the variables that form part of the model, and these lists can be interrogated to garner information about the model.  The Table below indicates some of the most important of these queries.  The variables for which information is sought can be specified directly or through a wildcard specification (see note).  


|Method | Example|Information returned |
|:--|:--|:--|
|`.names`|`mpak ['PAKNECON*XN] .name`| A python list of the mnemonics of all the variables defined and contained in the model object that match the search paremers in the `[]`|
|`.des`|`mpak ['PAKNECONPRVT?N'] .des` | A dictionary of mnemonics and their variable descriptions |
|`.<var name>.show`|`mpak.PAKNECONPRVTXN.show` | Lists the equation (formula), variable descriptions and data  values of a specific variable |





**Wildcards**

Most of the variable and equation information commands accept wildcard specifications in the search parameter.

The `*` character in the command ```mpak['PAKNECON*XN'].names``` example is a `wildcard` character and the expression will return all variables that begin PAKNECON and end XN.  

The `?` in the `.des` example is another wildcard expression. It will match only single characters.  Thus ```mpak['PAKNECONPRVT?N'].names```  would return three variables: ```PAKNECONPRVTKN```, ```PAKNECONPRVTXN```, and ```PAKNECONPRVTXN```.  The real, current value, and deflators for household consumption expenditure.

Note the final show example uses a slightly different syntax where the variable to be operated upon is specified directly: `modelname.PAKNECONPRVTXN.show`. 


The example below returns the mnemonics and descriptions of all variables matching the pattern `PAKNYGDP*KN`, i.e. Pakistani variables (PAK) from the National Income Accounts (NY) from the main sub-category GDP that are also real (K) expressed in local currency units (N) variables.

latexcommand \newpage





A typical World Bank model will have in excess of 300 variables.  Each has a mnemonic typically comprised of 14 characters that is structured in a specific way, The root for almost all variables is the three letters of the ISO code for the country to which the variable pertains.   Other letters describe the variable in ever finer detail (see below).
  
  
$$\texttt{12345678901234}$$
$$\color{green}{\texttt{CCC}}\color{red}{\texttt{AA}}\color{lime}{\texttt{MMM}}\color{blue}{\texttt{NNNN}}\color{magenta}{\texttt{U}}\color{black}{\texttt{C}}$$
    
where:

| Letters| Meaning |
|:---:|:---|
| $\color{green}{\texttt{CCC}}$ | The three-leter ISO code for a country -- i.e. IDN for Indonesia, RUS for Russia | 
| $\color{red}{\texttt{AA}}$ | The two-letter major accounting system to which the variable attaches (see following Table for more info) | 
| $\color{lime}{\texttt{MMM}}$ |The three-letter major sub-category of the data -  i.e. GDP, EXP - expenditure | 
|$\color{blue}{\texttt{NNNN}}$ | The four-letter minor sub-category  MKTP for market prices |
| $\color{magenta}{\texttt{U}}$ | The measure  (K: real variable;C: Current Values; X: Prices)|
|$\color{black}{\texttt{C}}$ | denotes the Currency (N: National currency; D: USD; P: PPP)|

Common major accounting systems mnemonics: 

The, $\color{red}{\texttt{AA}}$s from above include:

| Code | Meaning |
|:--:|:--|
| NY | National income |
| NE | National expenditure Accounts|
| NV | Value added accounts |
| GG | General Government Accounts|
| BX | Balance of Payments: Exports |
| BM | Balance of Payments: Imports |
| BN | Balance of Payments: Net |
| BF | Balance of Payments: Financial Account |

**Less common terminations:**
Occasionally you will see variables with and '\_' appended to the name.  This indicates that the variable is being expressed as a percent of something (usually GDP).  Thus PAKBNCABFUNDCD_ means Pakistan (PAK) Balance of Payments, net  (BN) of the Current Account (CAB) IMF definition (FUND) in Current (C) Dollars (D) expressed as a percent of GDP.

Others less common terminations include ER (Effective rate) and (SR) Statutory rate used to denote the average tax rate (ER) of a tax versus the legal rate (SR).

Thus:

| Mnemonic | Meaning |
|:--:|:---|
|IDNNYGDPMKTPKN| Indonesia GDP at market prices, real in Indonesian Rupiah|
|KENNECPNPRVTXN| Kenya Private (household) consumption expenditure schillings deflator |
|BOLGGEXPGNFSCN| Bolivia Government Expenditure on Goods and services (GNFS) in current Bolivars|
|HRVGGREVDCITCN| Croatia Government Revenues Direct Corporate Income Taxes in current Euros|
|NPLBXGSRNFSVCD| Nepal BOP Exports of non-factor services (goods and services) in current USD|

If executed, the command `mpak['*'].des` would return a dictionary of all the mnemonics and descriptions of all the variables in the `mpak` model object.

The below command is more restrictive and returns only the variables that start `PAKNYGDP` and `KN`.

```python
mpak['PAKNYGDP*KN'].des
```

```text
PAKNYGDPDISCKN : GDP Disc., 2000 LCU mn
PAKNYGDPFCSTKN : GDP Factor Cost Local Currency units Volumes National base year
PAKNYGDPMKTPKN : Real GDP
PAKNYGDPPOTLKN : Potential Output, constant LCU
```

#### The `!` operator -- searching on the variable description

The `!` operator allows the same methods to be used to retrieve information about variables, but based on their descriptions. Pre-pending the search string with the  `!` operator, tells it to try and match (and display) information about variables based on their descriptions not their mnemonics.


**The ! operator**
If a wildcard is preceded by an exclamation mark **!** the search will be done over the description of variables instead of the mnemonic

The below expression returns the mnemonics of all variables whose description includes the word Carbon. 

```python
mpak['!*Carbon*'].names
```

```text
['PAKCCEMISCO2TKN', 'PAKGGREVCO2CER', 'PAKGGREVCO2GER', 'PAKGGREVCO2OER']
```

The following expression returns the mnemonics and descriptions of the same variables.

```python
mpak['!*Carbon*'].des
```

```text
PAKCCEMISCO2TKN : Total Carbon emissions (tons)
PAKGGREVCO2CER  : Carbon tax on coal (USD/t)
PAKGGREVCO2GER  : Carbon tax on gas (USD/t)
PAKGGREVCO2OER  : Carbon tax on oil (USD/t)
```

The following expression returns the descriptions of a specific variable.

```python
mpak.var_description['PAKGGREVCO2OER']
```

```text
'Carbon tax on oil (USD/t)'
```

## Groups

`ModelFlow` incorporates a variant of the idea of groups from `EViews`.  In `ModelFlow` the groups defined in an imported `EViews` workfile are converted into entries in a dictionary called `var_groups` which can be interrogated, added to and amended like any dictionary in `python`.

The command
`mpak.var_groups` will return all of the groups already defined in mpak.

```python
mpak.var_groups
```

```text
{'Headline': '{cty}NYGDPMKTPKN {cty}NYGDPMKTPXN {cty}NRTOTLCN {cty}LMUNRTOTLCN {cty}BFFINCABDCD  {cty}BFBOPTOTLCD {cty}GGBALEXGRCN {cty}GGDBTTOTLCN_ {cty}GGDBTTOTLCN {cty}BNCABLOCLCD_ {cty}FPCPITOTLXN {cty}CCEMISCO2TKN',
 'National income accounts': '{cty}NY*',
 'National expenditure accounts': '{cty}NE*',
 'Value added accounts': '{cty}NV*',
 'Balance of payments exports': '{cty}BX*',
 'Balance of payments exports and value added ': '{cty}BX* {cty}NV*',
 'Balance of Payments Financial Account': '{cty}BF*',
 'General government fiscal accounts': '{cty}GG*',
 'World all': 'WLD*',
 'All variables': '*'}
```

A group can be added to the dictionary by giving it a unique identifier (key) and associating with it a string defining the group, using a wildcard specification or just a space de-limited list of mnemonics.

Thus the first command below will generate a new group called 'MyGroup' that contains all variables beginning PAKGGREV and ending CN, plus the variable PAKGGBALOVRLCN to the dictionary var_groups that is part of the model object `mpak`. The second creates a group called LaborMarket which contains the variables for Employment and the Unemployment rate.

```python
mpak.var_groups['MyGroup']='PAKGGREV*CN PAKGGBALOVRLCN'
mpak.var_groups['LaborMarket']='PAKLMEMPTOTLCN PAKLMUNRTOTLCN'
```

### The `#` operator -- searching on the variable description

The `#` operator allows the same methods to be used to retrieve information about groups. Pre-pending the search string with the  `#` operator, tells it to try and match (and display) information about the variables in groups that match the search expression following the #.


**The # operator**
If a wildcard is preceded by an exclamation mark **#** the search will be done over the groups in the model object and will return information about the members of the returned groups 

The below expression returns the mnemonics of all variables that are a member of the MyGroup Group. 

```python
mpak['#MyGroup'].names
```

```text
['PAKGGREVDRCTCN',
 'PAKGGREVEMISCN',
 'PAKGGREVGNFSCN',
 'PAKGGREVGRNTCN',
 'PAKGGREVOTHRCN',
 'PAKGGREVTOTLCN',
 'PAKGGREVTRDECN',
 'PAKGGBALOVRLCN']
```

### Information about the data of series in a group

The unadorned command `mpak[#MyGroups]` invokes a widget that shows all of the data in the group `MyGroup` and various representations (level and growth rates) both as tables and charts.

```python
mpak['#MyGroup']
```

```text
Tab(children=(Tab(children=(HTML(value='<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE svg …
```

    :alt: group output widget 
    :class: bg-primary mb-1
    :width: 100%
    :align: center

Alternatively just the graphs and or tables can be returned, by appending the `.df` method (tables) or `.plot()` methods (charts).  Modifying the command further by including the `.pct` command  would display the data as growth rates.

```python
mpak['#MyGroup'].df
```

```text
PAKGGREVDRCTCN  PAKGGREVEMISCN  PAKGGREVGNFSCN  PAKGGREVGRNTCN  \
2016    1.192249e+06  -187487.145909    1.319524e+06    28696.665824   
2017    1.354036e+06  -368998.340508    1.327860e+06    25349.188671   
2018    1.492389e+06  -373989.822906    1.516485e+06    49838.249132   
2019    1.721883e+06  -387328.506728    1.764865e+06    78978.628398   
2020    1.950849e+06  -391591.258782    1.998747e+06   110163.222909   
2021    2.178938e+06  -392424.135929    2.225111e+06   142678.758726   
2022    2.407303e+06  -393527.268737    2.450129e+06   176071.658387   
2023    2.644233e+06  -396768.489177    2.685256e+06   210616.945685   
2024    2.894933e+06  -402416.006333    2.936720e+06   246606.677379   
2025    3.161598e+06  -409971.057333    3.206328e+06   284195.083403   
2026    3.444363e+06  -418754.040478    3.493313e+06   323384.807391   
2027    3.743124e+06  -428241.872630    3.796738e+06   364156.631099   
2028    4.058704e+06  -438151.424167    4.116861e+06   406583.541154   
2029    4.393195e+06  -448385.655974    4.455458e+06   450879.142616   
2030    4.749689e+06  -458938.010399    4.815425e+06   497380.152814   
2031    5.131800e+06  -469817.783689    5.200188e+06   546498.760450   
2032    5.543290e+06  -481016.427014    5.613280e+06   598678.767764   
2033    5.987899e+06  -492506.888060    6.058177e+06   654372.159512   
2034    6.469364e+06  -504258.234782    6.538358e+06   714036.436278   
2035    6.991538e+06  -516250.612498    7.057461e+06   778144.672642   

      PAKGGREVOTHRCN  PAKGGREVTOTLCN  PAKGGREVTRDECN  PAKGGBALOVRLCN  
2016    1.704982e+06    4.463113e+06    4.051485e+05   -1.322586e+06  
2017    2.141104e+06    4.976845e+06    4.974946e+05   -1.833428e+06  
2018    2.505467e+06    5.802066e+06    6.118760e+05   -1.814775e+06  
2019    3.033525e+06    6.967846e+06    7.559233e+05   -1.764188e+06  
2020    3.574406e+06    8.136424e+06    8.938484e+05   -1.798450e+06  
2021    4.122857e+06    9.307621e+06    1.030460e+06   -1.857821e+06  
2022    4.677542e+06    1.048922e+07    1.171700e+06   -1.939507e+06  
2023    5.252367e+06    1.171840e+07    1.322695e+06   -2.033015e+06  
2024    5.856855e+06    1.301870e+07    1.486000e+06   -2.146245e+06  
2025    6.495230e+06    1.439974e+07    1.662364e+06   -2.279101e+06  
2026    7.167704e+06    1.586160e+07    1.851585e+06   -2.433659e+06  
2027    7.874000e+06    1.740321e+07    2.053431e+06   -2.610006e+06  
2028    8.615802e+06    1.902797e+07    2.268174e+06   -2.806904e+06  
2029    9.397577e+06    2.074544e+07    2.496720e+06   -3.022765e+06  
2030    1.022607e+07    2.257011e+07    2.740488e+06   -3.256688e+06  
2031    1.110928e+07    2.451915e+07    3.001198e+06   -3.508801e+06  
2032    1.205564e+07    2.661059e+07    3.280716e+06   -3.780096e+06  
2033    1.307361e+07    2.886255e+07    3.580994e+06   -4.072057e+06  
2034    1.417167e+07    3.129327e+07    3.904098e+06   -4.386355e+06  
2035    1.535858e+07    3.392175e+07    4.252273e+06   -4.724724e+06
```

Below the command has been placed inside a `with mpak.set_smpl()` clause to restrict the output to a shorter period.  If it was not used the output would cover the whole time period of the `.lastdf` DataFrame from which all of this data is drawn. In addition the round command is used to restrict the number of decimal places shown.  


When using a `with` clause, an explicit print statement is required. 

Below the same logic is used to display the data from variables matching a mnemonic search.  The results have been placed inside a `with mpak.set_smpl()` clause to restrict the output to a shorter period.  If it was not used the output would cover the whole time period of the `.lastdf  DataFrame` from which all of these data are drawn.  


When using a `with` clause, an explicit print statement is required. 

```python
with mpak.set_smpl(2020,2025):
    print(round(mpak['#MyGroup'].pct.df,2)) # round restricts the display to 2 decimal points
```

```text
      PAKGGREVDRCTCN  PAKGGREVEMISCN  PAKGGREVGNFSCN  PAKGGREVGRNTCN  \
2020           13.30            1.10           13.25           39.48   
2021           11.69            0.21           11.33           29.52   
2022           10.48            0.28           10.11           23.40   
2023            9.84            0.82            9.60           19.62   
2024            9.48            1.42            9.36           17.09   
2025            9.21            1.88            9.18           15.24   

      PAKGGREVOTHRCN  PAKGGREVTOTLCN  PAKGGREVTRDECN  PAKGGBALOVRLCN  
2020           17.83           16.77           18.25            1.94  
2021           15.34           14.39           15.28            3.30  
2022           13.45           12.69           13.71            4.40  
2023           12.29           11.72           12.89            4.82  
2024           11.51           11.10           12.35            5.57  
2025           10.90           10.61           11.87            6.19
```

When displaying a dataframe or a manipulation of a dataframe in cases where the output might include very many lines of output, Jupyter will, by default, truncate the output by showing the first and last five observations of the active sample period when the same call is  made without the with clause.

```python
mpak.smpl(2000,2100)  # change the default view to cover 100 observations
round(mpak['#MyGroup'].pct.df,2)  #Jupyter will truncate the output
```

```text
PAKGGREVDRCTCN  PAKGGREVEMISCN  PAKGGREVGNFSCN  PAKGGREVGRNTCN  \
2000            9.55          101.83           70.02             NaN   
2001           11.14           15.37           31.46             inf   
2002           14.66          -13.23            8.55           94.82   
2003            7.11           35.47           17.12          -36.96   
2004            8.43           21.64           13.05          -39.98   
...              ...             ...             ...             ...   
2096            9.03            2.85            9.07            9.03   
2097            9.02            2.84            9.06            9.02   
2098            9.02            2.84            9.06            9.02   
2099            9.01            2.84            9.06            9.01   
2100            9.01            2.84            9.05            9.01   

      PAKGGREVOTHRCN  PAKGGREVTOTLCN  PAKGGREVTRDECN  PAKGGBALOVRLCN  
2000             NaN            7.30          -21.68           15.14  
2001             inf           16.34            5.52          -35.57  
2002           17.59           22.84          -26.44          -19.00  
2003           15.20            6.04           43.96           23.55  
2004           26.30           15.68           32.11          -19.92  
...              ...             ...             ...             ...  
2096            9.03            9.03            8.96            9.03  
2097            9.02            9.03            8.96            9.03  
2098            9.02            9.02            8.95            9.02  
2099            9.01            9.02            8.95            9.02  
2100            9.01            9.01            8.95            9.01  

[101 rows x 8 columns]
```

### Display data from a group graphically

```python
mpak['#MyGroup'].pct.plot(title="Plot of Mygroup\ngrowth rates");
```

```text
<Figure size 1000x800 with 8 Axes>
```

## Information about equations

Information about specific equations can also be extracted and displayed.

###  The `endogene` property

The  `endogene` property returns a list of all variables in the model that are endogenous (have an equation). It can also be used to test whether a specific mnemonic has an equation associated with it. 

The  `endogene` property returns a `list`. For brevity only the first 5 elements are show below.

```python
sorted(mpak.endogene)[:5]
```

```text
['CHNEXR05', 'CHNPCEXN05', 'DEUEXR05', 'DEUPCEXN05', 'FRAEXR05']
```

The expression `'PAKNECONPRVTKN' in mpak.endogene` returns True if the passed mnemonic is in the list returned by `mpak.endogene`.

```python
'PAKNECONPRVTKN' in mpak.endogene
```

```text
True
```

### Retrieving info on equations

There are three functions to extract the equations from a model.  

|Command|Effect|
|:--|:--|
|`mpak['PAKNECONPRVTKN'].frml`|Returns a **normalized** version of the equation (the one actually used in ModelFlow)|
|`mpak['PAKNECONPRVTKN'].eviews`|In models imported from Eviews, reports the original eviews specification|
|`mpak.PAKNECONPRVTXN.show` | Displays the equation (formula); variable descriptions; and variable values.|

### The `.eviews` method

The ```mpak['PAKNECONPRVTKN'].eviews``` command returns the equations before they were normalized. In most cases this is a slightly more legible form. Here following the EViews syntax, $\Delta ln()$ is written as dlog().

```python

mpak['PAKNECONPRVTKN'].eviews
```

```text
PAKNECONPRVTKN : 
DLOG(PAKNECONPRVTKN) =- 0.2*(LOG(PAKNECONPRVTKN( - 1)) - LOG(1.21203101101442) - LOG((((PAKBXFSTREMTCD( - 1) - PAKBMFSTREMTCD( - 1))*PAKPANUSATLS( - 1)) + PAKGGEXPTRNSCN( - 1) + PAKNYYWBTOTLCN( - 1)*(1 - PAKGGREVDRCTXN( - 1)/100))/PAKNECONPRVTXN( - 1))) + 0.763938860758873*DLOG((((PAKBXFSTREMTCD - PAKBMFSTREMTCD)*PAKPANUSATLS) + PAKGGEXPTRNSCN + PAKNYYWBTOTLCN*(1 - PAKGGREVDRCTXN/100))/PAKNECONPRVTXN) - 0.0634474791568939*@DURING("2009") - 0.3*(PAKFMLBLPOLYXN/100 - DLOG(PAKNECONPRVTXN))
```

### The `.frml`  property

The `.frml` method returns the normalized equation that is actually used in ModelFlow.  

In this instance the variable to be displayed is referenced directly (not as the result of a search operation `['partial*variablename']` syntax.

Note: The `.frml` method also returns a long-text description of all the variables in the equation (assuming that one was defined for each variable).  Below, the DURING_2019 variable has had no dseciption defined so it returns a blank.


Following the normalized equation is a listing of all the dependent variables of the equation and their descriptions.


latexcommand \begin{samepage}

```python
mpak.PAKNECONPRVTKN.frml
```

```text
Endogeneous: PAKNECONPRVTKN: HH. Cons Real
Formular: FRML <DAMP,STOC> PAKNECONPRVTKN = (PAKNECONPRVTKN(-1)*EXP(PAKNECONPRVTKN_A+ (-0.2*(LOG(PAKNECONPRVTKN(-1))-LOG(1.21203101101442)-LOG((((PAKBXFSTREMTCD(-1)-PAKBMFSTREMTCD(-1))*PAKPANUSATLS(-1))+PAKGGEXPTRNSCN(-1)+PAKNYYWBTOTLCN(-1)*(1-PAKGGREVDRCTXN(-1)/100))/PAKNECONPRVTXN(-1)))+0.763938860758873*((LOG((((PAKBXFSTREMTCD-PAKBMFSTREMTCD)*PAKPANUSATLS)+PAKGGEXPTRNSCN+PAKNYYWBTOTLCN*(1-PAKGGREVDRCTXN/100))/PAKNECONPRVTXN))-(LOG((((PAKBXFSTREMTCD(-1)-PAKBMFSTREMTCD(-1))*PAKPANUSATLS(-1))+PAKGGEXPTRNSCN(-1)+PAKNYYWBTOTLCN(-1)*(1-PAKGGREVDRCTXN(-1)/100))/PAKNECONPRVTXN(-1))))-0.0634474791568939*DURING_2009-0.3*(PAKFMLBLPOLYXN/100-((LOG(PAKNECONPRVTXN))-(LOG(PAKNECONPRVTXN(-1)))))) )) * (1-PAKNECONPRVTKN_D)+ PAKNECONPRVTKN_X*PAKNECONPRVTKN_D  $

PAKNECONPRVTKN  : HH. Cons Real
DURING_2009     : 
PAKBMFSTREMTCD  : Imp., Remittances (BOP), US$ mn
PAKBXFSTREMTCD  : Exp., Remittances (BOP), US$ mn
PAKFMLBLPOLYXN  : Key Policy Interest Rate
PAKGGEXPTRNSCN  : Current Transfers
PAKGGREVDRCTXN  : Direct Revenue Tax Rate
PAKNECONPRVTKN_A: Add factor:HH. Cons Real
PAKNECONPRVTKN_D: Fix dummy:HH. Cons Real
PAKNECONPRVTKN_X: Fix value:HH. Cons Real
PAKNECONPRVTXN  : Implicit LCU defl., Pvt. Cons., 2000 = 1
PAKNYYWBTOTLCN  : Total Wage Bill
PAKPANUSATLS    : Exchange rate LCU / US$ - Pakistan
```

latexcommand \end{samepage}

### The `.show` method

The `.show` method returns:
1. The description of the variable
1. The normalized equation that is actually used in ModelFlow.
1. A listing of the mnemonics and descriptions of the RHS variables
1. The data of that variable (drawn from the `basedf` and `.lastdf` DataFrames in the model object as well as the data of the RHS variables of the equation from both the `basedf` and `.lastdf` DataFrames.

```python
mpak.smpl(2020,2025) #change the actual sample range to limit the number of columns displayed
mpak.PAKNECONPRVTKN.show
```

```text
Endogeneous: PAKNECONPRVTKN: HH. Cons Real
Formular: FRML <DAMP,STOC> PAKNECONPRVTKN = (PAKNECONPRVTKN(-1)*EXP(PAKNECONPRVTKN_A+ (-0.2*(LOG(PAKNECONPRVTKN(-1))-LOG(1.21203101101442)-LOG((((PAKBXFSTREMTCD(-1)-PAKBMFSTREMTCD(-1))*PAKPANUSATLS(-1))+PAKGGEXPTRNSCN(-1)+PAKNYYWBTOTLCN(-1)*(1-PAKGGREVDRCTXN(-1)/100))/PAKNECONPRVTXN(-1)))+0.763938860758873*((LOG((((PAKBXFSTREMTCD-PAKBMFSTREMTCD)*PAKPANUSATLS)+PAKGGEXPTRNSCN+PAKNYYWBTOTLCN*(1-PAKGGREVDRCTXN/100))/PAKNECONPRVTXN))-(LOG((((PAKBXFSTREMTCD(-1)-PAKBMFSTREMTCD(-1))*PAKPANUSATLS(-1))+PAKGGEXPTRNSCN(-1)+PAKNYYWBTOTLCN(-1)*(1-PAKGGREVDRCTXN(-1)/100))/PAKNECONPRVTXN(-1))))-0.0634474791568939*DURING_2009-0.3*(PAKFMLBLPOLYXN/100-((LOG(PAKNECONPRVTXN))-(LOG(PAKNECONPRVTXN(-1)))))) )) * (1-PAKNECONPRVTKN_D)+ PAKNECONPRVTKN_X*PAKNECONPRVTKN_D  $

PAKNECONPRVTKN  : HH. Cons Real
DURING_2009     : 
PAKBMFSTREMTCD  : Imp., Remittances (BOP), US$ mn
PAKBXFSTREMTCD  : Exp., Remittances (BOP), US$ mn
PAKFMLBLPOLYXN  : Key Policy Interest Rate
PAKGGEXPTRNSCN  : Current Transfers
PAKGGREVDRCTXN  : Direct Revenue Tax Rate
PAKNECONPRVTKN_A: Add factor:HH. Cons Real
PAKNECONPRVTKN_D: Fix dummy:HH. Cons Real
PAKNECONPRVTKN_X: Fix value:HH. Cons Real
PAKNECONPRVTXN  : Implicit LCU defl., Pvt. Cons., 2000 = 1
PAKNYYWBTOTLCN  : Total Wage Bill
PAKPANUSATLS    : Exchange rate LCU / US$ - Pakistan

Values :
```

```text
Input last run:
```

```text
<pandas.io.formats.style.Styler at 0x21e92849f40>
```

```text
Input base run:
```

```text
<pandas.io.formats.style.Styler at 0x21e8f839df0>
```

```text
Difference for input variables
```

```text
<pandas.io.formats.style.Styler at 0x21e930f1490>
```

latexcommand \par


    :alt: show output 
    :class: bg-primary mb-1
    :width: 100%
    :align: center

latexcommand \par


    :alt: show output 
    :class: bg-primary mb-1
    :width: 100%
    :align: center

latexcommand \par


    :alt: show output 
    :class: bg-primary mb-1
    :width: 100%
    :align: center

latexcommand \par


    :alt: show output 
    :class: bg-primary mb-1
    :width: 100%
    :align: center

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

```python
# Prepare the notebook for use of ModelFlow 

# Jupyter magic command to improve the display of charts in the Notebook
%matplotlib inline

# Import pandas 
import pandas as pd

# Import the model class from the modelclass module 
from modelclass import model 

# functions that improve rendering of ModelFlow outputs
model.widescreen()
model.scroll_off();
```

```python
#Replace the path below with the location of the pak.pcim file (or some other world bank model file) on your computer
mpak,bline = model.modelload('../models/pak.pcim', \
                                alfa=0.7,run=1,keep= 'Baseline')
```

```text
Zipped file read:  ..\models\pak.pcim
```

# Equations in MFMod and `ModelFlow`

As noted above an `MFMod` is comprised of two types of equations: identities and behavioral equations. Identities are mathematical or accounting relationships that are always true.  The GDP accounting identity is a well known one:

$$Y_t=C_t+I_t+G_t+X_t-M_t$$

The general government deficit as revenues less spending is another.

Behavioral equations are also endogenous equations, but in a macrostructural model they describe an economic not an accounting relationship.  Typically these relationships are estimated econometrically and do not hold exactly.

:class: tip

This chapter provides a very brief overview of the type of equation in `MFMod` models (identities and behavioral equations), and a deep dive into the behavioral or econometrically estimated equations in these models.

Three main issues are discussed:

1) The importance of **Addfactors** (`_A` variables) in behavioral equations.
2) The mechanism by which behavioral equations can be exogenized or de-activated in the `ModelFlow` environment using the \_D and \_X variables.
3) An explanation of the Error Correction Model used to estimate many of the econometric relations in World Bank `MFMod` models.

## A behavioral equation

Normally a behavioral equation is comprised of a left-hand-side variable (the regressand or dependent variable), right-hand side variables (the regressors in the econometric relationship, or explanatory variables), estimated parameters, perhaps some imposed parameters, and an error term.  

Assume $y_t$ is the dependent variable, $X_t$ a vector of explanatory variables and $\eta_t$ the error term, then a simple regression can be written as:

$$y_t = \alpha + \beta X_t + \eta_t$$

where $\alpha$ and $\beta$ are parameters to be estimated or in most cases $\beta$ wil be a vector of estimated parameters.  

One the estimation has occurred $\alpha, \beta$ and $\eta_t$ take on precise values and the equation is rewritten as:

$$y_t = \hat{\alpha} + \hat{\beta} X_t + \hat{\eta_t}$$

where the hats "^" signify the specific value for the parameter that emerged from the estimation process. 

We can also write an expression for $\hat{y}_t$ the fitted value from the regression as:

$$\hat{y}_t = \hat{\alpha} + \hat{\beta} X_t $$

Substituting this expression into the previous expression and re-arranging gives us

$$y_t-\hat{y}_t= \hat{\eta_t}$$


All of which are fairly elementary results from econometrics.



## The add factor in behavioral equations

The econometrics used to estimate the equation ensure that the expected value of $\eta_t$ is zero. So the expectation of the above equation during the forecast period is 

\begin{align*}
E(y_t-\hat{y}_t) &= E (\hat{\eta_t}) \\
y_t-\hat{y}_t &= 0 \\
\end{align*}


In Macrostructural models the first of these equations is rewritten by substituting $AF_t$ for $\hat{\eta}_t$.  

$$y_t= \hat{y}_t + AF_t$$

By imposing a nonzero value on $AF_t$, the modeller can ***add*** her judgment to the model's fitted value, either to reflect a view that the forecast value of y will deviate from the fitted value, or because some change in circumstances (say a policy change) will cause the underlying equation to be different in the future than it was when the parameters were estimated (regime change or structural break). 

In World Bank models using `ModelFlow` the addfactor of an equation is given the same mnemonic as the dependent variable with an \_A appended to it.  Thus, in the above simplified version, the equation would be written as

$$y_t = \hat{\alpha} + \hat{\beta} X_t + y\_A_t$$



## Excluding behavioral equations

In `ModelFlow` behavioral equations can be excluded "de-activated" or included ("activated").  This is achieved by adding two additional variables to each equation. The first is given the name of the dependent variable with **\_D** appended.  The second is given the name of the dependent variable with **\_X** appended. 

The preceding equation is then re-written as below


\begin{equation*}
y_t = (1-y\_D_t)\cdot\underbrace{\biggl[\hat{\alpha} + \hat{\beta} X_t + y\_A_t\biggr]}_{\begin{array}{c} \text{Econometric equation}\end{array}} + y\_D_t\cdot \underbrace{y\_X_t}_{\begin{array}{c} \text{Exogenized} \\ \text{value} \end{array}}
\end{equation*}


**When $y\_D_t$ = 0**, the second part of the equation $y\_D_t*y\_X_t$ evaluates to zero and drops out, while the expression $(1-y\_D_t)$ evaluates to one. Thus the whole equation simplifies to the standard behavioral equation. 

\begin{align*}
y_t &= 1\cdot\biggl[\hat{\alpha} + \hat{\beta} X_t + y\_A_t\biggr]+ 0\\
y_t &= \hat{\alpha} + \hat{\beta} X_t + y\_A_t
\end{align*}

**When $y\_D_t$ = 1**, the $(1-y\_D_t)$ evaluates to zero so the first part of the equation drops out, and the equation simplifies to:

\begin{align*}
y_t &= 0\cdot\biggl[\hat{\alpha} + \hat{\beta} X_t + y\_A_t\biggr]+ 1\cdot y\_X_t\\
y_t &= y\_X_t\\
\end{align*}

Thus, when $y\_D_t$ = 1 the whole equation simply sets the endogenous variable $y_t$ equal to the exogenous variable $y\_X_t$. 

## Behavioral equations in ModelFlow

It follows therefore that equations in `ModelFlow` have three special variables associated with them.

**Special variables in ModelFlow behavioral equations**
|Terminator| Meaning|Role|
|:--|:--|:--|
|**\_A**|Add factor:| Special variable to allow judgment to be added to an equation|
|**\_X**|Exogenized value:| Special variable that stores the value that the equation should return if exogenized|
|**\_D**|Exogenous dummy:| Dummy variable. When set to one, the equation will return the value of the $\_X$ variable, if zero, it returns the fitted value of the equation plus the Add factor. |

Below the `EViews` and `ModelFlow` representations of the Household consumption equation are extracted from the model object using `.frml()` and `.eviews()` methods discussed in the previous chapter.

In the `EViews` representation we do not see the special variables but in the `frml` representation (which is the one actually used by `ModelFlow` they are visible.

```python
mpak.PAKNECONPRVTKN.eviews
```

```text
DLOG(PAKNECONPRVTKN) =- 0.2*(LOG(PAKNECONPRVTKN( - 1)) - LOG(1.21203101101442) - LOG((((PAKBXFSTREMTCD( - 1) - PAKBMFSTREMTCD( - 1))*PAKPANUSATLS( - 1)) + PAKGGEXPTRNSCN( - 1) + PAKNYYWBTOTLCN( - 1)*(1 - PAKGGREVDRCTXN( - 1)/100))/PAKNECONPRVTXN( - 1))) + 0.763938860758873*DLOG((((PAKBXFSTREMTCD - PAKBMFSTREMTCD)*PAKPANUSATLS) + PAKGGEXPTRNSCN + PAKNYYWBTOTLCN*(1 - PAKGGREVDRCTXN/100))/PAKNECONPRVTXN) - 0.0634474791568939*@DURING("2009") - 0.3*(PAKFMLBLPOLYXN/100 - DLOG(PAKNECONPRVTXN))
```

```python
mpak.PAKNECONPRVTKN.frml
```

```text
Endogeneous: PAKNECONPRVTKN: HH. Cons Real
Formular: FRML <DAMP,STOC> PAKNECONPRVTKN = (PAKNECONPRVTKN(-1)*EXP(PAKNECONPRVTKN_A+ (-0.2*(LOG(PAKNECONPRVTKN(-1))-LOG(1.21203101101442)-LOG((((PAKBXFSTREMTCD(-1)-PAKBMFSTREMTCD(-1))*PAKPANUSATLS(-1))+PAKGGEXPTRNSCN(-1)+PAKNYYWBTOTLCN(-1)*(1-PAKGGREVDRCTXN(-1)/100))/PAKNECONPRVTXN(-1)))+0.763938860758873*((LOG((((PAKBXFSTREMTCD-PAKBMFSTREMTCD)*PAKPANUSATLS)+PAKGGEXPTRNSCN+PAKNYYWBTOTLCN*(1-PAKGGREVDRCTXN/100))/PAKNECONPRVTXN))-(LOG((((PAKBXFSTREMTCD(-1)-PAKBMFSTREMTCD(-1))*PAKPANUSATLS(-1))+PAKGGEXPTRNSCN(-1)+PAKNYYWBTOTLCN(-1)*(1-PAKGGREVDRCTXN(-1)/100))/PAKNECONPRVTXN(-1))))-0.0634474791568939*DURING_2009-0.3*(PAKFMLBLPOLYXN/100-((LOG(PAKNECONPRVTXN))-(LOG(PAKNECONPRVTXN(-1)))))) )) * (1-PAKNECONPRVTKN_D)+ PAKNECONPRVTKN_X*PAKNECONPRVTKN_D  $

PAKNECONPRVTKN  : HH. Cons Real
DURING_2009     : 
PAKBMFSTREMTCD  : Imp., Remittances (BOP), US$ mn
PAKBXFSTREMTCD  : Exp., Remittances (BOP), US$ mn
PAKFMLBLPOLYXN  : Key Policy Interest Rate
PAKGGEXPTRNSCN  : Current Transfers
PAKGGREVDRCTXN  : Direct Revenue Tax Rate
PAKNECONPRVTKN_A: Add factor:HH. Cons Real
PAKNECONPRVTKN_D: Fix dummy:HH. Cons Real
PAKNECONPRVTKN_X: Fix value:HH. Cons Real
PAKNECONPRVTXN  : Implicit LCU defl., Pvt. Cons., 2000 = 1
PAKNYYWBTOTLCN  : Total Wage Bill
PAKPANUSATLS    : Exchange rate LCU / US$ - Pakistan
```

Careful inspection of the output from the `.frml()` and `eviews()` methods, reveals that in the `.frml()` specification the three special variables have been added to the model formula that are not part of the `EViews` output.  These variables each have the same root mnemonic as the dependent variable **PAKNECONRPVTKN** but have special terminators \_A \_X \_D appended to them.


To exclude an equation, the \_D variable is set to 1 and the equation simplifies to `PAKNECONRPVTKN=PAKNECONRPVTKN\_X` if \_D=0 then the econometric relationship and the add-factor will jointly determine the value of PAKNECONRPVTKN.

## The ECM specification

Many of the behavioral equations in World Bank models are written as Error Correction Models (ECMs).  

The Error correction specification was developed to deal with two important problems in econometric equations.
1. Many time-series data tend to increase over time. As a result, a regression of one series on another series tends to have good fit even if the two variables are not really connected economically. For example, the price of cookies tends to rise over time because of inflation. Similarly, the quantity of screws produced in the manufacturing sector tends to rise over time because of increased population and, therefore, demand for manufactured goods. Regressing screw production on cookie prices will show a strong but spurious correlation. 
2. Purely short run models focus on growth or differences and get around the problem of the spurious correlation arising from regressing two unrelated series that each have a trend. While, these explained the short run deviations, stringing the estimated growth rates together could result in implicit levels that were unstable because they were not anchored to the long-run relationship between variables dictated by underlying economic theory (or empirical behavior).


The co-integration approach to econometrics ({cite:t} `engle_co-integration_1987`) combined with the closely related ECM approach provided a solution to the above problem by providing a mechanism for modeling both the long run relationship and short-run relationships between variables.

The ECM specification used in World Bank models is a single equation approach that follows ({cite:t}`wickens_dynamic_1988`) and is comprised of two parts (the long run relationship, and the short-run relationship), which are estimated simultaneously.

Consider as an example two variables say consumption and disposable income.  Both have an underlying trend or in the parlance are co-integrated to degree 1.  For simplicity we call them y and x.

### The short run relationship

In its simplest form, a short run relationship between the growth rates of two variables could be written as:

$$\Delta ln(Y_t) = \alpha + \beta \Delta ln(X_t) +\epsilon_t$$

or substituting lower case letters for the logged values.

$$\Delta y_t = \alpha + \beta \Delta x_t +\epsilon_t$$



### The long run equation


The long run relates the level of two (or more) variables.  A simplified version of that equation can be written as:

$$Y_t=αX_t^β+ \eta_t$$


Rewriting this (in logarithms) it can be expressed as:

$$y_t = ln⁡(α) + βx_t + \eta_t$$


#### The long run equation in the steady state

Note that in the steady state the expected value of the error term in the long run equation is zero ($\eta_t=0 $) so in those conditions the long run relationship can be simplified to:

$$y_t=ln⁡(α)+\beta x_t + 0$$

or equivalently (substituting A for the log of $\alpha$).

$$y_t-A-βx_t=0$$

Moreover if this expression is multiplied by some arbitrary constant, say $-\lambda$, it would still equal zero.

$$-\lambda(y_t -A-βx_t)$$ 

and in the steady state this will also be true for the lagged variables 

$$-\lambda(y_{t-1}- A - βx_{t-1})$$ 

The part of the equation between the parenthesis is equal to the lagged error term of the long-run equation ($\eta_{t-1}$). In the Long Run its expected value is zero, but at any give instant it could be different from zero. The distance it is from zero at any point in time, reflects the distance that the dependent variable is from its long-run equilibrium value at that moment. 

### Putting it together

From before we have the short run equation:

$$\Delta y_t = \alpha + \beta \Delta x_t +\epsilon_t$$

Inserting the steady state expression for the long-run into the short run equation makes no difference (in the long run) because in the long run it is equal to zero.

$$\Delta y_t = -\lambda(y_{t-1}-A-\beta x_{t-1})  + \alpha + \beta \Delta x_t +\epsilon_t$$

When the model is not in the steady state, the expression $y_{t-1}-A-βx_{t-1}$ is of course the error term from the long run equation from the previous period (a measure of how far the dependent variable was from equilibrium).  

### Lambda, the speed of adjustment
The parameter $\lambda$ can then be interpreted as the speed of adjustment. It determines what share of the previous period error (distance from equilibrium) is absorbed in the following period. As long as $\lambda$ is greater than zero and less or equal to one if there are no further disturbances ( $\epsilon_t=0$) the expression multiplied by lambda will slowly decline toward zero. How fast depends on how large or small is $\lambda$.   


<mark>Intuitively, the lagged long-run error-term measures how far the model was from equilibrium one period earlier (at t-1). The ECM term (multiplied by $\lambda$ ensures the model will slowly converge to equilibrium -- the point at which the long run equation holds exactly -- if $\lambda$ is greater than zero but less than or equal to one. In these conditions during each each time period some portion $\lambda$ of the previous period year's disequilibrium will be absorbed each year. How much is absorbed depends on the size of estimated speed of the adjustment coefficient $\lambda$. </mark>

An ECM equation can, therefore be broken into two component parts.  For the consumption function it will look something like this:

$$\Delta c_t = -\lambda (\underbrace{
        log(C_{t-1})-log(Wages_{t-1}-Taxes_{t-1}+Transfers_{t-1}) -log(\alpha))}  _\text{Long run}
+\beta \underbrace{\Delta x_t}_\text{short run}$$



More precisely to be convergent $\lambda$ must be between 0 and 2. If Lambda is greater than 1 but less than two, the error term will oscillate from positive to negative but will slowly converge to zero. 

If lambda is greater than 2 (or less than zero), then the long run portion of the equation will cause the disequilibrium to grow each period not diminish. 

If lambda is less is greater than zero but less than one, the equation will converge more or less directly at a speed determined by the value of $\lambda$.  

#### An illustrative example

Below three ECMs are written out, each with and equilibrium value of 50 and different speeds of adjustment ranging from 0.3, 0.5 and 0.9.  The figure and table below illustrate the adjustment to the equilibrium value starting from an initial value of 100 (error of 50) under the three speeds of adjustment.

```python
import pandas as pd
ECMdf = pd.DataFrame({'E': 100},index=[v for v in range(2020,2051)])
ECMdf=ECMdf.upd('lbda3 lbda9 lbda5 = 100')
ECMdf=ECMdf.mfcalc('''
<2021 2050> dlog(Lbda3) = -.3 * (log(Lbda3(-1))-log(50))
<2021 2050> dlog(Lbda9) = -.9 * (log(Lbda9(-1))-log(50))
<2021 2050> dlog(Lbda5) = -.5 * (log(Lbda5(-1))-log(50))

''')
              
ECMdf.plot(title="Error correction process for different speeds of adjustment");
```

```text
<Figure size 640x480 with 1 Axes>
```

With a slow speed of adjustment, the equilibrium level of 50 is not achieved until around 2030 (<51) or 2032 (50.5). With $\lambda$=0.5 the gap is closed in around 5 years (2025=50.5), while with  $\lambda$=0.9 it takes just two years (2023=50.3).

```{note} Advanced formatting of tables
The table below introduces some advanced formatting routines, using the Pandas style property.  For more see [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html).

Info on python named colors can be found here: [https://matplotlib.org/stable/gallery/color/named_colors.html](https://matplotlib.org/stable/gallery/color/named_colors.html).
```

```python
    
def color_proximity(val):
    if val > 80:
        color="red"
    elif val > 70:
        color="orangered"
    elif val > 55:
        color="coral"
    elif val > 51:
        color="lightsalmon"
    elif val > 50.5:
        color="peachpuff"
    else: 
        color="white"
    return 'background-color: %s' % color



ECMdf.loc[2020:2035,['LBDA3','LBDA5','LBDA9']].style.map(color_proximity) \
.format(precision=2).set_table_attributes('style="font-size: 10px"')
```

```text
<pandas.io.formats.style.Styler at 0x14840067e90>
```

    :alt: ecm lambda
    :class: bg-primary mb-1
    :width: 30%
    :align: center

# Scenario analysis

Building and running scenarios is central to working with a macroeconomic model. Scenarios help to quantify the expected impacts of different policies and external events. In so doing they give valuable insights to policy makers concerning potential policies.  This chapter introduces users to scenario analysis using World Bank models and `ModelFlow`.  The scenarios presented are relatively simple, but cover all of the different kind of scenarios typically performed and insights into how to get around shortcomings that a specific model may have for a given question. 

:class: tip

This chapter presents examples of running simulations. Four types of simulation are covered:

1) **Permanent Exogenous Shocks**: These involve either *shocking an exogenous variable* (say World oil prices) or *deactivating an equation* and treating its dependent variable as if it were exogenous and shocking it directly.
2) **Endogenous Shocks**: In these shocks, a behavioral equation is left active, but its *add-factor is shocked* in order to impact its trajectory. This might be used when an external shock is expected, but the analyst wants the subsequent (and even contemporaneous) behavior of the variable to react to second-round effects that occur in the model (i.e., an increase in investment by one firm could be modelled using an add-factor, but as GDP rises, other firms would normally also want to increase their investment to meet the additional demand. By using the add-factor this second order effect is enabled).
3) **Temporary Exogenous Shocks**: Here a behavioral equation can be temporarily deactivated — give the endogenous variable an initial shock by setting its level directly to a specific level for a given period — but then reactivated in subsequent periods so that the variable's trajectory is affected by second- and third-round effects of the initial shock. This differs from the add-factor shock in that there is no endogenous reaction of the shocked variable during the period it is exogenized.
4) **Mixed Scenarios**: More complex scenarios that combine one or more shocks.

Similar shocks using each method are presented, allowing the reader to visualize the consequences of choosing one method over another.

## Prepare the python session
A first step in any policy analysis is to prepare your python environment for a new `ModelFlow` session. Starting with a fresh session (a clean slate as it were) is a critical assure reproducibility by ensuring that each time a scenario or scenarios are run they do so from the same starting point. This is done below starting a new python session, initializing pandas and `ModelFlow` and the reading a previously saved WBG model read from disk and solving it.

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

```python
# Prepare the notebook for use of ModelFlow 

# Jupyter magic command to improve the display of charts in the Notebook
%matplotlib inline

# Import pandas 
import pandas as pd

# Import the model class from the modelclass module 
from modelclass import model 

# functions that improve rendering of ModelFlow outputs
model.widescreen()
model.scroll_off();
```

These are precisely the same commands used to start the previous chapter and form the essential initialization commands of any python session using `ModelFlow`.

Set some pandas display options.

```python
# pandas options to make output more legible: 
pd.set_option('display.width', 100)
pd.set_option('display.float_format', '{:.2f}'.format)
```

Following the discussion in the previous chapter a model object `mpak` is loaded and solved with the result being stored in a new dataframe called `bline`.The `keep` option causes a copy of the solved scenario to be stored as "Baseline" within the model object mpak.

```python
#Load a saved version of the Pakistan model and solve it, 
#saving the results in the model object mpak, and the resulting dataframe in bline

#Replace the path below with the location of the pak.pcim file on your computer
mpak,bline = model.modelload('../models/pak.pcim', \
                                run=True,keep= 'Baseline')
```

```text
Zipped file read:  ..\models\pak.pcim
```

:class: tip
In addition, to the keep dataframe and the `bline` dataframe the ```model``` object (```mpak``` in this instance) always contains two `DataFrames`. The`.basedf` dataframe that contains the initial values for the variables of the model, and the `.lastdf` contains the results of the most recently executed scenario -- in this case `lastdf` will have the same values as `bline`.

### Checking that the simulated results reproduce the inputs
A critical component of reproducibility is that when a model is solved without changing any inputs (as was the case of the load) the model should return (reproduce) exactly the same data as before[^fn2].  The results from the simulation run on loading the model (caused by the `Run=True` option in the `modelload` command) can be examined by comparing the values in the ```basedf``` and ```lastdf``` `DataFrame`s.

[^fn2]: If a model does not reproduce itself when solved, then mathematically it means that the system of equations is not closed (there is no single answer) or data are inconsistent (usually one or more identities do not hold). In such circumstances, either the model will not solve or it will but it will not be possible to have confidence in any of the results generated.

 Below, the percent difference between the values of the variables for real GDP and Consumer demand in the two `dataframes` `.basedf` and `lastdf` are displayed.  They return zero following a simulation where the inputs were not changed -- confirming that the model reproduced the original data.

The .difpctlevel method of the model object display for the variables indicated the contents of the .lastdf (results of most recent simulation) and .basedf (initial simulation results) `DataFrame`s, expressed  as the percent change from the original (.basedf). ${\frac{.lastdf-.basedf}{.basedf}} * 100$ The .df modifier instructs the model object to return the results as a `DataFrame` (Chapter 14 below has more on report-writing options an techniques).

```python
with mpak.set_smpl(2020,2030):
    print(mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN'].difpctlevel.rename().df)
```

```text
      Real GDP  HH. Cons Real
2020      0.00           0.00
2021      0.00           0.00
2022      0.00           0.00
2023      0.00           0.00
2024      0.00           0.00
2025      0.00           0.00
2026      0.00           0.00
2027      0.00           0.00
2028      0.00           0.00
2029      0.00           0.00
2030      0.00           0.00
```

## Different kinds of simulations

The `ModelFlow` package performs 4 different kinds of simulation:

1. A shock to an exogenous variable in the model.
2. An exogenous shock of a behavioral variable, executed by exogenizing the variable (de-activating its equation).
3. An endogenous shock of a behavioral variable, executed by shocking the add factor of the variable.
4. A mixed shock of a behavioral variable, achieved by temporarily exogenizing the variable.

Although technically ModelFlow would allow us to shock identities, that would violate their nature as accounting rules. **Effectively such a shock would break the economic sense of the model.** 

As a result, this possibility is not discussed. 

### A shock to an exogenous variable

A World Bank model will reproduce the same values if inputs (exogenous variables) are not changed (as demonstrated above).  In the simulation below, the oil price is changed -- increasing by $25 for the three years between 2025 and 2027 inclusive. As a result, we expect the solution to return different values for the endogenous variables that are sensitive to changes in the price of oil, such as GDP, inflation, consumption and the current account balance for example.

#### Preparing the data for simulation

The following steps are performed to prepare the simulation:

1. Using the `.upd` method, a new input dataframe `oilshockdf` is created where the oil price is increased by $25 during 2025, 2026 and 2027.
2. A dataframe `compdf` is assigned the pre-shock and post-shock values of the oil price and the difference between the initial and shocked values.
3. Finally the results are displayed, confirming that the mfcalc statement revised the oil price data.

More on the `.upd` method here:[The upd method returns a DataFrame with updated variables](The_upd_method_returns_a_DataFrame_with_updated_variables)


Even more [upd test](upd)

```python
# Use the upd routine to create a new dataframe where $25 is added to the oil price bewteen 2025 and 2027

oilshockdf = mpak.basedf.upd('<2025 2027> WLDFCRUDE_PETRO + 25')
#compdf.drop(axis=0, inplace=True) #snure compdf is empty
# Create new df compdf and initialize it for the period
# 2000-2030 with the values from basedf
compdf=mpak.basedf.loc[2000:2030,['WLDFCRUDE_PETRO']]
compdf = compdf.rename(columns={'WLDFCRUDE_PETRO': 'Original'})

# Add a new series LASTDF with the World Crude price from the shock dataframe
compdf['Shock']=oilshockdf.loc[2000:2030,['WLDFCRUDE_PETRO']]

# Add a final series as the difference between the first two.
compdf['Dif']=compdf['Shock']-compdf['Original']

# Display the new comparison dataframe
compdf.loc[2024:2030]
```

```text
Original  Shock   Dif
2024     80.37  80.37  0.00
2025     85.34 110.34 25.00
2026     90.61 115.61 25.00
2027     96.22 121.22 25.00
2028    102.17 102.17  0.00
2029    108.48 108.48  0.00
2030    115.19 115.19  0.00
```

#### Running the simulation

Having created a new dataframe comprised of all the old data plus the changed data for the oil price, a simulation can now be run.  

In the command below, the simulation is run from 2020 to 2040, using the `oilshockdf` as the input `DataFrame` (this is the `Dataframe` that has the higher oil price).  The results of the simulation are assigned to a new `DataFrame`  named `ExogOilSimul`.  The `Keep` command ensures that the mpak model object stores (keeps) a copy of the results identified by the text name *'$25 increase in oil prices 2025-27'*.

```python
#Simulate the model 
ExogOilSimul = mpak(oilshockdf,2020,2040,keep='$25 increase in oil prices 2025-27')
```

##### Results

`ModelFlow` tools can be used to visualize the impacts of the shock; as a table; as a chart and, within Jupyter notebook, as an interactive widget.

The display below confirms that the shock was executed as desired. The `dif.df` method returns the difference between the `.lastdf` and `.basedf` values of the selected variable(s) as a `DataFrame`. The `with mpak.set_smpl(2020,2030):` clause temporarily restricts the sample period over which the following **indented** commands are executed.  

Alternatively the `mpak.smpl(2020,2030)`could be used. This would restricts the time period of over which **all** subsequent commands are executed.

```python
with mpak.set_smpl(2020,2030):
    print(mpak['WLDFCRUDE_PETRO'].dif.df);
```

```text
      WLDFCRUDE_PETRO
2020             0.00
2021             0.00
2022             0.00
2023             0.00
2024             0.00
2025            25.00
2026            25.00
2027            25.00
2028             0.00
2029             0.00
2030             0.00
```

Below the impact of this change on a few variables are expressed graphically and in a table.

The first variable ```PAKNYGDPMKTPKN``` is Pakistan's real GDP, the second ```PAKNECONPRVTKN``` is real consumption, the third is REAL IMPORTS OF GOODS AND SERVICES (`PAKNEIMPGNFSKN`) and the final is the level of the Consumer price deflator ```PAKNECONPRVTXN```.

The modifier `.difpctlevel` instructs ModelFlow to calculate the difference in the selected variables and express them as a percent of the original level.

$$
= \frac{x_{new}-x_{original}}{x_{original}} * 100
$$

The modifier `rename()`will replace the variable **name** with the variable **description** in the graphs. 

```python
(mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN PAKNEIMPGNFSKN PAKNECONPRVTXN'].
 difpctlevel.rename().plot(title="Impact of temporary $25 hike in oil prices"));
```

```text
<Figure size 1000x400 with 4 Axes>
```

```python
with mpak.set_smpl(2020,2035):
    print(mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN PAKNEIMPGNFSKN PAKNECONPRVTXN'].difpctlevel.df)
```

```text
      PAKNYGDPMKTPKN  PAKNECONPRVTKN  PAKNEIMPGNFSKN  PAKNECONPRVTXN
2020            0.00            0.00            0.00            0.00
2021            0.00            0.00            0.00            0.00
2022            0.00            0.00            0.00            0.00
2023            0.00            0.00            0.00            0.00
2024            0.00            0.00            0.00            0.00
2025           -0.89           -1.32           -1.49            1.64
2026           -0.85           -1.48           -2.65            1.35
2027           -0.64           -1.37           -3.19            1.08
2028            0.34           -0.08           -2.17           -0.51
2029            0.50            0.20           -1.25           -0.43
2030            0.45            0.19           -0.80           -0.31
2031            0.33            0.11           -0.57           -0.22
2032            0.20            0.02           -0.46           -0.15
2033            0.10           -0.04           -0.39           -0.12
2034            0.04           -0.07           -0.33           -0.10
2035            0.00           -0.07           -0.28           -0.09
```

The graphs show the change in the level as a percent of the previous level. They suggest that a temporary $25 oil price hike would reduce GDP in the first year by about 0.9 percent, but that the impact would diminish by the third year to -.64 percent, and then turn positive in the fourth year when the temporary price hike was no longer in effect. By the end of the simulation period the net effect on GDP would be zero.

The impacts on household consumption are stronger but follow a similar pattern.  

The GDP impact is smaller partly because the decline in domestic demand (due to reduced real incomes from high oil prices) reduces imports.  Because imports enter into the GDP identity with a negative sign, a reduction in imports actually increase aggregate GDP -- or in this case partially offsets the declines coming from reduced consumption (and investment - which is not shown above).

Finally as could be expected, initially prices rise sharply with higher oil prices. However, as the slowdown in growth is felt, inflationary pressures turn negative and the overall impact on the price level declines. When the oil price hike is eliminated, the overall impact on prices turns negative, and is still slowly returning to zero by the end of the simulation period.   

Note: The graph and table above shows what is happening to the **price level**. To see the impact on inflation (the rate of growth of prices), a separate graph can be generated using ```difpct```, which shows the change in the rate of growth of variables where the growth rate is expressed as a per cent $\bigg[\bigg(\frac{x^{shock}_t}{x^{shock}_{t-1}}-1\bigg)$ $ - \bigg(\frac{x^{baseline}_t}{x^{baseline}_{t-1}}-1\bigg)\Bigg]*100$. 

```python
mpak['PAKNECONPRVTXN'].difpct.rename().plot(
    title="Change in inflation from a temporary $25 hike in oil prices",
                                                   colrow=1,ysize=4);
```

```text
<Figure size 1000x400 with 1 Axes>
```

    
This view, gives a more nuanced result.  The inflation rate increases initially by about 1.6 percentage points, but falls compared with the baseline during the 2026-2027 period as the influence of the slowdown in GDP more than offsets the continued inflationary impetus from the lagged increase in oil prices. In 2028, when oil prices drop back to their previous level, an additional dis-inflationary force is generated and a sharp drop in inflation as compared with the baseline ensues. Over time, the boost to demand from lower prices translates into an acceleration in growth and a return of inflation back to its trend rate.

### An exogenous shock to a Behavioral variable 

Behavioral equations can be de-activated by exogenizing them, either for the entire simulation period, or for a selected sub-period.  When exogenized, instead of the equation returning the value returned by its econometrially equation plus the add-factor, it returns the value placed in the variable $\_X_t$ (see the discussion in Chapter  Ten).

In the following scenario, consumption is exogenized for the entire simulation period. 

To motivate the simulation, it is assumed that a change in weather patterns has increased the number of sunny days by 10 percent. This increases households happiness and causes them to permanently increase their spending by 2.5% beginning in 2025.

Such a shock can be specified either manually or by using the`.fix()` method. Below the simpler `.fix()` method is used, but the equivalent manual steps performed by `.fix()` are also explained.

To exogenize `PAKNECONPRVTKN` for the entire simulation period, initially a new `DataFrame` `Cfixed` is created as a slightly modified version of  `mpak.basedf` using the `.fix()` command.

`Cfixed=mpak.fix(mpak.basedf,PAKNECONPRVTKN)`

This does two things, that could have been done manually.  First it sets the dummy variable `PAKNECONPRVTKN_D=1` for the entire simulation period. Recall the consumption equation like all behavioral equations of World Bank models implemented in `ModelFlow`is expressed in two parts.


$$ cons_t= (1-cons\_D)*\bigg[C'(X_t)\bigg] + cons\_D*cons\_X_t$$

When $cons\_D=1$ (as it does in this scenario) the first part of the equation $(1-cons\_D)*C'(X)$ evaluates to zero and consumption is equal to (1)* $cons\_X$.  If instead (which would be the normal case $cons\_D$ were set to zero, the equation would simplify to $ cons_t= C'(X_t) $ where $C'(X_t)$ is the estimated equation that determines the value of real consumption in the model conditioned on the value of other variables in the model (the $X_t$ of $C'(X_t)$ and the add factor $C\_A-t$.

The `.fix()` method also sets the variable ```PAKNECONPRVTKN_X``` in the ```Cfixed``` `DataFrame` equal to the value of ```PAKNECONPRVTKN``` in the ```basedf``` `DataFrame`. All the other variables are  just copies of their values in `.basedf`.

With `PAKNECONPRVTKN_D=1` throughout the simulation period, the normal behavioral equation is de-activated or exogenized and consumption will just equal its exogenized value: $PAKNECONPRVTKN=PAKNECONPRVTKN\_X$.

```python
# reset the active sample period to the full model.
mpak.smpl() 
#Create a new df equal to the initial one (bline initialized when we loaded the model) 
# but set real consumption exogenous
Cfixed=mpak.fix(bline,'PAKNECONPRVTKN')
```

```text
The folowing variables are fixed
PAKNECONPRVTKN
```

The fix command above effectively does in one line each of the following lines of code.
```
bline_real=bline.copy() #make a copy of the baseline dataframe

#Create the _X variables if we exogenize the equation
baseline_real = baseline_real.mfcalc('''
PAKNECONPRVTKN_X = PAKNEPRVTKN
''')

#create the _D variable so we can exogenize the equation (set _D=1)-- currently it is exogenized 
baseline_real = baseline_real.upd('''
<-0 -1> 
PAKNECONPRVTKN_D = 1
''')
```

#### Preparing the shock
For the moment, the equation is exogenized but the values have been set to the same values as the ```.basedf``` `DataFrame` (bline and basedf have the same values on load), so solving the model will not change anything.

The `.upd()` method can now be used to implement the assumption that real consumption (`PAKNECONPRVTKN`) would be 2.5% stronger.  Because the equation has been turned off, it is the $\_X$ version of the variable that is increased by 2.5 percent.

```python
# Bump the _X version of the variable by 2.5% between 2025 and 2040
Cfixed=Cfixed.upd("<2025 2040> PAKNECONPRVTKN_X  * 1.025")
```

#### Performing the simulation
To perform the simulation, the revised `CFixed` DataFrame is input to the `mpak` model solve routine, and the model is solved over the period 2020 through 2040.

`CFixedRes = mpak(Cfixed,2020,2040,keep='2.5% increase in C 2025-40 (fix)')`

```python
# simulates the model for the period 2020 2040 and gives the name '2.5% increase in C 2025-40 to the simulation
CFixedRes = mpak(Cfixed,2020,2040,keep='2.5% increase in C 2025-40')
```

The results can be examined graphically as before.

```python
#plots the percent difference (*100) between the lastdf and basedf versions of the specified variables
(mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN PAKNEIMPGNFSKN PAKNECONPRVTXN'].
 difpctlevel.rename().plot(title="Impact of a permanent 2.5% increase in Consumption"));
```

```text
<Figure size 1000x400 with 4 Axes>
```

Below results are displayed in tabular form.  Note the use of the pandas options with the `with` clause.  This sets the display format of floating point variables to one decimal points.  The second `with` clause temporarily restricts the display to the period 2020 to 2040.

```python
with pd.option_context('display.float_format', '{:,.1f}%'.format):
    with mpak.set_smpl(2020,2040):
        print(mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN PAKNEIMPGNFSKN'].
              difpctlevel.rename().df)
```

```text
      Real GDP  HH. Cons Real  Imports real
2020      0.0%           0.0%          0.0%
2021      0.0%           0.0%          0.0%
2022      0.0%           0.0%          0.0%
2023      0.0%           0.0%          0.0%
2024      0.0%           0.0%          0.0%
2025      2.0%           2.5%          2.3%
2026      2.1%           2.5%          2.4%
2027      2.1%           2.5%          2.6%
2028      2.0%           2.5%          2.8%
2029      1.9%           2.5%          3.0%
2030      1.8%           2.5%          3.2%
2031      1.7%           2.5%          3.5%
2032      1.6%           2.5%          3.7%
2033      1.5%           2.5%          3.9%
2034      1.4%           2.5%          4.2%
2035      1.3%           2.5%          4.4%
2036      1.2%           2.5%          4.6%
2037      1.1%           2.5%          4.8%
2038      1.1%           2.5%          5.0%
2039      1.0%           2.5%          5.2%
2040      0.9%           2.5%          5.3%
```

The permanent rise in consumption by 2.5 percent causes a temporary increase in GDP of about 2% . Higher imports tend to diminish the effect on GDP. Over time higher prices due to the inflationary pressures caused by the additional demand cause the GDP impact to diminish to less than 1 percent by 2040. 

### Exogenize a behavioral variable and temporarily shock it

The third method of formulating a scenario involves exogenizing an endogenous variable and shocking its value for a defined period of time. The methodology is the same except the period for which the variable is exogenized is different. 

Here the set up is basically the same as before.

```python
#reset the active sample period to the full period
mpak.smpl(2020,2040)                                  
# create a copy of the bline DataFrame, but setting the PAKNECONPRVTKN_D variable to 1 for the period 2025 through 2027
CTempExogAll=mpak.fix(bline,'PAKNECONPRVTKN')
```

```text
The folowing variables are fixed
PAKNECONPRVTKN
```

The above `.fix()` command exogenizes the variable `PAKNECONPRVTKN` real consumer consumption.  The `.upd()` method in the following line increases the exogenized value of the consumption variable `PAKNECONPRVTKN_X` by 1.25 percent for three years only, 2025, 2026 and 2027.

```python
# multiply the exogenized value of consumption by 2.5% for 2025 through 2027
CTempExogAll=CTempExogAll.upd("<2025 2027> PAKNECONPRVTKN_X * 1.025")
```

Finally the model is solved and selected  results displayed as shock-control in percent from the baseline (pre-shock values of the displayed variables).

```python
#Solve the model
CTempXAllRes = mpak(CTempExogAll,2020,2040,keep='2.5% increase in C 2025-27 -- exog whole period') # simulates the model 
(mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN PAKNEIMPGNFSKN PAKNECONPRVTXN'].difpctlevel.
 rename().plot(title="Temporary hike in Consumption 2025-2027"));
```

```text
<Figure size 1000x400 with 4 Axes>
```

The results are quite different in this scenario.  GDP is boosted initially as before but when consumption drops back to its pre-shock level in 2028, GDP and imports decline sharply.

Prices (and inflation) are higher initially but when the economy starts to slow after 2025 prices actually fall (deflation). Although prices are falling, the level of prices remains higher at the end of the simulation than it was in the baseline.

#### Temporary shock exogenized for the whole period (with KG Option)

This scenario is the same as the previous, but this time the `--KG` (keep_growth) option is used to maintain the pre-shock growth rates of consumption in the post-shock period.  Effectively this is the same as a permanent increase in the level of consumption by 2.5% because the final shocked value of consumption (which was 2.5% higher then its pre-shock level) is grown at the same pre-shock rate -- ensuring that post-shock the level of consumption remains 2.5% higher in the baseline scenario.

```python
mpak.smpl() # reset the active sample period to the full model.
CTempExogAllKG=mpak.fix(bline,'PAKNECONPRVTKN')
CTempExogAllKG = CTempExogAllKG.upd('''
<2025 2027> PAKNECONPRVTKN_X * 1.025 --kg
''',lprint=0)

#Now we solve the model

CTempXAllResKG = mpak(CTempExogAllKG,2020,2040,keep='2.5% increase in C 2025-27 -- exog whole period --KG=True') # simulates the model 
(mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN PAKNEIMPGNFSKN PAKNECONPRVTXN'].difpctlevel.
 rename().plot(title="2.5% boost to cons 2025-27 --kg=True"));
```

```text
The folowing variables are fixed
PAKNECONPRVTKN
```

```text
<Figure size 1000x400 with 4 Axes>
```

### Exogenize the variable only for the period during which it is shocked

This scenario introduces a subtle but import difference.  Here the variable is again exogenized using the fix syntax. **But this time it is exogenized only for the period where the variable is shocked.**

This means that the consumption equation will only be de-activated for  three years (instead of the whole period as in the previous examples).  As a result, the values that consumption takes in 2028, 2029, ... 2040 depend on the model, not the level it was set to when exogenized (which was the case in the previous scenario).

Looking at the maths of the model the consumption equation is effectively split into three.

1. for the period before 2025 $cons\_D=0$ and the consumption equation simplifies to:<br/>
    $cons=C(X)$
2. for the period 2025-2028 it is exogenized ($cons_D=1$) so it simplifies to:<br>
    $cons=cons\_X$
3. but in the final period 2028-2040 ($cons\_D=0$) and the equation reverts to:
    $cons=C(X)$

```python
# reset the active sample period to the full model.
mpak.smpl() 

#Consumption is exogenized only for three years 2025 2026 and 2027 
#     PAKNECONPRVTKN_D=1 for 2025,2026, 2027 0 elsewhere.
# NB the 2025,2027 sets the period over which the change is made not specific dates
# -- i.e. 2025, 2026 and 2027 anot just 2025 and 2027
#In subsequent years (2028 onwards) the level of consumption will be determined by the equation 
CExogTemp=mpak.fix(bline,'PAKNECONPRVTKN',2025,2027)

#Now increase Consumption by 2.5% over the period 2025-2027
CExogTemp = CExogTemp.upd('<2025 2027> PAKNECONPRVTKN_X * 1.025',lprint=0)       

#Solve the model by passing it the revised DataFrame
CExogTempRes = mpak(CExogTemp,2020,2040,keep='2.5% increase in C 2025-27 -- temporarily exogenized') # simulates the model 


#display the impulse response functions of the specified variables
(mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN PAKNEIMPGNFSKN PAKNECONPRVTXN'].difpctlevel.
rename().plot(title="Temporary 2.5% boost to cons 2025-27 - equation active"));
```

```text
The folowing variables are fixed
PAKNECONPRVTKN
```

```text
<Figure size 1000x400 with 4 Axes>
```

These results have important differences compared with the previous.  The most obvious is visible in looking at the graph for Consumption.  Rather than reverting immediately to its earlier pre-shock level, it falls more gradually and actually overshoots (falls below its earlier level), before returning slowly to its pre-shock level.  That is because unlike in the previous shocks, its path after 2027 is being determined endogenously and reacting to changes elsewhere in the model, notably changes to prices, wages and government spending as well as the lagged level of consumption.

```python
print('Consumption base and shock levels\r\n');

print('\r\nReal values in 2030');
print(f'Base value:  {bline.loc[2028,"PAKNECONPRVTKN"]:,.0f}.\tShocked value: {CExogTempRes.loc[2028,"PAKNECONPRVTKN"]:,.0f}.\r\n'
    f'Percent difference: {round(100*((CExogTempRes.loc[2030,"PAKNECONPRVTKN"]-bline.loc[2028,"PAKNECONPRVTKN"])/bline.loc[2028,"PAKNECONPRVTKN"]),2)}')
print('\r\n\r\nReal values in 2040');
print(f'Base value:  {bline.loc[2040,"PAKNECONPRVTKN"]:,.0f}.\tShocked value: {CExogTempRes.loc[2040,"PAKNECONPRVTKN"]:,.0f}.\r\n'
    f'Percent difference: {round(100*((CExogTempRes.loc[2040,"PAKNECONPRVTKN"]-bline.loc[2040,"PAKNECONPRVTKN"])/bline.loc[2040,"PAKNECONPRVTKN"]),2)}')
```

```text
Consumption base and shock levels


Real values in 2030
Base value:  27,241,278.	Shocked value: 27,616,949.
Percent difference: 5.36


Real values in 2040
Base value:  38,692,815.	Shocked value: 38,693,167.
Percent difference: 0.0
```

### Simulation with Add factors

Add factors are a crucial element of the macromodels of the World Bank and serve multiple purposes.

In simulation, add-factors allow simulations to be conducted **without** de-activating behavioral equations.  Such shocks are often referred to as **endogenous** shocks because the equation of the behavioral variable that is shocked remains  active throughout.

In some ways they are very similar to a temporary exogenous shock. Both ways of producing the shock allow the shocked variable to respond endogenously in the period after the shock.  The main difference between the two approaches is in an endogenous shock (add-factor shock), the equation remains active throughout, including during the period the variable is being shocked. 

The intuition here for our previous consumption example might be that animal spirits cause households to increase consumption by 2.5 percent all things equal.  However, all things are not equal -- GDP is higher employment demand is higher which would boost consumption even more; but inflation is also higher which would reduce real incomes and supress consumption.  The net effect will balance these three (and other) factors out even in the shock period.





 * **Endogenous** shocks (Add-Factor shocks) allow the shocked variable to respond to changed circumstances that occur during the period of the shock.
     * This approach makes most sense for "animal spirits", shocks where the underlying behavior is expected to change.
     * It also makes sense when actions of one part of an aggregate is likely to impact behavior of other sectors within an aggregate.
         * Increased investment by a particular sector would be an example here as the associated increase in activity is likely to increase investment incentives in other sectors, while increased demand for savings will increase interest rates and the cost of capital operating in the opposite direction.  
         * The final simulation level of the shocked variable during the period of the shock will be equal to the original level plus the shock, plus whatever endogenous additional changes in the shocked variable arise because the conditioning variables (the $X_t$ in the equation) change.
     
     
 * **Exogenous** shocks to endogenous variables fix the level of the shocked variable during the shock period. 
     * Changes in government spending policy, something that is often largely an economically exogenous decision.
     * the final simulation level of the shocked variable during the period of the shock will be exactly equal to the original level plus the shock

#### Simulating the impact of a planned investment

The following simulation uses the add-factor to simulate the impact of a 3 year investment  program beginning in 2025 of 1 percent of GDP per year. This might reflect a specific large scale plant that is being constructed due to a deal reached by the government with a foreign manufacturer.  The add-factor approach is chosen because the additional investment is likely to increase demand for the products of other firms, which is likely to incite them to add to their investments as well -- both after the shock as in previous examples **but also during the period that investment is being shocked**.

##### How to translate the economic shock into a model shock

Add-factors in the ```MFMod``` framework are applied to the intercept of an equation (not the level of the dependent variable).  This preserves the estimated elasticities of the equation, but makes introduction of an add-factor shock somewhat more complicated than the exogenous approach.  Below a step-by-step how-to guide:

1. Identify numerical size of the shock
2. Examine the functional form of the equation, to determine the nature of the add factor.  If the equation is expressed as a:
    * **growth rate** then the add-factor will be an addition or subtraction to the growth rate
    * **percent of GDP (or some other level)** then the add-factor will be an addition or subtraction equal to the desired shock expressed as a percent of pre-shock GDP.
    * **Level** then the add-factor will be a direct addition to the level of the dependent variable
3. Convert the economic shock into the units of the add-factor
4. Shock the add-factor by the above amount and run the model


The add-factor is an exogenous variable in the model, so shocking it follows the well-established process for shocking an exogenous variable.

##### Determine the size of shock

Above the shock was identified as a 1 percent of GDP increase in private-sector investment.  A first step would be to determine the variable(s) that need to be shocked --- private investment. To do this we can query the variable dictionary, in this case by listing all variables where `invest` is part of the variable description.  


**Variable selection**<br>
More on how to use wildcards to select variables can be found at
{ref}`Variable selection with wildcharts <variable-selection>`

```python
mpak['!*invest*'].des
```

```text
PAKNEGDIFGOVKN        : Pub investment real
PAKNEGDIFPRVKN        : Prvt. Investment real
PAKNEGDIFPRVKN_A      : Add factor:Prvt. Investment real
PAKNEGDIFPRVKN_D      : Fix dummy:Prvt. Investment real
PAKNEGDIFPRVKN_FITTED : Fitted  value:Prvt. Investment real
PAKNEGDIFPRVKN_X      : Fix value:Prvt. Investment real
PAKNEGDIFTOTKN        : Investment real
```

Querying for all variables that "invest" in their descriptor gives us the mnemonic for the private investment variable `PAKNEGDIFPRVKN`.

##### Identify the functional form(s)

To understand how to shock using the add factor, it is essential to understand how the add-factor enters into the equation. 

|Addfactor is on the intercept of|Shock needs to be calculated as|
|:--|:--|
|a growth equation|a change in the growth rate|
|Share of GDP|a percent of GDP |
|Level| as change in the level|

Use the .eviews command command to identify the functional forms of the equation to be shocked.

```python

mpak['PAKNEGDIFPRVKN'].eviews
```

```text
PAKNEGDIFPRVKN : 
(PAKNEGDIFPRVKN/PAKNEGDIKSTKKN( - 1)) = 0.00212272413966296 + 0.970234989019907*(PAKNEGDIFPRVKN( - 1)/PAKNEGDIKSTKKN( - 2)) + (1 - 0.970234989019907)*(DLOG(PAKNYGDPPOTLKN) + PAKDEPR) + 0.0525240494260597*DLOG(PAKNEKRTTOTLCN/PAKNYGDPFCSTXN)
```

In this case the equation is written as a share of the capital stock in the preceding period **PAKNEGDIKSTKKN(-1)**.

##### Calculate the size of the required add factor shock

The shock to be executed is 1.0 percent of GDP.

It is assumed that the money will be spent in one year on private investment.

The private investment equation is written as a share of the capital stock lagged one period.  Therefore, the add-factor needs to be shocked by adding 1 percent of GDP to private investment in 2028 divided by the capital stock in 2027.

```python
#Create a DataFrame AFShock that is equal tothe baseline
AFShock=bline

#Display the level of the AF
print("Pre shock levels")
AFShock.loc[2025:2030,['PAKNEGDIFPRVKN_A','PAKNEGDIFPRVKN','PAKNEGDIKSTKKN']]

#print(AFShock.loc[2025:2030,'PAKNEGDIFPRVKN']/AFShock.loc[2025:2030,'PAKNYGDPMKTPKN']*100)
```

```text
Pre shock levels
```

```text
PAKNEGDIFPRVKN_A  PAKNEGDIFPRVKN  PAKNEGDIKSTKKN
2025             -0.00      1602853.65     47303916.21
2026             -0.00      1581104.20     48148785.83
2027             -0.00      1569541.20     49009798.90
2028             -0.00      1569140.97     49898686.55
2029             -0.00      1580576.85     50826938.84
2030             -0.00      1604394.55     51805897.58
```

Below the mfcalc routine is used to set the addfactor variable equal to its previous value plus the equivalent of 1 percent of GDP when expressed as a percent of the previous period's level of capital stock.

```python
AFShock=AFShock.mfcalc("""
 <2028 2028> PAKNEGDIFPRVKN_A = PAKNEGDIFPRVKN_A +(.01*PAKNYGDPMKTPKN/PAKNEGDIKSTKKN(-1))
 """);

print("Shocked AF levels")
AFShock.loc[2025:2030,'PAKNEGDIFPRVKN_A']
```

```text
Shocked AF levels
```

```text
2025   -0.00
2026   -0.00
2027   -0.00
2028    0.01
2029   -0.00
2030   -0.00
Name: PAKNEGDIFPRVKN_A, dtype: float64
```

##### Run the shock

The shock is executed by submitting the revised dataframe to the model object, and solving the model over the period 2020 through 2040.

```python
# the simulation is done until 2050, for later use of the keept values
AFShockRes = mpak(AFShock,2020,2050,keep='1% of GDP increase in FDI and private investment (AF shock)')
mpak.smpl(2020,2035)
(mpak['PAKNYGDPMKTPKN PAKNEGDIFPRVKN PAKNECONPRVTKN PAKNEIMPGNFSKN PAKNEGDIFTOTKN PAKNECONPRVTXN'].
 difpctlevel.rename().plot(title="Add factor shock on private investment 1% of GDP"));
```

```text
<Figure size 1000x600 with 6 Axes>
```

The above graphs are expressed as a percent of the baseline value of each value.  Because private investment in the baseline is only 5 percent of GDP,  the  1% of GDP shock, expressed as a percent of private investment is much larger (about 20 times larger).  

Below to double-check the calculations, two variables `IFPRVOLD_ORIG` and `IFTOT_ORIG` are created that reflect **pre-shock** private and total investment as a share of **pre-shock** GDP. Two additional variables `IFPRV_SHOCK` and `IFTOT_SHOCK` are also created as the shocked values of private and total investment as a percent of the original GDP.  The difference between the two sets of variables is the increase in fixed private and fixed total investment as a percent of the same denominator (the original level of GDP).

The ex-post change in private investment and of total investment in 2028  is 1.06 and 1.11 percent respectively, 0.6 and 1.1 percentage points larger than the actual shock 1 percent of GDP shock to the addfactor.

This difference represents the endogenous reaction of other investors in the same time period to the changed circumstances. It is precisely to capture this effect that an endogenous or add-factor shock is employed.

latexcommand \begin{samepage}

```python
AFShockRes['GDPOLD']=bline['PAKNYGDPMKTPKN']
AFShockRes['IFPRVOLD']=bline['PAKNEGDIFPRVKN']
AFShockRes['IFTOTOLD']=bline['PAKNEGDIFTOTKN']
AFShockRes=AFShockRes.mfcalc('''
                       IFPRV_SHOCK = PAKNEGDIFPRVKN / GDPOLD*100
                       IFTOT_SHOCK = PAKNEGDIFTOTKN / GDPOLD*100
                       IFPRV_Orig = IFPRVOLD / GDPOLD*100
                       IFTOT_Orig = IFTOTOLD / GDPOLD*100
                       IFPRV_IMPACT = IFPRV_SHOCK - IFPRV_Orig
                       IFTOT_IMPACT = IFTOT_SHOCK - IFTOT_Orig

                       ''')

print(round(AFShockRes.loc[2025:2030,['IFPRV_ORIG','IFPRV_SHOCK',
                                      'IFTOT_ORIG','IFTOT_SHOCK', 
                                      'IFPRV_IMPACT', 'IFTOT_IMPACT']],2))
```

```text
      IFPRV_ORIG  IFPRV_SHOCK  IFTOT_ORIG  IFTOT_SHOCK  IFPRV_IMPACT  IFTOT_IMPACT
2025        5.73         5.73       11.31        11.31          0.00          0.00
2026        5.52         5.52       11.21        11.21          0.00          0.00
2027        5.34         5.34       11.12        11.12          0.00          0.00
2028        5.19         6.25       11.05        12.16          1.06          1.11
2029        5.08         6.19       11.01        12.17          1.10          1.16
2030        5.01         6.13       10.99        12.16          1.12          1.17
```

latexcommand \end{samepage}

## The results visualization widget view

When working in Jupyter Notebook, referencing a selection of series will cause a data visualization widget to be generated that allows you to look at results (`basesdf` vs `latestdf`) for the selected variables as tables or charts, as levels, as growth rates and as percent differences from baseline.

```python
display(mpak['PAKNYGDPMKTPCN PAKNYGDPMKTPKN PAKGGEXPTOTLCN PAKGGREVTOTLCN PAKNECONGOVTKN'])
```

```text
Tab(children=(Tab(children=(HTML(value='<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE svg …
```

    :alt: Scenario analyzes 
    :class: bg-primary mb-1
    :width: 100%
    :align: center

## Save simulation results to a pcim file for later exploration

The next chapter explores the different results generated during these simulations.  Rather than re-run them, the model object `mpak` (and the simulation results that are stored by the keep command used above) are saved to a local file for retrieval in the next chapter. 

NB: The `keep=True` instructs `ModelFlow` to save the results from any kept solutions as well.

```python
help(mpak.modeldump)
```

```text
Help on method modeldump in module model_parquet_mixin:

modeldump(file_path='', keep=False, large=False, compact=False, **kwargs) method of modelclass.model instance
    Dump model to disk.

    Parameters
    ----------
    file_path : str
        Destination path.
    keep : bool
        If True, also persist ``self.keep_solutions``.
    large : bool
        If False (default), use the original JSON/gzip ``.pcim`` format.
        If True, use the fast Feather/zip ``.pcimz`` format —
        recommended for large CGE models with many variables.
    compact : bool
        If True (only effective when large=True), store float64
        columns as float32 to roughly halve file size.
        On load the data is restored to float64.
```

```python
mpak.modeldump(r'../models/mpakw.pcim',keep=True)
```

```python
mpak.keep_solutions.keys()
```

```text
dict_keys(['Baseline', '$25 increase in oil prices 2025-27', '2.5% increase in C 2025-40', '2.5% increase in C 2025-27 -- exog whole period', '2.5% increase in C 2025-27 -- exog whole period --KG=True', '2.5% increase in C 2025-27 -- temporarily exogenized', '1% of GDP increase in FDI and private investment (AF shock)'])
```

# More complex scenarios 

The preceding chapter introduced four different ways of preparing a solution and the forms the backbone of running simulations on World Bank models in `ModelFlow`. This chapter builds on those examples and delves into some of the challenges involved in translating a real-world policy problem into the model-world and then back again.


The particular scenario to be examined is the introduction of a Carbon Tax. The model used, and the example presented are both taken from the model of Pakistan presented in {cite:author}`burns_climate_2021`(2021).

:class: tip

This chapter presents some more complex scenarios, and illustrates how to develop a script that introduces changes to the model. 

A complex scenario is developed as deficiencies in initial scenarios are unearthed.  Scenarios presented include:

1) The introduction of a simple carbon tax (a simple shock of an exogenous variable) three exogenous variables in this case.  
2) Upon examining results, it is recognized that the initial nominal shocks loses impact over time because of inflation. Therefore, the shock is re-estimated as an ex-ante real shock (i.e. the initial shock is up-scaled over time in line with inflation to keep its real value constant). 
3) This example is judged imperfect because it does not account for the in-scenario inflation impacts. In a third scenario, the model equations are adjusted so that the ex-post inflation rate is used to maintain the real-value of the Carbon tax. 

The chapter also illustrates how to modify the description of variables in a scenario, and illustrates various techniques for visualizing scenario results. 

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

```python
# Prepare the notebook for use of ModelFlow 

# Jupyter magic command to improve the display of charts in the Notebook
%matplotlib inline

# Import pandas 
import pandas as pd

# Import the model class from the modelclass module 
from modelclass import model 

# functions that improve rendering of ModelFlow outputs
model.widescreen()
model.scroll_off();
```

## Load a pre-existing model, data and descriptions 

After initializing a `ModelFlow` pandas session in the usual way,  the Pakistan model, which is comprised of the model object, its estimated equations and the data is loaded.  The `pcim` file was created by the World Bank from a slightly modified version of the original EViews model used in the paper ({cite:author}`burns_climate_2021`,2021).  

```python
mpak,bline = model.modelload('../models/pak.pcim',alfa=0.7,run=1,keep="Baseline")
```

```text
Zipped file read:  ..\models\pak.pcim
```

## The policy problem

The model object ```mpak``` loaded above contains the model instance, the variables, equations and the data for the model.  On load, the model was solved, and the results of that initial solve was assigned to the `DataFrame` ```bline```. 

The Pakistan model contains three carbon tax variables: 

|Mnemonic | Meaning |
|:--|:--|
|PAKGGREVCO2CER|The effective carbon tax rate on Coal|
|PAKGGREVCO2GER|The effective carbon tax rate on Gas|
|PAKGGREVCO2OER|The effective carbon tax rate on Crude Oil|

As discussed in earlier chapters the meaning of the mnemonics can be retrieved from the model object `mpak`using the `.des` method and a wild-card search.

```python
mpak['PAKGGREVCO2*ER'].des
```

```text
PAKGGREVCO2CER : Carbon tax on coal (USD/t)
PAKGGREVCO2GER : Carbon tax on gas (USD/t)
PAKGGREVCO2OER : Carbon tax on oil (USD/t)
```

Alternatively, one can search on the variable descriptions to retrieve the mnemonics of variables. Below, the exclamation mark (!) at the beginning of the string notifies the matching algorithm to search the variables' descriptions (not the mnemonics) and return all variables that match.

```python
mpak['!*Carbon*'].des
```

```text
PAKCCEMISCO2TKN : Total Carbon emissions (tons)
PAKGGREVCO2CER  : Carbon tax on coal (USD/t)
PAKGGREVCO2GER  : Carbon tax on gas (USD/t)
PAKGGREVCO2OER  : Carbon tax on oil (USD/t)
```

Technqiues to query the model object for the meaning of mnemonics or the mnemonics associated with economic concepts are discussed in more detail here: [^selection].

[^selection]: Techniques to identify mnemics that correspond to economic ideas are explored here: {ref}`Variable selection with wildcharts <variable-selection>`   

## Add variable descriptions
A `ModelFlow` model imported from `EViews` will inherit the variable descriptors coming from `Eviews`.  The variable descriptors are stored in a dictionary named: `.var_description`. Not all EViews variables will necessarily have a description so additional definitions (descriptions) may need to be provided. 

Below we define a python dictionary in the same format as the dictionary var_description that is contained in the model object `mpak`.  Each dictionary entry is comprised of a key (the variables mnemonic) and a value (the description of the variable).

latexcommand \begin{samepage}

```python
extra_description = {'PAKNYGDPMKTPKN': 'GDP',
'EMISCOAL'        : 'Coal emissions',
'EMISGAS'         : 'Gas Emissions',
'EMISOIL'         : 'Gas Emissions',
'PAKCCEMISCO2CKN' : 'Coal emissions, tCO2e',
'PAKCCEMISCO2GKN' : 'Natural Gas emissions, tCO2e',
'PAKCCEMISCO2OKN' : 'Crude Oil emissions, tCO2e',
'PAKCCEMISCO2TKN' : 'Total emissions, tCO2e',
'PAKGGREVEMISCN'  : 'Revenue from emissions taxes',
 'PAKLMUNRTOTLCN': 'Unemployment rate',
 'PAKGGDBTTOTLCN_': 'Debt (%GDP)',
 'PAKGGREVTOTLCN': 'Fiscal revenues',
 'PAKWDL': 'Working days lost due to pollution'}
```

latexcommand \end{samepage}

These new definitions can be merged with the existing description by using the | operator. 

The command 
 > mpak.var_description = mpak.var_description | extra_description

Sets  `mpak.var_description` to a merge between the contents of the dictionary: `mpak.var_description` (its current content) and the dictionary: `extra_description`

Following execution, the `.var_desciption` will be changed to contain both its old values and those added in the extra_description dictionary defined above.

```python
mpak.var_description = mpak.var_description | extra_description
```

Several `ModelFlow` methods take advantage of this dictionary to provide more reader-friendly descriptions of variables -- typically through the `rename` option. For those methods that define it, if rename is set to True, the method will substitute the description for the variable name in any outputs.  

Variables with descriptions can also be selected for by using the `mpak['!*subtext*']` syntax, where subtext is some text that appears in the variable descriptor.

## Simulating the impact of imposing a carbon price

To run a simulation, the following steps must invariably be followed.

1. Create a new DataFrame, typically a copy of an existing one.
2. Change the value  in the new df of the variable(s) to be shocked.
3. Solve the model using the newly altered df as the input df.

```python
# Create copy of the bline df
alternative_df = bline.copy()
#set the effective carbon tax of all three carbon tax variables equal to 30 USD
alternative_df.loc[2025:2100,['PAKGGREVCO2CER','PAKGGREVCO2GER', 'PAKGGREVCO2OER']] = 30
```

The above used the `pandas` function `.loc[]` to change the Carbon Tax rate variables.

The `ModelFlow` method `.upd()` could be used to perform the same change. 

```python
# This ModelFlow command is equivalent to the previous standard pandas command abive that used the .loc[] syntax
CT30df  =  bline.upd("<2025 2100> PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER = 30")
```

### Solve the model

Solving the model is as simple as calling the mpak function with the altered `DataFrame` as an input and assigning the results to a new dataframe (`resultsdf` in this instance).  The `keep` option causes a copy of the dataframe to be stored within the `mpak` model object.

```python
resultsdf = mpak(CT30df,2020,2100,keep="Nominal $30USD Carbon tax") # simulates the model
```

This simulation is a shock on an exogenous variable (the first kind of shock discussed in the previous chapter), although in this case the shock is applied to three exogenous variables simultaneously, whereas in earlier examples only one variable was shocked.

#### Examining the results

Every time the model is solved the results of the simulation are assigned to a variable on the left hand side of the solve call (`resultdf` in the example above).  The results of the most recent scenario are also always stored in the `.lastdf` `DataFrame` that is one of the properties of any `ModelFlow` model object (`mpak` in this case). `basedf` is also a property of `mpak` and contains a copy of the initial DataFrame from which the model was built.

The `bline`,  `.basedf` and the original `.lastdf` `Dataframes` were created when the model was initially loaded and solved. The `resultsdf` database and a revised `.lastdf` were generated when the  model was solved for the new carbon prices.


The standard `dataframes` are part of the `ModelFlow` object and managed by it.

- **mpak.basedf**: `Dataframe` with the values for baseline
- **mpak.lastdf**: `Dataframe` with the values from the most recent simulation

The command below shows the results of the simulation on the four emissions variables in the model expressed as a percent deviation from the level of the baseline (the `.difpctlevel` operator below),  and where the mnemonics have been replaced by their descriptions using the `.rename` option.

latexcommand \begin{samepage}

```python
with mpak.set_smpl(2023,2030):
    print(mpak['PAKCCEMISCO2*'].difpctlevel.rename().df);
```

```text
      Coal emissions, tCO2e  Natural Gas emissions, tCO2e  \
2023                   0.00                          0.00   
2024                   0.00                          0.00   
2025                 -41.19                        -26.99   
2026                 -40.06                        -25.72   
2027                 -38.85                        -24.48   
2028                 -37.59                        -23.30   
2029                 -36.26                        -22.14   
2030                 -34.89                        -21.01   

      Crude Oil emissions, tCO2e  Total emissions, tCO2e  
2023                        0.00                    0.00  
2024                        0.00                    0.00  
2025                      -10.93                  -22.17  
2026                      -10.98                  -21.56  
2027                      -10.89                  -20.89  
2028                      -10.68                  -20.17  
2029                      -10.35                  -19.38  
2030                       -9.95                  -18.55
```

latexcommand \end{samepage}

The impact of the imposition of the carbon tax in the model is relatively quick, resulting in an overall decline in emissions of 22.2% in the first year, with coal emissions (coal is a relatively carbon intensive source of energy so harder hit by the carbon tax) recording the biggest hit at -41.2 percent.

```python
mpak['PAKCCEMISCO2?KN'].difpctlevel.rename().plot(title="Emissions impact of a $30 USD Carbon tax");
```

```text
<Figure size 1000x400 with 4 Axes>
```

Abstracting from the fact that the impact is occurring too quickly (it would take time for the substitution towards alternative sources of power to occur), the fact that impacts are fading with time suggests an error in the specification of the shock. 

Indeed, high domestic inflation means that the real price change of the $30 nominal increase in the Carbon price is declining over time -- suggesting that the scenario needs tweaking.

## Re-thinking the shock as an ex-ante real shock

Inflation in Pakistan is relatively high so a $30 shock quickly loses its relative price effect. Increasing the nominal value of the Carbon Tax by the amount of domestic inflation (converted into USD each year) would resolve the problem. 

Below a new `DataFrame` is created as a copy of the baseline and the three Carbon taxes are first set to $30 in 2025 and then grown at the rate of domestic inflation to keep the **ex ante** relative price of the Carbon Tax constant.

Finally the model is re-solved.

```python

CT30realdf  =  bline.copy()
CT30realdf=CT30realdf.upd("<2025 2025> PAKGGREVCO2CER PAKGGREVCO2OER PAKGGREVCO2GER = 30")

#NB: Variables used 
#   PAKNECONPRVTXN is the consumer price deflator
#   PAKPANUSATLS id the USD exchange rate
CT30realdf=CT30realdf.mfcalc('''
                              <2026 2100> PAKGGREVCO2CER = PAKGGREVCO2CER(-1)*(PAKNECONPRVTXN*PAKPANUSATLS)/(PAKNECONPRVTXN(-1)*PAKPANUSATLS(-1))
                                      PAKGGREVCO2OER = PAKGGREVCO2OER(-1)*(PAKNECONPRVTXN*PAKPANUSATLS)/(PAKNECONPRVTXN(-1)*PAKPANUSATLS(-1))
                                      PAKGGREVCO2GER = PAKGGREVCO2CER(-1)*(PAKNECONPRVTXN*PAKPANUSATLS)/(PAKNECONPRVTXN(-1)*PAKPANUSATLS(-1))
                          ''')                         

CT30realdf.loc[2023:2030,'PAKGGREVCO2CER']


resultsdf = mpak(CT30realdf,2020,2100,keep="Ex ante Real $30USD Carbon tax") # simulates the model
```

The above code first sets the Carbon prices to 30USD and then  grows them at the same rate as inflation.  Below we see that with inflation of 30% per annum the domestic carbon price is rising rapidly.

```python
with mpak.set_smpl(2023,2030):
    print(mpak['PAKGG*ER'].rename().df)
```

```text
      Carbon tax on coal (USD/t)  Carbon tax on gas (USD/t)  \
2023                       -5.55                     -41.00   
2024                       -5.55                     -41.00   
2025                       30.00                      30.00   
2026                       31.83                      31.83   
2027                       33.64                      33.64   
2028                       35.45                      35.45   
2029                       37.26                      37.26   
2030                       39.09                      39.09   

      Carbon tax on oil (USD/t)  
2023                      -8.71  
2024                      -8.71  
2025                      30.00  
2026                      31.83  
2027                      33.64  
2028                      35.45  
2029                      37.26  
2030                      39.09
```

```python

mpak['PAKCCEMISCO2?KN'].difpctlevel.rename().plot(title="Emissions impact of a $30 USD Carbon tax");
```

```text
<Figure size 1000x400 with 4 Axes>
```

These results are better, but still there is an erosion of the effect of the tax.


On introspection, this is likely due to the fact that the carbon tax itself is inflationary.  As a result, prices probably rose to a higher level than supposed by the ex ante calculation.

To deal with this, a different approach is needed.  Rather than maintaining the carbon price as an exogenous variable, instead it should be made an endogenous variable by changing the model and adding equations for all of the carbon tax variables.

Before doing so lets save the current version of the model for further work later.

```python
mpak.modeldump('../models/pakCarbonTaxScenarios.pcim')
```

## Changing the model -- modifying and or adding equations

To endogenize the carbon price, an equation for each carbon price has to be added to the model.   This can be done with the `.equpdate()` method.  

```python
#Reload original model and data
mpak1,bline = model.modelload('../models/pak.pcim',alfa=0.7,run=1,keep="Baseline")


#Create a new model object mpakreal and new baseline dataframe-- baselinereal 
#The nominal carbon taxes (expressed in USD) are now endogenous 
#and increase with domestic inflation and the exchange rate

mpakreal,blinereal = mpak1.equpdate('''
<fixable> PAKGGREVCO2CER = PAKGGREVCO2CER(-1) * (PAKNYGDPMKTPXN*PAKPANUSATLS) / (PAKNYGDPMKTPXN(-1)*PAKPANUSATLS(-1))
<fixable> PAKGGREVCO2OER = PAKGGREVCO2OER(-1) * (PAKNYGDPMKTPXN*PAKPANUSATLS) / (PAKNYGDPMKTPXN(-1)*PAKPANUSATLS(-1))
<fixable> PAKGGREVCO2GER = PAKGGREVCO2GER(-1) * (PAKNYGDPMKTPXN*PAKPANUSATLS) / (PAKNYGDPMKTPXN(-1)*PAKPANUSATLS(-1))
''',add_add_factor=False, calc_add=False,newname='Pak model, with real Carbon price equations')
```

```text
Zipped file read:  ..\models\pak.pcim

The model:"PAK" got new equations, new model name is:"Pak model, with real Carbon price equations"
New equation for For PAKGGREVCO2CER
Old frml   :new endogeneous variable 
New frml   :FRML <fixable> PAKGGREVCO2CER = (PAKGGREVCO2CER(-1)*(PAKNYGDPMKTPXN*PAKPANUSATLS)/(PAKNYGDPMKTPXN(-1)*PAKPANUSATLS(-1)))* (1-PAKGGREVCO2CER_D)+ PAKGGREVCO2CER_X*PAKGGREVCO2CER_D$
Adjust calc:No frml for adjustment calc  

New equation for For PAKGGREVCO2OER
Old frml   :new endogeneous variable 
New frml   :FRML <fixable> PAKGGREVCO2OER = (PAKGGREVCO2OER(-1)*(PAKNYGDPMKTPXN*PAKPANUSATLS)/(PAKNYGDPMKTPXN(-1)*PAKPANUSATLS(-1)))* (1-PAKGGREVCO2OER_D)+ PAKGGREVCO2OER_X*PAKGGREVCO2OER_D$
Adjust calc:No frml for adjustment calc  

New equation for For PAKGGREVCO2GER
Old frml   :new endogeneous variable 
New frml   :FRML <fixable> PAKGGREVCO2GER = (PAKGGREVCO2GER(-1)*(PAKNYGDPMKTPXN*PAKPANUSATLS)/(PAKNYGDPMKTPXN(-1)*PAKPANUSATLS(-1)))* (1-PAKGGREVCO2GER_D)+ PAKGGREVCO2GER_X*PAKGGREVCO2GER_D$
Adjust calc:No frml for adjustment calc
```

As written, the `.equpdate()` command creates a new model, which is a copy of the existing model with three new equations.

Each equation grows the nominal rate of the carbon tax at the same rate as *ex post* inflation (`PAKNECONPRVTXN`) converted into USD via the exchange rate `PAKPANUSATLS`. The equations are introduced as exogenizable equations (as distinct from an identity which must always hold) by adding the \<fixable\> prefix to each equation. The equations are not estimated, so no add-factors are included in the equations.

The output for the `.equpdate()` reports the actual formulae included in the model. 
```
New equation for For PAKGGREVCO2CER
Old frml   :new endogeneous variable 
New frml   :FRML <fixable> PAKGGREVCO2CER = (PAKGGREVCO2CER(-1)*(PAKNECONPRVTXN*PAKPANUSATLS)/(PAKNECONPRVTXN(-1)*PAKPANUSATLS(-1)))* (1-PAKGGREVCO2CER_D)+ PAKGGREVCO2CER_X*PAKGGREVCO2CER_D$
Adjust calc:No frml for adjustment calc 
```
Note that because the equations are to be fixable, an \_X and \_D variable are added to the specified equations. Combined they effectively split each equation into  two:
1. the specified equations when \_D equals zero
2. equal to \_X when the \_D equals one.

The newly created model is given the name mpakreal and is given a text description.

Following the addition of the equations, the new variables (\_D and \_X) must be initialized. The \_X variables are made equal to the current values of the various tax rates, while the \_D is set to 1 everywhere -- effectively turning the equation off and re-creating the same situation as the initial model where the tax rates are fully exogenous.

As with the `mpak` model the variable descriptions need to be updated. 

```python
mpakreal.var_description = mpakreal.var_description | extra_description
```

```python
#Exogenizes the newly added equations and sets the dummy =1 amd the _x to the current value of the dependent variable  
bline_real=mpakreal.fix(blinereal,'PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER')
```

```text
The folowing variables are fixed
PAKGGREVCO2CER
PAKGGREVCO2GER
PAKGGREVCO2OER
```

Finally the new model is solved, the result is kept in a new baseline and a quick check ensures that the model did indeed reproduce the data that it was originally fed, including the initial Carbon Tax levels.

```python

#Solve the model for the new baseline
res = mpakreal(bline_real,2021,2100,alfa=0.5,keep='Baseline - adjusted model') 

mpakreal['PAKNYGDPMKTPKN PAKNECONPRVTXN PAKGGBALOVRL PAKGGREVCO2CER PAKCCEMISCO2TKN'].difpctlevel.rename().df
```

```text
GDP  Implicit LCU defl., Pvt. Cons., 2000 = 1  \
2021 0.00                                      0.00   
2022 0.00                                      0.00   
2023 0.00                                      0.00   
2024 0.00                                      0.00   
2025 0.00                                      0.00   
...   ...                                       ...   
2096 0.00                                      0.00   
2097 0.00                                      0.00   
2098 0.00                                      0.00   
2099 0.00                                      0.00   
2100 0.00                                      0.00   

      Carbon tax on coal (USD/t)  Total emissions, tCO2e  
2021                       -0.00                    0.00  
2022                       -0.00                    0.00  
2023                       -0.00                    0.00  
2024                       -0.00                    0.00  
2025                       -0.00                    0.00  
...                          ...                     ...  
2096                       -0.00                    0.00  
2097                       -0.00                    0.00  
2098                       -0.00                    0.00  
2099                       -0.00                    0.00  
2100                       -0.00                    0.00  

[80 rows x 4 columns]
```

### Solving the revised model

With the new model generated, it can now be solved with the real tax rate endogenized in the forecast period.  This involves three steps.

1. Set the nominal tax rate to 30 in 2025
2. Now Endogenize the equation for the rest of the period
3. Solve the model.

```python
scenario_real_CTax = bline_real.upd('''
<2025 2025> 
PAKGGREVCO2CER_X PAKGGREVCO2GER_X PAKGGREVCO2OER_X = 30 # Sets the exogenous value to 30 in 2025
<2026 2100 > 
PAKGGREVCO2CER_D PAKGGREVCO2GER_D PAKGGREVCO2OER_D = 0   # Endogenizes the new equations for the rest of time so that the real-rate stays at 30USD
''')


_ = mpakreal(scenario_real_CTax,2021,2100,alfa=0.5,keep='Real model real tax = 30 at 2025 prices and exchange  rates')
```

Initially the Carbon tax comes in at 30 but gradually its rate in USD rises in line with inflation such that it reaches $1358 by 2100.  

```python

mpakreal['PAKGGREVCO2?ER PAKNECONPRVTXN PAKNYGDPMKTPXN '].rename().df
```

```text
Carbon tax on coal (USD/t)  Carbon tax on gas (USD/t)  \
2021                       -5.55                     -41.00   
2022                       -5.55                     -41.00   
2023                       -5.55                     -41.00   
2024                       -5.55                     -41.00   
2025                       30.00                      30.00   
...                          ...                        ...   
2096                     1098.50                    1098.50   
2097                     1158.34                    1158.34   
2098                     1221.44                    1221.44   
2099                     1287.97                    1287.97   
2100                     1358.11                    1358.11   

      Carbon tax on oil (USD/t)  Implicit LCU defl., Pvt. Cons., 2000 = 1  \
2021                      -8.71                                      1.82   
2022                      -8.71                                      1.98   
2023                      -8.71                                      2.14   
2024                      -8.71                                      2.30   
2025                      30.00                                      2.51   
...                         ...                                       ...   
2096                    1098.50                                    106.62   
2097                    1158.34                                    112.69   
2098                    1221.44                                    119.11   
2099                    1287.97                                    125.89   
2100                    1358.11                                    133.06   

      GDP, Marker Prices, LCU Price defl., 2000 = 1  
2021                                           1.95  
2022                                           2.14  
2023                                           2.32  
2024                                           2.50  
2025                                           2.72  
...                                             ...  
2096                                         112.39  
2097                                         118.75  
2098                                         125.47  
2099                                         132.58  
2100                                         140.08  

[80 rows x 5 columns]
```

This seemingly very high level is just a reflection of the 75 years of inflation that compounded require a much higher nominal Carbon tax rate to have the same relative price effect. The cumulative effect of inflation in the range of 5.5 real  per annum causes the price level to increase 74 times (7400 percent increase  133/1.8 from fourth data column in the above table).  

The table below shows the same data but in growth rate terms -- indicating that the nominal Carbon tax rate is gradually rising each year in line domestic inflation adjusted for the exchange rate -- i.e. it is constant in real terms.

```python
mpakreal['PAKGGREVCO2?ER PAKPANUSATLS PAKNYGDPMKTPXN'].pct.rename().df
```

```text
Carbon tax on coal (USD/t)  Carbon tax on gas (USD/t)  \
2021                        0.00                       0.00   
2022                        0.00                       0.00   
2023                        0.00                       0.00   
2024                        0.00                       0.00   
2025                     -640.56                    -173.17   
...                          ...                        ...   
2096                        5.45                       5.45   
2097                        5.45                       5.45   
2098                        5.45                       5.45   
2099                        5.45                       5.45   
2100                        5.45                       5.45   

      Carbon tax on oil (USD/t)  Exchange rate LCU / US$ - Pakistan  \
2021                       0.00                               -0.16   
2022                       0.00                               -0.16   
2023                       0.00                               -0.14   
2024                       0.00                               -0.12   
2025                    -444.41                               -0.30   
...                         ...                                 ...   
2096                       5.45                               -0.20   
2097                       5.45                               -0.20   
2098                       5.45                               -0.20   
2099                       5.45                               -0.20   
2100                       5.45                               -0.20   

      GDP, Marker Prices, LCU Price defl., 2000 = 1  
2021                                          10.69  
2022                                           9.76  
2023                                           8.71  
2024                                           7.76  
2025                                           8.90  
...                                             ...  
2096                                           5.66  
2097                                           5.66  
2098                                           5.66  
2099                                           5.66  
2100                                           5.66  

[80 rows x 5 columns]
```

### Results

The results from the simulation with the Carbon Tax rate endogenized so as to maintain its real value over time, are broadly consistent with the results from the ex ante real scenario performed above.

```python

mpakreal['PAKCCEMISCO2?KN'].difpctlevel.rename().df
```

```text
Coal emissions, tCO2e  Natural Gas emissions, tCO2e  \
2021                   0.00                          0.00   
2022                   0.00                          0.00   
2023                   0.00                          0.00   
2024                   0.00                          0.00   
2025                 -41.19                        -26.99   
...                     ...                           ...   
2096                 -24.23                        -10.33   
2097                 -24.09                        -10.25   
2098                 -23.95                        -10.18   
2099                 -23.81                        -10.11   
2100                 -23.67                        -10.04   

      Crude Oil emissions, tCO2e  Total emissions, tCO2e  
2021                        0.00                    0.00  
2022                        0.00                    0.00  
2023                        0.00                    0.00  
2024                        0.00                    0.00  
2025                      -10.93                  -22.17  
...                          ...                     ...  
2096                       -5.30                  -10.85  
2097                       -5.25                  -10.78  
2098                       -5.20                  -10.70  
2099                       -5.15                  -10.63  
2100                       -5.11                  -10.55  

[80 rows x 4 columns]
```

```python
(mpakreal['PAKCCEMISCO2?KN PAKNYGDPMKTPKN'].difpctlevel.
 rename().plot(title="Emissions impact of a constant real $30 USD Carbon tax"));
```

```text
<Figure size 1000x600 with 6 Axes>
```

The modified model, which preserves the real value of the carbon tax has a permanent and substantial negative effect on emissions. The impact is not at an unchanging level, reflecting in part adaptation within the economy. Of particular import is what is being done with the revenues from the Carbon tax. As the structure of GDP (shifts to less carbon intensive activities) carbon tax revenues fall even as the Carbon Tax rate rises. 

Note, the percent deviation of emissions tends to decrease over time in this scenario principally because the level of activity (GDP) is higher with the Carbon Tax than without it. As a result,  emissions are higher than they would have been had GDP remained unchanged. For the Pakistan model, the positive impact of the Carbon tax is mainly explained by co-benefits, notably reduced reliance on more distortionary taxes such as payroll taxes and because of reductions in informality and due to health and productivity benefits from lower pollution levels (see {cite:author}`burns_climate_2021`(2021) for more details how these effects operate in the Pakistan model).

# A simulation that targets a specific outcome

Normally, when working with a model, the trajectory of the exogenous variables determine the trajectory of the endogenous (left hand side) variables. However, sometimes it can be useful to reverse the causality in the model, to find a trajectory for some exogenous variables that will result in certain endogenous variables achieving specific values.  

A simple example might be where a policy maker wants to know what level of Carbon Tax, if implemented in a budget neutral fashion, would be needed to achieve a specific level of emissions.  As specified, the analytical question is to achieve two targets: 

 1. A specific $CO^2$ emissions trajectory 
 2. An unchanged fiscal deficit 

:class: tip

This chapter illustrates how to target specific outcomes using `ModelFlow`. In the example, a specific outcome for carbon emissions is introduced and instruments (carbon taxes) are specified for achieving the target.  

The chapter introduces a `ModelFlow` routine that searches for the values of the instruments (the carbon tax) that achieve the desired target level of carbon emissions (the target).

A second example illustrates a scenario with two targets (one a specific trajectory for emissions as above) and the second the stipulation that the policy be introduced in a budget neutral manner (a second target of an unchanged budget deficit) to be achieved by re-cycling Carbon tax revenues as transfers (a second instrument) to households.  

In addition to these examples, techniques for fine-tuning the process in instances where the default parametrization of the system fails to find a result are also presented.  

 
## Targeting in ModelFlow 
**Targeting** in `ModelFlow` requires that there be **at least as many instruments as there are targets**. So in the above example two instruments would be required. 

The instrument to achieve the emissions could be a Carbon tax (applied uniformly on emissions from coal, gas and crude oil).  The instrument to achieve an unchanged fiscal deficit, could be government spending or some form of revenue, say taxes on labor.

To illustrate targeting, the climate-aware model of Pakistan ({cite:t}`burns_climate_2021`) is used.


To run a targeting solution, the following main steps must be undertaken

1. Initialize a `ModelFlow` python session.
1. Load the model and data
2. Create a baseline 
3. Define instrument variables (one instrument can consist of several variables). 
4. Define a `dataframe` with the trajectory of the target variables.  
3. Solve the problem using the `.invert` method. 
4. Visualize the results 

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

```python
# Prepare the notebook for use of ModelFlow 

# Jupyter magic command to improve the display of charts in the Notebook
%matplotlib inline

# Import pandas 
import pandas as pd

# Import the model class from the modelclass module
```

```python
%matplotlib inline
```

```python
from modelclass import model 

# functions that improve rendering of ModelFlow outputs
model.widescreen()
model.scroll_off();
```

## Load a  model, data and descriptions 
Following the initialization of the python session, the model is loaded and a model object `mpak` declared. The file `pak.pcim` contains the model object for the Pakistan model described in Burns (2021), including all of the equations data and variables. 

```python
mpak,initial = model.modelload('../models/pak.pcim')
```

```text
Zipped file read:  ..\models\pak.pcim
```

```python
mpak.var_description = mpak.var_description | {
    'PAKCCEMISCO2TKN' : 'Pakistan Total Carbon emissions (tons)'

}
```

## Solve the model to create a baseline

Next the model is solved, using the initial dataframe that was generated on the modelload.  

In this instance, the model is solved from 2022 through 2100. The option `ljit=True` tells the model object to compile the model. Model compilation takes time, but once a model is compiled it will solve faster. When a model will be solved multiple times, the additional time required to compile the model, can be made up by the faster execution time each time the model is solved. Targeting requires the model to be solved many times, which makes the additional overhead of compilation worthwhile.

```python
baseline = mpak(initial,2022,2100,alfa=0.7,silent=1,ljit=True)
mpak.basedf = baseline.copy()
```

```text
Compile prolog: 100%|██████████| 1/1  1.92s/code chunk
Compile core  : 100%|██████████| 4/4  1.56s/code chunk
Compile epilog: 100%|██████████| 9/9  1.30s/code chunk
```

Python is an interpreted language, so solving can be improved by compiling the solving routines to machine code. The [Numba package](https://numba.pydata.org/) can help overcome this by translating Python code into machine code, significantly speeding up computation. The extent of this speed improvement depends on the complexity of the model and the computational resources required.

When solving a model, you can enable Numba compilation with by setting the option `ljit=True`
 
This setting cause the model to be compiled. The first time it is used for a model, the compilation will take some time. The compiled code is cached in the `modelsource` subfolder. As a result, subsequent runs of the model — even across different Python sessions — will use the precompiled model and solve much faster than the uncompiled versions.

**Note: If there are issues with the solution, error messages may not be visible when the model is compiled. To troubleshoot, set ljit to False and rerun the model.**

**If you recreate a model with different logic but retain the same model name, consider clearing the `modelsource` subfolder to remove any cached compiled code that could interfere with the new model version.**
 

## Target CO2 emission - a  very simple example

To illustrate the process for solving the model in targeting mode, an initial very simple example is set up, where **only  emissions** are targeted (one target), and the objective is to have emissions grow at an annual rate of 1 percent. 

### Define targets
Having loaded the model, created a baseline and designated the target (steps 1-3 from above), the next step is to create the target variable(s).  

This is done below by defining two series.  The first, `target_before_simple`, is set equal to the value of the total emissions variable `PAKCCEMISCO2TKN` in the baseline.  The second, `target_simple`, is the target for the same variable. 

For this example we assume policy makers are looking for a carbon price that will restrict emissions growth to 1 percent per annum. The `target_simple` variable is therefore set equal to `target_before_simple` through 2024 and then, using the `.upd()` method,  grown slowly at 1 percent per year afterwards.

```python
# Create dataframe with only the target variable (for memmory)
target_before_simple = baseline.loc[2024:2100,['PAKCCEMISCO2TKN']]  
target_simple = target_before_simple.upd(f'<2025 2100> PAKCCEMISCO2TKN =growth 1')
```

### Define instruments 

As noted above, for each target there must be one instrument. However, **one instrument** can consist of **several instrument variables** . Below the instrument is defined as three instrument variables: the carbon tax rate on each of Oil, Natural Gas and Coal. A list `instruments_simple` is created comprised of the mnemonics of each of the three variables.The three variables together are considered one instrument.

```python
instruments_simple = [['PAKGGREVCO2CER','PAKGGREVCO2GER', 'PAKGGREVCO2OER']]
```

### Finding the values for the instruments that achieve the desired target

To find the value for the instrument(s) that achieves the target of a 1 percent growth in emissions, the `ModelFlow` `.invert()` method is used: passing it the baseline database, the target `dataframe` that we defined above and the list of the instruments to use.

The `.invert()` method will solve the model once for each of the 77 years of the active sample period, and will solve multiple times for each year until it finds a set of instrument values that result in the desired targets. The dataframe containing the solution to the targeting problem is returned by the `.invert()` method and also stored in the `.lastdf` internal dataframe.  

#### Invert options

The `.invert()` method has many options.  The first three define the problem, the remainder influence how the solver operates.  Finding the right options for a given problem is not always straightforward.  The following table provides some hints on how to work with these options to optimize solution speed for a given problem.

\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}p{2.5cm}>{\raggedright\arraybackslash}p{3.5cm}>{\raggedright\arraybackslash}X}

|Option|Parameters |Explanation|
|:--|:--|:--|
|databank|name of dataframe|Dictates the initial conditions of the model (same as in a normal solve)|
|targets|list|A list of the variables to be targeted|
|instruments|list|A list of the variables that will be used as instruments to achieve the targets. Individual instruments may have multiple variables (as in the example above). Instrument list may contain Impulse parameters specific to the instrument (see below).|
|silent|bool|True: Suppress detailed outputs; False: Show detailed outputs (one line per iteration per year)|
|defaultimpuls|float|Determines the size of the change in instruments as the model searches for answers. Choose a value relative to the size of the actual series being modified.|
|defaultconv|float| Specifies the amount by which targeted variables may deviate from the target value and still be considered a solution.  Should reflect the size of the target.|
|delay|Integer|Causes the instrument value changed to be lagged N periods from the target period being solved; For WBG models this should almost always be 0|
|varimpulse|bool|True: Sets the initial change in the instrument for the future to the same as in the most recently solved period. This will greatly speed solves where instruments are expected to evolve smoothly.|
|nonlin|integer|N: Jacobian will be updated after N iterations without a solution; Most WBG models are near-linear so setting to 0 will solve faster.  If the solution fails, try non-linear=5|
|maxiter|integer|Maximum number of Newton iterations; If passed model will fail with a non-convergence error. If model does not converge try with nonlin=False|
|progressbar|boolean| default=False Determines whether or not a progress bar is displayed|


#### Multiple instruments for one target

As mentioned, while there must be at least one instrument for each target it is possible to have more than one variable in a given instrument.  Moreover, it is possible to assign specific impulse defaults to different instruments, or different weights for different variables in a multi-variable instrument.

Below are specific illustrations of how the instrument list can be specified. 


\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}p{4cm}>{\raggedright\arraybackslash}p{3.5cm}>{\raggedright\arraybackslash}X}

|Type|Instruments|Explanation|
|:--|:--|:--|
|Single Target; Single Instrument|\['myvar'\]|The instrument list includes only one variable, default impulse|
|3 Targets; 3 Instruments, each with 1 variable|\['myvar1', 'myvar2', 'Myvar3'\]|All variables get the default impulse|
|2 Targets; 2 Instruments; different impulse|\[('myvar1',0.7), ('myvar2',.2000) ]|The first instrument takes an impulse value of 0.7 (presumably because its values are relatively small). The second takes a much larger impulse value of 2000, reflecting its larger scale.|
|2 Targets; 2 variables for first instrument; 1 for second|\[['myvar1', 'myvar2'\], 'myvar3')]|The first instrument takes two variables: myvar1 and myvar2; the second instrument has just  one variable: myvar3|
|1 Target; 1 Instrument with 3 variables; different impulse|\[[('myvar1',50), ('myvar2',25), ('myvar3',10) ]]|Three instrument variables, each is assigned an impulse/weight, such that in finding values to achieve the target, 'myvar' will be pertubed twice as much as myvar2 and 5 times as much as myvar3|
|1 Target; 1 Instruments with 3 variables; smaller impulse|\[\('myvar1',0.5), ('myvar2',0.25), ('myvar3',0.10)\]\]|Again three instrument variables, each is assigned an impulse/weight, such that in finding values to achieve the target, 'myvar1' will be perturbed twice as much as myvar2 and 5 times as much as MyVar3.  **NB this example will generate the same results as above, because although the impulse values have changed, the relative size of the impulse are the same**|




The final section of this chapter explains in more detail the solution algorithm of the `.invert()` method and the meaning of the various options of the method.

### Solving for the instruments to reach the targets

Below is the actual call to invert used for this example. 

```python
%%time  
simple = mpak.invert(baseline, targets = target_simple, )
```

```text
Finding instruments :   0%|          | 0/77
```

```text
CPU times: total: 43.2 s
Wall time: 43.3 s
```

### Display result

Once the simulation is complete the results are, as usual, stored in the `mpak` model object in the `.lastdf` dataframe.  Results can be inspected either by using tables or graphically.

Below the `.plot()` method with option `datatype='growth'`is used to compare the total emissions and the carbon taxes from the solution set and the initial baseline, first in growth rates, then as a percent deviation from baseline option `datatype='difpctlevel'`.  The option `base_last=True` ensures that the results from the most recent simulation (the `lastdf DataFrame` are displayed along side those from the `basedf DataFrame`.  If multiple series are specified each series will be dispayed on a separate figure.

```python
mpak.plot('PAKCCEMISCO2TKN',
          datatype='growth',
          legend=True,
          base_last=True).show
```

```text
<Figure size 1000x600 with 1 Axes>
```

```python

mpak['PAKCCEMISCO2?KN'].plot(
    title="Emissions: slow growth of emissions to 1% per annum",
    datatype='difpctlevel',
    showfig=True);
```

```text
<Figure size 1000x400 with 4 Axes>
```

```python
with mpak.set_smpl(2020,2050):    # change if you want another  timeframe 
    fig1=mpak.plot('PAKCCEMISCO2TKN',
          datatype='level',
          legend=True,
          base_last=True)
    fig2=mpak.plot('PAKGGREVCO2CER',
          datatype='level',
          title=f'Pakistan, tax rate required to achieve slower emissions growth',
                   base_last=True,
          legend=True)
combo=(fig2+fig1)
combo.show
```

```text
<Figure size 1000x600 with 1 Axes>
```

```text
<Figure size 1000x600 with 1 Axes>
```

```python
with mpak.set_smpl(2020,2050):    # change if you want another  timeframe 
    fig = mpak[f'PAKCCEMISCO2TKN'].plot_alt(title='Pakistan CO2 emission') 
    fig2 = mpak[f'PAKGGREVCO2CER'].plot_alt(
    title=f'Pakistan, tax rate required to achieve slower emissions growth'); 
    
fig1
fig2
```

```text
<Figure size 1500x600 with 1 Axes>
```

```text
<Figure size 1000x600 with 1 Axes>
```

```text
<Figure size 1500x600 with 1 Axes>
```

```text
<Figure size 1500x600 with 1 Axes>
```

## Targeting carbon emissions in a budget neutral manner
 

In this example, a more complex targeting exercise is conducted.  

In this instance two targets are identified:
1. An unchanged fiscal deficit
2. A 40 percent decline in overall emissions 
 
This requires at least two instruments: 
 1. The carbon emissions target will be determined by 3 instrument variables (the carbon taxes on each of coal, oil and natural gas)
 2. The fiscal balance target will be met by one instrument Government spending on goods and services, implying that revenues from the Carbon Taxes will be used to increase government services. 
 
{cite:author}`burns_climate_2021`(2021), using the same model explores, the macroeconomic consequences implications of alternative uses of the revenues from the Carbon Tax.

 

### Define target trajectory for CO2 emission. 
The objective is to reduce Carbon emissions by 40% (as compared with the baseline) by the year 2050 and hold them constant in level terms afterwards.  

The two variables `reduction_percent`, which reflects by how much emissions are to decline, and `achieved_by`, which represents by when the reduction should be achieved, are used to define the objectives series in a flexible way. 

Using variables like this to express the constraint may be a bit more complicated.  However, in the long run it may be easier as it allows the same code to be used to explore how different emission targets and different years in which the target should be fulfilled might affect the results.

```python
reduction_percent = 40  # Input the desired reduction in percent. 
achieved_by       = 2050
```

If the target is to achieve a 40 percent reduction in emissions by 2050, the pathway toward that objective can be described as a rate of growth of emissions that leads us to a 40 percent lower level by 2050.  

That growth rate can be calculated by:
 1. Calculating the level of emissions to be reached in the target year  as $PAKCCEMISCO2TKN_{2050} \cdot (1-40/100)$ 
 2. Calculate the growth rate of the target variable needed to reach that level in 2050=<br> 
    $\biggl(\dfrac{PAKCCEMISCO2TKN_{2050}\cdot (1-40/100)}{PAKCCEMISCO2TKN_{2024}}\biggr)^{\dfrac{1}{2050-2024}}-1$
 
Once the target is defined the model can then calculate the values of carbon taxes necessary to reach those levels. 
 
Below the target growth rate is calculated.

```python
bau_emissions_final = baseline.loc[achieved_by,'PAKCCEMISCO2TKN'] #baseline emissions
                                                                  # in 2050
bau_emissions_2024  = baseline.loc[2024,'PAKCCEMISCO2TKN'] #baseline emissions 
                                                           # in 2024

target_emissions_final  = bau_emissions_final*(1-reduction_percent/100) #target
                                                               # emissions in 2050

#growth rate needed between 2024 and 2050 to reach the target emissioons level in 2050
target_growth_rate  = (target_emissions_final/bau_emissions_2024)**(1/(achieved_by-2024))-1
bau_growth_rate     = (bau_emissions_final/bau_emissions_2024)**(1/(achieved_by-2024))-1
```

Below a quick routine to display the parameters and objectives.

```python
print(f"Baseline Emissions in {achieved_by}               : {bau_emissions_final:13,.0f} tons")
print(f"Target  Emissions  in {achieved_by}               : {target_emissions_final:13,.0f} tons")
print(f"Business as usual growth rate in percent : {bau_growth_rate:13,.1%}")
print(f"Target growth rate in percent            : {target_growth_rate:13,.1%}")
```

```text
Baseline Emissions in 2050               :   439,930,562 tons
Target  Emissions  in 2050               :   263,958,337 tons
Business as usual growth rate in percent :          2.5%
Target growth rate in percent            :          0.5%
```

### Create a dataframe with the target emissions 

To prepare the simulation, a dataframe needs to be prepared with the target variable(s) set to the desired growth path, calculated above. 

The target dataframe will contain as many variables as there are targets, at this stage just one. 

Initially the target variable is set to the values of the original data in the baseline, then it is set to grow at the growth rate calculated above between 2024 and 2050 to achieve the 40 percent reduction in emissions and then it is held constant at this level.

```python
# Create dataframe with only the target variable (data defined from 2024 onwards)
target_before = baseline.loc[2024:,['PAKCCEMISCO2TKN']]     
# create a target dataframe with a projection of the target variable 
target = target_before.upd(f'<2025 {achieved_by}> PAKCCEMISCO2TKN =growth {100*target_growth_rate}')
target = target.upd(f'<{min(2100,achieved_by+1)} {2100}> PAKCCEMISCO2TKN = {target_emissions_final}')
#target.loc[:2055]
```

### Create target for government deficit 

In this example, there is a second target -- to maintain the government deficit unchanged. As the objective is to hold the deficit constant as a share of GDP (at the levels in the baseline), the target for this variable will just take the same values as the government balance variable (expressed as a percent of GDP) `PAKGGBALOVRLCN_` in the baseline.  

```python
#add to the target dataframe the GG balance variable from 2022 through 2100
target.loc[:,'PAKGGBALOVRLCN_'] = baseline.loc[2022:2100,'PAKGGBALOVRLCN_']
```

The target dataframe now holds two Series, defined over the period 2024 through 2100.

```python
target
```

```text
PAKCCEMISCO2TKN  PAKGGBALOVRLCN_
2024     2.303703e+08        -3.131896
2025     2.315794e+08        -3.045253
2026     2.327948e+08        -2.984815
2027     2.340166e+08        -2.945600
2028     2.352449e+08        -2.921505
...               ...              ...
2096     2.639583e+08        -2.540508
2097     2.639583e+08        -2.540567
2098     2.639583e+08        -2.540636
2099     2.639583e+08        -2.540713
2100     2.639583e+08        -2.540798

[77 rows x 2 columns]
```

## Define instruments

The instruments to achieve these targets are the **3 carbon taxes** and **government spending on goods and services**.  To find the mnemonics for these variables a search is done over the descriptions of the variables, first over the carbon tax:

```python
mpak['!*Carbon*'].des
```

```text
PAKCCEMISCO2TKN : Pakistan Total Carbon emissions (tons)
PAKGGREVCO2CER  : Carbon tax on coal (USD/t)
PAKGGREVCO2GER  : Carbon tax on gas (USD/t)
PAKGGREVCO2OER  : Carbon tax on oil (USD/t)
```

A separate search is done to identify the government spending variable to be used as an instrument. It makes sense to use a variable which has a fairly direct impact on the government deficit.

```python
mpak['!*government*expenditure*goods*'].des
```

```text
PAKGGEXPGNFSCN        : General government expenditure on goods and services (millions lcu)
PAKGGEXPGNFSCN_A      : Add factor:General government expenditure on goods and services (millions lcu)
PAKGGEXPGNFSCN_D      : Fix dummy:General government expenditure on goods and services (millions lcu)
PAKGGEXPGNFSCN_FITTED : Fitted  value:General government expenditure on goods and services (millions lcu)
PAKGGEXPGNFSCN_X      : Fix value:General government expenditure on goods and services (millions lcu)
```

For the purposes of this simulation the `PAKGGEXPGNFSCN_A` variable (the add-factor for the government spending on goods and services equation) is selected. The add-factor is chosen so that the underlying equation remains active during the simulation.

Then a list called `instruments` is populated with two lists:
* the first is a list of variables for the first instrument (in this case the three carbon taxes)
* the second a list of one instruments for the second instrument (just one variable the add-factor on government spending on goods and services

```python
instruments = [['PAKGGREVCO2CER','PAKGGREVCO2GER', 'PAKGGREVCO2OER'],
               'PAKGGEXPGNFSCN_A']
```

## Solve the two-target targeting  problem: 

Having defined the dataframes for the target values and the instrument variables, the model can be solved.




The `%%times` command at the beginning of the cell below instructs Jupyter Notebook to keep track of how long it takes for the cell to execute and displays the result.

```python
%%time  
unweighted= mpak.invert(baseline,                  # Invert calls the targeting routine 
                targets = target.loc[:,: ],        #our targets defined above           
                instruments=instruments,           # our instruments defined above
                defaultimpuls=20,                  # The default impulse value for the instruments 
                defaultconv=2000.0,                # Convergergence criteria for targets ( a relatively large number)
                varimpulse=True,                   # Change in instruments after each iteration are carried over to the future
                nonlin=5,                          # If no convergence in 15 iteration recalculate jacobi 
                silent=True,                       # Don't show iteration output (try 1 for showing)
                delay=False,
                maxiter = 75,
                progressbar = True)
```

```text
Finding instruments :   0%|          | 0/77
```

```text
CPU times: total: 7.3 s
Wall time: 7.38 s
```

### Results

The following two chart illustrate that the objective of slowing emissions growth was achieved, with the growth rate in the targeted series equal to  1 percent.

```python
mpak.plot('PAKCCEMISCO2TKN',base_last=True,legend=False).show
```

```text
<Figure size 1000x600 with 1 Axes>
```

Below the carbon tax that was required to achieve the desired emissions result.

```python
with mpak.set_smpl(2020,2050):
    mpak['PAKGGREVCO2CER'].plot_alt(title='Carbon tax on coal: baseline versus target ')
```

```text
<Figure size 1000x600 with 1 Axes>
```

```text
<Figure size 1500x600 with 1 Axes>
```

```python
fig2.figs.keys()
```

```text
dict_keys(['Pakistan Total Carbon emissions (tons), growth'])
```

## Weighting the instruments  

When using multiple instruments for a single target, the modeler may  want to privilege changes in one instrument over another by specifying weights to attach to each.  In the example below, specific weights are attached to the instruments, instructing the solver to place twice as much emphasis on adjusting the carbon tax on coal emissions (as compared with the other two carbon taxes).  The actual number applied to the weights is not important as it is the relative weights that play a role.  Thus here the weights 50,25,25 would have precisely the same effect as 2,1,1.

```python
new_instruments =[[('PAKGGREVCO2CER',50),
                   ('PAKGGREVCO2GER', 25),
                   ('PAKGGREVCO2OER',25)],
                 'PAKGGEXPGNFSCN_A']

weighted = mpak.invert(baseline,                  # Invert calls the target instrument device                   
                targets = target.loc[:,: ],                   
                instruments=new_instruments,
                defaultimpuls=20,              # The default impulse instrument variables 
                defaultconv=2000.0,              # Convergergence criteria for targets
                varimpulse=True,             # Changes in instruments in each iteration are carried over to the future
                nonlin=5,                    # If no convergence in 15 iteration recalculate jacobi 
                silent=1,                     # Don't show iteration output (try 1 for showing)
                delay=0,
                maxiter = 50,
                progressbar = True)
```

```text
Finding instruments :   0%|          | 0/77
```

With a weight twice as large on the coal carbon tax instrument, the carbon tax on coal rises to a level twice as fast as that of the other carbon taxes.

```python
with mpak.set_smpl(2020,2050):    # change if you want another  timeframe 
    fig1 = mpak[f'PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER' ].rename().plot(
        title='Carbon taxes in weighted-target scenario ') 
    
with mpak.set_smpl(2020,2050):    # change if you want another  timeframe 
    fig = mpak.plot('PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER',
                   datatype='level',base_last=True,name='fignewstyle',
                   mul=1,samefig=True,title='Different tax levels')    
fig.figs['fignewstyle'].axes[0].set_title('Coal')    
fig.figs['fignewstyle'].axes[1].set_title('Gas')    
fig.figs['fignewstyle'].axes[2].set_title('Oil')  
fig.figs['fignewstyle'].axes[0].set_ylim(0, 1000)
fig.figs['fignewstyle'].axes[1].set_ylim(0, 1000)
fig.figs['fignewstyle'].axes[2].set_ylim(0, 1000)
fig.show
```

```text
<Figure size 1000x400 with 4 Axes>
```

```text
<Figure size 2000x1200 with 4 Axes>
```

Instead of putting different weights on the carbon taxes, an alternative might have been to add more instruments to the budget balance target (say direct and indirect taxes), with the weights equal to each tax type's share in total revenues.  Set up this way, the scenario would maintain budget balance neutrality by using the revenues from the carbon taxes to reduce other (perhaps more distorting taxes).

The concept of targets and instruments in economic modeling was introduced by {cite:t}`tinbergen_economic_1967`

When solving a targeting problem it can be thought as follows: 

Take a generic system of equations (a model): 
$\textbf{y}_t= \textbf{F}(\textbf{x}_{t})$ 

Where, $\textbf{x}_{t}$ are all predetermined variables - lagged endogenous and exogenous variables. 

A condensed model ($\textbf{G}$) can be defined comprised of a few endogenous variables ($\bar{\textbf{y}}_t$) -- the targets and a few a few exogenous variables($\bar{\textbf{x}}_{t}$) -- the instrument variables. 

In this model, the remaining predetermined variables are fixed. Thus this model can be expressed as $\bar{\textbf{y}}_t= \textbf{G}(\bar{\textbf{x}}_{t})$.

In some models the result depends on the level of exogenous variables with a lag. For instance in a disease spreading model, the *number of infected* on a day depends on the *probability of transmission* some days before. If the *probability of transmission* is the instrument and the *number of infected* is the target. Therefor it can be useful to allow a **delay**, when finding the instruments. In this case we want to look at  $\textbf{y}_t= \textbf{F}(\textbf{x}_{t-delay})$ 

Inverting G,  gives a model where  instruments are a functions of targets: $\bar{\textbf{x}_{t-delay}}= \textbf{G}^{-1}(\bar{\textbf{y}_{t}})$. 

In other words, the inverted model is solved for the value of the instruments that gives the desired level for the targets: $\textbf{G}^{-1}(\bar{\textbf{y}_{t}})$

For most models $\bar{\textbf{x}}_{t-delay}= \textbf{G}^{-1}(\bar{\textbf{y}_{t}})$ does not have a nicely closed-form solution. However it can be solved numerically -- in ModelFlow this is done using the **Newton–Raphson** method.

So $\bar{\textbf{x}}_{t-delay}= \textbf{G}^{-1}(\bar{\textbf{y}_{t}^*})$ will be found using :

for $k$ = 1 to convergence  

>$\bar{\textbf{x}}_{t-delay,end}^k= \bar{\textbf{x}}_{t-delay,end}^{k-1}+ \textbf{J}^{-1}_t \times (\bar{\textbf{y}_{t}^*}-
\bar{\textbf{y}_{t}}^{k-1})$

>$\bar{\textbf{y}}_t^{k}= \textbf{G}(\bar{\textbf{x}}_{t-delay}^{k})$

convergence: $\mid\bar{\textbf{y}_{t}^*}-
\bar{\textbf{y}_{t}}
\mid\leq \epsilon$

ModelFlow uses numerical differentiation, to find the Jacobian of the inverted matrix because it is simple and fast.

$\textbf{J}_t = \frac{\partial \textbf{G} }{\partial \bar{\textbf{x}}_{t-delay}}$


$\textbf{J}_t \approx \frac{\Delta \textbf{G} }{\Delta \bar{\textbf{x}}_{t-delay}}$

Mechanically that requires the model should be solved once for each instrument with a given delta applied to the targets. Recording the impact on each of the targets from the ${\Delta {x}_{t-delay}^{instrument}}$ gives and estimate of $\textbf{J}_t$ 

In order for $\textbf{J}_t$ to be invertible there has to be **the same number of targets and instruments**. 

However, each instrument can be a basket of exogenous variable an they can have different impulse $\Delta$
.

\begin{equation}
\Delta x^{instrument=i} = 
\begin{bmatrix}
\Delta x^{instrument=i,variable=1} \\
\Delta x^{instrument=i,variable=2} \\
\Delta x^{instrument=i,variable=3} \\
\vdots \\
\Delta x^{instrument=i,variable=n} \\
\end{bmatrix}
\end{equation}

When an instrument changes the variables will change and the change will be in the proportions defined by their impulse. 

Notice that the level of $\bar{\textbf{x}}$ is updated (by  $\textbf{J}^{-1}_t \times (\bar{\textbf{y}_{t}^*}-
\bar{\textbf{y}_{t}}^{k-1})$) in all periods from $t-delay$ to $end$, where $end$ is the last timeframe in the dataframe. This is useful for many applications, where the instruments are level variable (i.e. not change variables). 

This is the default behavior. It can be changed.  

## Tuning the target input to get a result
Models implemented in `ModelFlow` can be very different, and the targeting routine `.invert()` is fairly general. In many cases, targeting will not work out-of-the-box, its options will have to be tweaked to fit the problem at hand.

### Targetting options

The invert options that affect the speed and accuracy of a solution are: 

* `defaultimpuls`
* `defaultconv`
* `nonlin`  
* `maxiter`  
* `varimpulse`

### defaultimpuls  -- set the size of the delta used when calculating the Jacobian
The impulse variable determines the size of the delta that is used to calculate the jacobian matrix. If it is too small or too large the resulting jacobian will solve only very slowly. Typically the impulse should be scaled in relation to the magnitude of the instrument it is to impact. 

If a large impulse is used for a small variable (or a small impulse for a large variable) $\textbf{x}+{\Delta \bar{\textbf{x}}_{t-delay}}$ the model may become unsolvable.

Separate impulse values can be set for each instrument.  This is done when setting the instruments (see discussion below).



### nonlin -- an integer - set to the number of iterations to attempt before recalculating the Jacobian 

If the model is nonlinear it makes sense to re-estimate the jacobian matrix $\textbf{J}_t$ frequently. The `nonlin=a number` option allows the user to set the number of iterations the solver should allow without finding a solution before calculating a new jacobian. 

If:
 - `nonlin=0` the jacobian will not be updated (default) -- implicitly indicates the model should be treated as if linear.
 - `nonlin=<a number>` the same jacobi matrix will be updated after \<a number\> iterations.
 -`nonlin=3`, 5 and 10 are all reasonable options in cases where model non-linearity requires the recalculation of he Jacobian.

   
### Convergence
    
The targeting is stopped when all target variables converge. The convergence criteria should reflect the size of the target variables. Too large and the solution may not actually reflect a close approximation of the target, too small and the model may take a very long-time to solve.  
    
 -  `defaultconv=<a number>`



### Maximum number of iterations

 -  `maxiter=<a number>`
    
This option determines the maximum number of iterations that the model should run in trying to find a solution.  Reasonable initial numbers may be between 50 and 100. If a model takes more than 100 iterations, there may be an issue. Potentially the chosen instruments do not have much impact on the target variables, or the model is relatively non-linear.  Try setting nonlin=10 to see if recalculating the Jacobian allows the model to solve. 
    

## Definition of Instruments 

As noted above there must be at least one instrument for each target. Instruments are passed as a python list.

Each element in the list is an instrument. 
-  An element can be:
   - a variable name 
   - a tuple with a variable name  and an associated impulse $\Delta$
   - an inner list which defines which contains:  
        - a list of variable names. Each element in the inner list is an instrument variable 
        - a list of tuples each tuple contains a variable name and the associated impulse $\Delta$. 
              

The $\Delta$ variable(s) is (are) used in the numerical differentiation. Also if one instrument contains several variables, the proportion of each variable will be determined by the relative $\Delta  variable$. 

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

```python
# Prepare the notebook for use of ModelFlow   

# Jupyter magic command to improve the display of charts in the Notebook
%matplotlib inline

# Import pandas 
import pandas as pd

# Import the model class from the modelclass module 
from modelclass import model 

# functions that improve rendering of ModelFlow outputs
model.widescreen()
#model.scroll_off();
```

# Report writing and scenario results

`ModelFlow`, is built on the back of  and inherits the functionalities of standard pandas routines and other python libraries like [matplotlib](https://matplotlib.org/), [seaborn](https://seaborn.pydata.org/), [plotly](https://plotly.com/), and  [bokeh](https://bokeh.org/). These libraries are well-integrated with `DataFrames`, and offer a wide-range of visualization capabilities. As has been done throughout this manual, they can be used to look at data, and compare simulation results among other things. 

:class: tip

This chapter focuses on tools and techniques for examining the data in a model and the results of simulations. Many of these techniques have been illustrated elsewhere, but are brought together in one place in this chapter to facilitate retrieval later. The chapter includes a discussion of techniques for creating comprehensive reports based on simulations and analyzes performed in `ModelFlow`. 

Examples in the chapter:

- Demonstrate how to generate structured tables, charts, and text outputs directly from simulation results.
- Introduces ModelFlow's reporting classes (`.table()`, `.plot()`, `.text()`) and how they can be used to produce reports that combine both tabular, graphical and textual results. 
- Issues dealt with include how to generate tables that display only selected time periods
- How to present data in landscape and portrait form
- Presenting graphs either on their own or in groups
- using the `.reports` method to store a set of tables and or graphs as a template that then can be applied to different scenario results yielding standardized reports

Outputs from all of these methods can be rendered as interactive widgets, html, pdf or various bitmap forms.

`ModelFlow` users are free to employ any Python-based library for visualization purposes. For specific tasks, `ModelFlow` also includes some specialized procedures derived from the above packages that may be of interest. These routines are tailored to utilize `ModelFlow` internal data structures, like the `.lastdf`, `.basedf` and `keep` `DataFrames` as well as metadata in the model object such as variable descriptions. Moreover, `ModelFlow` reporting routines include specific transformations (like growth rates) and scenario comparison routines that are useful in the analysis of macroeconomic model results.

The following box summarizes the four different kinds of report-writing objects incorporated into the `ModelFlow` package. 

`ModelFlow` augments standard Python routines with four report-writing classes: 

1. **table**: a class that represents data from the `.lastdf` and `.basedf`  in tabular form.
2. **plot**: a class that represents data from the `.lastdf` and `.basedf` and kept dataframes in graphical form.
3. **text**: a class for text-based tables, which can be specified using plain text, LaTeX, or HTML, or any combination of the three.
4. **report**: a container class that can be comprised of an arbitrary number of tables and plots in any order.

## Preparing a `ModelFlow` `Python` environment
To begin, a solution file that was saved at the end of the previous chapter is loaded, using the by now familiar `modelload` method.  Because the simulations performed in the previous chapter used the keep option, and, because the `mpakwScenarios.pcim` file was saved with the keep option set to true, the `modelload` method gives the current session access to all the results generated in the previous chapter.

```python
mpak,_ = model.modelload(r'../models/mpakw.pcim',run=1)
_ = mpak.smpl(2025,2029)
```

```text
Zipped file read:  ..\models\mpakw.pcim
```

When a model is solved (simulated), the result is returned as a `DataFrame`.

To facilitate reporting, the resulting `DataFrame` is also stored as the `.lastdf` property of the model object. The `.lastdf` property is overwritten every time the model is solved.  To preserve the results for future reference, the `keep='Some Solution Name'` option can be used.  This will store a copy of the `DataFrame` in a dictionary called `keep_solutions` where the  key will be the text descriptor given in the `keep` option -- in this case 'Some Solution Name'.

> result = mpak(dataframe_with_experiment,keep='Some Solution Name')

The  `.basedf` `DataFrame` contains the baseline values. It is set during the first simulation in a session, either when a model is loaded with `run=True` or when the model is simulated for the first time. But it can also be reset manually if desired `mapk.basedf=mydataframe`.
  
If a model has a lot of variables and there are a lot of scenarios it can be useful to limit the number of variables in the stored `DataFrame`. This is done by specifying: `keep_variables=<a string with list of variables including wildcards>`   

> result = mpak(dataframe_with_experiment,keep='some text',keep_variables = '*NYGDPMKTPKN *NECONPRVTKN')

Will only keep variables matching the wildcard expressions: '*NYGDPMKTPKN *NECONPRVTKN'

To reset `.keep_solutions` to an empty dictionary type: `{modelobject}.keep_solutions = {}`

Below, in order to have meaningful data for the following report-writing examples, the `.basedf` and `.lastdf` `DataFrames` of `mpak` are pre-populated with the "Baseline" and "1% of GDP increase in FDI and private investment (AF shock)" results from the kept scenarios of the previous chapter.

```python
mpak.basedf = mpak.keep_solutions['Baseline']
mpak.lastdf = mpak.keep_solutions['1% of GDP increase in FDI and private investment (AF shock)']
mpak.smpl(2025,2029);
```

The `.keep_solutions` dictionary can be interrogated to list all of the solutions (the keys) that were performed and stored in the previous chapter and the dataframes that were generated when the simulations were performed (the keys) in the dictionary.

## The `.table()` class


The `.table()` method is a constructor for the `ModelFlow` class `DisplayVarTableDef`. When called, it creates a table object from the data series passed to it. By default, it represents the data as growth rates and draws them from the `.lastdf` dataframe unless `.basedf`   is requested specifically.  

If a comparison display option is chosen (see below), the comparison will be between the values for the selected variables from the  `.lastdf` and the `.basedf` `DataFrame`s.

### Create a `.table()` object

The following generates a simple table object:  
``` 
 tab = mpak.tab(name='My_first_table',pat=' *NYGDPMKTPKN *NECONPRVTKN  *NEGDIFTOTKN *NEEXPGNFSKN *NEIMPGNFSKN', title='GDP components', foot='Source: World Bank ')
 ```

Arguments used: 

* **pattern** (pat) specifies the variables to be displayed. Here the `*` wildcard is used, allowing this pattern to be used for models for any World Bank model that conforms to the Bank's standard naming conventions 
* **name** is an internal identifier used to identify output from this table object when when different tables are producing output. 
* **title** specifies text to be used as a title for the Table  
* **foot** specifies text to be placed in a footer for the table

As written the command creates an object called `tab`. `tab` can be called subsequently to display or manipulate the table in different ways.

Below the same table is generated using a variable to represent the pattern of variables to be included in the table.

```python
pat=  ' *NYGDPMKTPKN *NECONPRVTKN  *NEGDIFTOTKN *NEEXPGNFSKN *NEIMPGNFSKN '
tab = mpak.table(name='My_first_table',pat=pat,title='GDP components',foot='Source: World Bank ')
```

### Rendering table objects 

Table objects can be rendered as html, text and pdf objects. The below table indicates the methods associated with each.

**Display options for table objects**

|command|output|
|:--|:--|
|None (just the object name)| In `Jupyter Notebook` displays the table in its html format.|
|display(tab)|Displays the table in html format.|
|.show|Returns a simple text version of the table.|
|.pdf|Returns a nicely formatted table in pdf format.|

#### `.tab()` example output

When the table object in the last line of a cell in `Jupyter` Notebooks it will cause the content of the object to be rendered in `html`.

```python
tab
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

#### The display(tab) method produces  exactly the same output
And it can be used in any line in a jupyter cell

#### The Table `.show` method

The `.show()` method renders the table inpure text form, without any html or pdf formatting.

```python
tab.show
```

```text
GDP components
                         2025   2026   2027   2028   2029
                              --- Percent growth ---     
Real GDP                 2.08   2.42   2.64   4.36   2.91
HH. Cons Real            2.03   2.32   2.48   3.45   2.62
Investment real          1.10   1.46   1.82  12.46   2.98
Exports real             4.37   4.20   4.04   3.88   3.72
Imports real             3.10   3.10   3.02   4.68   2.84
Source: World Bank
```

#### The `.pdf` method causes the table to be rendered to a pdf using latex.

In `Jupyter Notebook` the rendered file will be displayed within the `Jupyter Noteook`.  Alternatively if the `.pdf` method is called with the option (pdfopen=True) then the pdf will be opened in a separate browser. In either case, if the table is too large to appear on the pdf page, the scrollbar of the pdf viewer can be used to view the extra columns or rows.

```python
tab.pdf()
```

```text
<IPython.lib.display.IFrame at 0x243d00a1010>
```

Google Colab does not include an installation of latex by default.  As a result, when running the PDF routines on Colab they will not render.

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 90%
    :align: center

PDF files are generated using Latex as an intermediary.  As a result, Latex must be installed on the machine for this option to work. For this publication the `Miktex` package has been used, and routines have also been tested with the `Tex Live` package. More on installing the `Miktex` package can be found here: [https://miktex.org/download](https://miktex.org/download). When installing Miktex allow automatic download of latex packages.  

On a Mac, MacTex can be used. It can be found here: [https://www.tug.org/mactex/mactex-download.html](https://www.tug.org/mactex/mactex-download.html)

`ModelFlow` writes the intermediate latex commands from which the pdf is generated to a sub-directory entitled `latex` one level below the current work directory. The filename will be set to the table_name parameter specified when the table object was declared.  Thus, the table called "myTable" will be saved to `latex/myTable/MyTable.pdf`. The intermediate latex source code is placed in `latex/myTable/myTable.tex`.

In case of errors or if the user want to enhance the output this file can be edited manually and the pdf re-generated manually using TexWorks which is part of the Miktex instalation.              

### Table options

#### Data transformations  - Growth Rates, Levels, etc.


When the `table` object is invoked, it defaults to displaying the growth rates for specified variables. However, the constructor supports a range of transformations. Which specification is used is determined by the `datatype` argument, which can take the following values:




**Table: Data Types and Their Meanings**

| **datatype**    | **Meaning** |
|:-------------|:------------------------------------------------------------------|
| **growth**  | This is the default setting. Growth rate in percent in the most recent dataset (`.lastdf`).|
| level       | Values in `.lastdf`.                                            |
| gdppct      | Percentage of GDP in `.lastdf`.                                  |
| qoq_ar      | Quarterly growth annualized. - Quarterly models only.|
| **Difference views** |  |
| difgrowth   | Change ($\Delta$) in growth rates (`.lastdf` less `basedf`).   |
| diflevel    | Change ($\Delta$) in values (`.lastdf` less `basedf`).         |
| difgdppct   | Change ($\Delta$) in the percentage of GDP from (`.lastdf` less `basedf`). |
| difqoq_ar      | change in the annualized quarterly growth (`.lastdf` less `basedf`)  |
| difpctlevel | Percentage change ($\Delta$) in values (`.lastdf` less `basedf`). |
| **Values from  `.basedf`** |  |
| basegrowth  | Growth rate in percent in `.basedf`.|
| baselevel   |Level of the data in `.basedf`|
| basegdppct  | Percentage of GDP in `.basedf`.|
| baseqoq_ar  | Quarterly growth in `.basedf`|

#### `transpose ` option




When set, `transpose=True` (default is False), the table will be rendered so that series appear as columns (with dates progressing downward on the page). In this mode, many time-periods can be displayed, but the number of series will be limited by the width of the paper/screen.  

```python
with mpak.set_smpl(2022,2027):
    tab_t = mpak.table(name='A_transposed_table',pat=pat,title='GDP components',
                       foot='Source: World Bank ',transpose = True)
tab_t.show
```

```text
GDP components
     Real GDP HH. Cons Real Investment real Exports real Imports real
                          --- Percent growth ---                     
2022     0.66          0.80            0.70         4.71         3.00
2023     1.04          1.09            0.63         4.66         2.86
2024     1.60          1.60            0.79         4.53         2.99
2025     2.08          2.03            1.10         4.37         3.10
2026     2.42          2.32            1.46         4.20         3.10
2027     2.64          2.48            1.82         4.04         3.02
Source: World Bank
```

#### The dec=\#\# option: limits the decimals displayed





In the example below, only one decimal of the generated table is displayed.  Note this table uses the datatype option `"pctgdp"`. which displays the results as a percent of GDP.


The option `datatype='gdppct'` is only well-defined for variables that follow World Bank naming conventions and end either (CD,CN, KD or KN).  The `gdppct` routine uses these endings to determine whether to calculate the percent of GDP as a percent of nominal GDP either in local currency (CN) or USD (CD) or real GDP in local currency  (KN) or real USD (KD). 

```python
pat_gov = '*GGBALOVRLCN *GGDBTTOTLCN *BNCABFUNDCD'
tab_gov = mpak.table(pat_gov,datatype='gdppct',title='In percent of GDP ',dec=1)
tab_gov.show
```

```text
In percent of GDP 
                                              2025   2026   2027   2028   2029
                                                   --- Percent of GDP ---     
General Government Revenue, Deficit, LCU mn   -3.0   -3.0   -2.9   -2.8   -2.8
General government gross debt millions lcu    57.0   57.3   57.7   57.1   57.5
Current Account Balance, US$ mn               -3.6   -3.5   -3.4   -3.5   -3.4
```

### Handling Table Overruns (too much data)

It is possible to specify a table that is too large for conventional display systems.  For example, a table of data taken from  a model that covers 100 years could, if the dates run vertically, span more than 1 page, or one that covers many data series might overrun the right hand side of a computer screen, pdf file or printed page.
Displaying such tables in `Jupyter Notebooks` or other computer-based displays is straightforward because `Jupyter Notebook` will allow the user to scroll content that does not fit on the page. However, in `LaTeX` documents or printed materials, tables that overrun the page can become impossible to read. 

To address this issue, several strategies can be employed:

- **Drop Middle Columns**: This involves removing several columns from the middle of the table that may not be critical to the reader’s understanding, helping to condense the table into a more manageable size.
  
- **Display Tables in Chunks**: Specify a rule for breaking the table into multiple smaller tables, each covering a shorter time span. This not only makes each segment easier to fit on a page but also can help readers digest the information in smaller, more focused increments.

- **Display a Slice of Data**: Rather than showing the entire timeline, you can display a specific segment or 'slice' of the data that is most relevant to the analysis at hand. This approach focuses the reader's attention and avoids overwhelming them with too much information at once.

These methods can significantly enhance the readability and presentation of large tables when rendered on media that are less flexible than interactive digital platforms.

#### Default behavior for dealing with large tables

Below a long table is generated, which runs beyond the edges of the monitor on most computer displays. In `Jupyter Notebook` or other IDEs elements the standard display options \[table name or display(tablename) -- both of which produce html \] will generate outputs that that cannot render within one screen width but can scrolled to.  

```python
with mpak.set_smpl(2026,2050): 
    tab_large = mpak.table(pat,title='GDP components',name='large_table',dec=1)
```

```python
display(tab_large)
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

The `.show` and `.pdf` methods  automatically truncates the width of the table to fit on screen. By default it will show the beginning and ending data columns leaving out the intermediate columns.

```python
tab_large.show
```

```text
GDP components
                         2026   2027   2028  ...   2048   2049   2050
                                    --- Percent growth ---           
Real GDP                  2.4    2.6    4.4  ...    3.3    3.3    3.3
HH. Cons Real             2.3    2.5    3.4  ...    3.2    3.2    3.2
Investment real           1.5    1.8   12.5  ...    4.3    4.3    4.3
Exports real              4.2    4.0    3.9  ...    2.7    2.7    2.6
Imports real              3.1    3.0    4.7  ...    2.8    2.9    2.9
```

```python
tab_large.pdf()
```

```text
<IPython.lib.display.IFrame at 0x243d00d2210>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

#### Customizing the display of "too large" tables

These default behaviors can be modified using various `.table`  options (see table), notably the options (chunk_size=, time-slice=, tranpose=, max_cols=, last_cols-=)  which determine how excess data is treated.

##### `chunk_size=` to split pdf tables. 
If the option `chunk_size` is set. The pdf table will be split into sub tables each with chunk_size columns (except, perhaps, the final table). 

```python
tab_large.set_options(chunk_size=10).pdf(height = '700px')
```

```text
<IPython.lib.display.IFrame at 0x243d00d2350>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 80%
    :align: center

##### `landscape=` to show  a pdf in landscape mode. . 
If the option `landscape=` is set. The pdf table will be shown in landscape mode. In this case the `max_cols` option should also be used, as 
the default will only be 6.  

```python
tab_large.set_options(landscape=True, max_cols=18,name='large_table_landscape').pdf()
```

```text
<IPython.lib.display.IFrame at 0x243d00e9cd0>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 80%
    :align: center

##### The  `timeslice = ` option allows the user to select which years to render 
The `timeslice` option gives the user full control over which columns (years or quarters) will be displayed displayed. 

**Beware**, `timeslice` doesn't care if years are out of order. 

In the example below the years are out of order, and the resulting output reflects what was asked for. 

```python
tab_large.set_options(timeslice=[2026,2040,2028 ,2029,2050]).show
```

```text
GDP components
                         2026   2040   2028   2029   2050
                              --- Percent growth ---     
Real GDP                  2.4    3.4    4.4    2.9    3.3
HH. Cons Real             2.3    3.2    3.4    2.6    3.2
Investment real           1.5    4.3   12.5    3.0    4.3
Exports real              4.2    2.9    3.9    3.7    2.6
Imports real              3.1    2.6    4.7    2.8    2.9
```

In this example, a new table is generated with more conventional timeslices.

```python
with mpak.set_smpl(2026,2050): 
    tab2 = mpak.table(pat,title='GDP components',name='long_table_2',timeslice=[2026,2030,2035 ,2040, 2045, 2050]);
    
tab2.show
```

```text
GDP components
                         2026   2030   2035   2040   2045   2050
                                  --- Percent growth ---        
Real GDP                 2.42   2.75   3.37   3.41   3.36   3.33
HH. Cons Real            2.32   2.46   3.12   3.17   3.18   3.20
Investment real          1.46   2.92   3.80   4.29   4.34   4.25
Exports real             4.20   3.59   3.19   2.93   2.75   2.64
Imports real             3.10   2.51   2.59   2.58   2.72   2.88
```

### Other ´.table´ options

The `table` object has two kinds of options:

1) so-called **line options**  that can only be set when the basic table is created with the `.table()` call. 
2) so-called **table options** can be reset using the set_options method. 


latexcommand \newpage

**Line Options**
These options are set on table creation.
| Argument            | Default Value             | Description                                               |
|---------------------|---------------------------|-----------------------------------------------------------| 
| pat                 | '#Headline' (defined in the `ModelFlow` class)| variable names to be displayed, may include wildcard specifications                  |
| datatype            | 'growth'                  | Defines the data transformation displays (cf. next table) |
| mul                 | 1.0                       | Multiplier of values before display                       | 
| dec             | 2                     | set the decimal places to display      | line|
| col_desc            | as shown below            | A centered Description of columns (non transposed table)  | 
| heading             | ''                        | A centered text above columns (non transposed table)      | 
| rename              | True                      | If True use descriptions else variable names              | 


**Table Options**
These options can be revised after a table has been generated.

| Argument            | Default Value             | Description                                               |
|---------------------|---------------------------|-----------------------------------------------------------|
| name                | ''                        | Name for this display.                                    |
| custom_description  | {}                        | Custom description, override default descriptions.        |
| title               | ''                        | Title.                                                    |
| foot                | ''                        | Footer.                                                   |
| transpose           | False                     | If True, transposes the table                             |
| chunk_size          | 0                         | Specifies the number of columns per chunk in tables.      |
| timeslice           | []                        | Specifies the time slice for data display.                |
| max_cols            | 6                         | Maximum columns when displayed as string.                 |
| last_cols           | 3                       | In Latex, the number of last columns in a display slice.  |
| smpl             | ('','')                      | set or re-set the smpl for the table       | 

#### Some table examples

Displaying data as the difference in levels.  The `datatype=diflevel` option causes the difference between the level of the selected variables in the `.lastdf` and `.basedf` databases to be displayed.

```python
mpak.table(pat,datatype = 'diflevel').show
```

```text
Table
                        2025   2026   2027        2028        2029
                                  --- Impact, Level ---           
Real GDP                0.01   0.01   0.01  462,356.71  474,302.09
HH. Cons Real           0.00   0.01   0.01  227,277.15  214,784.60
Investment real         0.00   0.01   0.01  336,198.25  361,924.14
Exports real           -0.00  -0.00  -0.00     -530.52   -2,078.90
Imports real            0.00   0.01   0.01  139,487.97  148,662.16
```

#### The  `col_desc` option causes the default descriptions of variables to be overwritten

The user may change these default descriptors using by setting the `col_desc` option directly. In the example below, the default text displayed in the previous table is revised to something that is more accurate for this particular example.

```python
mpak.table(pat,datatype = 'diflevel',
           col_desc     = 'Delta, LCU, base year 2000'
        ).show
```

```text
Table
                                     2025   2026   2027        2028        2029
                                         --- Delta, LCU, base year 2000 ---    
Real GDP                             0.01   0.01   0.01  462,356.71  474,302.09
HH. Cons Real                        0.00   0.01   0.01  227,277.15  214,784.60
Investment real                      0.00   0.01   0.01  336,198.25  361,924.14
Exports real                        -0.00  -0.00  -0.00     -530.52   -2,078.90
Imports real                         0.00   0.01   0.01  139,487.97  148,662.16
```

If no description is requires set `col_desc=' '` That is a single blank. 

```python
mpak.table(pat,datatype = 'diflevel',
           col_desc     = ' '
                                   ).show
```

```text
Table
                  2025   2026   2027        2028        2029
Real GDP          0.01   0.01   0.01  462,356.71  474,302.09
HH. Cons Real     0.00   0.01   0.01  227,277.15  214,784.60
Investment real   0.00   0.01   0.01  336,198.25  361,924.14
Exports real     -0.00  -0.00  -0.00     -530.52   -2,078.90
Imports real      0.00   0.01   0.01  139,487.97  148,662.16
```

## Complex tables

In the real world more complex tables are often called for, either including a mixture of data display type (some series in levels, others as a percent of GDP) or ones that mix data and text in ways the simple table object does not deal with easily. 

A simple solution is to produce and then join two tables, which can be done with the `|` operator. More complex solutions  would involve the `report` object which allows different table, text and plot elements to be joined in a single report (see the discussion at the end of this chapter).

### The **|** operator joins non-transposed tables


The `|` operator allows two or more table objects (vertical not transposed) to be combined. 

This allows one table expressed in levels (or growth rates) to be combined with another table of data expressed as a percent of GDP.  The more complex conjoined table can therefore mix a number of different data representations. 

When constructing more complex tables, the heading parameter (`heading=some text`) can be used to delineate different sections within the combined table.  NB: The option heading is case sensitive, `Heading=` will do nothing.


Non-transposed tables can be joined with transposed tables and figures using the reports functionality described at the end of this chapter.


Below a simple table with a header. 

```python
test=mpak.table(heading=r'A test header',pat="PAKNYGDPMKTPKN PAKNYGDPPOTLKN")
test.show
```

```text
Table
                                 2025   2026   2027   2028   2029
                                          A test header          
                                      --- Percent growth ---     
Real GDP                         2.08   2.42   2.64   4.36   2.91
Potential Output, constant LCU   2.83   2.86   2.88   2.94   3.03
```

In this example, a more complex table is created as a combination of the earlier generated tables `tab` and `tab_gov`, each using different display types.

```python
(tab | tab_gov).show
```

```text
In percent of GDP 
                                              2025   2026   2027   2028   2029
                                                   --- Percent growth ---     
Real GDP                                      2.08   2.42   2.64   4.36   2.91
HH. Cons Real                                 2.03   2.32   2.48   3.45   2.62
Investment real                               1.10   1.46   1.82  12.46   2.98
Exports real                                  4.37   4.20   4.04   3.88   3.72
Imports real                                  3.10   3.10   3.02   4.68   2.84
                                                   --- Percent of GDP ---     
General Government Revenue, Deficit, LCU mn   -3.0   -3.0   -2.9   -2.8   -2.8
General government gross debt millions lcu    57.0   57.3   57.7   57.1   57.5
Current Account Balance, US$ mn               -3.6   -3.5   -3.4   -3.5   -3.4
Source: World Bank
```

Below several different tables are joined to create quite a complex table.

`tab_total` below is generated as the  of several sub tables and illustrates the use of the heading command and the display in a single object of a relatively complex table.

```python
pat=  '*NYGDPMKTPKN *NECONPRVTKN  *NEGDIFTOTKN *NEEXPGNFSKN *NEIMPGNFSKN'
pat_gov = '*GGBALOVRLCN *GGDBTTOTLCN *BNCABFUNDCD'

tab_na_base  = mpak.table(pat,    datatype='basegrowth',
                        heading=r'Baseline')
tab_gov_base = mpak.table(pat_gov,datatype='basegdppct')

tab_na       = mpak.table(pat,    datatype='growth',
                        heading=r'Alternative')
tab_gov      = mpak.table(pat_gov,datatype='gdppct')

tab_na_dif   = mpak.table(pat     ,datatype='difgrowth',
                        heading=r'Impact')
tab_gov_dif  = mpak.table(pat_gov ,datatype='difgdppct') 

# Use the | to concatenate the tabels
tab_total = tab_na_base | tab_gov_base |  tab_na | tab_gov | tab_na_dif | tab_gov_dif
```

latexcommand \newpage

```python
tab_total.show
```

```text
Table
                                              2025   2026   2027   2028   2029
                                                          Baseline            
                                              --- Baseline Percent growth --- 
Real GDP                                      2.08   2.42   2.64   2.79   2.91
HH. Cons Real                                 2.03   2.32   2.48   2.59   2.69
Investment real                               1.10   1.46   1.82   2.17   2.51
Exports real                                  4.37   4.20   4.04   3.90   3.77
Imports real                                  3.10   3.10   3.02   2.89   2.78
                                              --- Baseline Percent of GDP --- 
General Government Revenue, Deficit, LCU mn  -3.05  -2.98  -2.95  -2.92  -2.91
General government gross debt millions lcu   57.02  57.26  57.69  58.26  58.94
Current Account Balance, US$ mn              -3.55  -3.46  -3.40  -3.37  -3.36
                                                        Alternative           
                                                   --- Percent growth ---     
Real GDP                                      2.08   2.42   2.64   4.36   2.91
HH. Cons Real                                 2.03   2.32   2.48   3.45   2.62
Investment real                               1.10   1.46   1.82  12.46   2.98
Exports real                                  4.37   4.20   4.04   3.88   3.72
Imports real                                  3.10   3.10   3.02   4.68   2.84
                                                   --- Percent of GDP ---     
General Government Revenue, Deficit, LCU mn  -3.05  -2.98  -2.95  -2.81  -2.84
General government gross debt millions lcu   57.02  57.26  57.69  57.11  57.55
Current Account Balance, US$ mn              -3.55  -3.46  -3.40  -3.48  -3.43
                                                           Impact             
                                               --- Impact, Percent growth --- 
Real GDP                                      0.00   0.00   0.00   1.57  -0.00
HH. Cons Real                                 0.00   0.00   0.00   0.86  -0.07
Investment real                               0.00   0.00   0.00  10.29   0.47
Exports real                                 -0.00  -0.00  -0.00  -0.02  -0.05
Imports real                                  0.00   0.00   0.00   1.79   0.06
                                               --- Impact, Percent of GDP --- 
General Government Revenue, Deficit, LCU mn   0.00   0.00   0.00   0.11   0.07
General government gross debt millions lcu   -0.00  -0.00  -0.00  -1.15  -1.39
Current Account Balance, US$ mn               0.00  -0.00  -0.00  -0.11  -0.06
```

latexcommand \newpage

Below the rendering of the same table is revised by using the `set_options(smpl=(2025,2026))` modifier on the command line.

```python
# 
tab_total.set_options(smpl=(2026,2030)).show
```

```text
Table
                                              2026   2027   2028   2029   2030
                                                          Baseline            
                                              --- Baseline Percent growth --- 
Real GDP                                      2.42   2.64   2.79   2.91   3.03
HH. Cons Real                                 2.32   2.48   2.59   2.69   2.78
Investment real                               1.46   1.82   2.17   2.51   2.84
Exports real                                  4.20   4.04   3.90   3.77   3.65
Imports real                                  3.10   3.02   2.89   2.78   2.69
                                              --- Baseline Percent of GDP --- 
General Government Revenue, Deficit, LCU mn  -2.98  -2.95  -2.92  -2.91  -2.90
General government gross debt millions lcu   57.26  57.69  58.26  58.94  59.69
Current Account Balance, US$ mn              -3.46  -3.40  -3.37  -3.36  -3.37
                                                        Alternative           
                                                   --- Percent growth ---     
Real GDP                                      2.42   2.64   4.36   2.91   2.75
HH. Cons Real                                 2.32   2.48   3.45   2.62   2.46
Investment real                               1.46   1.82  12.46   2.98   2.92
Exports real                                  4.20   4.04   3.88   3.72   3.59
Imports real                                  3.10   3.02   4.68   2.84   2.51
                                                   --- Percent of GDP ---     
General Government Revenue, Deficit, LCU mn  -2.98  -2.95  -2.81  -2.84  -2.85
General government gross debt millions lcu   57.26  57.69  57.11  57.55  58.27
Current Account Balance, US$ mn              -3.46  -3.40  -3.48  -3.43  -3.38
                                                           Impact             
                                               --- Impact, Percent growth --- 
Real GDP                                      0.00   0.00   1.57  -0.00  -0.27
HH. Cons Real                                 0.00   0.00   0.86  -0.07  -0.32
Investment real                               0.00   0.00  10.29   0.47   0.09
Exports real                                 -0.00  -0.00  -0.02  -0.05  -0.06
Imports real                                  0.00   0.00   1.79   0.06  -0.17
                                               --- Impact, Percent of GDP --- 
General Government Revenue, Deficit, LCU mn   0.00   0.00   0.11   0.07   0.04
General government gross debt millions lcu   -0.00  -0.00  -1.15  -1.39  -1.42
Current Account Balance, US$ mn              -0.00  -0.00  -0.11  -0.06  -0.01
```

## The `.plot()` class 



The `.plot()` class can be used to display results graphically.

The `ModelFlow` class `.plot` extends the standard python charting libraries, making them aware of the `ModelFlow` databases (including *kept* `DataFrames`) and provides functionality to display data and results in ways commonly used by macroeconomic modelers.

The class's constructor is the `.plot` method which returns an object of type `DisplayVarFigDef`. 

The constructor for `.plot` takes four arguments:

1. **pattern** (pat_plot in the example below) which represents a space delimited string containing the mnemonics of the variables (which must be part of the model object to be charted.  As with standard `ModelFlow` search specifications, either mnemonic names, or descriptions can be specified in wildcard specifications. 
2. **plot_name** an identifier for the plot object, used when storing charts that are part of a plot.
3. **title** A title that will be displayed with any charts that are generated.
4. **scenarios**, an optional string concatenating with the `|` symbol the text names of scenarios to be plotted. If left blank (the default) plot will display data from the `.lastdf` `DataFrame` or compare the `.lastdf` results with the data from the `.basedf` `DataFrame`. 

Below the sample period for the model object `mpak` is set, the pattern that will determine which variables are to be displayed is defined, and a plot object `fig` is instantiated using the variables in pat_plot, with the name 'My_first_plot' and with the displayed title "Results from the most-recent simulation".

```python
mpak.smpl(2020,2040)
pat_plot=  '*NYGDPMKTPKN *NECONPRVTKN  '
fig = mpak.plot(pat_plot,name='My_first_plot',title="Results from the most-recent simulation")
```

The object is an instance of the class `DisplayVarFigDef`. Its construction does not cause the figure to be displayed. Unless the .show method is called explicitly as below.

```python
fig.show;
```

```text
<Figure size 1000x600 with 1 Axes>
```

```text
<Figure size 1000x600 with 1 Axes>
```

### Rendering a plot object

Like the table object, the plot object has several methods for rendering its figure(s).

These include:
* the name of the object -- displays an html widget of the object 
* display(object) will display a html widget of the object. 
* object.show will show all the charts sequentially
* object.pdf() 

### The display (fig) / name of fig command 

The first two options: the name of the figure itself executed as a command; and display(nameoffigure) generate exactly the same results.

Under `Jupyter Notebook`, these two methods generate an "accordion " widget that allows the user to flip through the various charts (possibly just one) that comprise the plot object. 

Different charts in the object can be visualized by selecting the triangle beside the variable name (found on the lefthand side of the screen). Each chart within the plot object has its own triangle beside its name.  Selecting one, will fold-up any other figures that may be open and unfold and display the chart associated with the selected variable. 

The below command generates the widget comprised of two charts (if more series had been indicated when the figure was instantiated, more widget items would be displayed), one for real GDP growth and the second for real household consumption growth.  By default the first is displayed, it can be minimized by clicking on the triangle beside its name. The second (household consumption) will appear under it (below the chart if its is displayed).  Click on the triangle beside its name will cause the widget to  change the displayed figure to the household consumption chart.  Directly clicking on household consumption would have had the same effect, first closing the GDP chart and then displaying the newly selected chart.

```python
display(fig)
```

```text
Accordion(children=(HTML(value='<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE svg PUBLIC "…
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

#### The `.show` method causes each chart in the figure to be displayed sequentially

Here the `.set_options()` method is used to adjust the display size of the rendered charts.

```python
fig.set_options(size=(10,5)).show
```

```text
<Figure size 1000x500 with 1 Axes>
```

```text
<Figure size 1000x500 with 1 Axes>
```

### `.pdf` Creates a .pdf version of the plots
The `.pdf` method will generate a pdf of the chart(s) that form part of the figure. Each chart will appear sequentially in a single `pdf`. The generated `pdf` will be found in a sub-directory with the name that was given to the figure as the root of the `pdf` file that was generated.

```python
fig.pdf()
```

```text
<IPython.lib.display.IFrame at 0x24410387490>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

### ´.plot´ options

The  `.plot()` object has many options. Like Table these can be split into those that can be set only when the figure is instantiated and those that can be revised later using the `.set_options()` method. Both types of options are listed below.

**Line options** are set when the plot is created with the `.plot() `call and can only be set when the object is instantiated.

| Argument           | Default Value             | Description   |
|--------------------|---------------------------|----------------------------------------|
| pat                | '#Headline'               | Pattern with wildcard for variable names |
| datatype           | 'growth'                  | Defines the datatransformation displayes (cf. next table)     |
| mul                | 1.0                       | Multiplier of values before display             | 
| ax_title_template | ''                        | Template for each chart title| 


**Plot options** can be revised after the plot has been created. 

| Argument           | Default Value             | Description   |
|--------------------|---------------------------|----------------------------------------|
| rename             | True                      | If True use descriptions else variable names    |
| scenarios               | ''                        | Show for `.basedf/.lastdf` or selected scenarios                        | 
| name               | ''                        | Name for this display.                           | 
| custom_description | {}                        | Custom description, override default descriptions. |
title              | ''                        | Title (used when samefig=True).                  | 
| samefig            | False                     | If True, displays all chart in the same plot area. |
| ncol               | 2                         | Number of columns when samefig=True.            | 
| size               | (10, 6)                   | Specifies the size of each chart                | 
| legend             | True                      | If True, includes a legend in the display.       |
| smpl             | ('','')                      | set smpl for this plot       | 


Like tables, the transformation of the data displayed is controlled by the datatype options, whose parameters are identified below.

### **Plot Data Types and Scenarios**

Tables  display output based only on `.basedf` and `.lastdf`, the `.plot` function can also be used to visualize charts based on the scenarios stored in the `.keep_solutions` dictionary.

- If `scenarios=''`, `.plot` will display lines corresponding to the data shown in tables, which is based on `.basedf` and `.lastdf`.
- If `scenarios='<list of scenarios>'`, `.plot` will display lines for the data associated with the scenarios specified in the list. 
- If `scenarios='*'`, all available scenarios will be plotted.
- If `scenarios='base_last'`, `.basedf` and `.lastdf` will be plotted as scenarios.
   

The table below summarizes how the combination of `datatype` and `scenarios` determines the data displayed in the chart.

#### **Table: Datatype and Scenario Settings**

| **Datatype**    | **scenarios=''** or omitted | **scenarios='\<list of scenarios>'** (Multiple Scenarios) |
|:-------------|:------------------------------------------------------------------|:-----------------------------|
| **Value Views** | | |
| **growth** (default) | Growth rate (%) in the most recent dataset (`.lastdf`). | Growth rates for all scenarios. |
| **level**       | Values from `.lastdf`. | Values for all scenarios. |
| **gdppct**      | Percentage of GDP in `.lastdf`. | Percentage of GDP for all scenarios. |
| **qoq_ar**      | Quarterly growth (annualized) for quarterly models in `.lastdf`. | Quarterly growth (annualized) for all scenarios. |
| | | |
| **Difference Views** | | |
| **difgrowth**   | Change ($\Delta$) in growth rates between `.lastdf` and `.basedf`. | Change ($\Delta$) in growth rates between the first and other scenarios. |
| **diflevel**    | Change ($\Delta$) in values between `.basedf` and `.lastdf`. | Change ($\Delta$) in values between the first and other scenarios. |
| **difgdppct**   | Change ($\Delta$) in the percentage of GDP between `.basedf` and `.lastdf`. | Change ($\Delta$) in the percentage of GDP between the first and other scenarios. |
| **difqoq_ar**   | Change in quarterly growth (annualized) between `.basedf` and `.lastdf`. | Change ($\Delta$) in quarterly growth (annualized) between the first and other scenarios. |
| **difpctlevel** | Percentage change ($\Delta$) in values between `.basedf` and `.lastdf`. | Percentage change ($\Delta$) in values between the first and other scenarios. |
| | | |
| **`.basedf` Views** | | |
| **basegrowth**  | Growth rate (%) in `.basedf`. | Growth rates for the first scenario. |
| **baselevel**   | Values from `.basedf`. | Values for the first scenario. |
| **basegdppct**  | Percentage of GDP in `.basedf`. | Percentage of GDP for the first scenario. |
| **baseqoq_ar**  | Quarterly growth (annualized) in `.basedf`. | Quarterly growth (annualized) for the first scenario. |

#### The  ´samefig=True´ option causes charts  to be rendered on a grid 

Often a single call to `.plot()` will result in many charts being produced.  The `samefig=True` option will cause them to be displayed in a grid (rather than the alternative where each chart occupies the full width of the screen or page).  This approach both saves real-estate but actually facilitates the comparison of results  -- across variables, as in the case below; or when used in combination with the by_vars option, across scenarios.

```python
fig.set_options(samefig=True,title='An Example plot').show
```

```text
<Figure size 2000x600 with 2 Axes>
```

###  The `by_var` option determines  whether to show results by variable (False) or scenario (True)

By default, `by_var` is set to `True` and a separate chart is created for each variable in the `pat` pattern. If multiple scenarios are being inspected, each chart will have a separate line for each scenario. 

Setting `by_var` to `False` causes plot to generate the charts in the figure by scenario.  Each chart shows the value for all specified variables in one scenario, with following charts showing the results for different scenarios. 



| **by_var** | **a plot for each** | **a line in each plot for each** |
|------------------|---------------------|---------------------|
| **True** (default) | Variable            | Scenario            |
| False             | Scenario            | Variable            |

The example below sets both the `by_var` and `samefig` options to True.  As a result, the charts are displayed in a grid and data for GDP and household consumption (the variables) from one scenario are shown on each graph, with results for one scenario on each graph.

```python
mpak.plot(pat_plot,name='fig_by_scenario',
                       scenarios='Baseline|$25 increase in oil prices 2025-27',
                       datatype='level',samefig=True,
                       by_var=False,legend=False,mul=1/1_000_000).show
```

```text
<Figure size 2000x600 with 2 Axes>
```

The example also illustrates the use of the **legend** and **mul** options. The option `legend=False` suppresses the legend (as a box with all series description in one place) and instead causes the series labels to be placed to the right of the line of each rendered series.

The `mul=1/1_000_000` option causes the axis to be rendered in millions.  Notice python allows large numbers to be split by `_` which makes them more readable.  It is not necessary to do this.

Below the same two results are shown but organized by variable with the `by_var` option set to `True`.

```python
mpak.plot(pat_plot,name='fig_by_scenario',
                       scenarios='Baseline|$25 increase in oil prices 2025-27',
                       datatype='level',samefig=True,
                       by_var=True,legend=False,mul=1/1_000_000).show
```

```text
<Figure size 2000x600 with 2 Axes>
```

### The `scenarios=` option selects the scenarios to be displayed 

The `scenarios=` option allows the user to specify which scenarios (from the kept scenarios in the model object)  to use in generating the plots.  Scenarios names must be the exact match to the text used when the keep command was executed, and must be separated by the | symbol.




:class: tip
To find all names of the stored scenarios use:

```python
for key  in mpak.keep_solutions:
    print(key);
```

```text
Baseline
$25 increase in oil prices 2025-27
2.5% increase in C 2025-40
2.5% increase in C 2025-27 -- exog whole period
2.5% increase in C 2025-27 -- exog whole period --KG=True
2.5% increase in C 2025-27 -- temporarily exogenized
1% of GDP increase in FDI and private investment (AF shock)
```

In the example below, the same pattern as before is utilized (real GDP and real household expenditure), but the scenarios option indicates that the charts should be generated from three scenarios: 
1. Baseline
2. "$25 increase in oil prices 2025-27";   
3. "1\% of GDP increase in FDI and private investment (AF shock)".  

In this use-case the datatype='growth' causes the growth rate from each scenario to be rendered. 

```python
mpak.plot(pat_plot,name='fig_select',datatype='growth',samefig=True,
         scenarios='Baseline|$25 increase in oil prices 2025-27|1% of GDP increase in FDI and private investment (AF shock)').show
```

```text
<Figure size 2000x600 with 3 Axes>
```

#### The special scenario `base_last` 
The scenario option `base_last` will use the `.basedf` and  `.lastdf` as scenarios dataframes as the scenarios. 

```python
mpak.plot(pat_plot,name='fig_select',datatype='growth',samefig=True,
         scenarios='base_last').show
```

```text
<Figure size 2000x600 with 3 Axes>
```

#####  `.basename` `.lastname` can be used to rename the scenarios 

```python
mpak.basename = 'Unchanged policy'
mpak.lastname = 'AF shock '
mpak.plot(pat_plot,name='fig_select',datatype='growth',samefig=True,
         scenarios='base_last').show
```

```text
<Figure size 2000x600 with 3 Axes>
```

### Template for each chart title: `ax_title_template`

The text associated with each graph can be customized by using the `ax_title_template` option. 

`ax_title_template` can be sent to any arbitrary string.  If the string contains the special characters {var_name}, and/ or {var_description} or {compare} then the name of the variable being displayed (or its description) or the name of the baseline scenario will be substituted for the expression in the figure.

| Placeholder       | Replaced by                                     |
|-------------------|--------------------------------------------|
| `{var_name}`      | Variable Mnemonic                              |
| `{var_description}` | Variable description                      |
| `{compare}`       | First scenario used for comparison         |

In the example below, all three placeholders are utilized, and the text includes a LaTeX expression (the sub-string ```$\Delta\$```) bordered by `$` signs, which renders in the chart as the Greek symbol $\Delta$.

```python
mpak.plot(pat_plot,datatype='difgrowth',
          scenarios='Baseline|$25 increase in oil prices 2025-27|1% of GDP increase in FDI and private investment (AF shock)',
          samefig=True,
        ax_title_template= r'{var_name}:{var_description} \n %$\Delta$ vs {compare}' ).show
```

```text
<Figure size 2000x600 with 3 Axes>
```

### Joing plots with  `|` 


Like Tables, Plots can be concatenated together using the `|`  operator. This allows plots with different  datatypes to be displayed together. 

In the example below, results for GDP in each scenario and household consumption for each scenario are displayed first as growth rates, secondly as levels, and finally as changes in the growth rates.

The three separate figures are then joined in the figure called fig_, with the samefig=True flag set so that the six separate charts are arranged in a grid to facilitate reading and comparison.

```python
fig1 = mpak.plot(pat_plot,name='growth',scenarios='*',ax_title_template= r'Growth rates\n {var_name}:{var_description}')
fig2 = mpak.plot(pat_plot,datatype='level',scenarios='*',ax_title_template= r'Levels\n {var_name}:{var_description}')
fig3 = mpak.plot(pat_plot,datatype='difgrowth',name= 'dif',
                 ax_title_template= r'%$\Delta$ from {compare}\n {var_name}:{var_description}',
                 scenarios='*')
fig_ = (fig1 | fig2 | fig3).set_options(samefig=True,name='fig_')
fig_.show
```

```text
<Figure size 2000x1800 with 7 Axes>
```

### `.savefigs()` Saving plots in other formats. 

Plots are created using the `matplotlib` library. If charts are going to be used further downstream they can be saved to file using a wide range of formats. 

**`.savefigs()` options**

| **Parameter**      | **Type**  | **Description**                                                                                        | **Default**       |
|--------------------|-----------|--------------------------------------------------------------------------------------------------------|-------------------|
| `location`         | `str`     | The  folder in which to save the charts.                                                           | `'./graph'`       |
| `experimentname`   | `str`     | A subfolder under `location` where charts are saved.                                                   | `'experiment1'`   |
| `addname`          | `str`     | An additional name added to each figure filename.                                                      | `''` (empty string) |
| `extensions`       | `list`    | A list of  file extensions for saving the figures.                                               | `['svg']`         |
| `xopen`            | `bool`    | If `True`, open the saved figure locations in a web browser.                                           |                   |


Charts can be saved using the following formats: 

| **Extension**     | **Description**                             |
|-------------------|---------------------------------------------|
| `.png`            | Portable Network Graphics                   |
| `.jpg` or `.jpeg` | t Photographic Experts Group            |
| `.tif` or `.tiff` | Tagged Image File Format                    |
| `.bmp`            | Bitmap                                      |
| `.gif`            | Graphics Interchange Format                 |
| `.svg`            | Scalable Vector Graphics                    |
| `.pdf`            | Portable Document Format                    |
| `.eps`            | Encapsulated PostScript                     |
| `.ps`             | PostScript                                  |
| `.raw`            | Raw image data                              |
| `.rgba`           | Raw RGBA bitmap                             |
| `.pgf`            | Portable Graphics Format                    |


An example: 

```python
fig_for_saving = mpak.plot(pat_plot,name='for_saving')
fig_for_saving.savefigs()
```

```text
'Saved at: graph/experiment1'
```

In this example the sub-directory name where the files will be saved is changed to Scenario1 and two copies of the each chart is saved, once as an SVG file the other as a PDF, by setting the extensions option to a list `extensions=['svg','pdf']`.

```python
fig_for_saving = mpak.plot(pat_plot,name='for_saving',experimentname="Scenario1");
fig_for_saving.savefigs(extensions=['svg','pdf'])
```

```text
'Saved at: graph/experiment1'
```

## The `.text()` class

The `.text()` class is less complex than the `.plot()` and `.table()` procedures. It is mainly used implicitly in Reports, but can be declared as an object and used either in a report or on its own.

The text class allows the user to define three different types of text: `.text_text` `.html_text` and `.latex_text`.  These properties are optional and can be declared explicitly or implicitly. 


 |object|delimited by |contains|
 |------|---------|---|
 |.text_text| nothing |Plain text |
 |.html_text|\<html> \</html> |html text  |
 |.latex_text|\<latex> \</latex> |latex text |


A text object can be declared in the same way as the .plot or table(), called in conjunction with a model object. In the example below we create an object mytext, and implicitly set the `.text_text` property to "Some text".  The html and latex properties are undeclared.

```python
mytext=mpak.text("Some text")
mytext.show
```

```text
Some text
```

In the example below a more complicated object is declared.

Note this is a multiline text object, and that the plain text, html and latex properties are all declared implicitly with the html text demarcated by the `<html></html>` tokens and the latex text similarly demarcated by the <latex></latex> tokens.

```python
multimodeText=mpak.text(r'''
Example of plain output
This is the plain contents of a multiline text 
object.
<html><h1> Example of html output</h1>
This is the <b>html content</b> of a multiline text<b>
object.</b>
</html>
<latex>
\section*{Example of latex output}
This is the \textbf{latex content} of a  multiline text
\textbf{object} 
</latex>
''')
```

The three different kinds of text that can be included in a text object can be  extracted from the text object.

```python
print(multimodeText.text_text)
print(multimodeText.html_text)
print(multimodeText.latex_text)
```

```text

Example of plain output
This is the plain contents of a multiline text 
object.

<h1> Example of html output</h1>
This is the <b>html content</b> of a multiline text<b>
object.</b>


\section*{Example of latex output}
This is the \textbf{latex content} of a  multiline text
\textbf{object}
```

### Renderings

When rendered as text, the text object will ignore the html and latex portions. When rendered as html it will ignore the text and latex. The pdf rendering ignores text and html.


Because the text of the three internal components of the text object (plain text, html and latex} are independent of one another they can hold completely unrelated text.  While this might be useful in some contexts, in most, the three formulations should contain the same message even if the embellishments may differ somewhat given the capabilities of the rendering engine.

### Html renderings

Executing the text object directly from the command line will cause it to render as html. By the same token, the function `Display()` when called on a text object will render it as text.  NB: if there is no html object, the plain text version will be rendered.

```python
multimodeText
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

```python
display(multimodeText)
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

### Simple text rendering

The `.show` method will render the object as plain text.

```python
multimodeText.show
```

```text

Example of plain output
This is the plain contents of a multiline text 
object.
```

### Pdf rendering

Finally the `.pdf()` method will r4edner the object's latex contents rendered to a pdf file.

```python
multimodeText.pdf()
```

```text
<IPython.lib.display.IFrame at 0x243cc5869f0>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 80%
    :align: center

## Reports

Joined tables and plots offer significant flexibility, but have limitations. In particular, joined tables must cover the same time-period, and tables cannot be joined with plots, while transposed tables cannot be joined with other tables.

`Report`s in `ModelFlow` are containers that can contains figures, plots, tables of different dimension and text. Moreover, `Report` objects can be saved in a model object and regenerated on new data without requiring any additional effort by the user.

### Creating a report

A `report` can be generated by combining tables, plots, text and even other `report`s with the `+` operator. 

Below a small report is generated from two tables generated earlier in this chapter (`tab` and its transpose `tab_t` and a the plot object `fig`.

```python
mpak.smpl(2020,2040)
smallreport = (fig.set_options(samefig=True,name='fig_df',scenarios='base_last')+tab+tab_t).set_name('small report')
```

The code instantiates a new report object called `smallreport`.  The objects included in the report are brought together by the `+` operator.  

These include the previously defined object `fig`, whose options are adjusted with the `fig.set_options(samefig=True)` command.  This alters the resulting output such that the charts in the original fig are organized in a grid (`samefig=True`). The Report is completed by adding the previously defined  tables: ```tab``` with years as columns and, ```tab_t```with years as rows.

The method `.set_name('small report')` gives the `report` a name, which identifies the container (and determines where its file outputs will be saved if a pdf version is generated). 


The report name will be used in a dictionary of reports to identify the report. As a result, users should ensure that each report has a unique name.  

### Rendering a report

Reports can be displayed using the same mechanisms as tables and plot.  Either by executing the name of the report itself, or with the command display(reportname), or with reportname.show or reportname.pdf.

Below is the output from the `.show` method

```python
smallreport.show
```

```text
<Figure size 2000x600 with 3 Axes>
```

```text


GDP components
                         2025   2026   2027   2028   2029
                              --- Percent growth ---     
Real GDP                 2.08   2.42   2.64   4.36   2.91
HH. Cons Real            2.03   2.32   2.48   3.45   2.62
Investment real          1.10   1.46   1.82  12.46   2.98
Exports real             4.37   4.20   4.04   3.88   3.72
Imports real             3.10   3.10   3.02   4.68   2.84
Source: World Bank 


GDP components
     Real GDP HH. Cons Real Investment real Exports real Imports real
                          --- Percent growth ---                     
2022     0.66          0.80            0.70         4.71         3.00
2023     1.04          1.09            0.63         4.66         2.86
2024     1.60          1.60            0.79         4.53         2.99
2025     2.08          2.03            1.10         4.37         3.10
2026     2.42          2.32            1.46         4.20         3.10
2027     2.64          2.48            1.82         4.04         3.02
Source: World Bank
```

The reportname alone or display(report) will render the report as html (suitable for Jupyter Notebooks or a computer screen.  The figure is rendered as an interactive widget the same as a normal figure.

```python
display(smallreport)
```

```text
Accordion(children=(HTML(value='<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE svg PUBLIC "…
```

```text
DisplayContainerDef(mmodel=<
Model name                              :                  PAK 
Model structure                         :         Simultaneous 
Number of variables                     :                  839 
Number of exogeneous  variables         :                  461 
Number of endogeneous variables         :                  378 
>, reports=[DisplayKeepFigDef(mmodel=<
Model name                              :                  PAK 
Model structure                         :         Simultaneous 
Number of variables                     :                  839 
Number of exogeneous  variables         :                  461 
Number of endogeneous variables         :                  378 
>, spec=DisplaySpec(display_type='', options=Options(name='fig_df', foot='', rename=True, decorate=False, width=5, custom_description={}, title='Results from the most-recent simulation', chunk_size=0, timeslice=[], max_cols=6, last_cols=3, ncol=2, samefig=True, size=(10, 6), legend=True, transpose=False, scenarios='base_last', smpl=('', ''), landscape=False, latex_text='', html_text='', text_text='', markdown_text=''), lines=[Line(datatype='growth', scale='linear', kind='line', centertext='', rename=False, dec=2, pat='*NYGDPMKTPKN *NECONPRVTKN  ', latexfont='', by_var=True, mul=1.0, yunit='', datatype_desc='', ax_title_template='', textlinetype='')]), name='fig_df'), MyDataClass(Options(name='My_first_table', foot='Source: World Bank ', rename=True, decorate=False, width=5, custom_description={}, title='GDP components', chunk_size=0, timeslice=[], max_cols=6, last_cols=3, ncol=2, samefig=False, size=(10, 6), legend=True, transpose=False, scenarios='', smpl=('', ''), landscape=False, latex_text='', html_text='', text_text='', markdown_text='') [Line(datatype='level', scale='linear', kind='line', centertext='--- Percent growth ---', rename=False, dec=2, pat='#Headline', latexfont='', by_var=True, mul=1.0, yunit='', datatype_desc='', ax_title_template='', textlinetype='textline'), Line(datatype='growth', scale='linear', kind='line', centertext='', rename=False, dec=2, pat=' *NYGDPMKTPKN *NECONPRVTKN  *NEGDIFTOTKN *NEEXPGNFSKN *NEIMPGNFSKN ', latexfont='', by_var=True, mul=1.0, yunit='', datatype_desc='', ax_title_template='', textlinetype='')]), MyDataClass(Options(name='A_transposed_table', foot='Source: World Bank ', rename=True, decorate=False, width=5, custom_description={}, title='GDP components', chunk_size=0, timeslice=[], max_cols=6, last_cols=3, ncol=2, samefig=False, size=(10, 6), legend=True, transpose=True, scenarios='', smpl=('', ''), landscape=False, latex_text='', html_text='', text_text='', markdown_text='') [Line(datatype='level', scale='linear', kind='line', centertext='--- Percent growth ---', rename=False, dec=2, pat='#Headline', latexfont='', by_var=True, mul=1.0, yunit='', datatype_desc='', ax_title_template='', textlinetype='textline'), Line(datatype='growth', scale='linear', kind='line', centertext='', rename=False, dec=2, pat=' *NYGDPMKTPKN *NECONPRVTKN  *NEGDIFTOTKN *NEEXPGNFSKN *NEIMPGNFSKN ', latexfont='', by_var=True, mul=1.0, yunit='', datatype_desc='', ax_title_template='', textlinetype='')])], name='small_report', options={})
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

The PDF rendering will show each chart separately (like the .show command) or if the `samefig=True` option is selected (as is the case here) the charts will be organized in a grid.

```python
smallreport.pdf()
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 80%
    :align: center

### A report with different text 

Unlike a table or a plot, a report can be customized by adding unlimited amounts of text.

In the example below text is entered using three formats -- plain text, Latex, and html.

Doing so in this way allows each rendering engine to do its best.  

If separate text is not entered between the \<html> and \</html> tags or between \<latex\>\</latex\> tags then the html and pdf outputs will use the plain text inputs.

If the text under html or latex tags differs from the plain text, the latex text will be used for pdfs and the html for html outputs.


Below the same content as in the small report but with annotated with text.

```python
textreport=(r'''
Text version: Real GDP and household consumption growth under alternative Carbon taxation regimes.
<latex>
\textbf{Latex version:} Real GDP and household consumption growth under alternative Carbon taxation regimes.
</latex>
<html>
<h1>Html version:</h1>
<h2> Real GDP and household consumption growth under alternative Carbon taxation regimes.</h2>
</html>
''' + 
fig.set_options(samefig=True)+
r'''Real GDP and Expenditure components growth rates following a 1% of GDP injection of foreign investment in 2027
<latex>
\textbf{Real GDP and Expenditure components growth rates following a 1\% of GDP injection of foreign investment in 2027}
</latex>
<html>
<h1>Real GDP and Expenditure components growth rates following a 1% of GDP injection of foreign investment in 2027</h1>
</html>''' +        
tab_t).set_name('report_with_text')
```

When rendered as text, no special formatting of the text is done.

```python
textreport.show
```

```text



Text version: Real GDP and household consumption growth under alternative Carbon taxation regimes.
```

```text
<Figure size 2000x600 with 2 Axes>
```

```text


Real GDP and Expenditure components growth rates following a 1% of GDP injection of foreign investment in 2027



GDP components
     Real GDP HH. Cons Real Investment real Exports real Imports real
                          --- Percent growth ---                     
2022     0.66          0.80            0.70         4.71         3.00
2023     1.04          1.09            0.63         4.66         2.86
2024     1.60          1.60            0.79         4.53         2.99
2025     2.08          2.03            1.10         4.37         3.10
2026     2.42          2.32            1.46         4.20         3.10
2027     2.64          2.48            1.82         4.04         3.02
Source: World Bank
```

When rendered as html, the html text is used and html formatting is rendered.

```python
textreport
```

```text
Accordion(children=(HTML(value='<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE svg PUBLIC "…
```

```text
DisplayContainerDef(mmodel=<
Model name                              :                  PAK 
Model structure                         :         Simultaneous 
Number of variables                     :                  839 
Number of exogeneous  variables         :                  461 
Number of endogeneous variables         :                  378 
>, reports=[DisplayTextDef(mmodel=<
Model name                              :                  PAK 
Model structure                         :         Simultaneous 
Number of variables                     :                  839 
Number of exogeneous  variables         :                  461 
Number of endogeneous variables         :                  378 
>, spec=DisplaySpec(display_type='', options=Options(name='some_text', foot='', rename=True, decorate=True, width=20, custom_description={}, title='', chunk_size=0, timeslice=[], max_cols=6, last_cols=3, ncol=2, samefig=False, size=(10, 6), legend=True, transpose=False, scenarios='', smpl=('', ''), landscape=False, latex_text='\n\\textbf{Latex version:} Real GDP and household consumption growth under alternative Carbon taxation regimes.\n', html_text='\n<h1>Html version:</h1>\n<h2> Real GDP and household consumption growth under alternative Carbon taxation regimes.</h2>\n', text_text='\nText version: Real GDP and household consumption growth under alternative Carbon taxation regimes.\n', markdown_text='\nText version: Real GDP and household consumption growth under alternative Carbon taxation regimes.\n'), lines=[]), name='some_text'), DisplayKeepFigDef(mmodel=<
Model name                              :                  PAK 
Model structure                         :         Simultaneous 
Number of variables                     :                  839 
Number of exogeneous  variables         :                  461 
Number of endogeneous variables         :                  378 
>, spec=DisplaySpec(display_type='', options=Options(name='My_first_plot', foot='', rename=True, decorate=False, width=5, custom_description={}, title='Results from the most-recent simulation', chunk_size=0, timeslice=[], max_cols=6, last_cols=3, ncol=2, samefig=True, size=(10, 6), legend=True, transpose=False, scenarios='', smpl=('', ''), landscape=False, latex_text='', html_text='', text_text='', markdown_text=''), lines=[Line(datatype='growth', scale='linear', kind='line', centertext='', rename=False, dec=2, pat='*NYGDPMKTPKN *NECONPRVTKN  ', latexfont='', by_var=True, mul=1.0, yunit='', datatype_desc='', ax_title_template='', textlinetype='')]), name='My_first_plot'), DisplayTextDef(mmodel=<
Model name                              :                  PAK 
Model structure                         :         Simultaneous 
Number of variables                     :                  839 
Number of exogeneous  variables         :                  461 
Number of endogeneous variables         :                  378 
>, spec=DisplaySpec(display_type='', options=Options(name='some_text', foot='', rename=True, decorate=True, width=20, custom_description={}, title='', chunk_size=0, timeslice=[], max_cols=6, last_cols=3, ncol=2, samefig=False, size=(10, 6), legend=True, transpose=False, scenarios='', smpl=('', ''), landscape=False, latex_text='\n\\textbf{Real GDP and Expenditure components growth rates following a 1\\% of GDP injection of foreign investment in 2027}\n', html_text='\n<h1>Real GDP and Expenditure components growth rates following a 1% of GDP injection of foreign investment in 2027</h1>\n', text_text='Real GDP and Expenditure components growth rates following a 1% of GDP injection of foreign investment in 2027\n', markdown_text='Real GDP and Expenditure components growth rates following a 1% of GDP injection of foreign investment in 2027\n'), lines=[]), name='some_text'), MyDataClass(Options(name='A_transposed_table', foot='Source: World Bank ', rename=True, decorate=False, width=5, custom_description={}, title='GDP components', chunk_size=0, timeslice=[], max_cols=6, last_cols=3, ncol=2, samefig=False, size=(10, 6), legend=True, transpose=True, scenarios='', smpl=('', ''), landscape=False, latex_text='', html_text='', text_text='', markdown_text='') [Line(datatype='level', scale='linear', kind='line', centertext='--- Percent growth ---', rename=False, dec=2, pat='#Headline', latexfont='', by_var=True, mul=1.0, yunit='', datatype_desc='', ax_title_template='', textlinetype='textline'), Line(datatype='growth', scale='linear', kind='line', centertext='', rename=False, dec=2, pat=' *NYGDPMKTPKN *NECONPRVTKN  *NEGDIFTOTKN *NEEXPGNFSKN *NEIMPGNFSKN ', latexfont='', by_var=True, mul=1.0, yunit='', datatype_desc='', ax_title_template='', textlinetype='')])], name='report_with_text', options={})
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

Finally when rendered as a pdf, the pdf specific text and formatting is used.

```python
textreport.pdf()
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 80%
    :align: center

## Storing `.reports` definitions for later use

The definitions of the different reports can be stored in the `.reports` dictionary that is part of the model object so they can be retrieved and used later. 

Notice it is the definition not the content of the table which is stored. So when applied later it is the values of the variables of that model object (notably the `.lastdf` and `.basedf` dataframes of the model object at that point in time that will be rendered.  

The `.reports` dictionary is saved when the model is dumped with `.modeldump` and restored when the function `model.modelload()` is used to load a model. 


A `table`, `plot` and `text` objects are each special cases of a `report` and can be stored as well.

### The method `.add_report` adds a report  to the `.reports` dictionary. 

```python
mpak.add_report([tab_large,smallreport,textreport])
```

```text
Reports added to report repo: large_table, small_report, report_with_text
```

```python
for key in mpak.reports:
    print(key);
```

```text
large_table
small_report
report_with_text
```

### The `.get_report` method creates a report from a stored specification. 

A report can be retrieved from the model object and assigned to a variable.  Changes to that new report will not be stored unless explicitly saved.

```python
newreport=mpak.get_report('small_report').show
```

```text
<Figure size 2000x600 with 3 Axes>
```

```text


GDP components
                         2025   2026   2027   2028   2029
                              --- Percent growth ---     
Real GDP                 2.08   2.42   2.64   4.36   2.91
HH. Cons Real            2.03   2.32   2.48   3.45   2.62
Investment real          1.10   1.46   1.82  12.46   2.98
Exports real             4.37   4.20   4.04   3.88   3.72
Imports real             3.10   3.10   3.02   4.68   2.84
Source: World Bank 


GDP components
     Real GDP HH. Cons Real Investment real Exports real Imports real
                          --- Percent growth ---                     
2022     0.66          0.80            0.70         4.71         3.00
2023     1.04          1.09            0.63         4.66         2.86
2024     1.60          1.60            0.79         4.53         2.99
2025     2.08          2.03            1.10         4.37         3.10
2026     2.42          2.32            1.46         4.20         3.10
2027     2.64          2.48            1.82         4.04         3.02
Source: World Bank
```

### Re-using a report on multiple simulation results

In this example the small_report is populated with results from three different simulations and the results displayed (see the above listing for names of scenarios in the kept_scenarios dictionary).

```python
mpak.basedf = mpak.keep_solutions['Baseline']
mpak.lastdf = mpak.keep_solutions['1% of GDP increase in FDI and private investment (AF shock)']
mpak.smpl(2025,2029);


firstreport=mpak.get_report('small_report').set_name('firstreport').show
```

```text
<Figure size 2000x600 with 3 Axes>
```

```text


GDP components
                         2025   2026   2027   2028   2029
                              --- Percent growth ---     
Real GDP                 2.08   2.42   2.64   4.36   2.91
HH. Cons Real            2.03   2.32   2.48   3.45   2.62
Investment real          1.10   1.46   1.82  12.46   2.98
Exports real             4.37   4.20   4.04   3.88   3.72
Imports real             3.10   3.10   3.02   4.68   2.84
Source: World Bank 


GDP components
     Real GDP HH. Cons Real Investment real Exports real Imports real
                          --- Percent growth ---                     
2022     0.66          0.80            0.70         4.71         3.00
2023     1.04          1.09            0.63         4.66         2.86
2024     1.60          1.60            0.79         4.53         2.99
2025     2.08          2.03            1.10         4.37         3.10
2026     2.42          2.32            1.46         4.20         3.10
2027     2.64          2.48            1.82         4.04         3.02
Source: World Bank
```

```python
mpak.basedf = mpak.keep_solutions['Baseline']
mpak.lastdf = mpak.keep_solutions['$25 increase in oil prices 2025-27']
mpak.smpl(2025,2029);
secondreport=mpak.get_report('small_report').set_name('secondreport').show
```

```text
<Figure size 2000x600 with 3 Axes>
```

```text


GDP components
                         2025   2026   2027   2028   2029
                              --- Percent growth ---     
Real GDP                 1.18   2.46   2.85   3.81   3.08
HH. Cons Real            0.68   2.15   2.60   3.94   2.97
Investment real          1.23   0.99   1.62   2.02   2.93
Exports real             4.36   4.21   4.06   3.92   3.78
Imports real             1.57   1.88   2.45   3.98   3.74
Source: World Bank 


GDP components
     Real GDP HH. Cons Real Investment real Exports real Imports real
                          --- Percent growth ---                     
2022     0.66          0.80            0.70         4.71         3.00
2023     1.04          1.09            0.63         4.66         2.86
2024     1.60          1.60            0.79         4.53         2.99
2025     1.18          0.68            1.23         4.36         1.57
2026     2.46          2.15            0.99         4.21         1.88
2027     2.85          2.60            1.62         4.06         2.45
Source: World Bank
```

```python
mpak.basedf = mpak.keep_solutions['Baseline']
mpak.lastdf = mpak.keep_solutions['2.5% increase in C 2025-27 -- exog whole period --KG=True']
mpak.smpl(2025,2029);
thirdreport=mpak.get_report('small_report').set_name('thirdreport').show
```

```text
<Figure size 2000x600 with 3 Axes>
```

```text


GDP components
                         2025   2026   2027   2028   2029
                              --- Percent growth ---     
Real GDP                 4.13   2.49   2.62   2.73   2.84
HH. Cons Real            4.58   2.32   2.48   2.59   2.69
Investment real          2.50   2.12   2.23   2.45   2.69
Exports real             4.35   4.14   3.96   3.80   3.66
Imports real             5.44   3.27   3.18   3.08   2.99
Source: World Bank 


GDP components
     Real GDP HH. Cons Real Investment real Exports real Imports real
                          --- Percent growth ---                     
2022     0.66          0.80            0.70         4.71         3.00
2023     1.04          1.09            0.63         4.66         2.86
2024     1.60          1.60            0.79         4.53         2.99
2025     4.13          4.58            2.50         4.35         5.44
2026     2.49          2.32            2.12         4.14         3.27
2027     2.62          2.48            2.23         3.96         3.18
Source: World Bank
```

### Reports are stored in `.pcim` files, and restored when a model is loaded

Once a report has been added to the model object it will be saved with the model object. 

Below we save the current state of `mpak`, inclusive of the reports that were added to the model object.
So first dump the model and data: 

```python
mpak.modeldump('testpak',keep=True)
```

Next a new model object is declared tempmodel, and the state and data from the saved mpak are read into that object.  

```python
xpak,baseline = model.modelload('testpak',run=True  )
```

```text
Zipped file read:  testpak.pcim
```

Next the `.basedf` and `.lastdf` dataframes are set equal to the data frames from the kept Baseline and investment shock scenarios.

```python
xpak.basedf = xpak.keep_solutions['Baseline']
xpak.lastdf = xpak.keep_solutions['1% of GDP increase in FDI and private investment (AF shock)']
```

With that, the reports can be run (and should show precisely the same results).

```python
trep=xpak.get_report('report_with_text')
trep.show
```

```text



Text version: Real GDP and household consumption growth under alternative Carbon taxation regimes.
```

```text
<Figure size 2000x600 with 2 Axes>
```

```text


Real GDP and Expenditure components growth rates following a 1% of GDP injection of foreign investment in 2027



GDP components
     Real GDP HH. Cons Real Investment real Exports real Imports real
                          --- Percent growth ---                     
2022     0.66          0.80            0.70         4.71         3.00
2023     1.04          1.09            0.63         4.66         2.86
2024     1.60          1.60            0.79         4.53         2.99
2025     4.13          4.58            2.50         4.35         5.44
2026     2.49          2.32            2.12         4.14         3.27
2027     2.62          2.48            2.23         3.96         3.18
Source: World Bank
```

## [].rtable and [].rplot - reports from []
Report tables and plots can also be created directly from the variable selector `[]`. The purpose is to enable easy reuse of variable selection like this. 

```python
mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN'].growth.rename().plot();
```

```text
<Figure size 1000x200 with 2 Axes>
```

To a plot like this: 

```python
mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN'].rplot(samefig=1).show
```

```text
<Figure size 2000x600 with 2 Axes>
```

Or a table like this: 

```python
mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN'].rtable(samefig=1).show
```

```text
Table
                         2025   2026   2027   2028   2029
                              --- Percent growth ---     
Real GDP                 4.13   2.49   2.62   2.73   2.84
HH. Cons Real            4.58   2.32   2.48   2.59   2.69
```

The  [].rtable and [].rplot are just wrappers around the `model instance.plot` and 
`model instance.table` so the arguments - except the variable selection - are the same, 
and the returne values can be used just the returned values of `model instance.plot` and 
`model instance.table`. So `+` and `|` can also be used. 

```python
(mpak.text('Growth in {cty_name}') + 
mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN'].rplot(samefig=1) + 
mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN'].rtable()).show
```

```text


Growth in Pakistan
```

```text
<Figure size 2000x600 with 2 Axes>
```

```text


Table
                         2025   2026   2027   2028   2029
                              --- Percent growth ---     
Real GDP                 4.13   2.49   2.62   2.73   2.84
HH. Cons Real            4.58   2.32   2.48   2.59   2.69
```

## Some other supported outputs

Below are an illustration of some charts and table features not discussed above, which  may be of interest in some contexts:

###  Heatmaps

For some model types heatmaps can be helpful, and they come out of the box. 

```python
with mpak.set_smpl(2020,2030):
    mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN'].pct.rename().heat(title='Growth rates',annot=True,dec=1,size=(10,3))
```

```text
<Figure size 1000x300 with 2 Axes>
```
