# Ali Sever - Heron Coding Challenge - File Classifier


## Running the app
1. Clone the repository:
    ```shell
    git clone <repository_url>
    cd join-the-siege
    ```

2. Install dependencies:
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
   
3. Install additional dependencies:
   
    Tesseract is required for OCR functionality. Installation instructions vary by OS:
   
    For Ubuntu, you can use:
    ```shell
    sudo apt-get install tesseract-ocr 
    ```
    For Windows users, you can download the installer from the official Tesseract GitHub repository:
    https://github.com/UB-Mannheim/tesseract/wiki.

    After installation, make sure to add the Tesseract executable to your system's PATH.

    Update the path in `src/extract_text.py` if necessary.

    python-magic is used for file type detection. https://pypi.org/project/python-magic/
    It requires the `libmagic` library. 
    On Ubuntu:
    ```shell
    sudo apt-get install libmagic1
    ```
    On Windows:
    ```shell
    pip install python-magic-bin
    ```

4. Run the Flask app:
    ```shell
    python -m src.app
    ```

5. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
    ```
   
### Running the tests
   ```shell
    pytest
   ```

# Approach
* Added Ruff as a linter, using a list of rules that I find useful for Python development. 
* I fixed most of the issues it found, which improved the readability of the code, and removed some
    rules that I found unnecessary for this project.
* Added RapidFuzz for fuzzy string matching. I used fuzzy matching to inspect the file names, which
    gave better results that string matching.
* Added mimetype detection using python-magic. Based on the mimetype, I used different methods 
    to extract text from the files. If the file is a scanned PDF, I used OCR to extract the text.
* Added support for docx files. 
* I generated some dummy files to test the classifier. I used a mix of file types, including scanned PDFs, 
    images and word documents. I wrote plenty of tests to ensure that the classifier works as expected.
* Added a list of matched keywords for each document type. The list is not exhaustive, but it covers the most common
    keywords that come to mind.
* Added the passport class as a new document type. This was fairly straightforward since the implementation
    does not really depend on the document class.
* Added a list of TODOs where the application can be improved, given more time.


# Ideas for improvement
* Obtain/generate files to train on and implement a machine learning model to classify the files.
* Dockerise the application. Make sure to include the Tesseract OCR installation and libmagic.
  * I chose not to add CI/CD now because of the complexity of installing the additional dependencies.
* Determine other file classes to identify and add them to the classifier.
  * With the ML model approach, this would be easier to implement. 
* Pre-commit hooks to run the linter and tests before committing.
* More logging and error handling, depending on the use cases.
  * I've added some logging when a file cannot be classified, but that can be expanded.