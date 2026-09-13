# The World Bank's MFMod Framework in Python with Modelflow - The World Bank's MFMod Framework and Modelflow


# The World Bank's MFMod Framework and Modelflow

# Introduction

This manual describes the implementation of the World Bank's `MFMod` Framework  \[{cite:t}`burns_world_2019`)\] using the open source modeling package `ModelFlow`. (Hansen, 2023 [https://ibhansen.github.io/doc/index](https://ibhansen.github.io/doc/index)). 

The impetus for this paper and the work that it summarizes was to make available to a wider constituency the work that the Bank has done over the past several decades to build and develop Macro-structural models[^1] for developing countries. 



## The MFMod Framework at the World Bank

MFMod is the World Bank's work-horse macro-structural economic modeling framework. It exists both as a linked system of 184 country-specific models that can be solved independently or as a larger system (```MFMod```), and as a series of  standalone customized models, known collectively as MFMod Standalones (MFModSA). These Standalone models have been developed from the central model to fit the specific needs of individual countries. Both the central and Standalone models were developed using the `EViews` modeling language, and are run in that environment directly or through the intermediation of an easy-to-use excel front-end developed by the Bank.


The main ```MFMod``` global model evolved from earlier macro-structural models developed during the 2000s to strengthen the basis for the forecasts produced by the World Bank. Some examples of these models were released on the World Bank's isimulate platform [(https://isimulate.worldbank.org)](https://isimulate.worldbank.org) early in 2010, along with several CGE models dating from this period. These earlier models were substantially extended into what has become the main MFMod model. Since 2015, MFMod has been the Bank's main tool for forecasting and economic analysis, and is used by all of the Bank's country economists for the World Bank's twice annual forecasting exercise *The Macro Poverty Outlook* (https://www.worldbank.org/en/publication/macro-poverty-outlook).


The main documentation for `MFMod` are {cite:t}`burns_world_2019` and {cite:t}`burns_estimating_2019`.





This chapter provides a high-level overview of the MFMod system and the motivation for releasing some of the models in an open-source format using the `ModelFlow` python package.

### Climate-aware version of MFMod
Most recently, the Bank has extended the standard `MFMod` framework to incorporate the main features of climate change {cite:t}`burns_climate_2021`-- both in terms of the impact of the economy on climate (principally through green-house gas emissions, like $CO_2, N_{2}O, CH_4, ...$) and the impact of the changing climate (higher temperatures, changes in rainfall quantity and variability, increased incidence of extreme weather) on the economy (agricultural output, labor productivity, physical damages due to extreme weather events, sea-level rises etc.). So called co-benefits from climate policy, such as pollution reduction, changes in informality, health and productivity effects are also incorporated into the `MFMod CC` models. For the moment {cite:t}`burns_climate_2021` is the most up to date documentation of the `MFMod CC` models, but the models have evolved substantially from the initial climate model described there.


As of June 2025, variants of the model initially described in {cite:t}`burns_climate_2021`, have been developed for 70 countries and underpin the economic analysis contained in the majority of the World Bank's  *Country Climate Development Reports* [(https://www.worldbank.org/en/publication/country-climate-development-reports)](https://www.worldbank.org/en/publication/country-climate-development-reports).


## Early steps to bring the MFMod system to the broader economics community

Bank staff were quick to recognize that the models built for its own needs could be of use to the broader economics community. An initial project, `isimulate`, made several versions of this earlier model available for simulation on the *isimulate platform* [(https://isimulate.worldbank.org)](https://isimulate.worldbank.org) in 2007, and these models continue to be available there.  The `isimulate` platform continues to house early versions of the MFMod system. While the platform  allows simulation of these and other models, it does not give researchers access to the code or the ability to construct complex simulations.


In another effort to make models widely available a large number (more than 100 as of June 2025) customized stand-alone models (collectively known as called MFModSA - MacroFiscalModel StandAlones) have been built from the main model. Typically developed for a country-client (Ministry of Finance, Economy or Planning or Central Bank), these Standalones extend the standard model by incorporating additional details not in the standard model that are of specific import to different economies and the country-clients for whom they were built. These features frequently include: a more detailed breakdown of the sectoral make up of an economy, more detailed fiscal and monetary accounts, and other economically important features of the economy that may exist only inside the aggregates of the standard model.

In addition to making customized models available to client governments, since 2013 the World Bank has conducted training and dissemination around these customized versions of MFMod, designed to train government officials in the use of these models, their maintenance, modification and revision. 


## Moving the framework to an open-source footing

Models in the `MFMod` family are normally built and simulated using [EViews](https://www.eviews.com), a proprietary econometric and modeling package. While offering many advantages for model development and maintenance, its cost may be a barrier to clients in developing countries.  As a result, the World Bank joined with Ib Hansen, a Danish economist formerly with the European Central  Danish Central Banks, who over the years has developed ```ModelFlow``` a generalized solution engine for economic models written in Python. Together with World Bank, Hansen has worked to extend `ModelFlow` so that `MFMod` models can be ported and run in the framework.  

This paper reports on the results of these efforts. In particular, it provides step-by-step instructions on how to install the `ModelFlow` framework, import a World Bank macrostructural model,  perform simulations with that model and report results using the many analytical and reporting tools that have been built into `ModelFlow`.  It is not a manual for `ModelFlow`, such a manual can be found [here (https://ibhansen.github.io/doc/index)](https://ibhansen.github.io/doc/index). Nor is this paper documentation for the `MFMod` system, such documentation can be found here {cite:t}`burns_world_2019`,{cite:t}`burns_estimating_2019`, {cite:t}`burns_macroeconomic_2021`, and here {cite:t}`burns_climate_2021`) for the specific models described and worked with below.

[^1]: Economic modeling has a long tradition at the World Bank.  Initial World Bank economic models were linear programming planning models {cite:t}`chenery_studies_1971`. These were followed with CGE models {cite:t}`dervis_general_1982`. Indeed, the popular modeling package [GAMS](https://www.gams.com/about/company/), which is widely used to solve CGE and Linear Programming models, started out as a project at the World Bank in the 1970s {cite:t}`meeraus_general_1982`. The RMSM-X model {cite:t}`addison_world_1989` was an effort to provide a simpler consistency framework for economic forecasting. Work on the macrostructural models that were precursors to `MFMod`began in the early 2000s and were used within the Bank beginning in 2006, although versions were not released to the public until the end of the decade.

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

# Macrostructural models

The economics profession uses a wide range of models for different purposes.  Macro-structural models (also known as semi-structural or Macro-econometric models) are a class of models that seek to summarize the most important interconnections and determinants of economic activity in an economy. Computable General Equilibrium (CGE), and Dynamic Stochastic General Equilibrium (DSGE) models are other classes of models that also seek, using somewhat different methodologies, to capture the main economic channels by which the actions of agents (firms, households, governments) interact and help determine the structure, level and rate of growth of economic activity in an economy. 

Typically, organizations, including the World Bank, use all of these tools, privileging one or the other for specific purposes. Macrostructural models like those that comprise the `MFMod` framework are widely used by Central Banks, Ministries of Finance; and professional forecasters to generate forecasts and to undertake policy analysis. 

While macrostructural models fell out of favor with academic economists, they remain central tools in policy making and forecasting circles. In a series of discussions and papers Olivier Blanchard {cite:t}`blanchard_future_2018`, former Chief Economist at the International Monetary Fund, concluded that academic economists are wrong to discard out-of-hand policy models such as macro-structural models.  Those conclusions were reinforced in a recent collection of papers by leading academics {cite:t}`vines_rebuilding_2020` that argued that until a better framework could be developed, "policy-makers need to rely on structural economic models and the detailed econometric work which they embody" rather than the DSGE models favored by academics.

:class: tip

This Chapter provides a high-level introduction to macro-structural models in general and the `MFMod` system in particular. It presents them as systems that balance theoretical rigor with practical utility, enabling comprehensive insights into economic systems. Macrostructural models are widely used by policymakers for scenario analysis and forecasting and `MFmod` is the main framework used by the World Bank for analyzing the economic progress and policies of developing economies.

It notes that these models are effectively a system of equations that describe the economic transactions (flow of funds) that occur in the economy, including those captured by the main economic accounting systems, including:

* GDP and its subcomponents from the National Accounts expenditure, production, and income accounts.
* Detailed government, monetary policy, and balance of payments accounts.
* General equilibrium flow of funds linking households, firms, government, and foreign sectors.

The chapter introduces key concepts like:

- **Equation Types**:
  - Identities: Accounting rules that always hold (e.g., GDP = C + I + G + X - M).
  - Behavioral Equations: Relationships based on economic theory, that are estimated econometrically and subject to error.

- **variable Types**:
  - Exogenous Variables: Inputs determined outside the model, such as global oil prices.
  - Endogenous Variables: Variables determined by equations
  
The chapter also provides a brief description of `ModelFlow` the python package used to run World Bank models in an open source context.

## A system of equations

Mathematically, a macro-structural model is a system of equations comprised of two kinds of equations and three kinds of variables. Variables that are determined by an equation are classified by the type of equation that determines them, variables without an equation are deemed exogenous as they are determined outside of the model.  

Models in the `MFMod` framework are comprised of:

* ```Identities``` variables: that are determined by an identity: an equation that is a well-defined accounting rule that always holds. The famous GDP formula Y=C+I+G+(X-M) is one such identity, it indicates that GDP at market prices is **definitionally** equal to Consumption plus Investment plus Government spending plus Exports less Imports.  The equation is an identity and the variable (Y in this instance) is also called an identity.



* ```Behavioral``` variables that are determined by equations that attempt to statistically summarize the economic (vs accounting) relationship between variables, where the structure of the statistical relationship is derived from economic theory, but the sensitivities of different causal variables is estimated from the data. Thus, the neo-classical equation that says Real Consumption is determined by households maximizing their utility through the consumption of goods and services subject to a budget constraint is a behavioral equation. Because these behavioral equations only explain part of the variation in the variable they seek to explain, and because the sensitivities of variables to the changes in other variables are uncertain, these equations and their parameters are  typically estimated econometrically and are subject to error.



* ```Exogenous``` variables: do not have equations and are not determined by the model. Typically there are set either by assumption or from data external to the model.  For an individual country model, the exogenous variables might include the global price of crude oil because the level of activity of a small economy itself is unlikely to affect the world price of oil. Similarly, the rate of growth of GDP in other economies may be treated as an exogenous variable, important to determining exports in the modeled developing country unlikely to be affected by activity in the modeled country (small country assumption). 


What dictates whether a variable is exogenous or endogenous is not set in stone. A variable that is exogenous in one model may be endogenous in another. For example in an single-country model, GDP growth of other countries may be exogenous, but in a multi-country model the GDP growth of those other countries would likely be endogenous (determined by the model).

Mathematically, a system of equations can be expressed as below:

\begin{align*}
y_t^1  &=  f^1(y_{t+u}^1...,y_{t+u}^n...,y_t^2...,y_{t}^n...y_{t-r}^1...,y_{t-r}^n,x_t^1...x_{t}^k,...x_{t-s}^1...,x_{t-s}^k) \\
y_t^2  &=  f^2(y_{t+u}^1...,y_{t+u}^n...,y_t^1...,y_{t}^n...y_{t-r}^1...,y_{t-r}^n,x_t^1...x_{t}^k,...x_{t-s}^1...,x_{t-s}^k) \\
\vdots \\
y_t^n  &=  f^n(y_{t+u}^1...,y_{t+u}^n...,y_t^1...,y_{t}^{n-1}...y_{t-r}^1...,y_{t-r}^n,x_t^1...x_{t}^r,x..._{t-s}^1...,x_{t-s}^k)
\end{align*}

where $ y_t^1 $ is one of n endogenous variables and $x_t^1$ is one of k exogenous variables. To have a solution the system must have as many equations as there are unknown (endogenous variables).

Substituting the variable mnemonics Y,C,I,G,X,M for the y's and x's above, a simple macrostructural model can be written as as a system of 6 equations in 6 unknowns:

\begin{align*}
Y_t  &=  C_t+I_t+G+t+ (X_t-M_t) \\
C_t &= c(C_{t-1},C_{t-2},I_t,G_t,X_t,M_t,P_t)\\
I_t &= i(I_{t-1},I_{t-2},C_t,G_t,X_t,M_t,P_t)\\
G_t &= g(G_{t-1},G_{t-2},C_t,I_t,X_t,M_t,P_t)\\
X_t &= x(X_{t-1},X_{t-2},C_t,I_t,G_t,M_t,P_t,P^f_t)\\
M_t &= m(M_{t-1},M_{t-2},C_t,I_t,G_t,X_t,P_t,P^f_t)
\end{align*}
 
Where $Y_t$ is an identity and $C_t, I_t, G_t, X_t, M_t$ are behavioral variables and $P_t, P^f_t$ (domestic and foreign prices, respectively) are exogenous in this simple model. 

Such a system of equations can then be solved for the endogenous variables $Y_t, C_t, I_t, G_t, X_t$ and $M_t$ as a function of the exogenous variables in the system, notably as written above $P_t$ and $P^f_t$, and the estimated parameters and functional forms of the behavioral equations that link them, represented here by: $c(), i(), g(), x()$ and $m()$.

## The MFMod Framework


World Bank models are somewhat more complex and comprise many more sectors, notably:

* GDP and sub components calculated from all three perspectives in Real, Nominal and implicit deflator terms
    * Expenditure Accounts
        * C + I + G + X - M
    * Production accounts (the level of detail varies from model to model)
        * Primary sector (Agriculture, Mining, Forestry)
        * Secondary Sector (Manufacturing, Industry)
        * Tertiary sector (Services, retail, Public Administration, Wholesale)
        * Energy sector (primarily broken out in climate models)
    * Income accounts (Wage Bill, Gross Operating surplus (Profits), Combined incomes)
* Government Accounts
    * Revenues
        * Personal income taxes
        * Corporate income taxes
        * Value added taxes (Sales taxes)
        * Excise Taxes
        * Trade taxes (Export taxes, import duties)
        * Other taxes, (Fees and charges)
        * Grants and Transfers
    * Expenditures
        * Goods and services
        * Wages and salaries
        * Transfers to households
        * Subsidies to households
        * Subsides to firms
        * Capital expenditures (New projects and repairs to existing capital stock)
        * Grants and Transfers
        * Interest payments on the debt
    * Balances
        * Overall fiscal balance
        * Primary fiscal balance
        * Debt (Domestic, Foreign)
* Monetary Policy
    * Main policy rate
    * Money Supplies
    * International Reserves
    * Credit to the private sector
* Balance of Payments
    * Current Account
        * Primary Exports and Imports (Merchandise and Services)
        * Secondary Exports and Services (Remittances, repatriation of profits, labor)
    * Financial Account
        * Equity financing
        * Debt financing
        * FDI
  
Within the models, these accounts are related in a general equilibrium flow of funds perspective, where households (as the owners of the factors of production) supply labor and capital to firms and the government via factor markets and earn salaries and profits paid for by the firms. Their earnings are spent on goods and services, taxes or saved, with their savings being intermediated through financial markets where they are either loaned to domestic firms, households and the government or to foreign firms and governments. Domestic households, firms and the government also lend to and borrow from the  foreign sector.  The output of firms is sold to households, the government or the rest of the world and the intermediate inputs they require are purchased from other firms, or the rest of the world.











Importantly every expenditure of a given actor in the economy is a revenue of another and, as a result, has impacts on the rest of the economy.  This flow of funds idea is common to most macroeconomic models and is illustrated in the following schematic.


```{figure} ./FlowofFunds.png
---
height: 225px
name: Flow of Funds diagram
---
The Flow of funds in MFMod
```
 
 
            

# Installation 

At the World Bank models built using the MFMod framework are developed in [EViews](http://www.eviews.com). When disseminated to clients, the models are solved and simulated using EViews -- often through the intermediary of an easy-to-use customized excel environment developed by the World Bank. That said, as a systems of equations and associated data, the models can be solved and operated under any software capable of solving a system of simultaneous equations. ```ModelFlow``` is such a package that permit not only solving the model, but also provide a rich and powerful suite of tools for analyzing the model and reporting results.     
`ModelFlow` is a python library that was developed by Ib Hansen over several years while working at the Danish Central Bank and the European Central Bank. The framework has been used both to port the U.S. Federal Reserve's macro-structural  model to python, but also been used to bring several stress-testing models developed by Central Banks into the python environment.  

Beginning in 2019, Hansen has worked with the World Bank to develop additional features that facilitate working with models built using the Bank's MFMod Framework, with the objective of creating an open source platform through which the Bank's models can be made available to the public.  

ModelFlow defines the ```model``` class, its methods and a number of other functions that extend and combine pre-existing python functions to allow the easy solution of complex systems of equations including macro-structural models like MFMod.  To work with ```ModelFlow```, a user needs to first install python (preferably the Anaconda or MiniConda variants). Then install the ```ModelFlow``` package and several supporting packages. 

While ```ModelFlow``` can be run directly from the python command-line or IDEs (Interactive Development Environments) like ```Spyder``` or Microsoft's ```Visual Code```, it is suggested that users install the Jupyter notebook system. Jupyter Notebook facilitates an interactive approach to building python programs, annotating them and ultimately doing simulations using `MFMod` under ```ModelFlow```. This entire manual, and the examples in it, was written and executed in the Jupyter Notebook environment using the [Jupyter Book](https://jupyterbook.org/) package.

To use the ModelFlow package **First** Python has to be installed. **Then** the ModelFlow package can be installed together with all the libraries on which it depends.   

:class: tip

This chapter provides step-by-step instructions for setting up the ModelFlow framework to work with World Bank macroeconomic models. It provides both novice and experienced python users with clear instructions on the steps necessary to install a reliable and reproducible `ModelFlow` environment for advanced modeling tasks.  

Key covered topics include:

- **Python Installation**:
  - Using the `Anaconda` or `MiniConda` environments. 
  - A discussion of the benefits of each notes that Anaconda offers a comprehensive package ecosystem (perhaps best suited for newcomers to python, while `MiniConda` is more lightweight and customizable and may be best suited for more experienced python users.

- **Installing the `ModelFlow` Environment**:
  - Create a dedicated Python environment for `ModelFlow` to avoid package conflicts.
  - Install `ModelFlow` and its dependencies using the provided commands.


- **System Compatibility**:
  - Supported on Windows, MacOS, and Linux.
  - Installation is straightforward, with Windows being the primary platform tested.

- **Updating `ModelFlow`**:
  - Using the `conda` command to update `ModelFlow` packages within the created environment.

# Installation of Python



`Python` is a powerful, versatile and extensible open-source programming language. It is widely used for artificial intelligence applications, interactive web sites, and scientific processing. As of May 2024, the `Python Package Index` (PyPI), the official repository for third-party Python software, contained over 530,000 packages that extend its functionality [^pythonLibrary]. ModelFlow is one of these packages.

Python comes in many flavors and `ModelFlow` will work with most of them. Nevertheless, users are **strongly advised** to use either the **Anaconda** distribution of Python or the closely related **MiniConda** distribution.

[^pythonLibrary]: [Wikipedia article on python](https://en.wikipedia.org/wiki/Python_(programming_language)). 



**Anaconda** is a full-featured distribution of python that comes with a comprehensive set of pre-installed packages and tools for scientific computing and data analysis. It is best suited for users who want a ready-to-use platform with a wide range of packages and don't mind the larger installation size. 

**MiniConda** is a more streamlined distribution, providing only the essential components for running python. It offers faster installation and a smaller footprint, making it suitable for users who prefer a more streamlined environment and want more control over package selection. Features that are in Anaconda, but not installed by miniconda by default, can be added manually.

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

## Which is better for me

In general, **Anaconda** is preferred by users who value convenience and desire a comprehensive package ecosystem. **MiniConda** is preferred by users who seek a minimalistic setup and have specific package requirements. If you are already familiar with python, plan to use it with `ModelFlow` and have space limitations `MiniConda` is probably the best solution for you.  For users new to python `Anaconda` may be a better solution.

The processes for installing  **Anaconda** and **MiniConda** are very similar. The main difference is which installer is downloaded and then where the distribution is stored in the file system. 

It is possible to install both distributions on the same machine without them interfering with each other.  

Both are available for the Windows, MacOS and Linux operating systems and `ModelFlow` should work equally well under all three operating systems. However, only the Windows version has been thoroughly tested and  was used in producing this manual. 

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

## Anaconda/MiniConda installation instructions

latexcommand \begin{flushleft}

### Windows
The definitive source for installing **Anaconda under windows** can be found [here](https://docs.anaconda.com/anaconda/install/windows/).  

The definitive source for installing **MiniConda under windows** can be found [here](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html). 

The version of `ModelFlow` and the examples in this manual were developed and tested using the 3.10 version of python.


**It is strongly advised that Anaconda/Miniconda be installed for a single user (Just Me)**.  This is much easier to maintain over time, especially in a professional environment where users may not have administrator rights on their computers.  Installing "For all users on this computer" (the other option offered by the installers) will substantially increase the complexity of maintaining python on your computer.

### MacOS

The definitive source for installing **Anaconda under macOS** can be found here: [https://docs.anaconda.com/anaconda/install/mac-os/](https://docs.anaconda.com/anaconda/install/mac-os/).  

The definitive source for installing **MiniConda under macOS** can be found here: [https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/](https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/).

### Linux

The definitive source for installing **Anaconda under Linux** can be found here: [https://docs.anaconda.com/anaconda/install/linux/](https://docs.anaconda.com/anaconda/install/linux/).  

The definitive source for installing **MiniConda under Linux** can be found here: [https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).


latexcommand \end{flushleft}

(installation_of_ModelFlow)=
# Installation of  ```ModelFlow``` 

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

`ModelFlow` is a python package that defines the model class, its methods and a number of other functions that extend and combine pre-existing python functions to allow the easy solution of complex systems of equations including macro-structural models like `MFMod`. To work with `ModelFlow`, a user needs to first install python (preferably the `Anaconda` or `MiniConda` variants). Then install the `ModelFlow` package and several other supporting packages.

```python
# Prepare the notebook for use of ModelFlow 

# Jupyter "magic" command to improve the display of charts in the Notebook
%matplotlib inline

# Import pandas (a python data storage and management package)
import pandas as pd

# Import the model class from the modelclass module 
from modelclass import model 

# functions that improve rendering of ModelFlow outputs
model.widescreen();
model.scroll_off();
```

## Creation of a ModelFlow environment





Although it is not strictly necessary, it is a good idea to create a specific python environment[^environ] for `ModelFlow`, this will be a space where the `ModelFlow` package itself will be installed and in which the specific dependencies on which `ModelFlow` relies will be installed. Other environments may require packages that conflict with `ModelFlow`. Declaring a separate environment for `ModelFlow` will help prevent conflicts between different versions of packages from arising.

The commands below create a `ModelFlow` environment and install into it the `ModelFlow` package and several supporting packages that are useful when using `ModelFlow` in conjunction with `EViews` or `Jupyter Notebook`[^JN6vs7].

The commands should be cut and paste (either one by one, or as a block) into the Anaconda or Miniconda command prompt environment. Instructions for activating the environment in windows are included in the box.




:class: tip

To open the Anaconda/MiniConda prompt:

1. In the windows command prompt, type Anaconda (or Miniconda)
2. If Anaconda/Miniconda have been successfully installed an icon entitled Anaconda(Minoconda) Prompt will be available in windows. Click on this.
3. This will open a python command shell where the commands listed in the main text can be entered.


    :alt: Windows Command Prompt
    :class: bg-primary mb-1
    :width: 50%
    :align: center



[^environ]: Both Anaconda and Miniconda support the idea of "environments". Environments are ring-fenced areas on your computer that can have different versions of Python and/or packages installed in them. If one application requires a specific version of pandas to run, and a second application requires a different version, by housing them in separate environment the dependencies of each application can be respected without generating a conflict between them. See [here](https://conda.io/activation) for more.

[^JN6vs7]: `ModelFlow` works equally well under both `Jupyter Notebook 6` and `Jupyter Notebook 7`. Howver, it was developed using `JN6` and this book and its examples were produced using `JN6`.  The installation instructions below will set up you `ModelFlow` environment to use `JN6`.

```
conda create -n ModelFlow -c ibh -c conda-forge ModelFlow_book -y
conda activate ModelFlow
##################
# Note skip the next line if installing under linux or Macintosh
#################
conda install py2eviews -c eviews

#############
# Continue from here on all Operating Systems
#############
pip install dash_interactive_graphviz
jupyter contrib nbextension install --user
jupyter nbextension enable hide_input_all/main
jupyter nbextension enable splitcell/splitcell
jupyter nbextension enable toc2/main
jupyter nbextension enable varInspector/main

```



* The first line in the code snippet above simultaneously creates the `ModelFlow` environment (the -n argument names the environment) and installs the `ModelFlow_book` package from conda-forge into this environment.\[NB:There also exists a `ModelFlow_stable` package.  The book package will be frozen at its current state of evolution to ensure that all the examples in this book will run using `ModelFlow_book`, the stable version may evolve over time and potentially break specific examples.  Longer-term users may wish to switch to the stable version, once they have absorbed the material in this book.\]

* The second command "activates" the newly created ModelFlow environment.

* The subsequent commands install some additional packages into the ModelFlow environment that are used by `ModelFlow`.  
    * The `py2eviews` package allows python to execute EViews commands on a machine where EViews has also been installed (this is only useful if the user intends to import existing EViews workfiles into the python environment of `ModelFlow`).
    * the `dash_interactive_graphviz` package enables a series of interactive dashboards which can be handy when using ModelFlow in Jupyter Notebooks.
    * The last 5 commands activate some useful jupyter notebook extensions.


Depending on the speed of your computer and of your internet connection, installation could take as little as 5 minutes or more than 1/2 an hour.

# Updating ModelFlow 


ModelFlow gets new features and fixes these will be reflected in the `ModelFlow_stable` package.  In order to use new features compared to the version on which this book is created the user might create a new environment to use this. This  would have the advantage of preserving the current `ModelFlow` environment for recreating the book examples. 


The command below creates a new environment `-n ModelFlow_new` and installs the most recent version of `ModelFlow` from the `modelflow_stable` repository. As noted above, this might introduce changes that break some of the examples in this book -- although every effort will be made to maintain backward compatibility.

```
conda deactivate
conda create -n ModelFlow_new -c ibh -c conda-forge ModelFlow_book -y
conda activate ModelFlow_new
```
And perform the additional commands specified in the previous section. 
