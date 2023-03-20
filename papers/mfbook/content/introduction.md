<!-- #region -->
# Introduction

```{warning}
This Jupyter Book is work in progress.

```
This paper describes the implementation of the World Bank's MacroFiscalModel (MFMod) {cite:p}`burns_world_2019` in the open source solution program ModelFlow ([Hansen, 2023](https://ibhansen.github.io/doc/index)).  

## Background
The impetus for this paper and the work that it summarizes was to make available to a wider constituency the work that the Bank has done over the past several decades to disseminate Macro-structural or models[^1]: My footnote text. -- notably those that form part of its MFMod (MacroFiscalModel) framework. 

[^1]: Economic modelling has a long tradition at the World Bank.  The Bank has had a long-standing involvement in CGE modeling is the World Bank {cite:p}`dixon_handbook_2013`, indeed the popular mathematics package GAMS, which is widely used to solve CGE and Linear Programming models, [started out](https://www.gams.com/about/company/) as a project begun at the World Bank in the 1970s.

MFMod is the World Bank's work-horse macro-structural economic modelling framework. It exists as a linked system of 184 country specific models that can be solved either independently or as a larger system. The MFMod system evolved from earlier models developed by the Bank during the 2000s to strengthen the basis for the forecasts produced by the World Bank.  

Beginning in 2015, this core model was developed and extended substantially into the main MFMod (MacroFiscalModel) model that is used for the World Bank's twice annual forecasting exercise [The Macro Poverty Outlook](https://www.worldbank.org/en/publication/macro-poverty-outlook).  This model continues to evolve and be used as the workhorse forecasting and policy simulation model of the World Bank. 

### Climate change and the MFMod system
Most recently, the Bank has extended the standard MFMod framework to incorporate the main features of climate change ({cite:authordatepars}`burns_climate_2021`)-- both in terms of the impact of the economy on climate (principally through green-house gas emissions, like $CO_2, N_{2}O, CH_4, ...$) and the impact of the changing climate on the economy (higher temperatures, changes in rainfall quantity and variability, increased incidence of extreme weather) and their impacts on the economy (agricultural output, labor productivity, physical damages due to extreme weather events, sea-level rises etc.).

These climate enhanced versions of MFMod serve as one of the two main modelling systems (along with the Bank's MANAGE CGE system) in the World Bank's [Country Climate Development Reports(https://www.worldbank.org/en/publication/country-climate-development-reports)



## Early steps to bring the MFMod system to the broader economics community

Bank staff were quick to recognize that the models built for its own needs could be of use to the broader economics community. An initial project ```isimulate``` in 2007 made several versions of this earlier model available for simulation on the [isimulate platform](https://isimulate.worldbank.org), and these models continue to be available there.  The isimulate platform housed (and continues to house) public access to earlier versions of the MFMod system, and allows simulation of these and other models -- but does not give researchers access to the code or the ability to construct complex simulations.

In another effort to make models widely available a large number (more than 60 as of June 2023) customized stand-alone models (collectively known as called MFModSA - MacroFiscalModel StandAlones)  have been developed from the main model. Typically developed for a country-client (Ministry of Finance, Economy or Planning or Central Bank), these Stand Alones extend the standard model by incorporating additional details not in the standard model that are of specific import to different economies and the country-clients for whom they were built, including: a more detailed breakdown of the sectoral make up of an economy, more detailed fiscal and monetary accounts, and other economically important features of the economy that may exist only inside the aggregates of the standard model.

Training and dissemination around these customized versions of MFMod have been ongoing since 2013. In addition to making customized models available to client governments, Bank teams have run technical assistance program designed to train government officials in the use of these models and their maintenance, modification and revision. 

## Moving the framework to an open-source footing

Models in the MFMod family are normally built using the proprietary [EViews](www.eviews.com) econometric and modelling package. While offering many advantages for model development and maintenance, its cost may be a barrier to clients in developing countries.  As a result, the World Bank joined with Ib Hansen, a Danish economist formerly with the European Central Bank and the Danish Central Bank, who over the years has developed ```modelflow``` a generalized solution engine written in Python for economic models. Together with World Bank, Hansen has worked to extend ```modelflow``` so that MFMod models can be ported and run in the framework.

This paper reports on the results of these efforts. In particular, it provides step by step instructions on how to install the ```modelflow``` framework, import a World Bank macrostructural model,  perform simulations with that model and report results using the many analytical and reporting tools that have been built into ```modelflow```.  It is not a manual for ```modelflow```, such a manual can be found [here](https://ibhansen.github.io/doc/index) nor is it documentation for the MFMod system ({cite:author}`burns_world_2019`,{cite:p}`burns_macroeconomic_2021`, {cite:p}`burns_climate_2021`) or the specific models described and worked with below.



<!-- #endregion -->

```python

```
