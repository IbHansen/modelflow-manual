# -*- coding: utf-8 -*-
"""
@author: ibhan

Some utilities to manage files in a jupyterbook 


"""

import yaml
from pathlib import Path
import nbformat as nbf
from glob import glob
import webbrowser
from subprocess import run
import webbrowser as wb
from pathlib import Path
from shutil import copy, copytree
import argparse
import re
 
bookdir='mfbook'
def get_all_files(fileloc=bookdir):
    all_notebooks = glob(f"{fileloc}/content/**/*.ipynb", recursive=True)
    return all_notebooks 

def get_all_notebooks(fileloc=bookdir):
    '''get all notebooks in the fileloc book'''
    all_notebooks = list(Path(f'{fileloc}/content').glob('**/*.ipynb'))
    relevant_notebooks = [f for f in all_notebooks if not '.ipynb_checkpoints' in f.parts]
    return relevant_notebooks 



def get_config(fileloc=bookdir):
    '''Get all files mentioned in the _toc but not the root'''
    with open(Path(fr'{fileloc}/_config.yml'), 'r') as f:
        config_data = yaml.safe_load(f)
    return config_data    

def get_latex_root(fileloc=bookdir):
    try:  
        latex_root = get_config(fileloc = fileloc)['latex']['latex_documents']['targetname'].split('.')[0]
    except: 
        latex_root = 'book'    
    return latex_root    


def is_notebook(filename):
    return  type(filename) == type(Path('ibs.ipynb')) and filename.suffix == '.ipynb'
    
    
def get_toc_files(fileloc=bookdir):
    '''Get all files mentioned in the _toc but not the root'''
    with open(Path(fr'{fileloc}/_toc.yml'), 'r') as f:
        toc_data = yaml.safe_load(f)

    # breakpoint() 
    
    
    file_list = []
    chapter_nr = 0

    def make_file_path(f):
        f_name  = f if f.endswith('.md') else f+'.ipynb'
        f_path = Path(fr'{fileloc}/{f_name}')
        return f_path

    
    def process_toc_entries(entries):
        nonlocal chapter_nr
        for i,entry in enumerate(entries):
            # print(i,entry)
            if 'file' in entry :
                filename = make_file_path(entry['file'])
                if filename.exists():
                    chapter_nr = chapter_nr + 1 
                    file_list.append(filename)
                else:   
                    file_list.append((filename,-1))

            if 'chapters' in entry:
                process_toc_entries(entry['chapters'])
            if 'sections' in entry:
                process_toc_entries(entry['sections'])
        # breakpoint() 

    file_list.append(make_file_path(toc_data['root']))
    
    process_toc_entries(toc_data.get('parts', []))
     # Print the list of file paths
     
    # for file_path in file_list:
    #     print(file_path)
    
    

    return file_list




def start_notebooks(notebook_list):
    ''' start all notebooks in jupyter in the notebook list '''
    base_url = "http://localhost:8889/notebooks/"

    for notebook_path in notebook_list:
        # print(notebook_path)
        #print(f'{notebook_path.suffix=}')
        if is_notebook(notebook_path) :
            url = base_url + str(notebook_path )
            print(url)
            webbrowser.open(url, new=2)



def hide_cells(notebook_list):
    # Text to look for in adding tags
    text_search_dict = {
        "# HIDDEN": "remove_cell",  # Remove the whole cell
        "# NO CODE": "remove_input",  # Remove only the input
        "# HIDE CODE": "hide_input"  # Hide the input w/ a button to show
    }
    
    # Search through each notebook and look for th text, add a tag if necessary
    for ipath in notebook_list:
        try:
            ntbk = nbf.read(ipath, nbf.NO_CONVERT)
            changed = False
            
            for cell in ntbk.cells:
                cell_tags = cell.get('metadata', {}).get('tags', [])
                for key, val in text_search_dict.items():
                    # breakpoint() 
                    if key in cell['source']:
                        if val not in cell_tags:
                            cell_tags.append(val)
                            changed = True 
                            print(f'Tags set in {ipath=} \n{cell_tags=}')    
                if len(cell_tags) > 0:
                    cell['metadata']['tags'] = cell_tags
        
            if changed:             
                nbf.write(ntbk, ipath)
                print(f'notebook written {ipath}')
            else: 
                print(f'notebook not changed by hide_cells  : {ipath}')
        except: 
                print(f'Hide did not work for this notebook : {ipath}')

