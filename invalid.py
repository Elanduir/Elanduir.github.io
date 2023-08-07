import os

def add_invalid_script_to_h1(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()

    script_tag_present = '<script' in html_content
    h1_index = html_content.find('<h1>')

    if not script_tag_present and h1_index != -1:
        h1_end_index = html_content.find('</h1>', h1_index)
        h1_element = html_content[h1_index:h1_end_index + 5]  # 5 accounts for the length of </h1>
        modified_content = html_content.replace(h1_element, '<h1>invalid script ' + h1_element[4:])
        
        with open(file_path, 'w') as file:
            file.write(modified_content)

def process_html_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            add_invalid_script_to_h1(file_path)

if __name__ == "__main__":
    folder_path = "./recipes/outputBatch2/"  # Replace this with the actual folder path containing .html files
    process_html_files(folder_path)

