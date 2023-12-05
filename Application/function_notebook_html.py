from nbconvert import HTMLExporter
import nbformat
import sys
directory = '/Users/augustincablant/Documents/GitHub/Pycar'
sys.path.append(directory)

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
