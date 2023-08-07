import os
import re

def edit_html_file(file_path):
    # Read the content of the .html file
    with open(file_path, 'r') as html_file:
        content = html_file.read()

    # Check if the corresponding .txt file exists and has <= 10 lines of text
    txt_file_path = file_path.replace('.html', '.txt')
    if os.path.exists(txt_file_path):
        with open(txt_file_path, 'r') as txt_file:
            lines = txt_file.readlines()
        if len(lines) <= 10:
            # Add "img only" to the first <h1> element
            content = re.sub(r'<h1>', r'<h1>img only ', content)

    # Write the modified content back to the .html file
    with open(file_path, 'w') as html_file:
        html_file.write(content)

if __name__ == "__main__":
    folder_path = "./recipes/output/"  # Replace with the actual folder path

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.html'):
            file_path = os.path.join(folder_path, file_name)
            edit_html_file(file_path)
