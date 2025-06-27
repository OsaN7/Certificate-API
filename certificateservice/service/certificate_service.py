from certificateservice.service.certificateutil import CertificateConfig
from scripts.generate_certificates import generate_certificates_from_file


# TODO  Add repo and all necessary methods to handle certificate generation
class CertificateService:
    def __init__(self):
        pass

    def generate_certificates(self, config: CertificateConfig, csv_path: str):
        return generate_certificates_from_file(csv_path, config)
