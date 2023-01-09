#!/usr/bin/env python
# coding: utf-8

# # What is a Model in ModelFlow ?

# The term [**model**](https://en.wikipedia.org/wiki/Model) can mean different things to different people. A model in the eyes of the ModelFlow library is a **discrete** model that can be defined as one or several **mathematical equations**. The equations are the same for every time frame, $t$ and *can* have **lagged** and **leaded** variables.
# 
# A good book on model solution is {cite:author}`Pauletto97` also  {cite:author}`Petersen1987` is a useful paper. 
# 
# Such a model could consist of one or several equations where:
# 
#  - $\mathbf{n}$ number of endogenous variables
#  - $\mathbf{k}$ number of exogenous variables
#  - $\mathbf{u}$ max lead of endogenous variables
#  - $\mathbf{r}$ max lag of endogenous variables
#  - $\mathbf{s}$ max lag of exogenous variables
#  - $t$ time frame (year, quarter, day or any other unit)
# 
# and can be written in a **normalized** or **un-normalized** form.

# ## Normalized model

# The following model consists of a number of equations. Each equations represents the relationship between an endogenous variable in the model (on the left side) and a series of variables that it depends on (on the right side of the equation). The number of endogenous variables is equal to the number of equations.

# \begin{align*}
# y_t^1  &=  f^1(y_{t+u}^1...,y_{t+u}^n...,y_t^2...,y_{t}^n...y_{t-r}^1...,y_{t-r}^n,x_t^1...x_{t}^k,...x_{t-s}^1...,x_{t-s}^k) \\
# y_t^2  &=  f^2(y_{t+u}^1...,y_{t+u}^n...,y_t^1...,y_{t}^n...y_{t-r}^1...,y_{t-r}^n,x_t^1...x_{t}^k,...x_{t-s}^1...,x_{t-s}^k) \\
# \vdots \\
# y_t^n  &=  f^n(y_{t+u}^1...,y_{t+u}^n...,y_t^1...,y_{t}^{n-1}...y_{t-r}^1...,y_{t-r}^n,x_t^1...x_{t}^r,x..._{t-s}^1...,x_{t-s}^k)
# \end{align*}

# The model can also be written in matrix notation where  $\mathbf{y}_t$ and $\mathbf{x}_t$ are vectors of endogenous/exogenous variables for time $t$.
# 
# $$
# \mathbf{y}_t = \mathbf{F}(\mathbf{y}_{t+u} \cdots \mathbf{y}_t \cdots \mathbf{y}_{t-r},\mathbf{x}_t \cdots \mathbf{x}_{t-s})
# $$
# 
# 
# ModelFlow allows the variables (the  $𝐱$'s and $𝐲$'s) to be scalars, matrices, arrays or Pandas DataFrames.

# ## Un-normalized form
# Some models can not easily be specified as normalized formulas.

# Especially for models with equilibrium conditions not involving price, the the more general un-normalized form is more suitable. This means that instead of our endogenous variables on the left side the left hand side is ```0``` and the right hand side is an expression. 
# 
# A very simple demand/supply model with three endogenous variables: demand, supply and price model looks like this:  
# 
# \begin{align*}
# demand_t  &=  f^1(price_t) \\
# supply_t  &= f^2(price_t)\\ 
# demand_t &= supply_t
# \end{align*}
# 
# If it is difficult to rewrite the model with  an explicit expression for the price, the model can be made to an un-normalized model:  
# 
# \begin{align*}
# 0   &=  f^1(price_t)-demand_t \\
# 0 &= f^2(price_t)-supply_t\\ 
# 0 &= supply_t-demand_t
# \end{align*}
# 
# Which can be solved. 
# The number of endogenous variables and equations should still be the same. And the model developer has to define which variables are endogenous. 

# Written in matrix notation an un-normalized model looks like this:
# 
# $$
# \mathbf{0} = \mathbf{G}(\mathbf{y}_{t+u} \cdots \mathbf{y}_t \cdots \mathbf{y}_{t-r},\mathbf{x}_t \cdots \mathbf{x}_{t-s})
# $$

