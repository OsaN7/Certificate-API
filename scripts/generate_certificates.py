"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 27/06/2025
"""
from traceback import print_exc

from certificateservice.service.certificateutil import Placeholder, Point, CertificateConfig, read_csv, \
    generate_certificates


def generate_certificates_from_file(csv_path, config: CertificateConfig):
    try:
        df = read_csv(csv_path)
        df = generate_certificates(df, config)
        return df
    except Exception as e:
        print_exc()
        raise


def bca_project_report_writing_webinar_example():
    template = "data/templates/PNC Certificate-BCA Project Report Writing.pdf"
    csv_file = "../../data/BCA Project Report - Form Responses.csv"
    output_dir = "20250517-webinar-bca-project-report"
    output_file_prefix = "20250517-webinar"
    font_file = "../../resources/fonts/Shelley_Script.otf"
    font_size = 55
    placeholders = [
        Placeholder(name="name",
                    value_attribute="name",
                    value=None,
                    tl=Point(x=0, y=320),
                    br=Point(x=0, y=0),
                    color=(0, 0, 0),
                    font_name="Shelley_Script",
                    font_file=font_file,
                    font_size=font_size)
    ]
    certificate_config = CertificateConfig(
        template=template,
        placeholders=placeholders,
        output_dir=output_dir,
        output_file_prefix=output_file_prefix,
        unique_attribute="email"
    )

    try:
        generate_certificates_from_file(csv_file, config=certificate_config)
    except Exception as e:
        print(f"Program failed: {str(e)}")


def csit_internship_report_writing_webinar():
    template = "data/templates/PNC Certificate-B.Sc.CSIT Internship Report Writing.pdf"
    csv_file = "../../data/PNC Webinar BSC Internship Report Writing.csv"
    output_dir = "20250510-webinar-csit-internship-report"
    output_file_prefix = "20250510-webinar"
    font_file = "../../resources/fonts/Shelley_Script.otf"
    font_size = 55
    placeholders = [
        Placeholder(name="name",
                    value_attribute="name",
                    value=None,
                    tl=Point(x=0, y=320),
                    br=Point(x=0, y=0),
                    color=(0, 0, 0),
                    font_name="Shelley_Script",
                    font_file=font_file,
                    font_size=font_size)
    ]
    certificate_config = CertificateConfig(
        template=template,
        placeholders=placeholders,
        output_dir=output_dir,
        output_file_prefix=output_file_prefix,
        unique_attribute="email"
    )

    try:
        generate_certificates_from_file(csv_file, config=certificate_config)
    except Exception as e:
        print(f"Program failed: {str(e)}")


if __name__ == '__main__':
    csit_internship_report_writing_webinar()
    bca_project_report_writing_webinar_example()
