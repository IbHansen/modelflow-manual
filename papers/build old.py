# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 19:50:51 2022

builds a jupyterbook 

look at the cheatcheet. 


@author: ibhan
"""
from subprocess import run
import webbrowser as wb
from pathlib import Path
from shutil import copy, copytree
 
import sys

import modelutil 

import re
print('Build  called with:', sys.argv)
options = sys.argv 
# raise Exception('stop')
for aname in options: 
    if aname.endswith('book'):
        bookdir = aname
        break
else:
    bookdir = 'mfbook'    
 
 
doall = '--all' if 'all' in options else ''

buildloc = Path(f'{bookdir}/_build/')
buildhtml = buildloc / 'html'
# (destination := Path(fr'C:/modelbook/IbHansen.github.io/{bookdir}')).mkdir(parents=True, exist_ok=True)
fileloc = str((buildhtml / 'index.html').absolute())

#print(f'{fileloc=}\n{destination=}')
print(f'{fileloc=}\n') #dropped destination
latexroot = modelutil.get_latex_root(bookdir)   

# breakpoint()
xx0 = run(f'jb build {bookdir}/ {doall}')
if not xx0.returncode:
    wb.open(rf'file://{fileloc}', new=2)
else: 
    exit()     


#%% 
latexdir = Path(f'{bookdir}/_build/jupyter_execute/content')
for dir in sorted(Path(f'{bookdir}/_build/jupyter_execute').glob('**')):
    # print(f'{dir=}')
    for i, picture in enumerate(sorted(dir.glob('*.png'))):
        # print(picture) 
        try:
            copy(picture,latexdir)
        except:
            # print(f'Not copied{picture}')
            ...
    for i, picture in enumerate(sorted(dir.glob('*.svg'))):
        # print(picture) 
        try:
            copy(picture,latexdir)
        except:
            ...
            # print(f'Not copied{picture}')
    for i, picture in enumerate(sorted(dir.glob('*.pdf'))):
        # print(picture) 
        try:
            copy(picture,latexdir)
        except:
            ...
            # print(f'Not copied{picture}')
            
#%%    

def replace_latex_citations(latex_string):
    """
    Replaces the LaTeX citation format from {[}...{]}) to {(}...{)})
    in the provided LaTeX string.

    Parameters:
    latex_string (str): A string containing LaTeX source code.

    Returns:
    str: The modified LaTeX string with updated citation format.
    """
    # Regex pattern to find the citations
    pattern = r'\{\[\}(\\hyperlink{cite\.Reference:id\d+}\{\d+\})\{\]\}'

    # Replacement pattern
    replacement = r'{(}\1{)}'

    # Replace the pattern in the string
    modified_string = re.sub(pattern, replacement, latex_string)

    return modified_string

         
def latex_process(latexroot ):
    r"""
    Processes a LaTeX file generated by Sphinx to address common issues.

    This function takes the root name of a LaTeX file generated by Sphinx (`latexroot`) as input and performs the following actions:

    1. **Adds missing packages:** Checks if the `.tex` file includes the `makeidx` package, necessary for generating an index. If missing, it inserts the `\usepackage{makeidx}` line at the beginning.
    2. **Fixes index entries:** Removes unnecessary `\spxentry` commands from the `.idx` file, which can clutter the index.
    3. **Inserts missing elements:** Adds the following elements to the `.tex` file at specific locations:
        - `\usepackage{makeidx}` (if missing)
        - `\addcontentsline{toc}{chapter}{\indexname}` to include the "Index" entry in the table of contents
        - `{\huge\bfseries\raggedright Foreword\par}` to create a large, bold, right-aligned heading for the Foreword
        - `\renewcommand{\cleardoublepage}{\clearpage}` to avoid blank pages between chapters
        - `\newpage % taksigelse` (Danish for "acknowledgements") to start a new page for the acknowledgements section
    4. **Removes unwanted elements:** Removes the following elements from the `.tex` file:
        - All `\spxentry` commands
        - Chapters titled "Index" and "Reference" (including their labels)
        - Unnecessary Sphinx directives related to the index and reference chapters

    Args:
        latexroot (str): The root name of the LaTeX file (e.g., "book").

    Raises:
        IOError: If there are errors reading or writing the `.tex` file.

    """


    r'''It seems that the generated .tex file is missing a \usepackage{makeidx} 
    and that the .idx file contains a lot of unvanted \spxentry  so we fix these two problems 
    
    and more problems which makes it look not so nice
    ''' 
    
    latexfile =  f'{bookdir}/_build/latex/{latexroot}.tex'
    
    with open(latexfile,'rt',encoding="utf8") as f:
        latex= f.read()
        
    lf= '\n'
    
   # now a list of some text inserted at specific places in the .tex file
   # the place is defined by the first string in the tupple. 
    insertbefore = [
        (r'\makeindex',r'\usepackage{makeidx}'), 
        (r'\printindex',r'\addcontentsline{toc}{chapter}{\indexname}'),   # forgot the foreword heading, so it is inserted 
         (r'''\sphinxAtStartPar
Over the decades''',r'{\huge\bfseries\raggedright Foreword\par}'),
        (r'\title',r'\renewcommand{\cleardoublepage}{\clearpage}'),       # to avoid blank pages between chapters 

        (r"""\begin{DUlineblock}{0em}