# ## A model solution
# The purpose of models (in this context) is to combine the model with data and find values for endogenous variables consistent with the model and the data - a **solution**
# 
# For a normalized model:
# 
# $$
# \mathbf{y}_t  = \mathbf{F}(\mathbf{y}_{t+u} \cdots \mathbf{y}_t \cdots \mathbf{y}_{t-r},\mathbf{x}_t \cdots \mathbf{x}_{t-r})
# $$
# 
# a solution is  $\mathbf{y}_t^{*}$ so that:
# 
# 
# $$
# \mathbf{y}_t^* = \mathbf{F}(\mathbf{y}_{t+u} \cdots \mathbf{y}_t^* \cdots \mathbf{y}_{t-r},\mathbf{x}_t \cdots \mathbf{x}_{t-r})
# $$

# For the un-normalized model:
# 
# $$
# \mathbf{0} = \mathbf{G}(\mathbf{y}_{t+u} \cdots \mathbf{y}_t \cdots \mathbf{y}_{t-r},\mathbf{x}_t \cdots \mathbf{x}_{t-s})
# $$
# 
# 
# a solution $\mathbf{y}_t^*$ is:
# 
# $$
# \mathbf{0} =\mathbf{G}(\mathbf{y}_{t+u} \cdots \mathbf{y}_t^* \cdots \mathbf{y}_{t-r},\mathbf{x}_t \cdots \mathbf{x}_{t-r})
# $$

# The functions $f^i$ can be linear or nonlinear. There is no guarantee that a model has a solution - or that it has only one solution. Hopeful Modelflow will be able to find a solution but it can depend on the starting point.

# # Solution methods
# 
# There are several ways to solve a model (a system of equations) as mentioned above. ModelFlow can apply three different types of model solution methods:

#  1. If the model has **no contemporaneous feedback** the equations can be sorted
#  [topologically](https://en.wikipedia.org/wiki/Topological_sorting) and can be solved in the topological order. This method is similar to the approach of an Excel spreadsheet.
#  2. If the model has **contemporaneous feedback**, the model should be solved in an iterative way. Using for example:
#      1. [The Gauss-Seidle method](https://en.wikipedia.org/wiki/Gauss%E2%80%93Seidel_method) (**Gauss**) which can handle large systems, is fairly robust and does not need the calculation of derivatives.
#      2. [The Newton-Raphson method](https://en.wikipedia.org/wiki/Newton%27s_method) (**Newton**) which requires the calculation of derivatives and solving of a large linear system but typically converges in fewer iterations.
#  3. If the model has **leaded endogenous variables**, the Gauss variation [Fair-Taylor](https://fairmodel.econ.yale.edu/rayfair/pdf/1983A.PDF) or Stacked-Newton Method should be used. The **stacked Newton** method can be used in all cases, but if not needed, it will usually use more memory and be slower.
#  
# 
# Nearly all of the models solved by ModelFlow don't contain leaded endogenous variables. Therefore, they can be solved one period at a time. For large sparse nonlinear models Gauss works fine. It solves a model quite fast and we don't need the additional handiwork of handling derivatives and solve large linear systems that Newton methods require. Moreover many models in question do not have smooth derivatives. The order in which the equation are calculated can however have a large impact on the convergence speed.
# 
# For some models the Newton algorithm works better. Some models are not able to converge with Gauss-Seidle other models are just faster using Newton. Also with Newton the ordering of equations does not matter for the convergence speed.
# 
# Some models like [FRB/US](https://www.federalreserve.gov/econres/us-models-about.htm)  and other with **rational expectations** or **model consistent expectations** contains leaded endogenous variables. Such models typical have to be solved as one system for all projection periods. In this case, the Gauss variation Fair-Taylor or Stacked-Newton Method should be used.

# | Model  | No contemporaneous feedback | Contemporaneous feedback | Leaded variables |
# | --- | --- | --- |--- |
# |Normalized | Calculate | Gauss or <br> Newton  | Fair Taylor or <br> Stacked Newton|
# |Un-normalized | Newton | Newton | Stacked Newton |

