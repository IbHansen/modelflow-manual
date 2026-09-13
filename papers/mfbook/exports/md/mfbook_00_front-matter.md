# The World Bank's MFMod Framework in Python with Modelflow - Front matter


# Front matter

# Foreword


Over the decades, the World Bank has invested heavily in the tools available to its country economists to analyze, forecast, and monitor economic activity.  

The `MFMod` framework is the ever-evolving fruit of those efforts. The framework is at the heart of the Bank's main `MFMod` model, a system of 184 macro-structural models of nearly all the economies in the world, that is the work-horse tool used by World Bank economists. The data and equations of `MFMod` are updated regularly and used to produce the twice-annual compendium  [**Macro Poverty Outlook**](https://www.worldbank.org/en/publication/macro-poverty-outlook), which presents concise statements of the Bank's views on the major challenges, outlook, and forecasts for almost every developing country in the world.

The `MFMod` framework is also used to generate customized models for individual countries and for complex policy analysis. Most recently it has been used extensively in the World Bank's [Country Climate Development Reports](https://www.worldbank.org/en/publication/country-climate-development-reports) to model the impact of climate change in developing economies, and is also being used to analyze long-term prospects for the Bank's forthcoming [Country growth and Jobs Reports](https://www.worldbank.org/en/topic/jobsandgrowth) (CGJRs). 

Making these models available to a broader audience has always been  a major focus of the Bank's modeling team. For years, the Bank has created customized models for developing country clients, and then transferred the models to client Ministries, training staff on the use, maintenance and modifications of these models. ***The World Bank's MFMod Framework in Python with Modelflow*** takes that process one step further by introducing an open-source tool for solving the models and by making models available on-line to anyone wanting to work with them.

While this manual is destined for a relatively small audience of macroeconomic modellers, it is hoped that it will generate significant benefits both for the Bank, via feedback on the models, and for clients who will have, for the first time, access to the Bank's models in a costless form.


Manuela Francisco

Director Economic Policy<br>

The World Bank<br>


# Acknowledgements

This book and the development of ModelFlow would not have been possible without the contributions of many individuals. 

Special thanks to Jens Boldt, formerly of Danmarks Nationalbank, for his participation in creating the first version of ModelFlow, which was developed initially for the top-down stress testing of banks.

We would also like to extend our gratitude to the following reviewers for their invaluable contributions and insights:

- Thanh Bui
- Unnada Chewpreecha
- Freya Casie
- Jacob Gyntenberg
- Charl Jooste
- Lasse Tryde


Their expertise and feedback have significantly enhanced the quality of this manual and the `ModelFlow` library. 

Many thanks also to the World Bank Reproducibility Team (Luis Eduardo San Martin; Ankriti Singh;and Nihaa Sajid), who painstakingly went through the book and all of the charts and tables to make sure that the results can be reproduced. In so doing they exposed several issues that have since been resolved, contributing to the overall quality and reliability of the manual.

Remaining errors are the sole responsibility of the authors.

The MFMod framework itself reflects the inputs of many, over many years. Major contributors include but are not restricted to: Andrew Burns; Thanh Bui; Benoit Campagne; Paola Castillo; Unnada Chewpreecha; Young Il Choi; Charl Jooste; Francis Dennig; Alex Haider; Monika Matyja; Chung Gu Lee; Theo Janse van Rensburg; Heather Ruberl; David Stephan; and Baris Tercioglu.


Preparation of this manual and the development of the World Bank extensions to `ModelFlow` have benefited enormously from the generous financial support of the Climate Support Facility  [https://www.worldbank.org/en/programs/climate-support-facility](https://www.worldbank.org/en/programs/climate-support-facility), a multi-donor Trust Fund administered by the World Bank that supports developing countries achieve a green recovery from the effects of COVID-19, implement their NDCs and develop long-term climate strategies.  

The findings, interpretations, and conclusions expressed herein are entirely those of the authors and do not necessarily represent the views of the World Bank, its Executive Directors, or the governments of the countries they represent.

Cover design: Marie-Anne Chambonnier.

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

```text
no update sheets No module named 'ipydatagrid'
No modelwidgets
```
