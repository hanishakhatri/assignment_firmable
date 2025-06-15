import zipfile
import os

def extract_zip(zip_path, extract_to_folder):
    """Extract a single zip file to a folder."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)
        print(f"Extracted: {zip_path} → {extract_to_folder}")

def extract_all_zips(source_folder, extract_root_folder):
    """Extract all zip files in a folder."""
    for filename in os.listdir(source_folder):
        if filename.endswith('.zip'):
            zip_path = os.path.join(source_folder, filename)
            extract_folder = os.path.join(extract_root_folder, filename.replace('.zip', ''))
            os.makedirs(extract_folder, exist_ok=True)
            extract_zip(zip_path, extract_folder)

# Example usage
if __name__ == "__main__":
    zip_folder = "abn_bulk_extract"  # Folder where .zip files are stored
    extract_root = "extracted_abn_zip_files"  # Where to extract files
    extract_all_zips(zip_folder, extract_root)
