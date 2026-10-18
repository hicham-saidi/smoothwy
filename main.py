"""
Entry point of the project.

Run with:  python main.py

Layout of the project
---------------------
main.py                  -> starts the app (this file)
ui/app.py                -> the window; knows nothing about specific file types
converters/base.py       -> the contract every converter follows
converters/__init__.py   -> auto-discovers every converter in this folder
converters/jpg_to_png.py -> one file per conversion type
"""
from ui.app import ConverterApp


def main() -> None:
    app = ConverterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
