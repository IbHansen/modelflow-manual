@echo off
rem Run the shared launcher for this book, from this folder.
rem   book          start the live server on localhost:3000
rem   book copy     build static HTML into C:\IbHansen.github.io\<this folder>
rem   book pdf      build a PDF into .\exports\pdf
rem   book md       build a markdown version into .\exports\md
cd /d "%~dp0"
call C:\books\start_book.bat %*
