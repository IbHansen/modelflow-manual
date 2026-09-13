# The World Bank's MFMod Framework in Python with Modelflow - Some python essentials for using World Bank models with modelflow


# Some python essentials for using World Bank models with modelflow

# Introduction to  Jupyter Notebook


`Jupyter Notebook` is an application for creating, annotating, simulating and working with computational documents.  Originally developed for python, the latest versions of EViews also support `Jupyter Notebooks`. 

`Jupyter Notebook` offers a simple, streamlined, document-centric experience and can be a great environment for documenting the work you are doing, and trying alternative methods of achieving desired results.  Many of the methods in ```ModelFlow``` have been developed to work well with `Jupyter` Notebook. Indeed this documentation was written as a series of `Jupyter Notebooks` bound together with the [Jupyter Book package](https://jupyterbook.org/en/stable/intro.html).
 
Jupyter Notebook is not the only way to work with `ModelFlow` or Python.  As users become more advanced they are likely to migrate to a more program-centric IDE (Interactive Development Environment) like Spyder or Microsoft Visual Code.  

However, to start, Jupyter Notebooks is a great environment in which to follow work done by others, try out code, and tweak the codes of others to fit your own needs.

:class: tip


This chapter introduces Jupyter Notebook. It can be safely skipped by readers already familiar with Jupyter Notebook (an interactive environment for programming, documenting, and analyzing data). 

Key points in the chapter include:

- **What is Jupyter Notebook**:
  - A tool for creating and sharing computational documents that integrate code, text, and visualizations.
  - Ideal for prototyping, debugging, and documenting workflows.

- **Getting Started**:
  - Activate the Python environment and launch Jupyter Notebook from the command line.
  - Navigate to your desired working directory and start a new notebook.

- **Notebook Structure**:
  - Composed of cells that can contain code, markdown, or outputs.
  - Cells have two modes: Edit (for writing code or text) and Command (for running cells or managing notebook structure).

- **Key Features**:
  - Write and execute Python code interactively.
  - Use Markdown for formatted text, including headers, bullet points, and inline mathematics.
  - Render complex mathematical equations with LaTeX.

- **Shortcuts and Tips**:
  - Use keyboard shortcuts to navigate, edit, and execute cells efficiently.
  - Combine code, results, and documentation in one notebook for replicability.

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

There are many fine tutorials on Jupyter Notebook on the web, and [The official Jupyter site](https://docs.jupyter.org/en/latest/) is a good starting point. Another good reference is [here](https://jupyter.brynmawr.edu/services/public/dblank/Jupyter%20Notebook%20Users%20Manual.ipynb).

The remainder of this chapter aims to provide enough information to get a user started.  

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

## Starting Jupyter Notebook

Each time, a user wants to work with `ModelFlow`, they will need to activate the `ModelFlow` environment by 

1) Opening the Anaconda command prompt window (Windows Start->Type Annaconda->Select Annaconda Command Prompt)

2) Activate the `ModelFlow` environment we just created by executing the following command: `conda activate ModelFlow`

3) Navigate to a position on his/her computer's directory structure where they want to store (or where they are already stored) their `Jupyter Notebooks`. (e.g. cd c:\users\MyUserName\MyJupyterNotebookDirectory)

4) Finally, the `Jupyter Notebook` python program must be started by executing the following command from the conda command line:

> `jupyter notebook`

This will launch the `Jupyter` environment in your default web browser, which should look something like the image below, where the directory structure presented is that of the directory from which the `jupyter notebook` command was executed (e.g. c:\users\MyUserName\MyJupyterNotebookDirectory).


```{figure} ./NewJNSession.png
---
height: 225px
name: jupyter file open
---
The Jupyter File explorer  view
```


Note the directory from which you execute the `jupyter notebook` will be the **root** directory for the jupyter session.  **Only directories and files below this root directory will be accessible by `Jupyter`**.

## Creating a notebook

The idea behind `Jupyter Notebook` is to create an interactive version of the physical notebooks that scientists use(d) to:

* record what they have done
* perhaps explain why
* document how data were generated, and 
* record the results of their experiments  

The motivation for these notebooks and `Jupyter Notebook` is to record the precise steps taken to produce a set of results, which, if followed, would allow others to generate the same results. 

To create a new blank notebook you must select from the `Jupyter Notebook` menu 

File-> New Notebook
```{figure} ./NewNotebook.png
---
height: 150px
name: create new Notebook
---
A newly created Jupyter Notebook session
```


This will generate a blank unnamed notebook with one empty cell, that looks something like this:


```{figure} ./Newcell.png
---
height: 225px
name: new Notebook
---
A newly created Jupyter Notebook
```



Each notebook has associated with it a "Kernel", which is an instance of the computing environment in which code will be executed. For `Jupyter Notebooks` that work with `ModelFlow` this will be a python Kernel. If your computer has more than one "kernel" installed on it, you may be prompted when creating a new notebook for the kernel with which to associate it. Typically this should be the Python Kernel under which your ModelFlow was built -- currently python 3.13 in June 2025. ::: 