# (solution-methods)=
# ## Solution methods for normalized models
# 
# ### Calculation, No contemporaneous feedback
# 
# In systems with no lags each period can be solved in succession.
# The equations have to be evaluated in a logical (topological sorted) order.
# 
# Let:
#  - $z$ be all predetermined values: all exogenous variables and lagged endogenous variables. 
# 
# Order the $n$ endogenous variables in topological order.
# 
# For each time period we can find a solution by:
# 
# >for $i$ = 1 to $n$
# >>$y_{i}^{k} = f_i(y_1^{k},\cdots,y_{i-1}^{k},y_{i+1}^{k-1},\cdots,y_{n}^{k-1},z)$

# ### The Gauss-Seidel algorithm. Models with contemporaneous feedback
# The Gauss-Seidel algorithm is quite straight forward. It basically iterates over the formulas, until convergence.
# 
# Let:
#  - $z$ be all predetermined values: all exogenous variables and lagged endogenous variables.
#  - $n$ be the number of endogenous variables.
#  - $\alpha$ dampening factor which can be applied to selected equations.
# 
# For each time period we can find a solution by doing Gauss-Seidel iterations:
# 
# >for $k = 1$ to convergence
# >>for $i$ = 1 to $n$
# >>>$y_{i}^{k} = (1-\alpha) * y_{i}^{{k-1}} + \alpha f_i(y_1^{k},\cdots,y_{i-1}^{k},y_{i+1}^{k-1},\cdots,y_{n}^{k-1},z)$

# ### The Newton-Raphson algorithm. Models with contemporaneous feedback
# 
# Let: 
#  - $\bf{z}$ be a vector all predetermined values: All exogenous variables and lagged endogenous variables.
#  - $\textbf{A}_t = \cfrac{\partial \textbf{F}}{\partial \textbf{y}_t^T}$ Jacobi matrix of derivatives with respect to current endogenous variables. 
#  - $\alpha$ dampening factor. 
# 
# 
# For each time period we can find a solution by doing Newton-Raphson iterations:<br>
# 
# >for $k = 1$ to convergence
# >>$\bf{y} = \bf{F(y^{k-1},z)}$
# >>$\bf{y}^{k} =  \bf{y} - \alpha \times  \bf{(A-I)}^{-1} \times ( \bf{y - y^{k-1} })$
# 
# ### On solving sets of linear equations
# 
# The expression: $\bf{(A-I)}^{-1}\times  (\bf{y - y^{k-1}})$ is the same as finding the solution $\bf{x}$ to the set of linear equations:
# 
# $\bf{y- y^{k-1} } = \bf{(A-I)} \times \bf{x}$
# 
# This problem can be solved much more efficiently than performing $\bf{(A-I)}^{-1}\times  ( \bf{y - y^{k-1} })$. One way is to 
# find a [LU decomposition](https://en.wikipedia.org/wiki/LU_decomposition). But other methods can also be used. 
# 
# The Python Scipy library provides a number of solvers to this linear set of equations. There are both solvers using LU-decomposition and iterative methods, and there are solvers for dense and sparse matrices. Any linear solvers can be incorporated into ModelFlows Newton-Raphson nonlinear solver. The [Scipy library](https://scipy.org/scipylib/index.html) utilizes the [Intel® Math Kernel Library](https://software.intel.com/en-us/mkl). 
# 
# The default solver is using a sparse LU-decomposition. It can handle quite large (as in very large) problems. 
# 
# The costly operation in this algorithm is the LU-decomposition. Therefore  $\bf{A}$ is not updated in every iteration. 

