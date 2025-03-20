pip install pyinstaller
pyinstaller --onefile --windowed --name "CatalogManagementSystem" --add-data "back.py;." --add-data "register.csv;." --add-data "test.csv;." front_end.py
copy test.csv dist\
echo "Finished compile script"