\item[] \sphinxstylestrong{\Large Acknowledgements}
\end{DUlineblock}""",
         r"\newpage % taksigelse  ")]
    
    for before,insert in insertbefore: 
        if not insert in latex:
            latex = latex.replace(before,insert+lf+before)

    # Now some text to purge from the text  
  
    purge =[r'\spxentry',
            r'\chapter{Index}',
            r'\label{\detokenize{genindex:index}}\label{\detokenize{genindex::doc}}',
            r'\chapter{Reference}',
            r'\label{\detokenize{Reference:reference}}\label{\detokenize{Reference::doc}}',
            r'''\sphinxstepscope


\chapter{Index}
\label{\detokenize{genindex:index}}\label{\detokenize{genindex::doc}}
\sphinxstepscope

''',
r'''\sphinxstepscope




\sphinxstepscope''',
] 
    for p in purge:
       latex = latex.replace(p,'')
    
    
    latex = replace_latex_citations(latex)
    
    # breakpoint() 
    with open(latexfile,'wt',encoding="utf8") as f:
        f.write(latex) 


#%%    
def is_acrobat_running():
    import subprocess

    try:
        output = subprocess.check_output('tasklist', encoding='utf-8')
        # print(output)
        return 'Acrobat.exe' in output
    except:
        return False
    

if 'latex-pdf' in options or 'pdf-latex' in options or 'latex' in options:
    
     while is_acrobat_running():
        input("Shut Acrobat before continuing. Once closed, press Enter to continue...")
    
        # Check again after the user has given input
        if is_acrobat_running():
            print("Acrobat is still running! Please close it.")
    
    
     xx0 = run(f'jb build {bookdir}/ --builder=latex')     
     latex_process(latexroot)

     # 
     # if the file is processed by miktex it works now, but due to a latexmk issue we use 
     # latexmk, then texindy to process it further and then latexmk to create the final pdf file  
     # 
     if not 'nopdf' in options: 
         xx0 = run(f'latexmk -pdf -dvi- -ps- -f {latexroot}.tex'      ,cwd = f'{bookdir}/_build/latex/')
         xx0 = run(f'texindy    -o "{latexroot}.ind" "{latexroot}.idx"',cwd = f'{bookdir}/_build/latex/')
         xx0 = run(f'latexmk -pdf -dvi- -ps- -f {latexroot}.tex'      ,cwd = f'{bookdir}/_build/latex/')
         # #xx0 = run('latexmk -pdf -f MFModinModelflow.tex',cwd = f'{bookdir}/_build/latex/')
         print(f'PDF generated: see {bookdir}/_build/latex/')

     
if 'copy' in options:
    try:
        (destination := Path(fr'C:/modelbook/IbHansen.github.io/{bookdir}')).mkdir(parents=True, exist_ok=True)
    except:
        print('you are probably not Ib, so this is impossible')
    else:     
        copytree(buildhtml,destination,dirs_exist_ok=True )
        print('Remember to push the repo ')
     
    