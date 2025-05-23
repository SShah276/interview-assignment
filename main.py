'''
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What are the main functions in PyPDF2?"}
    ]
)

print(response.choices[0].message.content)
'''
import os
import fitz
import pytesseract
from PIL import Image
import io
import pandas as pd
import re

input_folder = "input"
output_folder = "output"

def extract_products_and_manufacturers(text, page_number):
    products = []

    manufacturer_pattern = re.compile(r"([A-Z][a-zA-Z\s]+)\s+(?:Company|Corporation|Manufacturing|Inc(?:\.|orporated)?)")

    product_pattern = re.compile(
        r"(?:Product\s*:\s*(?P<prod1>[A-Za-z\s]+)|Model\s*:\s*(?P<prod2>[A-Za-z0-9\s\-]+)|(?P<prod3>[A-Za-z0-9\s\-\",]+(?:System|Unit|Model|Product)))"
    )

    def clean(text):
        text = re.sub(r"[\r\n\t]+", " ", text)        # Replace newlines/tabs with space
        text = re.sub(r"\s{2,}", " ", text)           # Collapse multiple spaces
        text = text.strip(' ,"')                     # Strip leading/trailing punctuation and whitespace
        return text.strip()
    
    manufacturers = set(clean(m) for m in manufacturer_pattern.findall(text))
    product_names = product_pattern.finditer(text)

    unique_manufacturers = list(set(manufacturers))
    unique_products = set()
    
    for match in product_names:
        raw = match.group("prod1") or match.group("prod2") or match.group("prod3")
        if raw:
            product = clean(raw)
            # Optional: Filter out noise terms
            if product.lower() not in {"job data", "submittal review", "alternates"}:
                unique_products.add(product)

    print("Manufacturers found:", unique_manufacturers)
    print("Products found:", list(unique_products))

    for manufacturer in unique_manufacturers:
        for product in unique_products:
            if product and manufacturer:  # Ensure not empty
                product_info = {
                    "Product Name": product,
                    "Manufacturer Name": manufacturer,
                    "Pages": page_number
                }
                products.append(product_info)
                print("Added product:", product_info)  # Debug
    
    return products

all_products = []

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):
        # Build the path safely
        pdf_path = os.path.join(input_folder, filename)
        # Open the PDF file
        doc = fitz.open(pdf_path)
        print(f"\nProcessing {filename}...")
        all_products = []
        for page_number in range(len(doc)):
            # Load the first page
            page = doc.load_page(page_number)  # Page 0 = first page
            # Render page to an image (as PNG in memory)
            pix = page.get_pixmap(dpi=300)
            img_data = pix.tobytes("png")
            # Open it with PIL
            image = Image.open(io.BytesIO(img_data))
            # Use Tesseract to extract text
            text = pytesseract.image_to_string(image)
            print(f"\n--- Text from {filename}, Page {page_number + 1} ---")
            print(text)

            products = extract_products_and_manufacturers(text, page_number + 1)
            if products:  # Ensure products is not None or empty
                all_products.extend(products)

        print("All Products:", all_products)

        if all_products:
            df = pd.DataFrame(all_products).drop_duplicates(subset=["Product Name", "Manufacturer Name"])
            df = df.groupby(["Product Name", "Manufacturer Name"])["Pages"].apply(list).reset_index()

            # Name CSV after the PDF file
            base_name = os.path.splitext(filename)[0]
            csv_output_path = os.path.join(output_folder, f'{base_name}_products.csv')
            df.to_csv(csv_output_path, index=False)
            print(f"✅ CSV file created at {csv_output_path}")
        else:
            print(f"⚠️ No products found in {filename}, skipping CSV creation.")