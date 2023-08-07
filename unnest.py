import os
import shutil

def extract_pdfs(src_dir, dest_dir):
    for root, _, files in os.walk(src_dir):
        for filename in files:
            if filename.endswith(".pdf"):
                src_path = os.path.join(root, filename)
                dest_path = os.path.join(dest_dir, filename)
                shutil.move(src_path, dest_path)

if __name__ == "__main__":
    src_directory = "./recipesRAW"
    dest_directory = "./recipes"

    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    extract_pdfs(src_directory, dest_directory)
