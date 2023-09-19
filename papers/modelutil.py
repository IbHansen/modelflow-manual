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

import re
 
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
 



def get_all_files(fileloc=bookdir):
    all_notebooks = glob(f"{fileloc}/content/**/*.ipynb", recursive=True)
    return all_notebooks 

def get_all_notebooks(fileloc=bookdir):
    '''get all notebooks in the fileloc book'''
    all_notebooks = list(Path(f'{fileloc}/content').glob('**/*.ipynb'))
    relevant_notebooks = [f for f in all_notebooks if not '.ipynb_checkpoints' in f.parts]
    return relevant_notebooks 



def get_toc_files(fileloc=bookdir):
    '''Get all files mentioned in the _toc but not the root'''
    with open(Path(fr'{fileloc}/_toc.yml'), 'r') as f:
        toc_data = yaml.safe_load(f)

    # breakpoint() 
    
    
    file_list_with_chapter = []
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
                    file_list_with_chapter.append((filename,chapter_nr))
                else:   
                    file_list_with_chapter.append((filename,-1))

            if 'chapters' in entry:
                process_toc_entries(entry['chapters'])
            if 'sections' in entry:
                process_toc_entries(entry['sections'])
        # breakpoint() 

    file_list_with_chapter.append((make_file_path(toc_data['root']),0))
    process_toc_entries(toc_data.get('parts', []))
     # Print the list of file paths
     
    # for file_path in file_list:
    #     print(file_path)
    
    
    notebook_paths_with_chapter = [ (f,nr) 
                               for f,nr in file_list_with_chapter]
    notebook_paths = [f for f,c in notebook_paths_with_chapter ]

    return notebook_paths ,notebook_paths_with_chapter   

def start_notebooks(notebook_list):
    ''' start all notebooks in jupyter in the notebook list '''
    base_url = "http://localhost:8888/notebooks/"

    for notebook_path in notebook_list:
        url = base_url + str(notebook_path)
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

def box_nr_cells(notebook_list_with_chapter):
    
    running_nr = 0 
    box_toc =[]

    def make_box_nr(chapter,text): 
        patbox = r'(:::{index} single: Box.*?\n:::\n*)?:::{[Aa]dmonition} [Bb]ox (\d+)\.(\d) (.*)'

        nonlocal running_nr 
        nonlocal box_toc 
    
        def replace_box(match):
            nonlocal running_nr 
            if 1:
                for idx, group in enumerate(match.groups(), 1):
                    print(f"Group {idx}: {group}")

            lf = '\n'
            running_nr =running_nr + 1
            box_index = f":::{{index}} single: Boxes; {running_nr} {match[4]}{lf}:::"
            box_name = f":::{{admonition}} Box {running_nr} {match[4]}"
            replace   = f"{box_index}{lf}{lf}{box_name}"
            box_toc.append( box_name )
            if 1: print(f'{replace=}')
            return replace 
        
        return re.sub(patbox, replace_box,text)
       
    if 0: 
        text = ':::{admonition} Box 3.1  A good explanation\n42:::'
        text2 = "{admonition} box 1.2 ibs text "

        text2 = ''':::{admonition} Box 1.1 A good explanation
2 + 2  = 4
:::
'''
        replace=':::{index} single: Box; 34.1  A good explanation\n:::\n\n:::{admonition} Box 34.1  A good explanation'

        print(make_box_nr(34, text))
        print(make_box_nr(35, text2))
        print(make_box_nr(40, replace))
        
        assert 1==2
#%%
    for ipath,chapter in notebook_list_with_chapter:
        # breakpoint() 
        try:
            ntbk = nbf.read(ipath, nbf.NO_CONVERT)
            changed = False
            for cell in ntbk.cells:
                    # breakpoint() 
                    if (newsource := make_box_nr(chapter,  cell['source'])):
                        if newsource != cell['source'] :
                            changed = True 
                            # print(f'box change {ipath=} \n{newsource=}')    
                            cell['source'] = newsource 
        
            if changed:             
                # nbf.write(ntbk, ipath)
                print(f'notebook written {ipath}')
            else: 
                print(f'notebook not changed by box numbering   : {ipath}')
        except: 
                print(f'Hide did not work for this file : {ipath}')
        
    print('\n boxes in the book',*box_toc,sep='\n')        
    return 

 #%% Search

def search(notebook_list_with_chapter,pat=r'.*[Bb]ox.*'):
    
    for ipath,chapter in notebook_list_with_chapter:
        try:

            ntbk = nbf.read(ipath, nbf.NO_CONVERT)
            for cell in ntbk.cells:
                    # breakpoint() 
                    source =  cell['source']
                    matches = re.findall(pat, source)
                    if len(matches):
                        ...
                        # breakpoint()
                    for m in matches: 
                            print(f"pat here: {'/'.join(ipath.parts[-2:])} : {m}")    
        except: 
                print(f'Search did not work for this file : {ipath}')
        

def insert_colab(notebook_list_with_chapter):
    content="""\
# HIDDEN in jupyterbook 
#This is code to manage dependencies if the notebook is executed in the google colab cloud service
if 'google.colab' in str(get_ipython()):
  import os
  os.system('apt -qqq install graphviz')
  os.system('pip -qqq install ModelFlowIb ipysheet  --no-dependencies ')
  incolab = True  
else:
  incolab = False 

%load_ext autoreload
%autoreload 2
"""  

    for ipath,chapter in notebook_list_with_chapter:
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
                    nbf.write(ntbk, f)
                    
                print(f'Notebook written {"/".join(ipath.parts[-2:])}')

    
        except: 
                print(f'Search colab did not work for this file : {ipath}')
        


            
# Call the function to start the notebooks
# start_notebooks(notebook_list)



toc_files,toc_files_with_chapter = get_toc_files()
all_notebooks = get_all_notebooks()

if 'open' in options:
        start_notebooks(toc_files)    


if 'list' in options:    
#%%    
    for name,chapter in toc_files_with_chapter:
        print(f'Chapter: {chapter} notebook: {name} ')
#%%
if 'hide_cells' in options:  
    hide_cells(toc_files)   
    
    
if  'boxes' in options:    
    box_nr_cells(toc_files_with_chapter)

    
    
if 'help' in options or len(options) ==1:  
    print('''Run with python modelutil.py <options>
    options: 
        open       : will open all files in the jupyterbook (a jupyter instance with port 8888 should be open)
        list       : will list all files in the jupyterbook 
        hide_cells : in all NB metadata will be set based on #HIDDEN #NO CODE #HIDE CODE   
        boxes      : will renumber boxes and place them in the index 
          '''   )
    

    
if __name__ == '__main__':

    toc_files,toc_files_with_chapter = get_toc_files()
    all_notebooks = get_all_notebooks()

    if 0: 
        for name,chapter in toc_files_with_chapter:
            print(f'Chapter: {chapter} notebook: {name}')
    if 0:    
        start_notebooks(toc_files)    
        
    if 1: 
        box_nr_cells(toc_files_with_chapter)
        
    if 0:
        pat = '''load_ext autoreload'''

        search(toc_files_with_chapter,pat)

    if 0:
        toc_test = [toc_files_with_chapter[1]]
        insert_colab(toc_test)

    # hide_cells(toc_files)
    
    #%% 