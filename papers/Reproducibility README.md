# Contents

1. [Overview](#overview)
2. [Data Availability](#data-availability)
3. [Instructions for Replicators](#instructions-for-replicators)
4. [List of Exhibits](#list-of-exhibits)
5. [Requirements](#requirements)
6. [Code Description](#code-description)
7. [Folder Structure](#folder-structure)


## Overview

This package includes all fo the information to reproeuce all of the Charts and Tables in *The World Bank's MFMod Frameworkin Python with Modelflow*. It is comprised of the data set used in the report and from which all the tables and charts are derived, the Jupyter Notebooks that perform the simulations and generate the graphics and tables in the report as well as a python build script that runs all of the Jupyter notebooks and outputs the Charts and Tables and binds them into a PDF which is the actual book.  The Jupyter Notebooks can be run independently or in the python build program.

## Data Availability

The data used for this report are drawn from the MFMod modelling system Burns et al. (2019), and are being released simultaneously with the report on the [World Bank's github site](https://github.com/worldbank/MFMod-ModelFlow). 

### Data Sources



### Statement about Rights

I certify that the author(s) of the manuscript have legitimate access to and permission to use the data used in this manuscript.


## Instructions for Replicators

To run the package, replicators will need to have Python version 3.10 installed, and the ModelFlow Package. To build the PDF file from the package using the build.py program they will also need to have installed the Jupyter Book package and a version of Latex.

The book and all files were tested using Miniconda and Anaconda versions of ModelFlow under windows. Full instructions on the installation of ModelFlow are included in Chapter 3 of the report, the technical details of which are reproduced in the [Requirements](#requirements) section below.



## List of Exhibits

Clearly identify and document the tables and figures as they appear in the manuscript by their corresponding numbers. If file names do not correspond to exhibit numbers, provide detailed explanations.

If not all data is provided in the reproducibility package, as described in the data section, then the list of tables should clearly indicate which tables, figures, and in-text numbers can be reproduced with the public material provided.

Example template for exhibit identification:

The provided code reproduces:

- [ ] All numbers provided in text in the paper
- [ ] All tables and figures in the paper
- [ ] Selected tables and figures in the paper, as explained and justified below

| Exhibit name | Output filename | Script | Note |
|--------------|-----------------|--------|------|
| Table 1      | Balancetable.xls | 02_analysis.do (line 23) | Found in Outputs/tables/main |
| Figure 1     | Regresults.png   | 02_analysis.do (line 40) | Found in Outputs/figures/annex, Image Format: Portable Network Graphic (PNG), Bits Per Pixel: 32, Color: Truecolour with alpha, Dimensions: 970 x 544, Interlaced: Yes, XResolution: 144, YResolution: 144 |

## Requirements

### Computational Requirements

Although it is not strictly necessary, it is a good idea to create a specific python environment[^environ] for `ModelFlow`, this will be a space where the `ModelFlow` package itself will be installed and in which the specific dependencies on which `ModelFlow` relies will be installed. Other environments may require packages that conflict with `ModelFlow`. Declaring a separate environment for `ModelFlow` will help prevent conflicts between different versions of packages from arising.

ModelFlow will install a range of dependencies, including Jupter Notebook 6.  Modelflow runs under Notebook 7 but the book and reproducibility package were built and tested under Jupyter Notebook 6.

### Software Requirements

  
- **Python 3.12.6**
  - Modelflow 2.58
  - Jupyter Notebook 6
- Jupyter Book
- MikTex or TexLive

#### Installing Python 

MiniConda providing only the essential components for running python.

A guide for installing **MiniConda under windows** can be found [here](https://www.anaconda.com/docs/getting-started/miniconda/main). 


#### Installing Modelflow and Jupyter Book

The commands below create a `ModelFlow` environment and install into it the `ModelFlow` package and several supporting packages that are useful when using `ModelFlow` in conjunction with `EViews` or `Jupyter Notebook`. 

Also the [Jupyter book library](https://jupyterbook.org/) is installed. This allows the replicator to generate the full book. 

The commands should be cut and paste (either one by one, or as a block) into the  Anaconda command prompt environment. 

To open the Anaconda/MiniConda prompt:

1. In the windows command prompt, type Anaconda (or Miniconda)
2. If Anaconda/Miniconda have been successfully installed an icon entitled Anaconda(Minoconda) Prompt will be available in windows. Click on this.
3. This will open a python command shell where the commands listed below can be entered.


```
conda create -n ModelFlow -c ibh -c conda-forge ModelFlow_book jupyter-book -y
conda activate ModelFlow

pip install dash_interactive_graphviz
jupyter contrib nbextension install --user
jupyter nbextension enable hide_input_all/main
jupyter nbextension enable splitcell/splitcell
jupyter nbextension enable toc2/main
jupyter nbextension enable varInspector/main

```



#### Installing Tex

To generate the book or the example report in PDF a latex package must also be installed on the computer, either the [Miktex](miktex.org) or the 
[TexLive](https://tug.org/texlive/) can be used and have been tested with the package. Installation instructions are provided on the linked sites.

#### Running Jupyter Book

To run the Jupyter Book open a Anaconda prompth and enter: 

```
conda activate ModelFlow
```



The main build routine for the book is buid.py.  This runs all of the Jupyter Notebooks that together comprise the report and in so doing generates all of the tables and charts in the report, with the exception of interactive widgets.  In the Jupyter book screenshots of the widgets are presented. Running the associated Jupyter Notebook will generate the widget and the screenshot if it that is shown in the report.


  - `build.py` #Runs all of the Jupyter Notyebooks that comprise the report and binds, translates them into Latex and binds them together into a pdf.

- Ensure all required software and dependencies are installed as listed in the [Requirements](#requirements) section.

To build the Jupyter Book as HTML enter: 

```
python build.py 
```  

To build the Jupyter Book as HTML and PDF enter: 

```
python build.py latex
```  

#### Running Jupyter Book
The complete **Jupyter Book** i created from a number of **Jupyter Notebooks**. These notebooks can be run individualy through the Jupyter system. 

To run the Jupyter Notebook  open a Anaconda prompth and enter: 

```
jupyter notebook 
```  



### Memory and Runtime and Storage Requirements


The build.py program should run and compile on a Windows 11 machine with an Intel 5 processor with 32G memory installed within 15 minutes.

Total storage required (after installation of python and required packages) is less than 500MB.


## Code Description 

Give an overview of the program files and their purposes. Remove redundant or obsolete files from the replication archive. For example, main.do sets file paths, installs necessary ADO packages, and executes all other dofiles. Meanwhile, cleaning.do loads data, handles missing values, and analysis.do performs basic statistical analysis and generate visualizations. 

Make sure to also include any crucial information that replicators should be aware of to facilitate a one-click run of the code.

## Folder Structure


```
build.py
modelutil_cli.py
Reproducibility README.md
mfbook
  ├─  _config.yml │ 
  ├─  _toc.yml │ 
  ├── genindex.md
  ├── Reference.md
  ├── genindex.md
  ├── genindex.md
  ├── reference.bib
  └── content
        ├── 01_introduction
        ├── 02_MacrostructuralModels
        ├── 03_Instalation
        ├── 04_PythonEssentials
        ├── 05_WBModels
        ├── 06_ModelAnalyticsintroduction
        ├── 07_MoreFeatures 
        ├── models
        ├── introducion.ipynb
        └── Overview.ipynb
 ```