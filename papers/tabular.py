import re

def modify_latex_file_tabularx(input_file, output_file):
    with open(input_file, 'r') as file:
        startlatex = file.read()
    newlatex = modify_latex_tabularx(startlatex)    
    with open(output_file, 'w') as file:
        file.write(newlatex)



def modify_latex_tabularx(latex_source):
    """
Modifies LaTeX tabularx environments in the provided text.

This function processes the LaTeX text, finds and comments out
tabularx environments, and converts tabulary environments back
to tabularx.

Args:
    latex_source (str): The input LaTeX text.

Returns:
    str: The modified LaTeX text with tabularx changes.
"""

    lines= latex_source.split('\n')

    # Pattern to match the line starting with \textbackslash{}begin{tabularx}
    tabularx_pattern = re.compile(r"^\\textbackslash\{\}begin\\\{tabularx")
                                #      \textbackslash{}begin\{tabularx\}\{\textbackslash{}textwidth\}\{>\{\textbackslash{}raggedright\textbackslash{}arraybackslash\}p\{3cm\}>\{\textbackslash{}raggedright\textbackslash{}arraybackslash\}p\{4cm\}>\{\textbackslash{}raggedright\textbackslash{}arraybackslash\}X\}

    # Function to unescape LaTeX text
    def unescape_latex(text):
        return text.replace('\\textbackslash{}', '\\').replace('\{', '{').replace('\}', '}')

    # Find and replace patterns
    modified_lines = []
    tabularx_line = None

    for line in lines:
        # Check if the line matches the tabularx pattern
        if tabularx_pattern.match(line.strip()):
            print(f'Hit {line.strip()}=')
            tabularx_line = unescape_latex(line.strip())
            modified_lines.append(f"% {line.strip()}\n")  # Comment out the original tabularx line
        elif line.strip().startswith(r'\begin{tabulary}') and tabularx_line:
            modified_lines.append(f"{tabularx_line}\n")
        elif line.strip().startswith(r'\end{tabulary}') and tabularx_line:
            modified_lines.append(r'\end{tabularx}'+'\n')
            tabularx_line = None
        else:
            modified_lines.append(line)
            
    return '\n'.join(modified_lines)        


# Example usage
input_file = r'mfbook\_build\latex\MFModinModelflow.tex'
output_file = r'mfbook\_build/latex/MFModinModelflowtab.tex'
modify_latex_file_tabularx(input_file, output_file)
