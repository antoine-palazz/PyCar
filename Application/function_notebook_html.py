from nbconvert import HTMLExporter
import nbformat
import sys
import os 


cwd=os.getcwd()
cwd_parent=(os.path.dirname(cwd))
sys.path.append(cwd_parent)

def notebook_to_html(notebook_path):
    with open(notebook_path) as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)
    html_exporter = HTMLExporter()
    html_output, _ = html_exporter.from_notebook_node(notebook_content)
    return html_output

notebook_path = 'notebooks/EDA.ipynb'
html_content = notebook_to_html(notebook_path)

with open('Application/templates/EDA_html.html', 'w') as output_file:
    output_file.write(html_content)
