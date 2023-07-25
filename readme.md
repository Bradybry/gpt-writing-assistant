# AI Document Reviewer 

This Python script is designed to automate the process of reviewing and editing documents using the Anthropic Claude AI assistant or OpenAI models. It provides a simple web UI using Flask and reads a Word document (.docx), parses it into paragraphs, and then sends each paragraph to Claude for editing based on supplied guidelines. The edited paragraphs are then written back to the document with tracked changes, so you can see what was modified.

## Changes from previous version

- No longer uses GPT-4 function calling abilities. Now works with Anthropic Claude and other OpenAI models that accept free-form text prompts.

- Added a Flask web UI for easier use. Users can now upload documents through a web form rather than running Python scripts directly. 

- Uses a .env file for configuration instead of a config.py file.

## How it works

The script sends each paragraph to Claude along with a provided preamble that gives editing guidelines. Claude's response for each paragraph is compared to the original and diffs are generated using diff_match_patch. The diffs are then applied to the original document XML using lxml.

See the example output included in the /output/ folder.

## Usage

To use the web UI:

1. Clone the repository
2. Install requirements with `pip install -r requirements.txt` 
3. Add your Anthropic API key to the .env file
4. Run `python app.py`
5. Navigate to http://localhost:5000 in your browser
6. Upload a .docx file and add your editing preamble if desired
7. Click "Submit" and view/download the edited file

The Flask app provides a simple interface for uploading files, viewing the diff, and downloading the edited document.

Advanced users can also run edit_document.py directly with their own input/output paths and parameters.

## Requirements

This script requires the following Python libraries:

- pathlib 
- tqdm  
- lxml
- uuid
- re
- zipfile
- diff_match_patch
- typing
- os
- flask
- python-dotenv

You also need an API key for Anthropic Claude, set in the .env file as `CLAUDE_API_KEY`.

## Caveats

- Formatting can get messed up when applying track changes, especially with complex documents.
- Images and some advanced formatting may get lost.
- Currently only supports .docx files.

Please use carefully and verify outputs! The AI is not perfect and may make unwanted changes.

## Next Steps

Potential improvements:

- Better handling of formatting to maintain docx integrity 
- Support for other file types besides .docx
- More robust diffing/patching
- Additional UI polish
- Tests!

Let me know if you have any other questions!