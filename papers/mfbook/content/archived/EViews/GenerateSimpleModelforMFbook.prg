close @all
wfopen M:\wbg_mfmod\data\BGDsoln.wf1

wfcreate example a 2000 2030

'Now we create the new varBGDsolnnolsoln::iables'
smpl @all
series y=BGDsoln::BGDnygdpmktpkn
series cpv=BGDsoln::BGDneconprvtkn 'cant call it c because c is a reserved name in eviews'
series g=BGDsoln::BGDnecongovtkn
series i=BGDsoln::BGDnegdiftotkn
series x=BGDsoln::BGDneexpgnfskn
series m=BGDsoln::BGDneimpgnfskn
series ydisc=y-(Cpv+i+g+X-m)
copy bgdsoln::mfmsaoptions
mfmsaoptions=@replace(mfmsaoptions,"BGD","SIM")
close BGDsoln


smpl 2010 2030
show y cpv i g x m ydisc


smpl 2000 2019
c(1)=.6
equation _cpv.ls dlog(cpv)= -.3*(log(cpv(-1))-log(y(-1)) - log(c(1)))+c(3)*dlog(y)

_cpv.resids(g)
_cpv.results

smpl 2000 2020 
equation _g.ls dlog(g)=-c(2)*(log(g(-1))-log(y(-1)) - log(c(1)))+c(3)*dlog(y)
show _g

equation _g.ls dlog(g)=-0.8*(log(g(-1))-log(y(-1)) - log(c(1)))+c(3)*dlog(y)

equation _i.ls dlog(i)=-c(2)*(log(i(-1))-log(y(-1)) - log(c(1)))+c(3)*dlog(y)
show _i

smpl @all

series gde=(cpv+G+I)

smpl 2000 2020
equation _M.ls dlog(m)=-c(2)*(log(m(-1))-log(gde(-1)) - log(c(1)))+c(3)*dlog(gde)
show _m

delete(noerr) example
model  SIM 'declare the model object'
SIM.merge _cpv
SIM.merge _G
SIM.merge _i
SIM.merge _m
SIM.append @identity y=cpv+i+g+x-m+ydisc
SIM.append @identity gde=cpv+i+g



show sim.text


string exogs=sim.@exoglist
show exogs

string endogs=sim.@endoglist
show endogs

string idents=sim.@identity
show idents

string stochs=sim.@stochastic
show stochs

smpl 2016 2030
'example.addassign(i,c) @stochastic
SIM.addassign(a,c) @stochastic
SIM.addinit(v=n) @stochastic


show cpv_A i_a g_a m_a


show SIM.text



show cpv*

smpl 2016 2030 ' set the sample to the period over which you wish to solve the model.  Typically include some history'
SIM.scenario "baseline" 'name the scenario baseline'
SIM.addassign(i,c) @stochastic 'place addfactors on the intercepts of the dependent variables of stochastic equations'
SIM.addinit(v=n) @stochastic 'initialize the addfactors with the exact number needed to reproduce the actual data'
SIM.solve(s=d,d=s) 'solve the model and generate the _0 variables'
scalar styffforib=2




wfsave(2) M:\modelflow\modelflow-manual\papers\mfbook\content\models\Simple
stop
show cpv*

show (y/y_0)*100 (cpv/cpv_0)*100 (g/g_0)*100 (i/i_0)*100 (m/m_0)*100



sim.scenario(n,a=2,i="baseline",c) "My fancy simulation"
sim.scenario "My fancy simulation"


smpl 2016 2030
sim.solve(s=d,d=D,o=g,i=a,c=1e-6,f=t,v=t,g=n)

'Should all be zeros
show y_2 i_2 cpv_2 g_2 y_2/y_0 i_2/i_0 cpv_2/cpv_0 g_2/g_2 


'declare scenario
setmaxerrs 2
 EXAMPLE.scenario(d) "10 percent increase in exports between 2024 and 2026"
 seterrcount 0
setmaxerrs 1

sim.scenario(n,a=3,i="baseline",c) "10 percent increase in exports between 2024 and 2026"
sim.scenario "10 percent increase in exports between 2024 and 2026"

smpl @all
'save the original values of x'
series x_orig=x
'change exports'

'shock x by 10 percent between 2024 and 2026
smpl 2024 2026
x=x*1.10

smpl 2016 2030
sim.solve(s=d,d=D,o=g,i=a,c=1e-6,f=t,v=t,g=n)

smpl @all
'restore original values of x'
x=x_orig
smpl 2020 2030
plot (y_3/y_0-1)*100  (cpv_3/Cpv_0-1)*100  (i_3/i_0-1)*100  (m_3/m_0-1)*100 
stop
'declare scenario
setmaxerrs 2
 EXAMPLE.scenario(d) "10 percent increase in government spending"
 seterrcount 0
setmaxerrs 1

example.scenario(n,a=4,i="baseline",c) "10 percent increase in government spending"
example.scenario "10 percent increase in government spending"

smpl @all
'save the original values of g'
series g_orig=g
'change govt spending'

'shock g by 10 percent'
smpl 2024 2027
g=g*1.10

'Turn off the g equation
'now g is an exogenous variable'
example.exclude g

smpl 2016 2030
example.solve(s=d,d=D,o=g,i=a,c=1e-6,f=t,v=t,g=n)

