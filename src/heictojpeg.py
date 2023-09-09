# https://github.com/NatLee/HEIC2PNG
from PIL import Image
from pathlib import Path
from pillow_heif import register_heif_opener

register_heif_opener()
# TODO: add PNG as a secondary format
class HEIC2JPEG:
    def __init__(self, image_file_path: str, output_directory: str):
        self.image_file_path = Path(image_file_path)
        if self.image_file_path.suffix.lower() != '.heic':
            raise ValueError
        self.output_directory = Path(output_directory)
        # Create output directory
        self.output_directory.mkdir(parents=True, exist_ok=True)
        self.image = Image.open(self.image_file_path)

    def save(self, extension='.jpeg') -> Path:
        output_path = self.output_directory / (self.image_file_path.stem + extension)
        if output_path.exists():
            raise FileExistsError
        self.image.save(output_path)
        return output_path