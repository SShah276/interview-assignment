# Project Writeup

## Approach & Assumptions

[Describe your overall approach to solving this problem. What was your thought process? What were the key challenges you identified?]

My initial thought process was to extract text directly from PDFs using libraries such as PyPDF2 or pdfminer.six, which I found were for handling text-based PDFs. However, after inspecting the input files, I realized that the PDFs were either image-based or had poorly encoded text, so a standard parsing approach wouldn't create proper results.

I realized I needed a library to extract from images, which is why there was a need for optical character recognition (OCR), and so I pivoted to using Tesseract OCR in combination with the pytesseract Python wrapper. This allowed me to convert each page of a PDF into an image and then extract readable text from those images.

Challenges:

1.
Library Setup & Compatibility:
One of the first challenges was correctly installing and configuring the necessary libraries — especially pytesseract, Pillow, and PyMuPDF (fitz) — and ensuring that the Tesseract OCR engine itself was installed and properly linked to my Python environment. Getting the pipeline from PDF to image to text working smoothly took some experimentation.

2.
I initally desired the solution to work for any number of PDFs dropped into a folder. To do this, I wrote code that dynamically loops over all .pdf files in the input folder and processes each page individually. This made the solution flexible and scalable for batch processing, but it took quite a while for my system to process and so I reverted back to using single .pdf file extraction per run.

3.
The greatest challenge was designing regex patterns that could reliably detect and extract both product names and manufacturer names from the often inconsistent and noisy OCR output. I went through several iterations to refine the regular expressions and filtering logic. One specific issue was that even when matches were found, the results weren’t being added to the all_products[] list — which I traced back to edge cases in string formatting and match validation.

Through refining extraction patterns, consulting AI feedback, and adding debug print statements, I was able to isolate those issues and create more accurate final output.


## Limitations & Future Improvements

[If you had more time, what would you improve?]

If I had more time, I would focus on significantly improving the accuracy and reliability of the regex patterns used to extract product and manufacturer names. In this version of the code, my priority was to build a working pipeline that could efficiently process and parse the PDF files, and to resolve bugs related to file handling, OCR, and data aggregation.

As a result, the regex logic was kept relatively simple and may miss some valid matches or capture irrelevant data. With additional time, I would:

1. 
Dive deeper into the structure and variations of product/manufacturer text in the documents.

2. 
Create more comprehensive regex patterns that handle edge cases and inconsistencies.

3. 
Validate the output against the sample dataset to assess and improve extraction accuracy.

This refinement would make the solution more application ready, and that would be my plan moving forward to improve this code.