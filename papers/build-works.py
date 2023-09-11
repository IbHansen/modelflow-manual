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
print(sys.argv)
options = sys.argv 
# raise Exception('stop')
for aname in options: 
    if aname.endswith('book'):
        bookdir = aname
        break
else:
    bookdir = 'mfbook'    
 
latexroot = 'MFModinModelflow'    
 
doall = '--all' if 'all' in options else ''

buildloc = Path(f'{bookdir}/_build/')
buildhtml = buildloc / 'html'
# (destination := Path(fr'C:/modelbook/IbHansen.github.io/{bookdir}')).mkdir(parents=True, exist_ok=True)
fileloc = str((buildhtml / 'index.html').absolute())

#print(f'{fileloc=}\n{destination=}')
print(f'{fileloc=}\n') #dropped destination

# breakpoint()
xx0 = run(f'jb build {bookdir}/ {doall}')
# wb.open(rf'file://C:\wb new\Modelflow\working_paper\{bookdir}\_build\html\index.html', new=2)
wb.open(rf'file://{fileloc}', new=2)


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
def latex_process(latexroot ):
    r'''It seems that the generated .tex file is missing a \usepackage{makeidx} 
    and that the .idx file contains a lot of unvanted \spxentry  so we fix these two problems 
    
    
    ''' 
    
    latexfile =  f'{bookdir}/_build/latex/{latexroot}.tex'
    idxfile   =  f'{bookdir}/_build/latex/{latexroot}.idx'
    
    with open(latexfile,'rt',encoding="utf8") as f:
        latex= f.read()
        
    if not r'\usepackage{makeidx}' in latex:
        lf= '\n'
        latexout1 = latex.replace(r'\makeindex',r'\usepackage{makeidx}'+lf+
                                r'\makeindex')
    else: 
        latexout1 = latex 
  
    latexout2 = latexout1.replace(r'\spxentry','') 
    # breakpoint() 
    with open(latexfile,'wt',encoding="utf8") as f:
        f.write(latexout2) 


#%%    
        

if 'latex-pdf' or 'pdf-latex' in options: 
     xx0 = run(f'jb build {bookdir}/ --builder=latex')     
     latex_process(latexroot)
     xx0 = run('latexmk -pdf -dvi- -ps- -f MFModinModelflow.tex',cwd = f'{bookdir}/_build/latex/')
     xx0 = run(f'texindy    -o "MFModinModelflow.ind" "MFModinModelflow.idx',cwd = f'{bookdir}/_build/latex/')
     xx0 = run('latexmk -pdf -dvi- -ps- -f MFModinModelflow.tex',cwd = f'{bookdir}/_build/latex/')
     #xx0 = run('latexmk -pdf -f MFModinModelflow.tex',cwd = f'{bookdir}/_build/latex/')
     print(f'PDF generated: see {bookdir}/_build/latex/')

     
if 'copy' in options:
    copytree(buildhtml,destination,dirs_exist_ok=True )
     
    