## Jupyter Notebook cells

A `Jupyter Notebook` is comprised of a series of cells.

***Jupyter Notebook cells can contain:***
* **computer code**: typically python code, but, as noted, other kernels -- like EViews -- can also be used with `Jupyter`.

* **markdown text**: plain text that can include special characters that make some text appear as bold, or indicate the text is a header, or instruct `Jupyter` to render the text as a mathematical formula.  All of the text in this document was entered using `Jupyter Notebook`'s markdown language (more on this below).
* Results (in the form of tables or graphs) from the execution of computer code specified in a code cell.



**Every cell has two modes:**

1. Edit mode -- indicated by a green vertical bar. In edit mode, the user can change the code, or the markdown.
2. Command mode -- indicated by a blue vertical bar.  This will be the state of the cell when its content has been executed.  For markdown cells this means that the text and special characters have been rendered into formatted text.  For code cells, this means the code has been executed and its output (if any) is displayed in an output cell that will be generated in the space immediately below the code cell that generated the output. Also the keyboard is mapped to actions which allows the user to perform tasks like selecting and copying on the cells. 

**Users can switch between Edit and Command  Mode by hitting Esc (to Command mode) or Enter (to Edit mode). With the mouse a double-click in the cell content will switch to Edit Mode and a click in the cell margin will switch to the Command mode.**

```{note} `Jupyter Notebook`s were designed to facilitate _replicability_: the idea that a scientific analysis should contain - in addition to the final output (text, graphs, tables) - all the computational steps needed to get from raw input data to the results.
```

### How to add, delete and move cells

The newly created Jupyter Notebook will have a code cell by default.  Cells can be added, deleted and moved either via mouse using the toolbar or by keyboard shortcut.


**Using the Toolbar**
* **+ button**: add a cell below the current cell
* **scissors**: cut  current cell (can be undone from "Edit" tab)
* **clipboard**: paste a previously cut cell to the current location
* **arrows (up and down)**: move cells (cell must be in Select/Copy mode -- vertical side bar must be blue)
* **hold shift + click cells in left margin**: select multiple cells (vertical bar must be blue)

**Using keyboard short cuts**
* **esc + a**: add a cell above the current cell
* **esc + b**: add a cell below the current cell
* **esc + d+d**: delete the currently selected cell(s)



### Change the type of a cell
You can also change the type of a cell. New cells are by default "code" cells. 

**Using the Toolbar**
* Select the desired type from the drop down.  options include 
    * Markdown
    * Code
    * Raw NBConvert

**Using keyboard short cuts**
* **esc + m**: make the current cell a markdown cell
* **esc + y**: make the current cell a code  cell

    
**Auto-complete and context-sensitive help**

When editing a code cell, you can use these short-cuts to autocomplete and or call up documentation for a command.

* **tab**: autocomplete and  method selection
* **double tab**: documention (double tab for full doc)
    
    

### Execution of cells 

Every cell in a Jupyter Notebook can be executed. Executing a markdown cell will cause the cell's content to be rendered as html.  Executing a python code cell, will cause its content to be executed. Cells can be executed either by using the Run button on the Jupyter Notebook menu, or by using one of __two keyboard shortcuts__:

* **ctrl + Enter**: Executes the code in the cell or formats the markdown of a cell.  The current cell retains the focus.  The cursor will stay on the cell that was executed.
* **shift + enter**: Executes the code in the cell or formats the markdown of a cell. The focus (cursor) jumps to the next cell.

For other useful shortcuts see "Help" => "Keyboard Shortcuts" or simply press the keyboard icon in the toolbar.



