from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import pythoncom
from worddocument import run_doc_review
import xml.etree.ElementTree as ET
import html
from config import preamble
from copy import deepcopy
import time

def gen_prompt(d):
    xml = f"{generate_xml('assistant_instruction', d)}"

    xml = prettify_xml(xml)
    return xml

def generate_xml(k, v):
    if isinstance(v, str):
        xml = f"<{k}>{html.escape(v)}</{k}>"
    elif isinstance(v, dict):
        xml = f"<{k}>"
        for key, value in v.items():
            xml += generate_xml(key, value)
        xml += f"</{k}>"
    elif isinstance(v, list):
        xml = ""
        for element in v:
            if isinstance(element, dict):
                for sub_k, sub_v in element.items():
                    xml += generate_xml(sub_k, sub_v)
            else:  # If the element is not a dictionary, treat it as a string
                xml += generate_xml(k, element)
    return xml
def prettify_xml(xml_string):
    root = ET.fromstring(xml_string)
    ET.indent(root)
    return ET.tostring(root, encoding="unicode")


app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def handle_upload():
    model_params = {
        "model_name": "",
        "temperature": 0.0,
        "max_tokens": 4096,
        'model_name': request.form.get('model_name'),
    }
    preamble_copy = deepcopy(preamble)
    # Get new guidelines, new attributes, and context from the form
    new_guideline = request.form.get('new_guideline')
    attribute_name = request.form.get('attribute_name')
    attribute_value = request.form.get('attribute_value')
    context = request.form.get('context')

    # Update preamble with the new guidelines, attributes, and context
    if new_guideline:
        preamble_copy['guidelines']['guideline'].append(new_guideline)

    if attribute_name and attribute_value:
        preamble_copy['attributes'].append({attribute_name: attribute_value})

    if context:
        preamble_copy['context'] = context

    rewrite_intensity = request.form.get('rewrite_val')
    preamble_copy['attributes'][0]['Rewrite_Intensity'] = rewrite_intensity
    preamble_copy = gen_prompt(preamble_copy)
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400
    UPLOAD_FOLDER = 'uploads'

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    OUTPUT_FOLDER = 'output'

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    if file:
        now = time.time()
        filename = secure_filename(file.filename)
        input_path = Path(f'uploads/{filename}')
        output_path = Path(f'output/{now}_{filename}')

        file.save(str(input_path))
        pythoncom.CoInitialize()
        try:
            run_doc_review(input_path, output_path, model_params, preamble_copy)
        finally:
            pythoncom.CoUninitialize()

        input_path.unlink()

        return jsonify({"filename": output_path.name})

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_file(f'output/{filename}')

if __name__ == '__main__':
    app.run(debug=True)
