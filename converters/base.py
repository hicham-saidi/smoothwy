"""The contract every converter must follow."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConversionOptions:
    """Options shared by all converters. Add new fields here as features grow
    (quality, target file size, DPI, ...). Converters ignore what they don't use."""
    output_dir: Path | None = None        # None -> save next to the source file
    resize_percent: int | None = None     # e.g. 50 -> half the width and height
    max_dimensions: tuple[int, int] | None = None  # (width, height) cap
    overwrite: bool = False


class BaseConverter(ABC):
    #: Label shown in the UI, e.g. "JPG → PNG"
    name: str = ""
    #: Accepted input extensions, lowercase, with dot
    source_extensions: tuple[str, ...] = ()
    #: Extension of the produced file, with dot
    target_extension: str = ""

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.source_extensions

    def build_output_path(self, source: Path, options: ConversionOptions) -> Path:
        folder = options.output_dir or source.parent
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / (source.stem + self.target_extension)
        if options.overwrite:
            return target
        counter = 1
        while target.exists():  # never silently replace a file
            target = folder / f"{source.stem} ({counter}){self.target_extension}"
            counter += 1
        return target

    @abstractmethod
    def convert(self, source: Path, options: ConversionOptions) -> Path:
        """Convert `source` and return the path of the new file."""
