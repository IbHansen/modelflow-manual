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
    
    def process_toc_entries(entries):
        nonlocal chapter_nr
        for i,entry in enumerate(entries):
            # print(i,entry)
            if 'file' in entry :
                chapter_nr = chapter_nr + 1 
                file_list_with_chapter.append((entry['file'],chapter_nr))
            if 'chapters' in entry:
                process_toc_entries(entry['chapters'])
            if 'sections' in entry:
                process_toc_entries(entry['sections'])
            if 'root' in entry:
                file_list_with_chapter.append((entry['root'],0))

    file_list_with_chapter.append((toc_data['root'],0))
    process_toc_entries(toc_data.get('parts', []))
     # Print the list of file paths
     
    # for file_path in file_list:
    #     print(file_path)
    
    def make_file_path(f):
        f_name  = f if f.endswith('.md') else f+'.ipynb'
        f_path = Path(fr'{fileloc}/{f_name}')
        return f_path
    
    notebook_paths_with_chapter = [ (make_file_path(f),nr) 
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


# Call the function to start the notebooks
# start_notebooks(notebook_list)



toc_files,toc_files_with_chapter = get_toc_files()
all_notebooks = get_all_notebooks()

if 'open' in options:
        start_notebooks(toc_files)    


if 'list' in options:    
#%%    
    for name,chapter in toc_files_with_chapter:
        exist = Path(name).exists()
        note = '' if exist else "Dont exist:"
        print(f' {note} Chapter: {chapter} notebook: {name} ')
#%%
if 'hide_cells' in options:  
    hide_cells(toc_files)   
    
    
if 'help' in options or len(options) ==1:  
    print('''Run with python modelutil.py <options>
    options: 
        open       : will open all files in the jupyterbook (a jupyter instance with port 8888 should be open)
        list       : will list all files in the jupyterbook 
        hide_cells : in all NB metadata will be set based on #HIDDEN #NO CODE #HIDE CODE   
          '''   )
    

    
if __name__ == '__main__':

    if 0: 
        for name,chapter in toc_files_with_chapter:
            print(f'Chapter: {chapter} notebook: {name}')
    if 0:    
        start_notebooks(toc_files)    
    
    # hide_cells(toc_files)
    
    
    