def box_nr_cells(notebook_list):
    
    running_nr = 0 
    box_toc =[]

    def make_box_nr(text): 
        patbox = r'(:::{index} single: Box.*?\n:::\n*)?:::{[Aa]dmonition} [Bb]ox (\d+)(\.\d*)* (.*)'

        nonlocal running_nr 
        nonlocal box_toc 
    
        def replace_box(match):
            nonlocal running_nr 
            if 0:
                for idx, group in enumerate(match.groups(), 1):
                    print(f"Group {idx}: {group}")

            lf = '\n'
            running_nr =running_nr + 1
            box_index = f":::{{index}} single: Boxes; Box{running_nr:>4}. {match[4]}{lf}:::"
            box_name = f":::{{admonition}} Box {running_nr}. {match[4]}"
            replace   = f"{box_index}{lf}{lf}{box_name}"
            box_toc.append( box_name )
            if 1: print(f'{replace=}')
            return replace 
        
        return re.sub(patbox, replace_box,text)
       
    for ipath in notebook_list:
        # breakpoint() 
        try:
            ntbk = nbf.read(ipath, nbf.NO_CONVERT)
            changed = False
            for cell in ntbk.cells:
                    # breakpoint() 
                    if (newsource := make_box_nr( cell['source'])):
                        if newsource != cell['source'] :
                            changed = True 
                            # print(f'box change {ipath=} \n{newsource=}')    
                            cell['source'] = newsource 
        
            if changed:             
                nbf.write(ntbk, ipath)
                print(f'notebook written {ipath}')
            else: 
                print(f'notebook not changed by box numbering   : {ipath}')
        except: 
                print(f'Box did not work for this file : {ipath}')
        
    print('\n boxes in the book',*box_toc,sep='\n')        
    return 


def search(notebook_list, pat=r'.*[Bb]ox.*', notfound=False, silent=0, showfiles=True,
           fileopen=False, printmatch=False, replace=False, savecell=True):
    """
    Search for a specified pattern in Jupyter notebooks within a list of paths and optionally replace it.

    Parameters:
    - notebook_list (list): A list of paths to Jupyter notebooks.
    - pat (str): The regular expression pattern to search for in the cells' source code. 
                 Default is '.*[Bb]ox.*'.
    - notfound (bool): If True, return a list of notebooks where the pattern is not found.
                       If False, return a list of notebooks where the pattern is found.
                       Default is False.
    - silent (int): If not 0, suppress print statements. Default is 0.
    - showfiles (bool): If True, print the list of files where the pattern is found or not found.
                        Default is True.
    - fileopen (bool): If True, open the notebooks where the pattern is found with the default system application.
                       Default is False.
    - printmatch (bool): If True, and if silent is 0, print the matched patterns; otherwise, print the entire cell content.
                         Default is False.
    - replace (str or False): The replacement string for the pattern. If False, no replacement is done.
                              Default is False.
    - savecell (bool): If True and replace is not False, save the cell with the replaced content back to the notebook.
                       Default is True.

    Returns:
    - list: A list of paths to notebooks where the pattern is found or not found, based on the 'notfound' parameter.
    
    Note:
    - The function uses regex to search for and optionally replace the specified pattern in the source code of each cell.
    - If 'showfiles' is True, it prints the list of files where the pattern is found or not found.
    - If 'fileopen' is True, it opens the notebooks with the pattern found using the default system application.
    - If 'replace' is a string, the pattern is replaced with this string in the notebook cells, and changes are saved if 'savecell' is True.
    """


    

    found_list = []
    notebook_list_path = [i for i in notebook_list if is_notebook(i)]
    
    
    if not silent: print(f'Search patter:{pat}')
    for ipath in notebook_list_path:
        found = False 
        
        try:

            with open(ipath, 'r',encoding='utf-8') as f:
                ntbk = nbf.read(f, nbf.NO_CONVERT)
                
            for cell in ntbk.cells:
                    # breakpoint() 
                    source =  cell['source']
                    matches = re.findall(pat, source)
                    if len(matches):
                        found = True                            
                        # breakpoint()
                        if not silent:     
                                print(f"\nPattern  here: {'/'.join(ipath.parts[-2:])}")         
                                if printmatch: 
                                    print(*matches,sep='\n')
                                else: 
                                    print(source)
                        if replace: 
                            newsource = re.sub(pat,replace,source)
                            print(f'\nThis\n{source}\nReplaced by:{newsource}')
                            if savecell: 
                                cell.source=newsource
            if found: 
               found_list.append(ipath)  
               if replace and savecell: 
                   with open(ipath, 'w',encoding='utf-8') as f:
                       nbf.write(ntbk,f)

        except Exception as e: 
                print(f'Search did not work for this file : {ipath} , {e}')
    not_found_list =     [f for f in notebook_list_path if f not in found_list] 
    
    if  showfiles: 
        print(f'\n{pat} found here: ')
        print(*[name for name  in found_list],sep='\n')
        print(f'\n{pat} Not found here: ')
        print(*[name for name  in not_found_list],sep='\n')
        
    if fileopen: 
        start_notebooks(found_list)

    return not_found_list if notfound else found_list 

