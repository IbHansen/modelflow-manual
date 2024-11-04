:::{note}
I would find a home for this which is more general concerning modelflow /Ib 

Modelflow is a library based on the needs of Economists in particular. Economists often work with time series and want to make calculations based on the time indexed values of a number of variables. 

For example we may say that 

$\hat p_t = \hat p^e_{t}+  \alpha * (Y_t/Y^{pot}_t -1) + \beta *  (\hat p_{t-1}- \hat p^e_{t-1})$

The inflation rate ($\hat p_t$) in time t is a function of expected inflation ($p^e_{t}$), the output gap $(Y_t/Y^{pot}_t -1)$ and the one period earlier difference between the inflation rate and expected inflation  $\hat p_{t-1}$

Or we may want to have a system of simultaneous equations that allow for circular references, such that 

$Y_t = C_t +I_t +G_t +X_t - M_t$ 

$C_t= f(Y_t)$

$I_t= f(Y_t)$

$M_t= f(C_t,I_t)$
:::