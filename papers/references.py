# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 16:05:17 2024

@author: ibhan
"""
from pathlib import Path
import modelutil_cli as mu 


# toc_files  =  mu.get_toc_files(fileloc='mfbook')

def make_reflist(bookdir):
    toc_files  =  mu.get_toc_files(fileloc=bookdir)

    # reflist =  mu.search(toc_files,r"^\(([^)]+)\)=",notfound=False,silent=1,printmatch=0,showfiles=False,onlymarkdown=True,returnfound=True)
    reflist0 =  mu.search(toc_files,r"^\((.*?)\)=",notfound=False,silent=1,printmatch=0,showfiles=False,onlymarkdown=True,returnfound=True)
    reflist2 =  mu.search(toc_files,r":::\{index\} .+\n:name: *([^\s]+) *",notfound=False,silent=1,printmatch=0,showfiles=False,onlymarkdown=True,returnfound=True)
    
    out0 = '\n'.join([f'[{ref.replace("_"," ")}]({ref}) # nb =  {nb.stem}' for ref,nb in  reflist0])
    out1 = '\n'.join([f'[{ref.replace("_"," ")}]({ref}) # nb =  {nb.stem}' for ref,nb in  reflist2])
    out = f'Reference targets in {bookdir}\nFrom (xxx)=\n'+ out0+'\n\nAnd from index names \n' + out1
    outfile = Path(bookdir) / 'references.txt'
    # with open(outfile,'wt') as f: 
    #     f.write('References in this jupyter book\n'+out)
    return 

if __name__ == '__main__':
    make_reflist('mfbook') 