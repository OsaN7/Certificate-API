from certificate_issuing_service_cursor.main import generate_certificates_from_file, CertificateConfig

class CertificateService:
    def generate_certificates(self, config: CertificateConfig, csv_path: str):
        return generate_certificates_from_file(csv_path, config)