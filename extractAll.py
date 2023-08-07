import os
import subprocess
import openai

def extract_text(pdf_path, output_path):
    command = ["pdftotext", "-layout", pdf_path, output_path]
    subprocess.run(command, check=True)

def extract_images(pdf_path, output_folder):
    command = ["pdfimages", "-png", pdf_path, os.path.join(output_folder, "image")]
    subprocess.run(command, check=True)

def process_pdf(pdf_path, output_folder):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    text_output_path = os.path.join(output_folder, f"{pdf_name}.txt")
    image_output_folder = os.path.join(output_folder, pdf_name)

    if not os.path.exists(image_output_folder):
        os.makedirs(image_output_folder)

    extract_text(pdf_path, text_output_path)
    extract_images(pdf_path, image_output_folder)

    return text_output_path, [os.path.join(image_output_folder, image_file) for image_file in os.listdir(image_output_folder)]

def send_request(prompt):
    openai.api_key = "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"
    completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                    }
                ]
            )
    return completion.choices[0].message

def create_index_html(folder_path, output_file):
    # List all HTML files in the folder
    html_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.html')]

    # Sort the file names alphabetically
    html_files.sort()

    with open(output_file, 'w') as index_file:
        index_file.write('<html>\n')
        index_file.write('<head>\n')
        index_file.write('<title>Index</title>\n')
        index_file.write('</head>\n')
        index_file.write('<body>\n')
        for html_file in html_files:
            file_path = os.path.join(folder_path, html_file)
            link_path = os.path.join(".", folder_path, html_file)
            index_file.write(f'<a href="{link_path}">{html_file}</a><br>\n')
        index_file.write('</body>\n')
        index_file.write('</html>\n')


def main(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extracted_data = []

    for filename in os.listdir(input_folder):
        print("processing: " + filename)
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            text_output_path, image_paths = process_pdf(pdf_path, output_folder)
            for i in range(len(image_paths)):
                p = image_paths[i]
                image_paths[i] = "." + p.replace(output_folder, "")
            extracted_data.append({"pdf_name": filename, "text_path": text_output_path, "image_paths": image_paths})

    # Print the extracted data to the console
    for data in extracted_data:
        textPrompt = f"Create a static html for the following recipe in german supporting the schema.org/recipe standard using these images {data['image_paths']} as showcase linking them also in the html also categorize it correctly: "
        recipe = ("").join(open(data['text_path']).readlines())
        try: 
            response = send_request(textPrompt + recipe)
            html = response["content"]
            htmlPath = data['text_path'][:-4] + ".html"
            with open(htmlPath, 'w') as outfile:
                outfile.write(html)
        except Exception as e:
             print(f"Caught an exception: {e}")
        print("completed: " + filename)

    folder_path = "./recipes/output"
    output_file = "index.html"
    create_index_html(folder_path, output_file)


if __name__ == "__main__":
    input_folder = "./recipes"
    output_folder = "./recipes/output"
    main(input_folder, output_folder)

