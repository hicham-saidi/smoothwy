"""JPG -> PNG."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

from .base import BaseConverter, ConversionOptions


class JpgToPng(BaseConverter):
    name = "JPG → PNG"
    source_extensions = (".jpg", ".jpeg")
    target_extension = ".png"

    def convert(self, source: Path, options: ConversionOptions) -> Path:
        output = self.build_output_path(source, options)
        with Image.open(source) as img:
            img = ImageOps.exif_transpose(img)  # respect phone-camera rotation

            if options.resize_percent:
                factor = options.resize_percent / 100
                img = img.resize(
                    (max(1, int(img.width * factor)), max(1, int(img.height * factor))),
                    Image.LANCZOS,
                )
            if options.max_dimensions:
                img.thumbnail(options.max_dimensions, Image.LANCZOS)

            img.save(output, format="PNG", optimize=True)
        return output
