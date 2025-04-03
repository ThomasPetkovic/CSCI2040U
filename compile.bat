pip install pyinstaller
pyinstaller --onefile --windowed --name "CatalogManagementSystem" --add-data "back.py;." --add-data "*.csv;." front_end.py

REM Copy all CSV files to the dist\ directory
for %%f in (*.csv) do copy %%f dist\

echo "Finished compile script"
dist\CatalogManagementSystem.exe
