import fitz  # PyMuPDF
import os
import csv
import shutil

def clean_output_directory(directory):
    """Clean the output directory before generating new certificates."""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    print(f"Cleaned output directory: {directory}")

    
def add_name_centered(input_pdf, output_pdf, name, font_path, y=325, font_size=48):
    try:
        doc = fitz.open(input_pdf)
        page = doc[0]
        page_width = page.rect.width

        # Register Shelley Script font with a string alias
        font_alias = "shelley_script"
        page.insert_font(fontname=font_alias, fontfile=font_path)
        font = fitz.Font(fontfile=font_path)
        
        # Calculate text dimensions
        text_width = font.text_length(name, fontsize=font_size)
        
        # Calculate center position
        x = (page_width - text_width) / 2
        
        # Add text with exact coordinates
        page.insert_text(
            (x, y), 
            name,
            fontname=font_alias,
            fontsize=font_size,
            color=(0, 0, 0)
        )

        # Save the modified PDF
        doc.save(output_pdf)
        doc.close()
        print(f"Certificate generated successfully: {output_pdf}")
        return True
    except Exception as e:
        print(f"Error generating certificate for {name}: {str(e)}")
        return False

def generate_certificates_from_csv(csv_path, template, font_path, y=325, font_size=48):
    try:
        # Validate input files
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        if not os.path.exists(template):
            raise FileNotFoundError(f"Template PDF not found: {template}")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        # Clean and create output directory
        output_dir = 'certificates'
        clean_output_directory(output_dir)

        # Read CSV file
        successful = 0
        failed = 0
        total = 0
        failed_certificates = []  # List to track failed certificates

        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for idx, row in enumerate(csv_reader, 1):
                total += 1
                name = str(row['name']).strip()
                if not name or name == 'nan':  # Skip empty names or NaN values
                    print(f"Skipping invalid name at row {idx}")
                    failed += 1
                    failed_certificates.append(f"Row {idx}: Empty or invalid name")
                    continue

                # Get date from Column 1 and format it
                date = str(row['Column 1']).strip()
                if date == 'nan' or not date:
                    print(f"Skipping row {idx} due to missing date")
                    failed += 1
                    failed_certificates.append(f"Row {idx}: Missing date for {name}")
                    continue
                    
                # Format date: replace slashes with hyphens and remove time
                formatted_date = date.split()[0].replace('/', '-')
                # Format name: replace spaces with underscores
                formatted_name = name.replace(' ', '_')
                
                # Create filename with formatted date and name
                output = os.path.join(output_dir, f"{formatted_date}_{formatted_name}.pdf")
                
                if add_name_centered(
                    input_pdf=template,
                    output_pdf=output,
                    name=name,
                    font_path=font_path,
                    y=y,
                    font_size=font_size
                ):
                    successful += 1
                else:
                    failed += 1
                    failed_certificates.append(f"Row {idx}: Failed to generate certificate for {name}")

                # Print progress
                if idx % 10 == 0 or idx == total:
                    print(f"Progress: {idx}/{total} certificates processed")

        print(f"\nCertificate generation completed:")
        print(f"Successfully generated: {successful}")
        print(f"Failed: {failed}")
        print(f"Total processed: {total}")
        
        if failed_certificates:
            print("\nFailed Certificates:")
            for error in failed_certificates:
                print(f"- {error}")

    except Exception as e:
        print(f"Error in certificate generation: {str(e)}")
        raise

if __name__ == '__main__':
    template = "PNC Certificate - BCA Project Report Writing.pdf"  # Template name
    font_path = "Shelley_Script.otf"
    csv_file = "BCA Project Report - Form Responses.csv"
    
    try:
        generate_certificates_from_csv(csv_file, template, font_path, y=325, font_size=48)
    except Exception as e:
        print(f"Program failed: {str(e)}")




 
