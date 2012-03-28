@echo off
set PYTHONPATH=%cd%\src
python -m unittest discover -v -s test
