import os
from typing import Optional, List

import fitz  # PyMuPDF
import pandas as pd
from pydantic import BaseModel

from certificateservice.settings import Settings


class Point(BaseModel):
    x: int = 0
    y: int = 0

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


class Placeholder(BaseModel):
    name: Optional[str] = None
    value_attribute: Optional[str] = None
    value: Optional[str] = None
    tl: Point = Point(x=0, y=0)
    br: Point = Point(x=0, y=0)
    color: tuple[int, int, int] = (0, 0, 0)  # RGB color, defaulting to black
    font_name: Optional[str] = "Arial"
    font_file: Optional[str] = None
    font_size: Optional[int] = 11

    def __repr__(self):
        return f"Placeholder(name={self.name}, value_attribute={self.value_attribute}, value={self.value}, tl={self.tl}, br={self.br})"


class CertificateConfig(BaseModel):
    template: Optional[str] = None
    placeholders: List[Placeholder] = []
    output_dir: str = 'certificates'

    output_file_prefix: Optional[str] = None
    unique_attribute: Optional[str] = None

    def __repr__(self):
        return (f"CertificateConfig(template={self.template}, "
                f"placeholders={self.placeholders}, "
                f"output_dir={self.output_dir}, "
                f"output_file_prefix={self.output_file_prefix}, "
                f"unique_attribute={self.unique_attribute})")


def read_csv(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    df = pd.read_csv(csv_path)
    return df


def validate_placeholders(df, placeholders: Optional[List['Placeholder']] = None):
    if placeholders is None:
        return df
    attributes = [p.value_attribute for p in placeholders if p.value_attribute]
    font_files = [p.font_file for p in placeholders if p.font_file]
    for font_file in font_files:
        if not os.path.exists(font_file):
            raise FileNotFoundError(f"Font file not found: {font_file}")

    if not attributes:
        return df
    for attribute in attributes:
        if attribute not in df.columns:
            raise ValueError(f"Attribute '{attribute}' not found in data columns.")

    return df


def makedir(directory: str):
    """Create a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory created: {directory}")
    else:
        print(f"Directory already exists: {directory}")


def _generate_certificate(template, placeholders: List[Placeholder], output_file_path):
    doc = fitz.open(template)
    for page in doc:
        for placeholder in placeholders:
            page_width = page.rect.width

            # Register font with a string alias
            page.insert_font(fontname=placeholder.font_name, fontfile=placeholder.font_file)
            font = fitz.Font(fontfile=placeholder.font_file)

            # Calculate text dimensions
            print(placeholder.value)
            text_width = font.text_length(placeholder.value, fontsize=placeholder.font_size)

            # Calculate center position TODO add inside tl, br
            x = (page_width - text_width) / 2

            # Add text with exact coordinates
            page.insert_text(
                (x, placeholder.tl.y),
                placeholder.value,
                fontname=placeholder.font_name,
                fontsize=placeholder.font_size,
                color=placeholder.color
            )
    doc.save(output_file_path)
    doc.close()
    print(f"Certificate generated successfully: {output_file_path}")
    return output_file_path


def generate_certificate(template, placeholders: List[Placeholder], output_file_path):
    """
    :param template:  template file path
    :param placeholders:  list of Placeholder objects with values filled in
    :param output_file_path:  output file path where the generated certificate will be saved
    :return:  output_file_path
    """
    return _generate_certificate(template, placeholders, output_file_path)


def generate_certificates(df, config: CertificateConfig):
    validate_placeholders(df, config.placeholders)
    output_path = f"{Settings.OUTPUT_BASE_DIR}/{config.output_dir}"
    makedir(output_path)
    config.output_dir = output_path

    if "output_file_url" not in df.columns:
        df["output_file_url"] = None

    for idx, row in df.iterrows():
        if row.isnull().all() or all((pd.isna(x) or x == '') for x in row):
            print(f"Skipping empty row at index {idx}")
            continue

        placeholder_with_values = []
        for _placeholder in config.placeholders or []:
            placeholder = _placeholder.model_copy()
            if placeholder.value is not None:
                placeholder_with_values.append(placeholder)
            else:
                value = row.get(placeholder.value_attribute, None)
                if value is not None:
                    placeholder.value = value
                    placeholder_with_values.append(placeholder)
        filename = ""
        for placeholder in placeholder_with_values:
            if placeholder.value is not None:
                filename += f"{placeholder.value}"
                break
        fileid = row.get(config.unique_attribute, None)
        if fileid is not None:
            filename = f"{fileid}-{filename}"
        if config.output_file_prefix:
            output_filename = f"{config.output_file_prefix}-{filename}.pdf"
        else:
            output_filename = f"{filename}.pdf"

        output_path = os.path.join(config.output_dir, output_filename)

        certificate_path = generate_certificate(config.template, placeholder_with_values, output_file_path=output_path)
        df.at[idx, "output_file_url"] = certificate_path
    certificates_path = f"{config.output_dir}/certificates.csv"
    df.to_csv(certificates_path, index=False)
    return df
