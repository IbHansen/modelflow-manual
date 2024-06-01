# conf.py

# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'My Jupyter Book'
author = 'Author Name'

# -- General configuration ---------------------------------------------------

extensions = [
    # List your extensions here
]

# -- Options for LaTeX output ------------------------------------------------

latex_show_pagerefs = True  # Enable page references in LaTeX output

latex_elements = {
    'preamble': r'''
        \usepackage{booktabs}
        % Additional LaTeX customization can be added here
    '''
    'latex_table_style' :['booktabs', 'colorrows']
}
