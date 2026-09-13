# The World Bank's MFMod Framework in Python with Modelflow - Model Analytics


# Model Analytics

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

# Model structure and causal chains


A model has a well defined logical and causal structure. {cite:author}`kogiku_introduction_1968`(1968) provides an introduction to causal analysis of models, while {cite:author}`berndsen_causal_1995`(1995) gives a more elaborate discussion. 

At the simplest level, the equations of a model can be organized into blocks. 

* **Simultaneous block** include equations that have are co-determined simultaneously. They contain feedback loops that may require several iterations before a solution that satisfies them all is found. A classic simultaneous block would include GDP, Income and Consumption. Consumption depends on income. Income depends on GDP, but Consumption also determines GDP. 

* **Recursive blocks** include equations that are a simple function of other variables. For example, the current account balance is just the difference between Export Revenues and Import Revenues.  These can be solved with just one pass once the values of the simultaneous blocks have been resolved.

At the equation level, each endogenous variable is a function of one or more variables, but because some of these variables are also dependent on other variables in the model, those right hand side variables that are endogenous can have their equations substituted into the first level equation to get an extended set of dependencies.  Moreover, the endogenous right hand side variables of these second level variables can also have their right hand sides substituted into the equation etc.


`ModelFlow` uses the [networkx](https://networkx.org/) python package to analyze the interrelationships within the model and between equations and includes a number of methods and properties to present these interrelationships both in tabular and graphical form [^graphviz], a subset of which is exposed in this chapter. 

[^graphviz]:The relational graphs produced by `ModelFlow` use the Graphviz [https://graphviz.org/](https://graphviz.org/) program, and are based on the relationships determined by the Networkx package. 

## Setting up the python environment and loading a pre-existing model

:class: tip

This chapter introduces tools and techniques for analyzing the structure and behavior of models in the `ModelFlow` framework. In a system of equations like World Bank models, impacts on variables in a simulation can be the results of the direct effect from changes imposed on variables in the equation of a variable, but also indirect effects caused by changes in variables that are not in the equation of a specific variable, but do generate changes in variables that are in the equation.

The chapter presents tools that explore the structure of a model, and display both the direct and indirect determinants of given equations.  

Following a simulation, the routines presented can display the precise contribution of a given variable to the change in another.

In addition to displaying which variables impacted a given variable, the routines can also be used to understand which variables are most impacted by changes in a given variable.

Results can be displayed both graphically and in tabular form.

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

```text
no sheetwidget
```

```python
mpak,baseline = model.modelload('../models/pak.pcim',alfa=0.7,run=1)

mpak.model_description="World Bank climate aware model of Pakistan as described in Burns et al. (2019)"
```

```text
Zipped file read:  ..\models\pak.pcim
```

```python
latex=True # Enables the charts in latex
```

**latex=True** 

The default behavior when displaying graphs in a *jupyter notebook* is to produce images in .svg format.
These images scale well and the mouseover feature can be used. That is: On mouseover of a node, the variable and the equation are displayed.  On mouseover on a joining line, the extent to which the variable contributed to the change in the dependent variable is displayed.

Unfortunately this *jupyter book* (book -- not notebook) requires images be in the jpg or PNG format. To enable generation of PDFs the latex=True option is set, which forces `ModelFlow` routines to render graphics in the PNG format -- effectively disabling the features of svg.

If using the Notebooks that for this book, the variable latex could be set equal to False in which case the same code will generate graphics in the more versatile SVG format.

## Model information

As noted before, the model object contains information about the model itself, its name, its structure (does it contain simultaneous equations or is it recursive), the number of variables it contains and the number that are exogenous and endogenous (have associated equations).

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

## Model structure  

A quick way to visualize the structure of a model is to plot its adjacency matrix [(https://en.wikipedia.org/wiki/Adjacency_matrix)](https://en.wikipedia.org/wiki/Adjacency_matrix). 

The adjacency matrix plots the relationships between endogenous variables in the model, dividing them into one or more simultaneous blocks and one or more recursive blocks.

Below is the adjacency matrix for the Pakistan model. Variables in the red square block (simultaneous block) depend on one or more variables that in turn depend upon them, requiring the model to solve for their values simultaneously.  The variables in the green triangles (recursive blocks) do not enter directly or indirectly as an argument in the variables that determine them and therefore can be solved in one iteration once the values for the simultaneous variables are determined.

Internally `ModelFlow` takes these factors into consideration and solves the simultanrous block(s) first and then solves the recursive blocks.

```python
mpak.plotadjacency(size=(20,20));
```

```text
<Figure size 2000x2000 with 1 Axes>
```

As is evident in the above chart, the majority of the variables in MFMod Pakistan are recursive (green) and depend simply on the values of other variables.  The core of the model lies in the simultaneous (red) block, where the main wages, prices, real and nominal variables that drive other variables are determined.

## The dependencies of individual endogenous variables (the `.tracepre()` method)

As noted above, every endogenous variables is directly dependent on the variables that occur on its right hand side, but is also indirectly dependent on the variables that determine its RHS variables and in turn those that determine the variables to the right of them *ad infinitum*. 

`ModelFlow` includes several methods and properties that allow these dependencies to be explored.

The `.frml` property returns the normalized formula of an equation, from which the right hand variables for the equation can be discerned and these are reported along with their descriptions following the formula.

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

The method `.tracepre()` provides a graphical representation of this relationship, showing all the variables that directly determine an endogenous variable (in this example real GDP), distinguishing between RHS variables that are endogenous (in blue) and those that are exogenous (yellow).

```python
mpak.PAKNYGDPMKTPKN.tracepre(png=latex,size=(4,3))
```

If the model has been solved, `.tracepre()` goes one step further and uses the thickness of the lines to reflect the relative importance of each variable in the change of the dependent variable in the preceding scenario.

### Shock the model

Below a $30 nominal Carbon tax is applied beginning in 2025.

```python

alternative  =  baseline.upd("<2025 2100> PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER = 30")
result = mpak(alternative,2020,2100) # simulates the model
```

As a result GDP, consumption investment and most all variables in the model change, as illustrated in the below graphs that show the percent deviation of the main components of GDP from their baseline values.

```python
mpak['PAKNYGDPMKTPKN PAKNECONPRVTKN PAKNEGDIFTOTKN PAKNEEXPGNFSKN PAKNEIMPGNFSKN'].difpctlevel.rename().plot(title="Impact of $30 USD nominal carbon tax");
```

```text
<Figure size 1000x600 with 6 Axes>
```

###  `.tracepre()` following a shock 

Below the same `.tracepre()` command is executed again, but because a shock has been simulated, the width of the lines representing the causal links between variables is thicker the more important the change  in a given variable was in the previous simulation in explaining the change in the level of the dependent variable (GDP).  

```python
latex=True
mpak.PAKNYGDPMKTPKN.tracepre(png=latex,size=(5,3))
```

### The filter option, restricts the output of `.tracepre()`

The filter option can be used to restrict the output of `.tracepre()` to RHS variables that have had a large impact on the dependent variable. In the example below, the option `filter=20` instructs tracepre to only draw those rhs variables that contributed 20 percent or more to the total change in GDP.

```python
mpak.PAKNYGDPMKTPKN.tracepre(filter=20,png=latex,size=(5,3))
```

### The up option, extends the `.tracepre` plot beyond the first level of causal variables

The up option allows `.tracepre` dependencies to be followed beyond the first level of causal variables. Below, it is extended to variables as much as three levels back, and restricted to those whose variation explains at least 20 percent of the change in the variable of which they are a right-hand-side variable.

```python
mpak.PAKNYGDPMKTPKN.tracepre(filter = 20,up=3,png=latex)
```

#### Adding a table to the causal graph

The `Fokus2` option causes a table of values to be added to the casual flow graph. In this example, the `showgrowth=True` option instructs `ModelFlow` to show the table in both level and growth rate terms.

 

```python
with mpak.set_smpl(2025,2027):
    print(mpak.PAKNYGDPMKTPKN.tracepre(filter = 20,
                fokus2='PAKNEGDIFTOTKN PAKNECONPRVTKN PAKNECONGOVTKN PAKNYGDPMKTPKN PAKNEIMPGNFSKN',
                growthshow=True,
                png=latex)
         )
```

```text
None
```

### `.tracedep(down=xx)` traces the impact of a variable on other variables 

The preceding examples have focused on understanding how changes in other variables have impacted the variable of interest.  The closely related `tracedep()` method shows what other variables depend on the specified variable, with the `down=xx` option indicating how many levels of substitution to display. Here, the direction of the dependency graph is reversed and the chart shows the impact that the changes in the selected variable had on those which depend upon it.  Below is the impact of change in consumption on all of the variables up to 3 levels below the consumption equation.

```python
mpak.PAKNECONPRVTKN.tracedep(down=3,filter=20,png=latex)
```

### `.modeldash()` An interactive way to explore dependencies


The `.modeldash()` method  generates a widget that allows you to dynamicaly adjust the arguments to the `tracepre()` and `tracedep` functions.


```
 with mpak.set_smpl(2022,2026):
        mpak.modeldash('PAKNYGDPMKTPKN',jupyter=True,inline=False) 
```

The above commands generate a dashboard that looks a like the below, where the panel to the left allows the user to change options including the filter, the depth of the trace among other things.

![dash.png](dash.png)

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

# Analyzing the impact of a shock 

When working with a model, it is often useful to have a quantitative of the contribution of different channels to a final result.  For example, an increase in interest rates will tend to reduce investment and consumer demand -- contributing to a reduction in GDP. At the same time, lower inflation as the higher interest rate takes effect will tend to work in the opposite direction. 

The `tracedep()` and `tracepre()` methods introduced in the previous chapter give a sense of impacts. The `ModelFlow` methods `.dekomp()` and `.totdif()` take that one step further by calculating the contribution of each channel to the overall result.

:class: tip

This chapter provides the tools and techniques to dissect and understand the ripple effects of shocks within macroeconomic systems.

This chapter focuses on methods to analyze the impacts of external shocks within a macroeconomic model. The previous chapter explored the impacts of changes in one variable on other variables in a model by following the causal chain of any individual variable.

The techniques explored in this chapter illustrate and extend this by:
- attributing changes in any given model variable to the changes in the variables in the model that were shocked.  In the techniques used in the previous chapter it may be determined that increased inflation was the proximate cause of a decline in consumption, the methods presented here seek to illuminate which of the changes to exogenous variables caused the increase in inflation that caused the decline in consumption (say an increase in oil prices).
- Impacts can be traced either through a single equation method or using a model level decomposition

Examples include a range of graphical and textual visualization of results.

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
# set default precision 
pd.set_option("display.precision", 2)
```

```python
# For display reasons 
latex = 1
```

## Load the existing model, data and descriptions 
The file `pak.pcim` contains a dump of model equations, dataframe, simulation options and variable descriptions for the World Bank climate aware model for Pakistan described in {cite:t}`burns_climate_2021`. 

The code below:

 - Loads the model and simulates it using the `DataFrame` stored in the `pcim` file to establish a baseline.
 - Creates a `DataFrame` that is a copy (from 2020) of the active solution in `mpak` and changes the tax rate to 30 USD/Ton for carbon emissions from coal, oil and natural gas.
 - Runs a simulations with these new carbon taxes. 
 
The results from this simulation will be used below to explore the attribution functionality of ModelFlow.
  
  
{ref}`Single equation Impact Decomposition <impactsingle>`
  

```python
mpak,baseline = model.modelload('../models/pak.pcim',alfa=0.7,run=1,relconv=0.0000000001 ,keep='Business as Usual')
alternative  =  baseline.upd("<2020 2100> PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER = 30")
```

```text
Zipped file read:  ..\models\pak.pcim
```

```python
#simulate the model
result = mpak(alternative,2025,2100,keep='Nominal carbon tax of 30 USD',
              ljit=False,         # do not compile the model (default value for this option)
              nfirst=800,
              maxiteration=100   # if no convergence after 100 iterations - stop
             ) # simulates the model
```

## The mathematics of decomposition

At its root the idea of attribution is to take the total derivative of the model to identify the sensitivity of the equation of interest to changes elsewhere in the model and then combine that with the changes in other variables. 

Take a variable y that is a function of two other variables a and b.  In the model, the relationship might be written as:


$y = f(a,b)$

If there are two sets of results designated with a subscript 0 and 1, these can be written as: 

\begin{eqnarray}
y_0 = f(a_0,b_0)\\
y_1 = f(a_1,b_1)
\end{eqnarray}

If the change in the three variables is specified as $\Delta y, \Delta a, \Delta b$, the total derivative of y can be written as:


$\Delta y = \underbrace{\Delta a \dfrac{\partial {f}}{\partial{a}}(a,b)}_{\Omega a} + 
\underbrace{\Delta b \dfrac{\partial {f}}{\partial{b}}(a,b)}_{\Omega b}+Residual$

The first expression can be called $\Omega_a$ or the contribution of changes in a to changes in y, and the second $\Omega_b$,  or the contribution of changes in b to changes in y.  


`ModelFlow` performs a numerical approximation of $\Omega_a$ and $\Omega_b$ by performing two runs of the $f()$:

\begin{eqnarray}  
y_0&=&f(a_{0},b_{0}) \\
y_1&=&f(a_0+\Delta a,b_{0}+ \Delta b)
\end{eqnarray}

and calculates $\Omega_a$ and $\Omega_b$ as:

\begin{eqnarray}  
\Omega a&=&f(a_1,b_1 )-f(a_1-\Delta a,b_1) \\
\Omega b&=&f(a_1,b_1 )-f(a_1,b_1-\Delta  b)
\end{eqnarray}



And: 

\begin{eqnarray}
residual = \Omega a + \Omega b -(y_1 - y_0) 
\end{eqnarray}

If the model is fairly linear, the residual will be small. 

##  decomposition


$y = f(a,b)$

2 scenarios  0 and 1, these can be written as: 

\begin{eqnarray}
y_0 = f(a_0,b_0)\\
y_1 = f(a_1,b_1)
\end{eqnarray}

Change: $\Delta y, \Delta a, \Delta b$, the total derivative of y can be written as:


$\Delta y = \underbrace{\Delta a \dfrac{\partial {f}}{\partial{a}}(a,b)}_{\Omega a} + 
\underbrace{\Delta b \dfrac{\partial {f}}{\partial{b}}(a,b)}_{\Omega b}+Residual$


`ModelFlow` performs a numerical approx:
\begin{eqnarray}  
\Omega a&=&f(a_1,b_1 )-f(a_1-\Delta a,b_1) \\
\Omega b&=&f(a_1,b_1 )-f(a_1,b_1-\Delta  b)
\end{eqnarray}

## Model-level decomposition or  single equation decomposition?

Above, the relationship between y, a, and b was summarized by the function f(). 

$f(a,b)$ could represent **a single equation** in the model or it could represent **the entire model**. 

In the **single equation** mode, $\Delta a$ and $\Delta b$ would be treated as exogenous variables in the attribution calculation as they are both on the right hand side of the equation (i.e. exogenous to this equation -- even if they might be endogenous variables in some other equation). Here results will show the direct impact of changes in the RHS variable(s) on the LHS variable.

When analyzing the total derivative for the **entire model** instance, $a$ and $b$ will be purely exogenous variables. In this case, the decomposition shows the cumulative effect -- potentially operating through multiple channels of a change in the exogenous (or exogenized variables) on different endogenous variables in the model. Say we are looking at inflation, an exogenous change in wages would influence prices directly through higher costs of production and indirectly by inducing higher demand.  The  model-level decompoistion will return the sum of the two or more influences.

Assume the simple equation example such that  $a$ and $b$ are simple variables. When $\Delta y$, $\Delta a$ and $\Delta b$ reflect the difference across scenarios (say the value of the three variables in `.lastdf` less the value in `.basedf`) then;

$\Omega_a$, $\Omega_b$ are the absolute contribution of a and b to the change in y, and 
$100*\bigg[\cfrac{\Omega_a}{\Delta y}\bigg]$ is the share of the change in y explained by expressed as a percent and  $100*\bigg[\cfrac{\Omega_b}{\Delta y}\bigg]$ is the share of the change in y explained by b expressed as a percent.

If $\Delta y$, $\Delta a$ and $\Delta b$ are the changes over time ($\Delta y_t=y_t-y_{t-1}$), then $\Omega_a$, $\Omega_b$ are the contributions of a and b to the rate of growth of y, while $100*\bigg[\cfrac{\Omega_a}{\Delta y_{t-1}}\bigg]$  $100*\bigg[\cfrac{\Omega_b}{\Delta y_{t-1}}\bigg]$ are are the contributions of a and b to the rate of growth of y.

:name: impactsingle

## Decomposing the source of changes to a single endogenous variable

The `ModelFlow` method `.dekomp()` is used to calculate the contribution of RHS variables to the change in an endogenous (LHS) variable. 

This method takes advantage of the fact that the model object stores the initial and most recent simulation result in two dataframes called `.basedf` and `.lastdf`, as well as all of the equations of the model. 

The `dekomp()` method calculates the contribution to changes in the level of the dependent variable in a given equation. It does not calculate what caused the changes to the RHS variables.

In the example below, the contribution to the change in Total emissions is decomposed into the contribution from each of three sources in the model, the consumption of Crude Oil, Natural Gas and Coal.  As the equation for total emissions is just the sum of the three this is a fairly trivial decomposition, but it provides an easily understood illustration of the process at work.

Note that, initially some carbon taxes were negative because the associated energy products benefited from some sort of subsidy.  As a result, although each carbon tax is set to 30 in the simulation that was run earlier, the change in the levels of the Carbon tax is different across carbon taxes, with the increase in the net taxation on the carbon emissions from natural gas being particularly large.  

```python
print("Change in carbon taxes:") 
with mpak.set_smpl(2023,2030):
    print(mpak['PAKGGREVCO2CER PAKGGREVCO2GER PAKGGREVCO2OER'].dif.rename().df)
```

```text
Change in carbon taxes:
      Carbon tax on coal (USD/t)  Carbon tax on gas (USD/t)  \
2023                       35.55                       71.0   
2024                       35.55                       71.0   
2025                       35.55                       71.0   
2026                       35.55                       71.0   
2027                       35.55                       71.0   
2028                       35.55                       71.0   
2029                       35.55                       71.0   
2030                       35.55                       71.0   

      Carbon tax on oil (USD/t)  
2023                      38.71  
2024                      38.71  
2025                      38.71  
2026                      38.71  
2027                      38.71  
2028                      38.71  
2029                      38.71  
2030                      38.71
```

latexcommand \begin{samepage}

```python
dekomp_result = mpak.PAKCCEMISCO2TKN.dekomp(start=2024,end=2027);
```

```text

Formula        : FRML <IDENT> PAKCCEMISCO2TKN = PAKCCEMISCO2CKN+PAKCCEMISCO2OKN+PAKCCEMISCO2GKN $ 

                        2024         2025         2026         2027
Variable    lag                                                    
Base        0   230370296.36 236240661.98 242537408.00 248995663.61
Alternative 0   230370296.36 183872963.10 190234954.74 196979009.56
Difference  0           0.00 -52367698.88 -52302453.26 -52016654.05
Percent     0          -0.00       -22.17       -21.56       -20.89

 Contributions to difference for  PAKCCEMISCO2TKN
                          2024         2025         2026         2027
Variable        lag                                                  
PAKCCEMISCO2CKN 0         0.00 -22807768.70 -22763629.77 -22643891.23
PAKCCEMISCO2OKN 0         0.00 -13105358.04 -13576625.98 -13868109.25
PAKCCEMISCO2GKN 0         0.00 -16454572.13 -15962197.50 -15504653.56

 Share of contributions to difference for  PAKCCEMISCO2TKN
                     2024       2025       2026       2027
Variable        lag                                       
PAKCCEMISCO2CKN 0                44%        44%        44%
PAKCCEMISCO2GKN 0                31%        31%        30%
PAKCCEMISCO2OKN 0                25%        26%        27%
Total           0       0       100%       100%       100%
Residual        0    -100        -0%         0%        -0%

 Difference in growth rate PAKCCEMISCO2TKN
                      2024       2025       2026       2027
Variable    lag                                            
Base        0         2.3%       2.5%       2.7%       2.7%
Alternative 0         2.3%     -20.2%       3.5%       3.5%
Difference  0         0.0%     -22.7%       0.8%       0.9%
None

 Contribution to growth rate PAKCCEMISCO2TKN
                          2024       2025       2026       2027
Variable        lag                                            
PAKCCEMISCO2CKN 0         0.0%      -9.9%       0.4%       0.4%
PAKCCEMISCO2OKN 0         0.0%      -5.7%      -0.0%       0.1%
PAKCCEMISCO2GKN 0         0.0%      -7.1%       0.5%       0.5%
Total           0         0.0%     -22.7%       0.9%       1.0%
Residual        0         0.0%       0.0%       0.1%       0.1%
```

latexcommand \end{samepage}

The above results from the call to `.dekomp()` are presented in several sections.

|Section|Table|Contents|
|:--|:--|:--|
|**The first section**| |the normalized formula of the RHS variable `PAKCCEMISCO2TKN`|
|**The second section**| |Shows the changes in level terms. |
|| diff_level |First by showing the results of the simulation **base**, then the previous level **last**, then the difference and then the difference expressed as a percent|
|| att_level |This is followed by a table showing the contribution of the changes in every LHS variable to the observed change in the dependent variable.|
|**The third section**| att_pct |Shows the same results for the RHS variables, but expressed as a percent of the total change in the dependent variable. |
|**The fourth section**|| Shows the same results but for the change in the growth rate of the dependent variable.|
|| diff_growth |The first table shows the post-shock growth rate of the dependent variable from the `.lastdf` dataframe, followed by the pre-shock growth rate and the difference in the growth rates. |
|| att_growth |The second table of this section shows the contribution to the change in the growth rate from each RHS variable. |


The object returned by `.dekomp()` is a [namedtuple](https://realpython.com/python-namedtuple/) that contains each of these tables which can then be referred to later.

The code below extracts the different sub-components of the `.dekomp()` results and displays them individually.

latexcommand \begin{samepage}

```python
# Loop over the elements in the result of dekomp. 
# a named tuple can be used both as a straight tuple and the elements
# can be accessed through the field name. 

with pd.option_context('display.float_format', '{:.2f}'.format):
    for f,df in zip(dekomp_result._fields,dekomp_result):
        display(f)
        display(df)
```

```text
'diff_level'
```

```text
2024         2025         2026         2027
Variable    lag                                                    
Base        0   230370296.36 236240661.98 242537408.00 248995663.61
Alternative 0   230370296.36 183872963.10 190234954.74 196979009.56
Difference  0           0.00 -52367698.88 -52302453.26 -52016654.05
Percent     0          -0.00       -22.17       -21.56       -20.89
```

```text
'att_level'
```

```text
2024         2025         2026         2027
Variable        lag                                            
PAKCCEMISCO2CKN 0   0.00 -22807768.70 -22763629.77 -22643891.23
PAKCCEMISCO2OKN 0   0.00 -13105358.04 -13576625.98 -13868109.25
PAKCCEMISCO2GKN 0   0.00 -16454572.13 -15962197.50 -15504653.56
```

```text
'att_pct'
```

```text
2024   2025   2026   2027
Variable        lag                             
PAKCCEMISCO2CKN 0       NaN  43.55  43.52  43.53
PAKCCEMISCO2GKN 0       NaN  31.42  30.52  29.81
PAKCCEMISCO2OKN 0       NaN  25.03  25.96  26.66
Total           0      0.00 100.00 100.00 100.00
Residual        0   -100.00  -0.00   0.00  -0.00
```

```text
'diff_growth'
```

```text
2024   2025  2026  2027
Variable    lag                         
Base        0    2.27   2.55  2.67  2.66
Alternative 0    2.27 -20.18  3.46  3.55
Difference  0    0.00 -22.73  0.79  0.88
```

```text
'att_growth'
```

```text
2024   2025  2026  2027
Variable        lag                         
PAKCCEMISCO2CKN 0    0.00  -9.90  0.40  0.44
PAKCCEMISCO2OKN 0    0.00  -5.69 -0.01  0.09
PAKCCEMISCO2GKN 0    0.00  -7.14  0.53  0.50
Total           0    0.00 -22.73  0.92  1.02
Residual        0    0.00   0.00  0.13  0.14
```

latexcommand \end{samepage}

## A more complex example

The above decomposition is fairly straight forward because the decomposed equation is a simple identity, where Total Emissions are just the sum of its three component parts: Total Carbon emissions = Emissions from Oil+  Emissions from Coal + Emissions from Natural Gas.

The following single-equation decomposition looks to the impact of the same shock (introduction of a carbon tax) on a different variable (inflation).  The inflation equation is more complex and has more direct causal variables, so the decomposition is more interesting.

Recall the inflation equation is given by the `.frml` method for its normalized version and `.eviews` for its original specification.  The equation for the consumer price level (PAKNECONPRVTXN) was originally specified in eviews as:

```python
mpak['PAKNECONPRVTXN'].eviews
```

```text
PAKNECONPRVTXN : 
@IDENTITY PAKNECONPRVTXN  = ((PAKNECONENGYSH^PAKCESENGYCON)  * PAKNECONENGYXN^(1  - PAKCESENGYCON)  + (PAKNECONOTHRSH^PAKCESENGYCON)  * PAKNECONOTHRXN^(1  - PAKCESENGYCON))^(1  / (1  - PAKCESENGYCON))
```

The normalized equation is given by `mpak['PAKNECONPRVTXN'].frml`.  

Note in the Pakistan model, consumer inflation is derived as a constant elasticity of transformation (CET) aggregation of the price of energy goods(PAKNECONENGYXN) and non-energy goods (PAKNECONOTHRXN).

```python
mpak['PAKNECONPRVTXN'].frml
```

```text
PAKNECONPRVTXN : FRML <IDENT> PAKNECONPRVTXN = ((PAKNECONENGYSH**PAKCESENGYCON)*PAKNECONENGYXN**(1-PAKCESENGYCON)+(PAKNECONOTHRSH**PAKCESENGYCON)*PAKNECONOTHRXN**(1-PAKCESENGYCON))**(1/(1-PAKCESENGYCON)) $
```

Note further the normalized equation is solving for the **level** of the price deflator -- not inflation which is the rate of growth of this index.

Because the equation solves for the level of the price deflator, the decomposition show the contributions of each explanatory variable to the increase in the price level (not that of the inflation rate). However, the 4th table is showing the impacts on the rate of growth of the price level -- i.e. the level of inflation.

latexcommand \begin{samepage}

```python
mpak['PAKNECONPRVTXN'].dekomp(start=2024,end=2027);
```

```text

Formula        : FRML <IDENT> PAKNECONPRVTXN = ((PAKNECONENGYSH**PAKCESENGYCON)*PAKNECONENGYXN**(1-PAKCESENGYCON)+(PAKNECONOTHRSH**PAKCESENGYCON)*PAKNECONOTHRXN**(1-PAKCESENGYCON))**(1/(1-PAKCESENGYCON)) $ 

                      2024       2025       2026       2027
Variable    lag                                            
Base        0         2.30       2.45       2.60       2.75
Alternative 0         2.30       2.51       2.68       2.83
Difference  0         0.00       0.06       0.07       0.08
Percent     0        -0.00       2.47       2.74       2.92

 Contributions to difference for  PAKNECONPRVTXN
                         2024       2025       2026       2027
Variable       lag                                            
PAKNECONENGYSH 0        -0.00      -0.00      -0.00      -0.00
PAKCESENGYCON  0        -0.00      -0.00      -0.00      -0.00
PAKNECONENGYXN 0        -0.00       0.01       0.01       0.01
PAKNECONOTHRSH 0        -0.00      -0.00      -0.00      -0.00
PAKNECONOTHRXN 0        -0.00       0.05       0.06       0.07

 Share of contributions to difference for  PAKNECONPRVTXN
                    2024       2025       2026       2027
Variable       lag                                       
PAKNECONOTHRXN 0                77%        81%        83%
PAKNECONENGYXN 0                23%        20%        18%
PAKNECONENGYSH 0                -0%        -0%        -0%
PAKCESENGYCON  0                -0%        -0%        -0%
PAKNECONOTHRSH 0                -0%        -0%        -0%
Total          0       0       100%       100%       100%
Residual       0    -100         0%         0%         0%

 Difference in growth rate PAKNECONPRVTXN
                      2024       2025       2026       2027
Variable    lag                                            
Base        0         7.3%       6.7%       6.2%       5.8%
Alternative 0         7.3%       9.3%       6.5%       6.0%
Difference  0         0.0%       2.6%       0.3%       0.2%
None

 Contribution to growth rate PAKNECONPRVTXN
                         2024       2025       2026       2027
Variable       lag                                            
PAKNECONENGYSH 0        -0.0%       0.0%      -0.0%      -0.0%
PAKCESENGYCON  0        -0.0%       0.0%      -0.0%      -0.0%
PAKNECONENGYXN 0        -0.0%       0.6%      -0.0%      -0.0%
PAKNECONOTHRSH 0        -0.0%       0.0%      -0.0%      -0.0%
PAKNECONOTHRXN 0        -0.0%       2.0%       0.3%       0.2%
Total          0        -0.0%       2.7%       0.3%       0.2%
Residual       0        -0.0%       0.0%      -0.0%      -0.0%
```

latexcommand \end{samepage}

Interestingly only 23% of the increase in the price level each period is due to the direct channel (the impact on the price of energy consumed by households), the bulk of the increase comes indirectly through other prices.  Indeed as time progresses this share rises from 77% in the first year of the price change (2020) to 83% by 2024.

### Non-energy prices

Below is the formula for nonenergy consumer prices and their decomposition. This equation is written out as a more standard augmented-phillips-curve type inflation equation reflecting changes in the cost of local goods production (PAKNYGDPFCSTXN), Government taxes on goods and services (PAKGGREVGNFSXN), the price of imports (PAKNEIMPGNGSXN) and the influence of the economic cycle (PAKNYGDPGAP_) on the price level.

```python
mpak['PAKNECONOTHRXN'].eviews
```

```text
PAKNECONOTHRXN : 
DLOG(PAKNECONOTHRXN) = 0.590372627657176*DLOG(PAKNYGDPFCSTXN) + D(PAKGGREVGNFSXN/100) + (1 - 0.590372627657176)*DLOG(PAKNEIMPGNFSXN) + 0.2*PAKNYGDPGAP_/100
```

```python
mpak['PAKNECONOTHRXN'].dekomp(start=2025,end=2029);
```

```text

Formula        : FRML <DAMP,STOC> PAKNECONOTHRXN = (PAKNECONOTHRXN(-1)*EXP(PAKNECONOTHRXN_A+ (0.590372627657176*((LOG(PAKNYGDPFCSTXN))-(LOG(PAKNYGDPFCSTXN(-1))))+((PAKGGREVGNFSXN/100)-(PAKGGREVGNFSXN(-1)/100))+(1-0.590372627657176)*((LOG(PAKNEIMPGNFSXN))-(LOG(PAKNEIMPGNFSXN(-1))))+0.2*PAKNYGDPGAP_/100) )) * (1-PAKNECONOTHRXN_D)+ PAKNECONOTHRXN_X*PAKNECONOTHRXN_D  $ 

                      2025       2026       2027       2028       2029
Variable    lag                                                       
Base        0         2.50       2.65       2.81       2.96       3.11
Alternative 0         2.55       2.71       2.87       3.03       3.19
Difference  0         0.05       0.06       0.07       0.08       0.08
Percent     0         1.95       2.26       2.47       2.61       2.65

 Contributions to difference for  PAKNECONOTHRXN
                           2025       2026       2027       2028       2029
Variable         lag                                                       
PAKNECONOTHRXN   -1       -0.00       0.05       0.06       0.07       0.08
PAKNECONOTHRXN_A  0       -0.00      -0.00      -0.00      -0.00      -0.00
PAKNYGDPFCSTXN    0        0.00       0.01       0.01       0.02       0.02
                 -1       -0.00      -0.00      -0.01      -0.01      -0.02
PAKGGREVGNFSXN    0       -0.00      -0.00      -0.00      -0.00      -0.00
                 -1       -0.00      -0.00      -0.00      -0.00      -0.00
PAKNEIMPGNFSXN    0        0.05       0.05       0.05       0.05       0.05
                 -1       -0.00      -0.05      -0.05      -0.05      -0.05
PAKNYGDPGAP_      0        0.00       0.00       0.00       0.00       0.00
PAKNECONOTHRXN_D  0       -0.00      -0.00      -0.00      -0.00      -0.00
PAKNECONOTHRXN_X  0       -0.00      -0.00      -0.00      -0.00      -0.00

 Share of contributions to difference for  PAKNECONOTHRXN
                           2025       2026       2027       2028       2029
Variable         lag                                                       
PAKNECONOTHRXN   -1         -0%        87%        91%        95%        98%
PAKNEIMPGNFSXN    0         95%        79%        70%        63%        59%
PAKNYGDPFCSTXN    0          1%        12%        18%        22%        25%
PAKNYGDPGAP_      0          4%         6%         4%         3%         1%
PAKNECONOTHRXN_A  0         -0%        -0%        -0%        -0%        -0%
PAKGGREVGNFSXN    0         -0%        -0%        -0%        -0%        -0%
                 -1         -0%        -0%        -0%        -0%        -0%
PAKNECONOTHRXN_D  0         -0%        -0%        -0%        -0%        -0%
PAKNECONOTHRXN_X  0         -0%        -0%        -0%        -0%        -0%
PAKNYGDPFCSTXN   -1         -0%        -1%       -11%       -17%       -22%
PAKNEIMPGNFSXN   -1         -0%       -84%       -74%       -67%       -63%
Total             0        100%        99%        99%        99%        99%
Residual          0          0%        -1%        -1%        -1%        -1%

 Difference in growth rate PAKNECONOTHRXN
                      2025       2026       2027       2028       2029
Variable    lag                                                       
Base        0         6.7%       6.2%       5.8%       5.4%       5.1%
Alternative 0         8.7%       6.5%       6.0%       5.6%       5.2%
Difference  0         2.1%       0.3%       0.2%       0.1%       0.0%
None

 Contribution to growth rate PAKNECONOTHRXN
                           2025       2026       2027       2028       2029
Variable         lag                                                       
PAKNECONOTHRXN   -1        0.0%       2.0%       0.3%       0.2%       0.1%
PAKNECONOTHRXN_A  0        0.0%      -0.0%      -0.0%       0.0%      -0.0%
PAKNYGDPFCSTXN    0        0.0%       0.3%       0.2%       0.1%       0.1%
                 -1        0.0%      -0.0%      -0.3%      -0.2%      -0.1%
PAKGGREVGNFSXN    0        0.0%      -0.0%      -0.0%       0.0%      -0.0%
                 -1        0.0%      -0.0%      -0.0%       0.0%      -0.0%
PAKNEIMPGNFSXN    0        2.0%      -0.1%      -0.1%      -0.1%      -0.1%
                 -1        0.0%      -2.0%       0.1%       0.1%       0.1%
PAKNYGDPGAP_      0        0.1%       0.0%      -0.0%      -0.0%      -0.0%
PAKNECONOTHRXN_D  0        0.0%      -0.0%      -0.0%       0.0%      -0.0%
PAKNECONOTHRXN_X  0        0.0%      -0.0%      -0.0%       0.0%      -0.0%
Total             0        2.1%       0.3%       0.2%       0.1%       0.0%
Residual          0        0.0%      -0.0%      -0.0%      -0.0%      -0.0%
```

These results indicate that much of the initial impact on prices is coming from the increase in the price of imported goods (which includes a large fuel component). As time progresses, the imported inflation component declines (because fuel and import prices are no longer rising) and the lagged consumption price dominates (the level this period is basically determined by the price level in the previous period) .  Other factors such as the cost of domestically produced goods play a larger role and the net impact of imported prices (the total of the contemporaneous and lagged value) approaches zero. Cyclical pressure are initially adding to inflation before declining and eventually turning negative. 

## The `get_att()` method provides more control over the outputs of `.dekomp()`

Following a call to the `.dekomp()` method, the `.get_att()` method provides a range of mechanisms that allow the results to be displayed in different ways.

### The default display of `.get_att()` 

By default `.get_att()` displays the share contributions of RHS variables to the total change in the LHS variable.  The start= and end= options allow the period for which results are displayed to be restricted.

```python

mpak.PAKNECONPRVTKN.get_att(start=2025,end=2035)
```

```text
<pandas.io.formats.style.Styler at 0x2934c861940>
```

    :alt: get attribution 
    :class: bg-primary mb-1
    :width: 100%
    :align: center

### Options: Lag=True/False 

Because the decomposition of the equation is based on the normalized (levelized) version of the equation, for equations initially written as growth rates or ECMs many variables will occur several times in the attribution table with both the contribution of the current value of the variable and those of any lagged versions that appear in the normalized equation.

The `Lag=False` option changes the default behavior of `.get_att()` and aggregates the contributions of different lags.

By aggregating the lags, the net effect of changes in the variables can be more easily determined. Below it is clearer that the initial impact of higher import prices drove most of the inflation response.  In subsequent periods, import prices were stable or even falling so most of the contribution to the change in the level of other goods inflation was from the lagged dependent variable and the changed state of the economic cycle (the Gap variable which initially was adding to inflationary pressures eventually subtracts from inflation as the economy slows).

```python
mpak.PAKNECONOTHRXN.get_att(lag=False,start=2025,end=2035)
```

```text
<pandas.io.formats.style.Styler at 0x2934c5defd0>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 100%
    :align: center

### Options: Type="growth/pct/Level"

The option `Type` controls which of the tables generated by `dekomp()` is displayed. The contributions of RHS variables to the level of the dependent variable (`=level`), the share of the observed change in the RHS variable attributable to each dependent variable (`=pct`), and the change in the growth rate (`=growth`)of the LHS available attributable to the changes in the growth rate of each RHS variable.

### Options: threshold=xx"

The `threshold=` option will suppress from the output those variables whose contribution is less than the stated threshold.

In the example below, lags are suppressed, and only contributions to the growth rate of variables whose largest contribution was more than $\pm$0.1 percent are displayed.  The dropped variables influence is aggregated and displayed in a row labeled **small**.

#### Options: bare=True/False

If bare is set to `False` then the values of the LHS variable in the `basedf` and `lastdf` dataframes and their difference are also displayed. By default this option is `True` which suppresses the display.

```python
mpak.PAKNECONPRVTKN.get_att(lag=False,type='growth',bare=False,threshold=0.1,start=2020,end=2024)
```

```text
<pandas.io.formats.style.Styler at 0x2934b957250>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

### Several examples
Here the default type (pct) is displayed and the threshold is set to 10, so only variables whose aggregate impact was more than 10 percent of the total in one or more of the displayed years are shown.

```python
mpak.PAKNECONPRVTKN.get_att(lag=False,threshold=10,start=2025,end=2035)
```

```text
<pandas.io.formats.style.Styler at 0x2934b957250>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 100%
    :align: center

The three examples below show the impact on real consumption of the changes induced on its LHS variables as changes in percent level and growth, with the threshold set to focus only on the main channels.

```python
mpak.PAKNECONPRVTKN.get_att(lag=False,threshold=10,bare=False,start=2025,end=2029);
mpak.PAKNECONPRVTKN.get_att(lag=False,threshold=10,type='level',bare=False,start=2025,end=2029);
mpak.PAKNECONPRVTKN.get_att(lag=False,threshold=0.1,type='growth',bare=False,start=2025,end=2029);
```

```text
<pandas.io.formats.style.Styler at 0x2934c5defd0>
```

```text
<pandas.io.formats.style.Styler at 0x2934c5defd0>
```

```text
<pandas.io.formats.style.Styler at 0x2934c5defd0>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 100%
    :align: center

### Displaying `.dekomp()` results graphically


The `dekomp_plot` method allows singe-equation decompositions to be displayed graphically. Below in the initial periods, the import price, and cost-push factors dominate, but as the model equilibrates the lagged level of the price deflator explains virtually all of the movement in the level of the price.

```python
fig=mpak.dekomp_plot('PAKNECONOTHRXN',pct=False,rename=True,threshold=.01,lag=False); #decomp of the change in the level
```

```text
<Figure size 1000x500 with 1 Axes>
```

In the following example the change in the level of the dependent variable is displayed for a restricted time period.  Here the distinction between the initial impulse (import prices) and the lagged effect of past prices is very evident.

```python
with mpak.set_smpl(2020,2030):
    fig=mpak.dekomp_plot('PAKNECONOTHRXN',pct=False,rename=True,threshold=.005,lag=False); #decomp of the change in the level
```

```text
<Figure size 1000x500 with 1 Axes>
```

### the time_att option

The above displays focused on the difference between the values in the two dataframes `basedf` and `lastdf`.

By setting he time_att option to True, `get_att()` displays the contribution of changes in the levels of the RHS variables between t and t-1,in explaining the changes in the LHS variable between t and t-1 with all data pulled from the same `.lastdf` datafame.


With the `time_att` option set **only the .lastdf dataframe** is used.   The comparison is not .basedf vs .lastdf but the influence of last year's changes on the level of this year's variable. The attribution is calculated by lagging each right hand side variable one year and recalculating the equation.

```python
mpak.PAKCCEMISCO2TKN .get_att(time_att= True,type='level',bare=0);
```

```text
<pandas.io.formats.style.Styler at 0x2934e06ae90>
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

```python
help(mpak.get_att)
```

```text
Help on method get_att in module modelclass:

get_att(
    n,
    type='pct',
    filter=False,
    lag=True,
    start='',
    end='',
    time_att=False,
    threshold=0.0
) method of modelclass.model instance
    Calculate the attribution percentage for a variable.

    Parameters:
        n (str): Name of the variable to calculate attribution for.
        type (str): Type of attribution calculation. Options: 'pct' (percentage), 'level', 'growth'. Default: 'pct'.
        filter (bool): [Deprecated] Use threshold instead of filter. Default: False.
        lag (bool): Flag to indicate whether to include lag information in the output. Default: True.
        start (str): Start period for calculation. If not provided, uses the first period in the model instance. Default: ''.
        end (str): End period for calculation. If not provided, uses the last period in the model instance. Default: ''.
        time_att (bool): Flag to indicate time attribute calculation. Default: False.
        threshold (float): Threshold value for excluding rows with values close to zero. Default: 0.0.

    Returns:
        pandas.DataFrame: DataFrame containing the calculated attribution results.

    Raises:
        Exception: If an invalid type is provided.
```

```python
help(mpak.dekomp_plot)
```

```text
Help on method dekomp_plot in module modelclass:

dekomp_plot(
    varnavn,
    sort=True,
    pct=True,
    per='',
    top=0.9,
    threshold=0.0,
    lag=True,
    rename=True,
    nametrans=<function Dekomp_Mixin.<lambda> at 0x000002934C4783B0>,
    time_att=False
) method of modelclass.model instance
    Returns  a chart with attribution for a variable over the smpl

    Parameters
    ----------
    varnavn : TYPE
        variable name.
    sort : TYPE, optional
        . The default is False.
    pct : TYPE, optional
        display pct contribution . The default is True.
    per : TYPE, optional
        DESCRIPTION. The default is ''.
    threshold : TYPE, optional
        cutoff. The default is 0.0.
    rename : TYPE, optional
        Use descriptions instead of variable names. The default is True.
    time_att : TYPE, optional
        Do time attribution . The default is False.
    lag : TYPE, optional
       separete by lags The default is True.
    top : TYPE, optional
      where to place the title


    Returns
    -------
    a matplotlib figure instance .
```

## Trace and decomposition combined

The `.tracepre()` method can combine the graphical representation of the `tracepre()` method described in the previous chapter and the tabular results from `dekomp()`.  

This is implicit in the standard call to `.tracepre()`where the thickness of the lines is derived from the empirical importance of the changes in each LHS variable in determining the change in the RHS variable.  

```python
mpak.PAKNECONPRVTKN.tracepre(png=latex,size=(2,4));
```

## Tabular output from tracepre()

The results for `.tracepre` can be displayed in a number of ways and the results can be saved as pictures. 

|||
|:--|:--|
|**up = xx**|determines how many levels of parents to include|
|**showdata\|sd=True**|Causes the tables of attribution for each displayed variable to be displayed|
|**showdata\|sd=\<'pattern of variable names'>**|will include a table of values for each variable matching the pattern (including wildcharts|
|**attshow\|ats = True**| adds in the contribution of each to the total change|
|**growthshow\|gs = True**| will include a table of growth for each variable|
|**HR = True**| will reorient the dependency graph|
|**filter=\<xx>**|restrict outputs to variables that explain at least xx% of the change in the level of dependent variable |
|**browser = True**|Opens a browser with the resulting dependency graph - useful for zooming on a big graph or table|
|**pgn = True**|will display as a png picture
|**svg = True**|will display as a svg picture which can be zoomed
|**pdf = True**|will display as a pdf picture
|**eps = True**|will create a eps file (a latex format)
|**saveas = \<a file name without extension>**|will save the picture wit the filename with an added extension reflection the picture type     
    

```python
with mpak.set_smpl(2020,2030):
    mpak.PAKNECONOTHRXN.tracepre(filter=5.0,HR=False,showdata= True,attshow=True,per=2020,png=latex)
```

The big difference with this representation is the contributions of both the direct that directly impact the LHS variable (as well as the influence of those variables one or two steps up the causal chain) can be traced.

Below the same command as above but we specify that we want to go up two levels in the causal chain.

```python
with mpak.set_smpl(2020,2030):
    mpak.PAKNECONOTHRXN.tracepre(up=2,filter=5,HR=False,sd= True,ats=True,png=latex)
```

```python
with mpak.set_smpl(2020,2023):
    mpak.PAKNECONPRVTKN.tracepre(sd='*lcn',filter=10,HR=1,ats=1,up=2
    ,growthshow=1,png=latex)
```

```text
No graph PAKNECONPRVTKN
The graph is empty
Perhaps filter prunes to much
```

As indicated by the error message the filter is too fine, and has eliminated all variables from the output.  Below the same command without the filter option.

```python
with mpak.set_smpl(2020,2023):
    mpak.PAKNECONPRVTKN.tracepre(sd='*lcn',HR=1,ats=1,up=2
    ,growthshow=1,png=latex)
```

## Chart of the contributions over time 

```python


with mpak.set_smpl(2020,2030):
    mpak.dekomp_plot('PAKNYGDPFCSTXN',threshold=5);  # gives a waterfall of contributions
```

```text
<Figure size 1000x500 with 1 Axes>
```

## Chart of the contributions for one year
It can be useful to visualize the attribution as a waterfall chart for a single year

```python
mpak.dekomp_plot_per('PAKNYGDPFCSTXN',per=2027,threshold=5)  # gives a waterfall of contributions
```

```text
<Figure size 1000x700 with 1 Axes>
```

```python
mpak.dekomp_plot_per('PAKNYGDPFCSTXN',per=2027,threshold=5)  # gives a waterfall of contributions
```

```text
<Figure size 1000x700 with 1 Axes>
```

## Sorted waterfall of contributions

```python
mpak.dekomp_plot_per('PAKNYGDPFCSTXN',per=2029,threshold=5,sort=True)  # gives a waterfall of contributions
```

```text
<Figure size 1000x700 with 1 Axes>
```

:name: impactmodel


:name: exodif

## Impacts at the model level: the `.totdif()` method 

The method `.totdif()` returns an instance of the totdif class, which provides a number of methods and properties to explore decomposition at the model level.

It works by solving the model numerous times, each time changing one of the right hand side variables and calculating the impact on all dependent variables. By default it uses the values from the `.lastdf` `DataFrame` as the shock values and the values in `.basedf` as the initial values. Separate simulations are run for every exogenous (or exogenized) variables that have changed between the two `DataFrame`s. 

For advanced users the RHS variables can be grouped into user defined blocks, which in cases where there are many changes can help identify the main causal pathways.

### The `.exo_dif()` method 
The `.exodif()` method displays only the exogenous variables that have changed between the two `DataFrame`s (the shock). Exogenous variables whose results have not changed are omitted. It determines which of the exogenous variables have changed between `.lastdf`and `.basedf` and then returns a `DataFrame` with the changes in the values. 

In this case the `DataFrame` contains the effect of updating the $CO^2$ tax to 30 for coal, gas and oil. `.exo_dif()` is automatically called by the `.totdif()` method but can also be called directly b y the user. 

```python
mpak.exodif()
```

```text
PAKGGREVCO2CER  PAKGGREVCO2GER  PAKGGREVCO2OER
2020           35.55            71.0           38.71
2021           35.55            71.0           38.71
2022           35.55            71.0           38.71
2023           35.55            71.0           38.71
2024           35.55            71.0           38.71
...              ...             ...             ...
2096           35.55            71.0           38.71
2097           35.55            71.0           38.71
2098           35.55            71.0           38.71
2099           35.55            71.0           38.71
2100           35.55            71.0           38.71

[81 rows x 3 columns]
```

### The `.totdif()` command calculates the contribution of each changed variable to the changes in a specified LHS variable
This involves solving the model a number of times, so can take some time. How long it takes to execute will depend on the computer, the model and the number of changes made.  In this instance the `.totaldif` takes between 2 and 5 seconds depending on computer. 

```python
totdekomp = mpak.totdif() # Calculate the total derivative½s of all equations in the model.
```

```text
Total dekomp took       :         3.558 Seconds
```

### The method `.explain_all()` presents the results graphically

In the example below, the relative importance of the three shocked carbon taxes on the change in real GDP are presented.

```python
showvar = 'PAKNYGDPMKTPKN'
totdekomp.explain_all(showvar,kind='area',use='growth',stacked=True,
                      title="Contributions of different carbon taxes to Real GDP growth") ;
```

```text
<Figure size 1000x500 with 1 Axes>
```

```python
help(totdekomp.explain_all)
```

```text
Help on method explain_all in module modeldekom:

explain_all(
    pat='',
    stacked=True,
    kind='bar',
    top=0.9,
    title='',
    use='level',
    threshold=0.0,
    resample='',
    axvline=None
) method of modeldekom.totdif instance
    Explains all

    Args:
        pat (TYPE, optional): DESCRIPTION. Defaults to ''.
        stacked (TYPE, optional): DESCRIPTION. Defaults to True.
        kind (TYPE, optional): DESCRIPTION. Defaults to 'bar'.
        top (TYPE, optional): DESCRIPTION. Defaults to 0.9.
        title (TYPE, optional): DESCRIPTION. Defaults to ''.
        use (TYPE, optional): DESCRIPTION. Defaults to 'level'.
        threshold (TYPE, optional): DESCRIPTION. Defaults to 0.0.
        resample (TYPE, optional): DESCRIPTION. Defaults to ''.
        axvline (TYPE, optional): DESCRIPTION. Defaults to None.

    Returns:
        None.
```

### Many variables

If many variables are passed to explain_all then separate graphs will be created for each.

```python
showvar = 'PAKNYGDPMKTPKN PAKCCEMISCO2CKN PAKCCEMISCO2OKN PAKCCEMISCO2GKN PAKGGREVTOTLCN'

totdekomp.explain_all(showvar,kind='area',stacked=True,title="Contributions of different carbon taxes to Real GDP,growth") ;
```

```text
<Figure size 1000x2500 with 5 Axes>
```

### Similarly the impacts on different variables for one year can be shown

```python
showvar = 'PAKNYGDPMKTPKN PAKNECONPRVTXN'

totdekomp.explain_per(showvar,per=2028,ysize=8,title='Decomposition, level=2023')
```

```text
<Figure size 1000x1600 with 2 Axes>
```

### Or an interactive widgets can be generated
This allows the user to select the specific variable of interest and what to display: 



If this is read in a manual the widget is not live. 

In a notebook the selection widgets are live. 

```python
mpak.get_att_gui(var='PAKGGREVTOTLCN',ysize=7)
```

```text
interactive(children=(Dropdown(description='Variable', index=108, options=('CHNEXR05', 'CHNPCEXN05', 'DEUEXR05…
```

    :alt: Menu to start notebooks in subfolders
    :class: bg-primary mb-1
    :width: 70%
    :align: center

### Decomposition of the last year 

```python
showvar = 'PAKNYGDPMKTPKN'
totdekomp.explain_last(showvar,ysize=8,title='Decomposition last period, level')
```

```text
<Figure size 1000x800 with 1 Axes>
```

### Decomposition of accumulated effects 

```python
totdekomp.explain_sum(showvar,ysize=8,title="Decomposition, sum over all periods,level")
```

```text
<Figure size 1000x800 with 1 Axes>
```

## More advanced model attribution

For some  simulations the number of changed exogenous variables can be large. Using a dictionary to contain the experiments allows us to manage multiple scenarios and multiple outputs. 

Using this approach, if there are many simulations, data can be filtered in order to look only at the variables with an impact above a certain threshold. 

### Grouping variables
If many exogenous variables were shocked, exploring impacts may be made easier by aggregating the impacts of some groups or sub-groups of variables. Grouping  variables allows the user to explore the results in a more flexible way slicing and dicing the impact along different dimensions. 

In the example below, the impacts of changing the carbon tax on gas and oil tax are grouped together (aggregated) and the impact of the coal tax is displayed separately. 

```python
shocks = {'gas and Oil':['PAKGGREVCO2OER', 'PAKGGREVCO2GER'],'Coal':['PAKGGREVCO2CER']}
totdekomp_group = mpak.totdif(experiments = shocks) # Calculate the total derivative½s of all equations in the model.
```

```text
Total dekomp took       :         2.417 Seconds
```

```python
showvar = 'PAKNYGDPMKTPKN'
totdekomp_group.explain_all(showvar,kind='area',stacked=True,title='GDP impact of coal and non-coal carbon taxes');
```

```text
<Figure size 1000x500 with 1 Axes>
```

While this is a fairly simple example, the grouping mechanism allows us to focus our attention on one factor (the coal price in this instance).  

Here, even though the coal tax was increased by the most (in the baseline it was subsidized), it had a relatively small share in total energy production, so its GDP impact was relatively small.

### Single equation attribution chart 
The results can be visualized in different ways. 

```python
mpak.dekomp_plot_per('PAKNYGDPMKTPKN',
                     per=2025,           # Period to be displayed
                     pct=False,          # Do not show differences as percent changes
                     rename=True,        # Use the long-form vs mnemonic description of variable
                     sort=True,          # 
                     threshold =200000,
                     ysize=7            # Size of y axis in inches   
                     )
```

```text
<Figure size 1000x700 with 1 Axes>
```

### Decomposition of changes over time 



A classic query is to understand what is driving changes over time.  The `time_att=True` option quantifies the impact of changes over time in the LHS variables on changes in the dependent variable over time using data from the `lastdf` `DataFrame`.  

```python
with mpak.set_smpl(2020,2024):
    mpak['PAKNYGDPMKTPKN'].dekomp(time_att=True)
```

```text

Formula        : FRML <IDENT> PAKNYGDPMKTPKN = PAKNECONPRVTKN+PAKNECONGOVTKN+PAKNEGDIFTOTKN+PAKNEGDISTKBKN+PAKNEEXPGNFSKN-PAKNEIMPGNFSKN+PAKNYGDPDISCKN+PAKADAP*PAKDISPREPKN $ 

                      2020        2021        2022        2023        2024
Variable   lag                                                            
t-1        0   25760579.37 26273942.22 26511370.46 26685141.91 26963077.59
t          0   26273942.22 26511370.46 26685141.91 26963077.59 27393200.45
Difference 0     513362.86   237428.23   173771.45   277935.69   430122.85
Percent    0          1.99        0.90        0.66        1.04        1.60

 Contributions to difference for  PAKNYGDPMKTPKN
                         2020       2021       2022       2023       2024
Variable       lag                                                       
PAKNECONPRVTKN 0    654250.10  299926.97  191312.65  263735.02  390661.47
PAKNECONGOVTKN 0     67306.62   30293.58   26781.38   52462.03   84392.13
PAKNEGDIFTOTKN 0     60338.01   36679.60   21435.92   19393.71   24600.23
PAKNEGDISTKBKN 0      9896.77   10138.33   10385.78   10639.27   10898.95
PAKNEEXPGNFSKN 0     96445.77  110587.72  118464.57  122733.42  124943.57
PAKNEIMPGNFSKN 0   -376170.79 -251525.99 -195969.30 -192421.42 -206801.16
PAKNYGDPDISCKN 0      1296.39    1328.03    1360.45    1393.65    1427.67
PAKADAP        0        -0.00      -0.00      -0.00      -0.00      -0.00
PAKDISPREPKN   0        -0.00      -0.00      -0.00      -0.00      -0.00

 Share of contributions to difference for  PAKNYGDPMKTPKN
                         2020       2021       2022       2023       2024
Variable       lag                                                       
PAKNECONPRVTKN 0         127%       126%       110%        95%        91%
PAKNEEXPGNFSKN 0          19%        47%        68%        44%        29%
PAKNECONGOVTKN 0          13%        13%        15%        19%        20%
PAKNEGDIFTOTKN 0          12%        15%        12%         7%         6%
PAKNEGDISTKBKN 0           2%         4%         6%         4%         3%
PAKNYGDPDISCKN 0           0%         1%         1%         1%         0%
PAKADAP        0          -0%        -0%        -0%        -0%        -0%
PAKDISPREPKN   0          -0%        -0%        -0%        -0%        -0%
PAKNEIMPGNFSKN 0         -73%      -106%      -113%       -69%       -48%
Total          0         100%       100%       100%       100%       100%
Residual       0          -0%        -0%        -0%        -0%        -0%

 Difference in growth rate PAKNYGDPMKTPKN
                     2020       2021       2022       2023       2024
Variable   lag                                                       
t-1        0         4.7%       2.0%       0.9%       0.7%       1.0%
t          0         2.0%       0.9%       0.7%       1.0%       1.6%
Difference 0        -2.7%      -1.1%      -0.2%       0.4%       0.6%
None

 Contribution to growth rate PAKNYGDPMKTPKN
                         2020       2021       2022       2023       2024
Variable       lag                                                       
PAKNECONPRVTKN 0        -3.4%      -1.4%      -0.4%       0.3%       0.5%
PAKNECONGOVTKN 0        -0.3%      -0.1%      -0.0%       0.1%       0.1%
PAKNEGDIFTOTKN 0        -0.1%      -0.1%      -0.1%      -0.0%       0.0%
PAKNEGDISTKBKN 0         0.0%       0.0%       0.0%       0.0%       0.0%
PAKNEEXPGNFSKN 0         0.1%       0.1%       0.0%       0.0%       0.0%
PAKNEIMPGNFSKN 0         0.9%       0.5%       0.2%       0.0%      -0.0%
PAKNYGDPDISCKN 0         0.0%       0.0%       0.0%       0.0%       0.0%
PAKADAP        0         0.0%       0.0%      -0.0%       0.0%      -0.0%
PAKDISPREPKN   0         0.0%       0.0%      -0.0%       0.0%      -0.0%
Total          0        -2.8%      -1.1%      -0.3%       0.4%       0.6%
Residual       0        -0.1%      -0.0%      -0.0%      -0.0%      -0.0%
```

```python
mpak.dekomp_plot('PAKNYGDPMKTPKN',pct=0,rename=1,sort=1,threshold =0,time_att = True);
```

```text
<Figure size 1000x500 with 1 Axes>
```
