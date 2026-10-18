"""Main window. Generic: it works with any converter found in /converters."""
from __future__ import annotations

import threading
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from converters import ConversionOptions, get_converters

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class ConverterApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("File Converter")
        self.geometry("620x560")
        self.minsize(520, 480)

        self.converters = get_converters()
        self.files: list[Path] = []
        self.output_dir: Path | None = None

        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header: choose conversion type
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 8))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Convert files",
                     font=ctk.CTkFont(size=26, weight="bold")).grid(row=0, column=0, sticky="w")
        self.type_menu = ctk.CTkOptionMenu(header, values=list(self.converters),
                                           command=lambda _: self._clear_files())
        self.type_menu.grid(row=0, column=1, sticky="e")

        # Add files + output folder
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=1, column=0, sticky="ew", padx=24, pady=8)
        ctk.CTkButton(actions, text="Add files", width=110,
                      command=self._pick_files).pack(side="left")
        ctk.CTkButton(actions, text="Output folder", width=110, fg_color="transparent",
                      border_width=1, text_color=("gray10", "gray90"),
                      command=self._pick_output).pack(side="left", padx=8)
        self.output_label = ctk.CTkLabel(actions, text="Saving next to originals",
                                         text_color="gray50")
        self.output_label.pack(side="left", padx=8)

        # File list
        self.file_list = ctk.CTkScrollableFrame(self, label_text="Files")
        self.file_list.grid(row=2, column=0, sticky="nsew", padx=24, pady=8)
        self._refresh_list()

        # Footer: progress + convert
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", padx=24, pady=(8, 24))
        footer.grid_columnconfigure(0, weight=1)
        self.progress = ctk.CTkProgressBar(footer)
        self.progress.set(0)
        self.progress.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self.status = ctk.CTkLabel(footer, text="", anchor="w")
        self.status.grid(row=1, column=0, sticky="w")
        self.convert_btn = ctk.CTkButton(footer, text="Convert", height=40,
                                         command=self._start_conversion)
        self.convert_btn.grid(row=0, column=1, rowspan=2, padx=(16, 0))

    # ------------------------------------------------------------- actions
    @property
    def converter(self):
        return self.converters[self.type_menu.get()]

    def _pick_files(self) -> None:
        exts = " ".join(f"*{e}" for e in self.converter.source_extensions)
        paths = filedialog.askopenfilenames(
            title="Choose files", filetypes=[(self.converter.name, exts)])
        for p in map(Path, paths):
            if p not in self.files and self.converter.can_handle(p):
                self.files.append(p)
        self._refresh_list()

    def _pick_output(self) -> None:
        folder = filedialog.askdirectory(title="Choose output folder")
        if folder:
            self.output_dir = Path(folder)
            self.output_label.configure(text=str(self.output_dir))

    def _clear_files(self) -> None:
        self.files.clear()
        self._refresh_list()

    def _refresh_list(self) -> None:
        for child in self.file_list.winfo_children():
            child.destroy()
        if not self.files:
            ctk.CTkLabel(self.file_list, text="No files yet. Click “Add files”.",
                         text_color="gray50").pack(pady=24)
            return
        for path in self.files:
            ctk.CTkLabel(self.file_list, text=path.name, anchor="w").pack(fill="x", padx=4)

    # ---------------------------------------------------------- conversion
    def _start_conversion(self) -> None:
        if not self.files:
            self.status.configure(text="Add at least one file first.")
            return
        self.convert_btn.configure(state="disabled")
        self.progress.set(0)
        options = ConversionOptions(output_dir=self.output_dir)
        threading.Thread(target=self._run, args=(list(self.files), options),
                         daemon=True).start()

    def _run(self, files: list[Path], options: ConversionOptions) -> None:
        converter, done, failed = self.converter, 0, []
        for i, path in enumerate(files, start=1):
            try:
                converter.convert(path, options)
                done += 1
            except Exception as exc:  # keep going if one file fails
                failed.append(f"{path.name}: {exc}")
            self.after(0, self.progress.set, i / len(files))
        msg = f"Converted {done} of {len(files)} files."
        if failed:
            msg += f" Failed: {failed[0]}"
        self.after(0, self._finish, msg)

    def _finish(self, message: str) -> None:
        self.status.configure(text=message)
        self.convert_btn.configure(state="normal")