smpl @all
'restore original values of g'
g=g_orig
smpl 2020 2030
plot (y_4/y_0-1)*100  (cpv_4/Cpv_0-1)*100  (i_4/i_0-1)*100  (m_4/m_0-1)*100 

'declare scenario
setmaxerrs 2
 EXAMPLE.scenario(d) "10 percent increase in government spending via addfactor"
 seterrcount 0
setmaxerrs 1

example.scenario(n,a=5,i="baseline",c) "10 percent increase in government spending via addfactor"
example.scenario "10 percent increase in government spending via addfactor"

smpl @all
'save the original values of g'
series g_A_orig=g_A
'change exports'

'shock g level by 10 percent by increasing growth rate by 10 percent'
smpl 2024 2024
g_A=g_A+.1
'Reverse the level shock by reducing teh growth rate by 0.1'
'smpl 2028 2028
'g_A=g_A-.1


'No need to exclude because the affactor is an exogenous variable'

smpl 2016 2030
example.solve(s=d,d=D,o=g,i=a,c=1e-6,f=t,v=t,g=n)



smpl @all
'restore original values of g'
g_A=g_A_orig
'erase excludes for next solve
example.exclude 'exclude with nothing atfer erases all previous excludes
smpl 2020 2030
plot (y_5/y_0-1)*100  (cpv_5/Cpv_0-1)*100  (i_5/i_0-1)*100  (m_5/m_0-1)*100 (g_5/g_0-1)*100 

'declare scenario
setmaxerrs 2
 EXAMPLE.scenario(d) "10 percent increase in government spending using override"
 seterrcount 0
setmaxerrs 1

example.scenario(n,a=14,i="baseline",c) "10 percent increase in government spending using override"
example.scenario "10 percent increase in government spending using override"
delete(noerr) g_14
smpl @all
'create override variable
series g_14=g_0
'change spending

'shock g by 10 percent'
smpl 2024 2027
g_14=g_14*1.10

smpl 2016 2030
example.exclude g
example.override g
example.solve(s=d,d=D,o=g,i=a,c=1e-6,f=t,v=t,g=n)

smpl 2020 2030
plot (y_14/y_0-1)*100  (cpv_14/Cpv_0-1)*100  (i_14/i_0-1)*100  (m_14/m_0-1)*100 (g_14/g_0-1)*100 

'declare scenario
setmaxerrs 2
 EXAMPLE.scenario(d) "10 percent increase in government spending via addfactor and overrride"
 seterrcount 0
setmaxerrs 1

example.scenario(n,a=15,i="baseline",c) "10 percent increase in government spending via addfactor and overrride"
example.scenario "10 percent increase in government spending via addfactor and overrride"

smpl @all
'Create the override variable
series g_A_15=g_A
'change exports'

'shock g level by 10 percent by increasing growth rate by 10 percent'
smpl 2024 2024
g_A_15=g_A_15+.1
'Reverse the level shock by reducing teh growth rate by 0.1'
'smpl 2028 2028
'g_A_15=g_A_15-.1



smpl 2016 2030
example.override g_a
example.solve(s=d,d=D,o=g,i=a,c=1e-6,f=t,v=t,g=n)

smpl 2020 2030
plot (y_15/y_0-1)*100  (cpv_15/Cpv_0-1)*100  (i_15/i_0-1)*100  (m_15/m_0-1)*100 (g_15/g_0-1)*100 

'declare scenario
setmaxerrs 2
 EXAMPLE.scenario(d) "10 percent increase in government spending using override"
 seterrcount 0
setmaxerrs 1

example.scenario(n,a=16,i="baseline",c) "10 percent increase in government spending us8ing tremporary exclude"
example.scenario "10 percent increase in government spending us8ing tremporary exclude"

delete(noerr) g_16
smpl @all
'create override variable
series g_16=g_0
'change spending

'shock g by 10 percent'
smpl 2024 2027
g_16=g_16*1.10

smpl 2016 2030
example.exclude g("2024 2027")
example.override g("2024 2027")
example.solve(s=d,d=D,o=g,i=a,c=1e-6,f=t,v=t,g=n)

smpl 2020 2030
plot (y_16/y_0-1)*100  (cpv_16/Cpv_0-1)*100  (i_16/i_0-1)*100  (m_16/m_0-1)*100 (g_16/g_0-1)*100 

delete(noerr) _compare*
graph _compareg (g_14/g_0-1)*100 (g_15/g_0-1)*100 (g_16/g_0-1)*100
_compareg.addtext(.71,-0.7,font(+b,16)) Compare path of shocked variable using different simul methods
_compareg.addtext(-.44, -.25,font(+i,9)) Percent change of government spending from baseline
_compareg.name(1) Pure Exog shock
_compareg.name(2) Add factor shock
_compareg.name(3) Exog shock over specific period

graph _comparey (y_14/y_0-1)*100 (y_15/y_0-1)*100  (y_16/y_0-1)*100
_comparey.addtext(.71,-0.7,font(+b,16)) Compare GDP impact of same shock using different simul methods
_comparey.addtext(-.44, -.25,font(+i,9)) Percent change from baseline of real GDP 
_comparey.name(1) Pure Exog shock
_comparey.name(2) Add factor shock
_comparey.name(3) Exog shock over specific period

show _compareg _comparey


