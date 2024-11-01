@echo off
if not defined venv_path (
    set venv_path=D:\ProgramData\Miniconda3\envs\ocrmypdf_env\
)

if not defined tesseract_path (
    set tesseract_path=E:\OpenSources\ScreenPinKit\deps\Tesseract-OCR
)
set path=%venv_path%;%venv_path%\Scripts;%tesseract_path%;%path%

ocrmypdf.exe -l chi_sim --skip-text --jobs 4 --output-type pdfa %1 %2