# ### Stacked Newton-Raphson. Models with both leaded and lagged endogenous variable
# 
# If the model has leaded endogenous variables, it can generally not be solved one time period at a time. The model should therefore be solved as one large model.
# 
# Let: 
#  - $\bf{z}$ be a vector all predetermined values: all exogenous variables and lagged endogenous variables.
#  - $u$ Max number of leads  
#  - $r$ Max number of lags  
#  - $\alpha$ dampening factor 
# 
#  - $\textbf{A}_t = \cfrac{\partial \textbf{F}}{\partial \textbf{y}_t^T}$ Derivatives with respect to current endogenous variables 
#  - $\textbf{D}_t^j =  \cfrac{\partial \textbf{F}}{\partial \textbf{y}_{t+j}^T } \hspace{5 mm} j=1, \cdots , u  \hspace{1 mm}\mbox{  Derivatives with respect to leaded endogeneous variables  }$
#  - $\textbf{E}_t^i  =  \cfrac{\partial \textbf{F}}{\partial \textbf{y}_{t-i}^T } \hspace{5 mm} i=1, \cdots , r  \hspace{1 mm}\mbox{  Derivatives with respect to lagged endogeneous variables  }$
# 
# Now the $\bf{\bar A}$, $\bar y$ and $\bar F$ which covers the total model for all time frames can be constructed like this: 
# 
# $$\bf{\bar A} =\begin{bmatrix}
# 		\bf{A_1}   & \bf{D_1^1} & \bf{D_1^2} & \bf{0}     &\bf{0}      &\bf{0}      &\bf{0}      &\bf{0}  \\
#         \bf{E_2^1} & \bf{A_2}   & \bf{D_2^1} & \bf{D_2^2} &\bf{0}      &\bf{0}      &\bf{0}      &\bf{0} \\
#         \bf{E_3^2} & \bf{E_3^1} & \bf{A_3}   & \bf{D_3^1} & \bf{D_3^2} &\bf{0}      &\bf{0}      &\bf{0} \\
#         \bf{E_4^3} & \bf{E_4^2} & \bf{E_4^1} & \bf{A_4}   & \bf{D_4^1} & \bf{D_4^2} &\bf{0}      & \bf{0} \\
#         \bf{0}     & \bf{E_5^3} & \bf{E_5^2} & \bf{E_5^1} & \bf{A_5}   & \bf{D_5^1} & \bf{D_5^2} &\bf{0}\\
#         \bf{0}     & \bf{0}     & \bf{E_6^3} & \bf{E_6^2} & \bf{E_6^1} & \bf{A_6}   & \bf{D_6^1} & \bf{D_6^2}\\
#         \bf{0}     & \bf{0}     & \bf{0}     & \bf{E_7^3} & \bf{E_7^2} & \bf{E_7^1} & \bf{A_7}   & \bf{D_7^1} \\
#         \bf{0}     & \bf{0}     & \bf{0}     & \bf{0}     & \bf{E_8^3} & \bf{E_8^2} & \bf{E_8^1} & \bf{A_8} \\
# \end{bmatrix} \bar y = \begin{bmatrix}\bf{y_1}\\\bf{y_2}\\\bf{y_3}\\ \bf{y_4} \\\bf{y_5} \\\bf{y_6} \\ \bf{y_7} \\ \bf{y_8} \end{bmatrix} \bar F = \begin{bmatrix}\bf{F}\\\bf{F}\\\bf{F}\\ \bf{F} \\\bf{F} \\\bf{F} \\ \bf{F} \\ \bf{F} \end{bmatrix}$$
# 
# 
# And the solution algorithm looks like this:
# 
# Again, let $\bf{z}$ be a vector of all predetermined values: All exogenous variables and endogenous variables before and after the simulation time.
# 
# >for $k = 1$ to convergence<br>
# >>$\bf{\bar y} = \bf{\bar F(\bar y^{k-1},\bar z) }$<br>
# >>$\bf{\bar y^{k}} =  \bf{\bar y} - \alpha \times \bf{(\bar A-I)}^{-1}\times ( \bf{\bar y - \bar y^{k-1}})$
# 
# 
# The update frequency of $\bf{\bar A}$ and $\alpha$ and the value of $\alpha$ can be set to manage the speed and stability of the algorithm.
# 
# We solve the problem: $(\bf{\bar y - \bar y^{k-1} }) = \bf{(\bar A-I)}\times \bf{x}$ instead of inverting  $\bf{A}$.
# 
# The comments above on solving the sets of linear equations also apply for this case. 

