# AI Document Reviewer

This Python script is designed to automate the process of reviewing and editing documents using the OpenAI GPT-4 model. It reads a Word document (.docx), parses it into paragraphs, and then sends each paragraph to the GPT-4 model for editing based on supplied guidelines. The edited paragraphs are then written back to the document with tracked changes, so you can see what was modified.

The script leverages the new function calling capabilities from OpenAI for generating structured output that is more easy to use in the rest of the system.

Note: This system is not perfect. Some advanced formatting in word gets messed up when applying the track changes. However, it works well for documents with simple consistent formatting. It was hard enough getting the track changes to work in the first place.

## How it works

The script uses the `openai.ChatCompletion.create` function to generate a response from the GPT-4 model for each paragraph in the document. It also makes use of `lxml` for parsing and modifying the Word document XML, and `diff_match_patch` for generating diffs between the original and edited paragraphs.

See the example output included in the /output/ folder.

## Usage

To use this script, you need to provide the path to the Word document you want to edit, the output path for the edited document, and the model parameters. The model parameters should be a dictionary with the following keys: `temperature`, `frequency_penalty`, `presence_penalty`, `n`, and `max_tokens`.

You also need to provide a preamble that sets the guidelines for the editing. This should be a string that will be sent to the GPT-4 model before each paragraph. The preamble can be loaded from a text file.

You can also optionally run a VBA macro on the edited document after it's saved. This is useful for applying formatting changes, such as converting Markdown to Word formatting. The VBA for this macro is included, however it does require that the user has word installed and all macros enabled. The default behaviour does not reformat. I'm currenly looking for a way to accomplish this in a simpler pythong only manner. Any insight would be appreciated.

Here is an example of how to use the script:

```python
model_params = {
    "temperature": 0.00,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "n": 1,
    "max_tokens": 4096
}
preamble = open('./preamble.txt', 'r').read()

run_doc_review(
    input_path="./uploads/document.docx",
    output_path="./output/document.docx",
    model_params=model_params,
    preamble=preamble
)
```

## Requirements

This script requires the following Python libraries: `pathlib`, `tqdm`, `lxml`, `uuid`, `re`, `zipfile`, `diff_match_patch`, `typing`, `os`, `win32com.client`, `openai`, `json`.

You also need to have the OpenAI API key set in a `config.py` file:

```python
OPENAI_API_KEY = "your_openai_api_key"
```

Please note that usage of the OpenAI API is subject to usage fees.