#### Executing python code
Below is a code cell with some standard python that declares a variable "x", assigns it the value 10, declares a second variable "y" and assigns it the value 45.  The final line of y alone, instructs python to display the value of the variable y.  The results of the operation appear in Jupyter Notebook as an output cell Out\[#\].  By pressing **Ctrl-Enter** the code will be executed and the output displayed below.

```python
x = 10
y = 45
y
```

```text
45
```

**The semi-colon ";" suppresses output in Jupyter Notebook**

In the example below, a semi-colon ";" has been appended to the final line.  This suppresses the display of the value contained by y;  As a result there is no output cell.

```python
x = 10
y = 45
y;
```

Another way to display results is to use the print function.  In this instance even if there is a semicolon at the end of the line, the result of the print command is still output.

```python
x = 10
print(x);
```

```text
10
```

Variables in a Jupyter Notebook session are persistent, as a result in the subsequent cell, we can declare a variable 'z' equal to 2\*y and it will have the value 90.

```python
z=y*2
z
```

```text
90
```

::: {Note}Cells can be executed in any order. 
The natural order is to execute them sequentially in the order they appear in the `Jupyter Notebook`.  However, when debugging or developing code it may be useful to execute cells out of their natural order.  

The persistence of data (the fact that a variable `y` defined in one cell can be used in another cell) depends on the order in which cells were executed, not the order they appear in the notebook.

### Markdown cells and the markdown scripting language in Jupyter Notebook  
Text cells in a notebook can be made more interesting by using markdown.

Cells designated as markdown cells when executed are rendered in a rich text format (html).

Markdown is a lightweight markup language for creating formatted text using a plain-text editor.  Used in a markdown cell of `Jupyter Notebook` it can be used to produce nicely formatted text that mixes text, mathematical formulae, code and outputs from executed python code. 

Rather than the relatively complex commands of html \<h1\>\<\/h1\>, markdown uses a simplified set of commands to control how text elements should be rendered.




#### Common markdown commands
Some of the most common of these include:

| symbol           | Effect          |
|:--|:-----------------|
| \#               | Header        |
| \#\#             | second level |
| \#\#\#           | third level etc. |
| \*\*Bold text\*\* | **Bold text**   |
| \*Italics text\* | *Italics text*   |
| \* text |  * Bulleted text or dot notes |
| 1\. text  | 1. Numbered bullets   |





#### Tables in markdown
Tables like the one above can be constructed using the symbol \| as a separator.  

Below is the markdown code that generated the above table:

```
| symbol           | Effect          |
|:--|:--|                                # Specifies the justification for the columns of the table.
| \#               | Header        |
| \#\#             | second level |
| \*\*Bold text\*\* | **Bold text**   |
| \*Italics text\* | *Italics text*   |
| 
| 1\. text  | 1. Numbered bullets   |

```

The |:--|:--| on the second line tells the Table generator how to justify the contents of columns.  The `\` before the \#s above tells markdown to ignore the normal meaning of \# and just show the symbol.

|Symbol|Meaning|
|:--|:--|
|`:--`| left justify|
|`:--:`| center justify|
|`--:`| right justify.|
|`\`|Literal operator. Display what follows do not interpret it in the normal way.|

#### Displaying code
To display a  block of (unexecutable) code within a markdown cell, encapsulate it (surround it) with backticks \`.

##### Inine code blocks

For inline code references \' a single back tick at the beginning and end suffices.  For example, the below line

An example sentence with some back-ticked \`text as code\` in the middle **will render as:** 

An example sentence with some back-ticked `text as code` in the middle.

##### Multiline code block

For a multiline section of code use three backticks at the beginning and end. 

The below block of code:

` ``` `

`Multi line `

`text to be rendered as code `

` ``` `

will render as:

``` 
Multi line 
text to be rendered as code 
```

#### Rendering mathematics in markdown

Jupyter Notebook's implementation of Markdown supports `latex` mathematical notation.<br>

Maths can be displayed either *inline* -- surrounded by non mathematical text on the same line, or as a standalone equation.

Below is an example of inline mathematics, which was generated by surrounding the latex maths expression by the  `$` sign:

The inline code `$y_t = \beta_0 + \beta_1 x_t + u_t\$` will renders as: $y_t = \beta_0 + \beta_1 x_t + u_t$

if enclosed in `$$` `$$` the encapsulated javascript will render on its own line. 

```
$$y_t = \beta_0 + \beta_1 x_t + u_t$$
```
will be rendered centered on its own line -- as here.

$$y_t = \beta_0 + \beta_1 x_t + u_t$$





#### Complex and multi-line math 

Multiline expressions and equations can also be rendered:

```
\begin{align*}
Y_t  &=  C_t+I_t+G+t+ (X_t-M_t) \\
C_t &= c(C_{t-1},C_{t-2},I_t,G_t,X_t,M_t,P_t)\\
I_t &= i(I_{t-1},I_{t-2},C_t,G_t,X_t,M_t,P_t)\\
G_t &= g(G_{t-1},G_{t-2},C_t,I_t,X_t,M_t,P_t)\\
X_t &= x(X_{t-1},X_{t-2},C_t,I_t,G_t,M_t,P_t,P^f_t)\\
M_t &= m(M_{t-1},M_{t-2},C_t,I_t,G_t,X_t,P_t,P^f_t)
\end{align*}
```
The above `latex` mathematics code uses the  `&` symbol to tell `latex` to align the different lines (separated by `\\`) on the character immediately after the `&`. In this instance the equals "=" sign.  The `*` after align supresses equation numbering.

\begin{align*}
Y_t  &=  C_t+I_t+G+t+ (X_t-M_t) \\
C_t &= c(C_{t-1},C_{t-2},I_t,G_t,X_t,M_t,P_t)\\
I_t &= i(I_{t-1},I_{t-2},C_t,G_t,X_t,M_t,P_t)\\
G_t &= g(G_{t-1},G_{t-2},C_t,I_t,X_t,M_t,P_t)\\
X_t &= x(X_{t-1},X_{t-2},C_t,I_t,G_t,M_t,P_t,P^f_t)\\
M_t &= m(M_{t-1},M_{t-2},C_t,I_t,G_t,X_t,P_t,P^f_t)
\end{align*}

### links to more info on markdown
There are many very good markdown cheatsheets and tutorials on the internet, one cheatsheet can be found [here](https://www.markdownguide.org/cheat-sheet/).

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

# Some Python basics

Before using `ModelFlow` with the World Bank's `MFMod` models, users  will have to understand at least some basic elements of `python` syntax and usage.  Notably they will need to understand about packages, libraries and classes, and how to access them. 

:class: tip

This chapter provides an introduction to essential Python concepts for using World Bank models in ModelFlow. It provides a foundational understanding of Python, equipping users with the skills to engage in macroeconomic modeling tasks.

**Readers familiar with python can safely skip this chapter.**

Key points include:

- **Getting Started with Python**:
  - Launch Python through the terminal, an IDE, or Jupyter Notebook.
  - Use the Anaconda environment for managing dependencies and versions.

- **Core Concepts**:
  - Variables and data types: Store and manipulate data using integers, floats, strings, and lists.
  - Control structures: Use loops and conditionals for automating repetitive tasks and decision-making.

- **Libraries and Packages**:
  - Leverage Python libraries like `pandas` for data handling and `matplotlib` for visualization.
  - Import libraries, modules, and classes to extend Python’s functionality.

- **Interactivity in Jupyter Notebook**:
  - Write, execute, and document Python code interactively.
  - Use context-sensitive help and auto-completion for efficient coding.

- **Best Practices**:
  - Organize your code for readability and reusability.
  - Validate results step-by-step to ensure correctness.

## Starting python in windows

To begin using `ModelFlow`, python itself needs to be started.  This can be done either using the `Anaconda` navigator or from the command line shell. In either case, the user will need to start python and select the `ModelFlow` environment. 

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

### Anaconda navigator

1. Start Anaconda Navigator by typing Anaconda in the Start window and opening the Navigator (see Figure).
2. From Anaconda Navigator select the `ModelFlow` environment (see figure)

```{figure} ./AnacondaNav1.png
---
height: 450px
name: Start Anaconda Navigator
---
A newly created Jupyter Notebook session
```
3. Once the environment is selected the user can either select a command line environment, an IDE or `Jupyter Notebook` by clicking on the appropriate icon. Options typically include:  
    1. Jupyter Notebook environment
    2. The command line environment
    3. A programming IDE environment

In the figure below the user is selecting the `Jupyter Notebook` environment.

```{figure} ./NavigatorChoices.png
---
height: 225px
name: Start from Anaconda Navigator
---
A newly created Jupyter Notebook session
```
 :::{note}
If you start Jupyter Notebook with Anaconda Navigator you will need to select which environment you want jupyter to be running in (see the drop-down at the top center of the above screen shot), To have access to  `ModeFlow`, you will need to select an environment into which `ModelFlow` has been installed (there could be more than one).

## Python  packages, libraries and classes

Some features of `python` are built-in.  Others (like `ModelFlow`) are optional.  Optional packages build on basic python features (and those of other packages) but have to be installed separately.

A **python class** is a code template that defines a python object. Classes can have properties [variables or data] associated with them and methods (behaviors or functions) associated with them. In python, a class is created by the keyword class. An object of type class is created (instantiated) using the class's "constructor" -- a special method that creates an object that is an instance of a class.

A **module** is a Python object consisting of Python code. A module can define functions, classes and variables. A module can also include runnable code.

A **python package** is a collection of modules that are related to each other. When a module from an external package is required by a program, that package (or module in the package) must  be **imported** into the current session in order for its modules to be accessible.  

A **python library** is a collection of related modules or packages. 

`ModelFlow` is a python package that *inherits* (build on or adds to) the methods and properties of other `python` classes like `pandas`, `numpy` and `matplotlib`.
 

## Importing packages, libraries, modules and classes

Some libraries, packages, and modules are part of the core python package and will be available (importable) from the get-go.  Others are not, and need to be installed before importing them into a session.

If you followed the `ModelFlow` installation instructions you have already downloaded and installed on your computer all the packages necessary for running World Bank models under `ModelFlow`.  But to work with them in a given `Jupyter Notebook` session or in a program context, you will also need to ```import``` them into your session before you call them.  


Installation downloads a package's programs from the internet into a specific environment on the user's machine, making them available to be imported when required.  Once it has been installed, the environment into which it was installed must be activated and the package must be imported into each python session where it is to be used.

Typically a python program will start with the importation of the libraries, classes and modules that will be used.  Because a `Jupyter Notebook` is essentially a heavily annotated program, it also requires that packages used be imported.

### Import a package
As described above: packages, libraries and modules are containers that can include other elements.  Take for example the package Math.

To import the Math Package we execute the command ``` import math```.  Having done that we can call the functions and data that are defined in it (math is a standard package so we do not need to install it separately).

```python
# the "#" in a code cell indicates a comment, test after the # will not be executed
import math

# Now that we have imported math we can access some of the elements identified in 
# the package.
# For example math contains a definition for pi, we can access that by executing 
# the pi method of the library math

math.pi
```

```text
3.141592653589793
```

### Import specific elements or classes from a module or library

The python package ```math``` contains several functions and classes.  

Rather than importing the whole package (as above), these classes can be imported directly using the **from syntax**. 

 ```from math import pi,cos,sin```

When imported in this fashion, the user does not have to precede the class or method with the name of their library. The above ```from math import pi,cos,sin``` command imports the pi constant and the two functions cos and sin from the math package directly and allow  the user to call them using their names without preceding them with `math.`.

Compare these calls with the one in the preceding section -- there the call to the method pi has to be preceded by its namespace designator math.  i.e. ```math.pi```. Below we import pi directly and can just call it with `pi`.

```python
from math import pi,cos,sin

print(pi)
print(cos(3))
```

```text
3.141592653589793
-0.9899924966004454
```

### import a library but give it an alias

An imported library/packages can also be given an alias, that is hopefully shorter than its official name but still obvious enough that the user knows what class is being referred to.

For example  ```import math as m``` allows a call to pi using the more succinct syntax ```m.py```.

```python
import math as m
print(m.pi)
print(m.cos(3))
```

```text
3.141592653589793
-0.9899924966004454
```

### Standard aliases

Some packages are so frequently used that by convention they have been "assigned" specific aliases.

For example:

**Common aliases**

|Alias|aliased package | example | functionality|
|:--|:--|:--|:--|
|pd|pandas| import pandas as pd |Pandas are used for storing and retrieving data|
|np|numpy| import numpy as np | Numpy gives access to some advanced mathematical features|
|plt|matplotlib|import matplotlib as plt|matplotlib provides a wide-range of routines for plotting numerical data|

You don't have to use those conventions but it will make your code easier to read by others who are familiar with them.

# Introduction to Pandas,  Series and dataframes

`ModelFlow` is built on top of the `Pandas` library. `Pandas` is the Swiss Army knife of data science and can perform an impressive array of data oriented tasks.

This tutorial is a very short introduction to how pandas `Series` and `Dataframes` are used with `ModelFlow`. For a more complete discussion see any of the many tutorials on the internet, notably:


*  [*Pandas homepage*](https://pandas.pydata.org/)
*  [*Pandas community tutorials*](https://pandas.pydata.org/pandas-docs/stable/getting_started/tutorials.html)

:class: tip

This chapter introduces `pandas`, a powerful Python library for data manipulation and analysis, essential for working with World Bank models. It equips users with basic skills needed to manage and analyze data effectively, and work with the `ModelFlow` package. 

**This chapter can be safely skipped by users familiar with Python and Pandas.**

Key points include:

- **Core Data Structures**:
  - **Series**: One-dimensional arrays for handling single-variable data.
  - **DataFrames**: Two-dimensional, tabular data structures with labeled rows and columns.

- **Basic Operations**:
  - Create Series and DataFrames from lists, dictionaries, or external files (e.g., CSV, Excel).
  - Access and manipulate data using indexing, slicing, and filtering.

- **Common Methods**:
  - Analyze data with methods like `.mean()`, `.sum()`, and `.describe()`.
  - Clean data using `.dropna()` to handle missing values and `.apply()` for transformations.
  - Select and modify data subsets using `.loc[]` and `.iloc[]`.

- **Advanced Features**:
  - Merge and join datasets for integrating multiple sources.
  - Reshape data using pivot tables and group operations.

- **Best Practices**:
  - Structure data clearly for easier analysis.
  - Use `pandas`' extensive functionality for efficient handling of large datasets.

```python
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb   ')
```

## Import the pandas library

As with any python program, in order to use a package or library it must first be imported into the session. As noted above, by  convention pandas is imported as pd (assigning the alias pd to the imported pandas library).

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
import pandas as pd
```

By importing `pandas` with the alias pd (`import pandas as pd`), future references to the pandas library can be truncated as by using `pd.` instead of `pandas.`

The Pandas  library contains many classes and methods.  The discussion below focuses on **Series** and **DataFrames**, two classes that are part of the pandas library.  Both `series` and `dataframes` are containers that can be used to store time-series data and that have associated with them a number of very useful methods for displaying and manipulating time-series data.  

Unlike other statistical packages neither `series` nor `dataframes` are inherently or exclusively time-series in nature. `ModelFlow` and macro-economists use them in this way, but the classes themselves are not necessarily dated or numerical.

## The `Series` class in `Pandas`

`Series` is a class that is part of the pandas package and can be used to instantiate an object that holds a two dimensional array comprised of values and an index.

The constructor for a `Series` object is ```pandas.Series()```.  The content inside the parentheses will determine the nature of the series-object generated.  As an object-oriented language, Python supports ```overrides```. Overrides mean a method -- including constructors -- can have more than one way in which they can be called. Specifically there can be different constructors for a class, depending on how the data used to initialize the object are organized.

### Series declared from a list

The simplest way to create a `Series` is to pass an array of values as a Python list to the Series constructor.


```{note} 
A list in python is a comma delimited collection of items.  It could be text, numbers or even more complex objects.  When declared (and returned) lists are enclosed in square brackets.

For example both of the following two lines are perfectly good examples of lists.

mylist=[2,7,8,9]

mylist2=["Some text","Some more Text",2,3]

The list is entirely agnostic about the type of data it contains.

```

In the examples below `Simplest`, `Simple`, `Simple2` and `simple3` are all python data objects of type Pandas.Series. Each Series object is instantiated (created) in a different way. Simplest is instantiated by passing it a python list of numbers, `simple2` is instantiated by passing a list object (values), `series3` is instantiated indirectly by passing a list mixing text and numeric values. `Series3` would  be hard to interpret as an economic series, but is a perfectly valid python series.


All series have an index.  If no index is explicitly declared (see following section) python will assign a zero-based index (a numerical index that starts with 0).

```python
values=[7,8,9,10,11]
weird=["Some text","Some more Text",2,3]

# Here the constructor is passed a numeric list
Simplest=pd.Series([2,3,4,5,6,7])
Simplest
```

```text
0    2
1    3
2    4
3    5
4    6
5    7
dtype: int64
```

```python
# In this case the constructor is passed a variable that was defined above as a list 
simple2=pd.Series(values)
simple2
```

```text
0     7
1     8
2     9
3    10
4    11
dtype: int64
```

```python
# Here the constructor is passed a variable containing a list that is a mix of 
# alphanumerics and numerical values
simple3=pd.Series(weird)
simple3
```

```text
0         Some text
1    Some more Text
2                 2
3                 3
dtype: object
```

Note that all three series have different length (6 datapoints for `simplest`;5 for `simple2` and 4 for `simple3`).  




### Series declared using a specific index

In the example below, the series Simplest and Simple2 are recreated (overwritten), but this time an index is specified. Here the index is declared as a(nother) list. 

```python
# In this example the constructor is given both the values 
# and specific values for the index
Simplest=pd.Series([2,3,4,5,6],index=[1966,1967,1996,1999,2000])
Simplest
```

```text
1966    2
1967    3
1996    4
1999    5
2000    6
dtype: int64
```

```python
simple2=pd.Series(values,index=[1966,1967,1996,1999,2000])
simple2
```

```text
1966     7
1967     8
1996     9
1999    10
2000    11
dtype: int64
```

Now these Series look more like time-series data!

### Create Series from a dictionary

In python, a dictionary is a data structure that is more generally known in computer science as an associative array. A dictionary consists of a collection of key-value pairs, where each key-value pair *maps* or *links* the key to its associated value.  

```{note}
A dictionary is enclosed in curly brackets {}, versus a list which is enclosed in square brackets[].
```

Thus mydict={"1966":2,"1967":3,"1968":4,"1969":5,"2000":-15} creates a dictionary object called mydict.   ```mydict```maps (or links) the key "1966" to the value 2.
```{note}
In this example the Key was a string but we could just as easily made it a numerical value:  
```
In the following example the keys are numeric

```mydict2={1966:2,1967:3,1968:4,1969:5,2000:-15}```

Here, mydict2  links (maps) the key 1966 to the value 2 and "1969" links to the value 5.


The series constructor can also accept a dictionary. In this instance, the key of the dictionary becomes the index of the series that was used to instantiate the series.

```python
mydict2={1966:2,1967:3,1968:4,1969:5,2000:6}
simple2=pd.Series(mydict2)
simple2
```

```text
1966    2
1967    3
1968    4
1969    5
2000    6
dtype: int64
```

## The `DataFrame` class in `Pandas`

The `DataFrame` is the primary structure of pandas. It is a two-dimensional data structure with named rows and columns.  Each column can have different data types (numeric, string, etc).

By convention, a `dataframe` is often called df or some other modifier followed by df, to assist in reading the code.

Much more detail on standard pandas dataframes can be found on the *official pandas website* [https://pandas.pydata.org/docs/reference/frame.html](https://pandas.pydata.org/docs/reference/frame.html).

### Creating or instantiating a dataframe

Like any object, a `DataFrame` can be created by calling the constructor of the pandas class `DataFrame`.  

The `pandas.DataFrame()` method is constructor for the `DataFrame` class. It can take several forms (as with `Series`), but always returns (instantiates) an instance of a `DataFrame` object -- i.e. a variable whose contents are a `DataFrame`.

The code example below creates a `DataFrame` called `df` comprised of three columns B,C and E; indexed between 2018 and 2021. Macroeconomists may interpret the index as dates, but for pandas they are just numbers.  

The `DataFrame` is instantiated from a dictionary and assigned a specific index by passing a list of years as the index.

```python

df = pd.DataFrame({'B': [1,1,1,1],'C':[1,2,3,6],'E':[4,4,4,4]},
                  index=[2018,2019,2020,2021])
df
```

```text
B  C  E
2018  1  1  4
2019  1  2  4
2020  1  3  4
2021  1  6  4
```

```{note}
In the `DataFrame`s that are used in macrostructural models like MFMod, each  column is often interpreted as a time-series of an economic variable. So in this dataframe,  normally B, C and E would each be interpreted as an economic time-series. 

That said, there is nothing in the `DataFrame` class that suggests that the data it stores must be time-series or even numeric in nature.

```

### Alternative ways to set the time period of a dated index

A somewhat more creative way to initialize the `dataframe` for dates would use a loop to specify the dates that get passed to the constructor as an argument. 

Below a `DataFrame` `df` with two Series (A and B), is initialized with the values 100 for all data points.

The index is defined dynamically by a loop ```index=[2020+v for v in range(number_of_rows)]``` that runs `number_of_rows` times (6 times in this example) setting v equal to 2020+0, 2020+1,...,2020+5 (recall, that python is zero-indexed so the first value of v is 0, not one). The resulting list whose values are assigned to index is \[2020,2021,2022,2023,2024,2025\].

The big advantage of this method is that if the user wanted to have data created for the period 1990 to 2030, they would only have to change number_of_rows from 6 to 41, and then change the staring date in the loop from 2020 to 1990.

```python
#define the number of years for which the data is to be created.
number_of_rows = 6 

# call the dataframe constructor
df = pd.DataFrame(100,
       index=[2020+v for v in range(number_of_rows)], # create row index
       # equivalent to index=[2020,2021,2022,2023,2024,2025] 
       columns=['A','B'])                                 # Assign the output to two columns,named A and B
df
```

```text
A    B
2020  100  100
2021  100  100
2022  100  100
2023  100  100
2024  100  100
2025  100  100
```

This second example simplifies the creation even further by  specifying the begin and end point as a range.

```python


df1 = pd.DataFrame(200,
       index=[v for v in range(2020,2030)], # create row index
       # equivalent to index=[2020,2021,...,2029] 
       columns=['A1','B1'])                                 # create column name 
df1
```

```text
A1   B1
2020  200  200
2021  200  200
2022  200  200
2023  200  200
2024  200  200
2025  200  200
2026  200  200
2027  200  200
2028  200  200
2029  200  200
```

### Adding a column to a dataframe

If a value is assigned to a column that does not exist, pandas will add a column with that name and fill it with values resulting from  the calculation.



The size of the object assigned to the new column must match the size (number of rows) of the pre-existing `DataFrame`. Originally df has 6 rows so we must supply 6 data points for this command to run error free.

```python
df["NEW"]=[10,12,10,13,14,15]  #df originally has 6 rows so we must supply 6 data points for this command to run error free
df
```

```text
A    B  NEW
2020  100  100   10
2021  100  100   12
2022  100  100   10
2023  100  100   13
2024  100  100   14
2025  100  100   15
```

### Revising values

If the column exists, then the = method will revise the values of the rows with the values assigned in the statement.

```{warning}
The dimensions of the list assigned via the `=` method must be the same as the `DataFrame` (i.e. there must be exactly as many values as there are rows).  Alternatively if only one value is provided, then that value will replace all of the values in the specified column (be broadcast to the other rows in the column).
```

Below we change the values of the `NEW` Column that we generated earlier.

```python
df["NEW"]=[11,12,10,14,2,1]

df
```

```text
A    B  NEW
2020  100  100   11
2021  100  100   12
2022  100  100   10
2023  100  100   14
2024  100  100    2
2025  100  100    1
```

```python
# replace all of the rows of column B with the same value
df['B']=17
df
```

```text
A   B  NEW
2020  100  17   11
2021  100  17   12
2022  100  17   10
2023  100  17   14
2024  100  17    2
2025  100  17    1
```

The declaration of the column name, can either use single or double quotes -- but they cannot be mixed.  Thus

```df['A']=7```

is fine, and so is
```df["B"]=7```
but 
```df["Error']=7```
would generate an error because the string created with `"` is not closed by another matching `"`.  Similarily the string created with `'` is not closed by a matching `'`.

## Selected pandas methods

Pandas has a number of methods (functions that operate on the underlying data of a `pandas` object).  Several of them are used when working with a World Bank model in `ModelFlow` and these are discussed below.
### .columns lists the column names of a dataframe

The method ```.columns``` returns the names of the columns in the dataframe.

```python
df.columns
```

```text
Index(['A', 'B', 'NEW'], dtype='object')
```

### .size indicates the dimension of a list

so ```df.columns.size``` returns the number of columns in a dataframe.

```python
df.columns.size
```

```text
3
```

The `dataframe` `df` has 3 columns. 

### .eval() evaluates (calculates) an expression on the data of a dataframe

`.eval` is a native dataframe method, which does calculations on a `dataframe` and returns a revised `dataframe`. With this method expressions can be evaluated and new columns created.  

```python
df.eval('X = B*NEW')
```

```text
A   B  NEW    X
2020  100  17   11  187
2021  100  17   12  204
2022  100  17   10  170
2023  100  17   14  238
2024  100  17    2   34
2025  100  17    1   17
```

### multiple expressions can be evaluated with .eval()

With `.eval()` multiple expressions can be evaluated at the same time.  In the example below three apostrophe's are used to indicate a multiple-line block of text.  Each line is executed separately by eval.



In this example, two new variables X and THE_ANSWER are created in a single call to .eval().

```python
df.eval('''X = B*NEW
           THE_ANSWER = 42''')
```

```text
A   B  NEW    X  THE_ANSWER
2020  100  17   11  187          42
2021  100  17   12  204          42
2022  100  17   10  170          42
2023  100  17   14  238          42
2024  100  17    2   34          42
2025  100  17    1   17          42
```

In python three apostrophes `'''` signals a block of text.  Of course the block needs to be opened and closed -- in each case by three apostrophes.  New lines that appear within a block (if any) are an integral part of the block.

Because the result of the `.df.eval()` call was not assigned to anything, least of all the dataframe df, the value of df is unchanged.

```python
df
```

```text
A   B  NEW
2020  100  17   11
2021  100  17   12
2022  100  17   10
2023  100  17   14
2024  100  17    2
2025  100  17    1
```

To store the results of the calculation, the expression must be assigned to a variable.  The pre-existing `DataFrame` can be overwritten by assigning it the result of the `eval` statement or a new `DataFrame` could be created.

```python
df=df.eval('''X = B*NEW
           Y = 42''')
df
```

```text
A   B  NEW    X   Y
2020  100  17   11  187  42
2021  100  17   12  204  42
2022  100  17   10  170  42
2023  100  17   14  238  42
2024  100  17    2   34  42
2025  100  17    1   17  42
```

With this operation the new columns, X and Y have been appended to the dataframe df.


The ```.eval()``` method is a native `pandas` method.  As such it cannot handle lagged variables (because pandas do not support the idea of a lagged variable.

The ```.mfcalc()``` and the ```.upd()``` methods discussed in the next chapter are `ModelFlow` features that extend the functionalities native to `dataframe` that allows such calculations to be performed.  

```python
df2=df.eval('''X = B*NEW
           Y = 42''')
df2
```

```text
A   B  NEW    X   Y
2020  100  17   11  187  42
2021  100  17   12  204  42
2022  100  17   10  170  42
2023  100  17   14  238  42
2024  100  17    2   34  42
2025  100  17    1   17  42
```

Here the results are assigned to a new dataframe `df2`.

## The .loc[] method 

The `.loc[]` method is a powerful pandas routine used extensively in `ModelFlow`. `.loc[]` selects a portion (slice) of a dataframe and  allows the user to display and/or revise specific sub-sections of a single or several columns or rows in a dataframe.

### Selecting a single element in a dataframe:  `.loc[row,column]`

```.loc[row,column]``` operates on a single cell in the dataframe.  Thus, the below displays the value of the cell with index=2023 observation from the column NEW.

```python
df.loc[2023,'NEW']
```

```text
np.int64(14)
```

### Selecting a single columns: `.loc[:,column]`

The lone colon in a `.loc[]` statement indicates all the rows or columns.  Here all of the rows of the column labeled NEW are displayed.

```python
df.loc[:,'NEW']
```

```text
2020    11
2021    12
2022    10
2023    14
2024     2
2025     1
Name: NEW, dtype: int64
```

### Selecting a single row: `.loc[row,:] `

Here all of the columns, for the selected row are displayed.

```python
df.loc[2023,:]
```

```text
A      100
B       17
NEW     14
X      238
Y       42
Name: 2023, dtype: int64
```

###  Selecting specific rows and columns: .loc[xxx,xxx],[names...]]

Passing a list in either the rows or columns portion of the `.loc` statement will allow multiple rows or columns to be displayed.

```python
df.loc[[2021,2024],['B','NEW']]
```

```text
B  NEW
2021  17   12
2024  17    2
```

### Select a range: the ":" operator in a '.loc' statement

with the colon operator we can also select a range of results.

Here from 2018 to 2019.

```python

df.loc[2021:2023,['B','NEW']]
```

```text
B  NEW
2021  17   12
2022  17   10
2023  17   14
```

### Revising a sub-section of a `DataFrame,` using  `.loc[]` on the left hand side to assign values to specific cells
This can be handy when revising a `DataFrame` in preparation for running a scenario.<br>

```python
df.loc[2022:2024,'NEW'] = 20
df
```

```text
A   B  NEW    X   Y
2020  100  17   11  187  42
2021  100  17   12  204  42
2022  100  17   20  170  42
2023  100  17   20  238  42
2024  100  17   20   34  42
2025  100  17    1   17  42
```

```{warning}
The dimensions on the right hand side of = and the left hand side should match. That is: either the dimensions should be the same, or the right hand side should be a single value that is then ```broadcast``` into all of the lements of the left hand slice.

For more on broadcasting see here (https://jakevdp.github.io/PythonDataScienceHandbook/02.05-computation-on-arrays-broadcasting.html)
```

**For more info on the .loc[] method**
- Description [https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html).
- Search [https://www.google.com/search?q=pandas+dataframe+loc&newwindow=1](https://www.google.com/search?q=pandas+dataframe+loc&newwindow=1).


**For more info on pandas:**
- Pandas homepage [https://pandas.pydata.org/](https://pandas.pydata.org/).
- Pandas community tutorials [https://pandas.pydata.org/pandas-docs/stable/getting_started/tutorials.html](https://pandas.pydata.org/pandas-docs/stable/getting_started/tutorials.html).
