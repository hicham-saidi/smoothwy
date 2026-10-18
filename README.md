# File Converter

Cross-platform (Windows, macOS, Linux) file converter. Python + CustomTkinter + Pillow.

## Run
```
pip install -r requirements.txt
python main.py
```
Linux only: if Tk is missing, `sudo apt install python3-tk`.

## Structure
```
main.py                   starts the app
ui/app.py                 window (generic, no file-type logic)
converters/base.py        BaseConverter + ConversionOptions
converters/__init__.py    auto-discovers converters
converters/jpg_to_png.py  JPG -> PNG
```

## Add a new file type
1. Create `converters/<something>.py`
2. Subclass `BaseConverter`, set `name`, `source_extensions`, `target_extension`, implement `convert()`
3. Restart the app. It appears in the dropdown automatically.

## Roadmap
PNG→JPG, image→PDF, SVG, resize controls in the UI (the `resize_percent` and
`max_dimensions` options already exist in `ConversionOptions`), drag & drop,
packaging with PyInstaller.
