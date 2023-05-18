# -*- coding: utf-8 -*-
"""
@author: ibhan
"""




# Open and load the _toc.yml file


def get_toc_files(fileloc='mfbook'):
    import yaml
    from pathlib import Path
    
    with open(Path(fr'{fileloc}/_toc.yml'), 'r') as f:
        toc_data = yaml.safe_load(f)

    # breakpoint() 
    
    
    file_list = []
    
    def process_toc_entries(entries):
        for i,entry in enumerate(entries):
            # print(i,entry)
            if 'file' in entry :
                file_list.append(entry['file'])
            if 'chapters' in entry:
                process_toc_entries(entry['chapters'])
            if 'sections' in entry:
                process_toc_entries(entry['sections'])
            if 'root' in entry:
                file_list.append(entry['root'])
    
    process_toc_entries(toc_data.get('parts', []))
     # Print the list of file paths
     
    # for file_path in file_list:
    #     print(file_path)
    
    file_paths = [ Path(fr'{fileloc}/{f}').with_suffix('.ipynb')for f in file_list]
    return file_paths    
import webbrowser

def start_notebooks(notebook_list):
    base_url = "http://localhost:8888/notebooks/"

    for notebook_path in notebook_list:
        url = base_url + str(notebook_path)
        webbrowser.open(url, new=2)

# Specify the list of notebook paths
notebook_list = ["notebook1.ipynb", "notebook2.ipynb", "notebook3.ipynb"]

# Call the function to start the notebooks
# start_notebooks(notebook_list)

if __name__ == '__main__':

    xx = get_toc_files()
    
    for x in xx:
        print(x)
        
    start_notebooks(xx)    