# ## Un-normalized model
# 
# ### Stacked Newton-Raphson algorithm
# 
# If the model has leaded endogenous variables it can, in general, not be solved one time period at a time. We have to solve the model for all time frames as one large model.
# 
# For the Newton-Raphson algorithm we now have to stack all the derivative matrices. The stacked matrices of a model with a max lag of three and a max lead of two spanning over eight periods look like this </span>
# 
# $$\bf{\bar A} =\begin{bmatrix}
# 		\bf{A_1}   & \bf{D_1^1} & \bf{D_1^2} & \bf{0}     &\bf{0}      &\bf{0}      &\bf{0}      &\bf{0}  \\
#         \bf{E_2^1} & \bf{A_2}   & \bf{D_2^1} & \bf{D_2^2} &\bf{0}      &\bf{0}      &\bf{0}      &\bf{0} \\
#         \bf{E_3^2} & \bf{E_3^1} & \bf{A_3}   & \bf{D_3^1} & \bf{D_3^2} &\bf{0}      &\bf{0}      &\bf{0} \\
#         \bf{E_4^3} & \bf{E_4^2} & \bf{E_4^1} & \bf{A_4}   & \bf{D_4^1} & \bf{D_4^2} &\bf{0}      & \bf{0} \\
#         \bf{0}     & \bf{E_5^3} & \bf{E_5^2} & \bf{E_5^1} & \bf{A_5}   & \bf{D_5^1} & \bf{D_5^2} &\bf{0}\\
#         \bf{0}     & \bf{0}     & \bf{E_6^3} & \bf{E_6^2} & \bf{E_6^1} & \bf{A_6}   & \bf{D_6^1} & \bf{D_6^2}\\
#         \bf{0}     & \bf{0}     & \bf{0}     & \bf{E_7^3} & \bf{E_7^2} & \bf{E_7^1} & \bf{A_7}   & \bf{D_7^1} \\
#         \bf{0}     & \bf{0}     & \bf{0}     & \bf{0}     & \bf{E_8^3} & \bf{E_8^2} & \bf{E_8^1} & \bf{A_8} \\
# \end{bmatrix} \bar y = \begin{bmatrix}\bf{y_1}\\\bf{y_2}\\\bf{y_3}\\ \bf{y_4} \\\bf{y_5} \\\bf{y_6} \\ \bf{y_7} \\ \bf{y_8} \end{bmatrix} \bar F = \begin{bmatrix}\bf{F}\\\bf{F}\\\bf{F}\\ \bf{F} \\\bf{F} \\\bf{F} \\ \bf{F} \\ \bf{F} \end{bmatrix}$$
# 
# 
# $$\bf \bar z$$ contains all predetermined variable.
# 
# Now the solution algorithm looks like this.
# 
# >for $k = 1$ to convergence
# >>$\bf{\bar y\_residual} = \bf {\bar G(\bar y^{k-1},\bar z) }$
# >>$\bf{\bar y^{k}} =  \bf{\bar y} - \bf{\bar A}^{-1} \times \bf {\bar y\_residual}$
# 
# Notice that the model $\bf G$ is the same for all time periods
# 
# Again we don't compute $\bf{\bar y} - \bf{\bar A}^{-1} \times \bf {\bar y\_residual}$ which requires the "expensive" inversion of a matrix but solve the problem: $\bf{\bar y\_residual}=\bf{\bar A} \times \bf  x$ which can be done much faster.
# 
# 
# Models without leaded variables are solved period for period along the same lines. 

# ## Modelflow and solving
# Solving of models can incorporate a lot of methods to improve the speed. The approach in modelflow has been to use existing python libraries as much as possible and to apply the methods useful for the models at hand. 
# 
# With some knowledge of python and numerical methods it is possible to implement new methods and improvements. 