def insert_colab(notebook_list):
    content="""\
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb ipysheet  --no-dependencies ')

%load_ext autoreload
%autoreload 2
"""  

    for ipath in notebook_list:
        try:
            found = False
           
            with open(ipath, 'r') as f:
                ntbk = nbf.read(f, nbf.NO_CONVERT)
               
            for cell in ntbk.cells:
                    # breakpoint() 
                    source =  cell['source']
                    amatch = re.search(r'google\.colab', source)
                    if amatch:
                        ...
                        found = True # breakpoint()
            if found:             
                print(f"Colab cell found here   : {'/'.join(ipath.parts[-2:])} ")  
            else:
                # breakpoint() 
                print(f"NO Colab cell found here: {'/'.join(ipath.parts[-2:])} ") 
                new_cell = nbf.v4.new_code_cell(source=content)
                if 'id' in new_cell:
                    del new_cell['id']
                cell_tags = cell.get('metadata', {}).get('tags', [])
                cell_tags.append("remove_cell")
                new_cell['metadata']['tags'] = cell_tags
# Step 3: Insert the new cell at a specific position (e.g., second position)
                ntbk.cells.insert(1, new_cell)
                with open(ipath, 'w') as f:
                    ...
                    nbf.write(ntbk, f)
                    
                print(f'Notebook written {"/".join(ipath.parts[-2:])}')

    
        except: 
                print(f'Search colab did not work for this file : {ipath}')
        

def insert_cell(notebook_list,
     content="""\
# Prepare the notebook for use of modelflow 

# Jupyter magic command to improve the display of charts in the Notebook
%matplotlib inline

# Import pandas 
import pandas as pd

# Import the model class from the modelclass module 
from modelclass import model 

# functions that improve rendering of modelflow outputs
model.widescreen()
model.scroll_off();"""  ,
     condition= r'',
     tags=['remove_cell']):
    
    """
    Inserts a specific code cell into Jupyter notebooks if a certain condition is met.

    The function checks each notebook in the provided list. If the notebook contains 
    a cell that matches the given condition, it will print a message. If no such cell
    is found, a new cell with the specified content is added to the notebook.

    Parameters:
    - notebook_list (list): A list of paths to Jupyter notebooks.
    - content (str): The content of the cell to be inserted. By default, it contains
      code to manage dependencies for Google Colab.
    - condition (str, regex pattern): A regex pattern that, if found in a notebook cell,
      will prevent the insertion of the new cell.
    - tag (str): A tag to append to the metadata of the new cell.

    The function will print messages indicating:
    1. Notebooks where a cell matching the condition is found.
    2. Notebooks where the new cell is inserted.
    3. Notebooks where searching failed.

    Note: The function uses nbformat to manipulate notebooks and expects valid notebook paths.
    """    

    for ipath in [ n for n in notebook_list if is_notebook(n)]:
        try:
            found = False
               
            with open(ipath, 'r',encoding='utf-8') as f:
                ntbk = nbf.read(f, nbf.NO_CONVERT)
                
            for cell in ntbk.cells:
                    # breakpoint() 
                    if condition: 
                        source =  cell['source']
                        amatch = re.search(condition, source)
                        if amatch:
                            ...
                            found = True # breakpoint()
                    else: 
                         found=False 
            if found:             
                print(f"Cell found here   : {'/'.join(ipath.parts[-2:])} ")  
            else:
                # breakpoint() 
                print(f"NO  cell found here: {'/'.join(ipath.parts[-2:])} ") 
                new_cell = nbf.v4.new_code_cell(source=content)
                if 'id' in new_cell:
                    del new_cell['id']
                cell_tags = cell.get('metadata', {}).get('tags', [])
                for tag in tags: 
                    if tag not in cell_tags:
                        cell_tags.append(tag)
                new_cell['metadata']['tags'] = cell_tags
# Step 3: Insert the new cell at a specific position (e.g., second position)
                ntbk.cells.insert(1, new_cell)
                
                with open(ipath, 'w',encoding='utf-8') as f:
                    ...
                    nbf.write(ntbk, f)
                    
                print(f'Notebook written {"/".join(ipath.parts[-2:])}')

    
        except Exception as e: 
                print(f'Insert did not work for this file : {ipath} {e}')
        

            
# Call the function to start the notebooks
# start_notebooks(notebook_list)

#%% main

