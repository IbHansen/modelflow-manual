# Contents

1. [Overview](#overview)
2. [Data Availability](#data-availability)
3. [Instructions for Replicators](#instructions-for-replicators)
4. [List of Exhibits](#list-of-exhibits)
5. [Requirements](#requirements)
6. [Code Description](#code-description)
7. [Folder Structure](#folder-structure)


## Overview

This package includes information needed to reproduce the Charts and Tables in *The World Bank's MFMod Frameworkin Python with Modelflow*. It is comprised of the data set used in the report and from which all the tables and charts are derived, the Jupyter Notebooks that perform the simulations and generate the graphics and tables in the report as well as a python build script that runs all of the Jupyter notebooks and outputs the Charts and Tables and binds them into a PDF which is the actual book.  The Jupyter Notebooks can be run independently or in the python build program.

## Data Availability

The data used for this report are drawn from the MFMod modelling system [Burns et al. (2019)](https://documents1.worldbank.org/curated/en/294311565103938951/pdf/The-World-Bank-Macro-Fiscal-Model-Technical-Description.pdf), and are being released simultaneously with the report on the [World Bank's github site](https://github.com/worldbank/MFMod-ModelFlow). 

### Data Sources



### Statement about Rights

We certify that the author(s) of the manuscript have legitimate access to and permission to use the data used in this manuscript.


## Instructions for Replicators

To run the package, replicators will need to have anaconda Python version 3.13 installed, and the ModelFlow Package. To build the PDF file from the package using the build.py program they will also need to have installed the Jupyter Book package and a version of Latex.

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

Although it is not strictly necessary, it is a good idea to create a specific python environment for `ModelFlow`, this will be a space where the `ModelFlow` package itself will be installed and in which the specific dependencies on which `ModelFlow` relies will be installed. Other environments may require packages that conflict with `ModelFlow`. Declaring a separate environment for `ModelFlow` will help prevent conflicts between different versions of packages from arising.

ModelFlow will install a range of dependencies, including Jupter Notebook 6, pandas and matplotlib.  Modelflow runs under Notebook 7 but the book and reproducibility package were built and tested under Jupyter Notebook 6.

### Software Requirements

  
- **Python 3.13**
  - Modelflow 2.58
  - Jupyter Notebook 6
- Jupyter Book
- MikTex or TexLive

#### Installing Python 

MiniConda is a minimalist implementation of python. A guide for installing **MiniConda under windows** can be found [here](https://www.anaconda.com/docs/getting-started/miniconda/main). 


#### Installing Modelflow 

The commands below create a `ModelFlow` environment under `miniconda` or `anaconda`  and install into it the `ModelFlow` package and several supporting packages that are needed when using `ModelFlow` in conjunction with `Jupyter Notebook`. 

The commands should be cut and paste (either one by one, or as a block) into the  Anaconda command prompt environment. 

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
#### Installing Jupyter Book

The [Jupyter book library](https://jupyterbook.org/) is needed if the replicator wishes to generate the full publication, text as well as figures and tables. 

#### Installing Tex

To generate the book or the example report in PDF a latex package must also be installed on the computer, either the [Miktex](miktex.org) or the 
[TexLive](https://tug.org/texlive/) can be used and have been tested with the package. Installation instructions are provided on the linked sites.


### Memory and Runtime and Storage Requirements

The build.py program should run and compile on a Windows 11 machine with an Intel 5 processor with 32G memory installed within 15 minutes.

Total storage required (after installation of python and required packages) is less than 500MB.


## Replication Code Description

This project contains a set of Python scripts and Jupyter Notebooks that together replicate the analyses and figures presented in the  book.

### Unpack the `mfbook.zip` File

Once the Python environment has been set up, you are ready to replicate the book. All necessary files for replication are contained in the `mfbook.zip` archive.

Unzip this file to extract the full project structure. The core content is organized into a series of Jupyter Notebooks (`.ipynb` files), which are located in (subfolders)[#Folder Structure] under:

```
mfbook/content/
```

---

### Creating the Jupyter Book

To build the Jupyter Book, open an **Anaconda Prompt** and activate the relevant Python environment:

```
conda activate ModelFlow
```

`navigate to the directory where the replication package has been unzipped.`

The main script used to compile the book is `build.py`. This script executes all the Jupyter Notebooks, generating all tables and charts used in the report. Note that interactive widgets are **not** included in the final output; instead, screenshots of the widgets are shown. You can run the corresponding notebook manually to interact with the widget and verify that the screenshot correspond to elements of the widget displayed.

- `build.py`: Executes all notebooks, compiles them to LaTeX, and generates an HTML version of the book located in:

```
mfbook/_build/html/
```

To build both the HTML and PDF versions of the book, run:

```
python build.py latex
```

If LaTeX is not installed on your system, the PDF will not be generated.

---

### Running Jupyter Notebooks Individually

You may also run each notebook manually using Jupyter. To launch the Jupyter Notebook interface, enter the following in the Anaconda Prompt:

```
jupyter notebook
```

From there, navigate to `mfbook/content/` and select the notebook you wish to run.



## Folder Structure


```
Reproducibility README.md
build.py
modelutil_cli.py
mfbook
  ├─  _config.yml │ 
  ├─  _toc.yml │ 
  ├── genindex.md
  ├── Reference.md
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