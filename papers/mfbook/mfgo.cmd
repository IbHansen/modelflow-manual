rem This cmd file starts jupyter notebook in the replication enviorement
rem activate conda
call %USERPROFILE%\miniconda3\Scripts\activate.bat %USERPROFILE%\miniconda3 
call conda activate modelflow_replicate
call jupyter notebook content\Overview.ipynb