if __name__ == '__main__':
     
     import sys
     print('Modelutil called with', sys.argv)
    
    
     parser = argparse.ArgumentParser(description="CLI tool for jupyterbook.")
     bookdir_arg = {
        "type": str,
        "default": "mfbook",
        "help": "Directory of the jupyter book"
    }
     parser.add_argument('-b','--bookdir', **bookdir_arg)
    
     # Add subparsers for the sub-commands
     subparsers = parser.add_subparsers(dest="subcommand", help="Available sub-commands")
     # Common argument to be used in all subparsers
    
     box_parser = subparsers.add_parser("box", help="Renumber boxes in the jupyterbook")
     
     open_parser = subparsers.add_parser("open", help="Open all notebooks in the jupyter book ")
     
     list_parser = subparsers.add_parser("list", help="List all files in the jupyter book")
   
     search_parser = subparsers.add_parser("search", help="Search all files in the jupyter book")
     search_parser.add_argument('-p','--pattern', help='Regex search pattern ')
     search_parser.add_argument('-o','--open', action="store_true", help='Open files with pattern ')
     search_parser.add_argument('-ns','--nsilent', help='Not Silent ',action="store_false")

     insert_parser = subparsers.add_parser("insert", help="All notebooks which does not fulfill condition will have cell with content inserted")
   
     insert_parser.add_argument('-c','--colab', action="store_true", help='Insert a Colab enabeling cell ')
     insert_parser.add_argument('-a','--auto', action="store_true", help='Insert a auto load cell ')


     # Parse the arguments
     args = parser.parse_args()
     

    
     # Handle sub-commands
     if args.subcommand == "open":
         print(f"Open")
         toc_files  = get_toc_files(fileloc=args.bookdir)    
         start_notebooks(toc_files)    
         
     elif args.subcommand == "box":
         print('Box is run')
         toc_files  = get_toc_files(fileloc=args.bookdir)
         box_nr_cells(toc_files)
             
     elif args.subcommand == "list":
  
        toc_files  = get_toc_files(fileloc=args.bookdir)
        print(*[name for name  in toc_files],sep='\n')
        
     elif args.subcommand == "search":
         print('Search is run')

         toc_files  = get_toc_files(fileloc=args.bookdir)
        
         found_files = search(toc_files,pat=args.pattern, silent = args.nsilent)
         if  args.open: 
             start_notebooks(found_files)
         

     elif args.subcommand == "insert":
         print('insert is run')
         toc_files  = get_toc_files(fileloc=args.bookdir)
         if args.colab: 
             insert_cell(toc_files)
         if args.auto:
             insert_cell(toc_files,
            content="""\
%load_ext autoreload
%autoreload 2
"""  ,
     condition= r'autoreload',
     tag='remove_cell')
             



     elif args.subcommand is None:
        # Handle the case where no sub-command is given
        print(f"Using book directory: {args.bookdir}")    
    
    
 #%% run   
     toc_files = get_toc_files(args.bookdir)
     all_notebooks = get_all_notebooks()
     if 0:
         insert_cell(toc_files) 
     
     if 0: 
         insert_cell(toc_files,
         content="""\
     #This is code to manage dependencies if the notebook is executed in the google colab cloud service
     if 'google.colab' in str(get_ipython()):
       import os
       os.system('apt -qqq install graphviz')
       os.system('pip -qqq install ModelFlowIb ipysheet  --no-dependencies ')
     """            ) 

     
     if 0: 
        print(*[name for name  in toc_files],sep='\n')
     if 0:    
        start_notebooks(toc_files)    
        
     if 0: 
        box_nr_cells(toc_files)
        
     if 0:
        search(all_notebooks,r'keep_plot',notfound=False,silent=0)
        search(toc_files,r'\([A-Za-z-]+\) *=',notfound=False,silent=0)
        search(toc_files,r'\([A-Za-z-]+\) *=',notfound=False,silent=0,printmatch=1)
        search(toc_files,r'\([ A-Za-z-]+\) =',notfound=False,silent=0)
        search(toc_files,r'mul100',notfound=False,silent=0,printmatch=0)
        search(toc_files,r'{index} single: \[\] *',notfound=False,silent=0,printmatch=1,showfiles=False)
        search([r'mfbook\content\07_MoreFeatures\ModelFlowCommandReference.ipynb'],'../howto/attribution/',notfound=False,silent=0)
        search([Path(r'mfbook\content\06_ModelAnalytics\AttributionSomeFeatures.ipynb')],r'{index}single:Impact',notfound=False,silent=0)
        
        #%% search and replace 
        x = search(toc_files,r'```{index}(.*)\n```',replace=r':::{index}\1\n:::',
               notfound=False,silent=0,showfiles=False,printmatch=1,savecell=1)
        y = search(toc_files,r'\{cite:p\}',replace='{cite:t}',
               notfound=False,silent=0,showfiles=False,printmatch=1,savecell=1)
        
        
#%%
     if 0:
        toc_test = [toc_files[1]]
        insert_colab(toc_test)
    
    # hide_cells(toc_files)
    
    
