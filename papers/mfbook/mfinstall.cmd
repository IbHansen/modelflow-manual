rem This cmd file installs modelflow for the replication 
rem of the ModelFlow/MFMod manual 
rem in the end it starts up an jupyter notebook which lists all 
rem  notebooks from the manual 
rem 
IF NOT EXIST "%USERPROFILE%\miniconda3" (
    curl -L "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" --output %temp%\miniconda.exe
    %temp%\miniconda.exe /S /D=%USERPROFILE%\miniconda3
) 
rem activate conda
call %USERPROFILE%\miniconda3\Scripts\activate.bat %USERPROFILE%\miniconda3 

rem Install modelflow
call conda create -n modelflow_replicate -c ibh -c  conda-forge modelflow_stable312 -y

call conda activate modelflow_replicate
pip install dash_interactive_graphviz
jupyter contrib nbextension install --user
jupyter nbextension enable toc2/main
jupyter nbextension enable hide_input_all/main
jupyter nbextension enable splitcell/splitcell
jupyter nbextension enable varInspector/main

call jupyter notebook content\Overview.ipynb
