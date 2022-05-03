# Build Python application
Some files in package opencc should be added manually when using pyinstaller.
- s2t.json
- STCharacters.txt
- STPhrases.txt

## Build
``pyinstaller --onefile  main.py --add-binary ./opencc_missing_file/s2t.json;opencc/config --add-binary ./opencc_missing_file/STPhrases.txt;opencc/dictionary --add-binary ./opencc_missing_file/STCharacters.txt;opencc/dictionary``



