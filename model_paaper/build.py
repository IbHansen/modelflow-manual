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
bookdir = 'thetestbook' if 'test' in options else 'thebook' 
doall = '--all' if 'all' in options else ''

buildloc = Path(f'{bookdir}/_build/')
buildhtml = buildloc / 'html'
(destination := Path(r'C:/modelbook/IbHansen.github.io/mf')).mkdir(parents=True, exist_ok=True)
fileloc = str((buildhtml / 'index.html').absolute())

# print(fileloc)
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
     
if 'latex' in options: 
     xx0 = run(f'jb build {bookdir}/ --builder=latex')
     
if 'copy' in options:
    copytree(buildhtml,destination,dirs_exist_ok=True )
     
    