import os
import requests
import pandas as pd
from PIL import Image
import pytesseract
import re

# Constants for allowed units (these should be taken from constants.py in the challenge)
ALLOWED_UNITS = ['centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard','gram','kilogram','microgram','milligram','ounce','pound','ton','kilovolt', 'millivolt', 'volt','kilowatt', 'watt','centilitre','cubic foot','cubic inch','cup','decilitre','fluid ounce','gallon','imperial gallon','litre','microlitre','millilitre','pint','quart']

# Function to download images
def download_image(image_url, save_path):
    try:
        img_data = requests.get(image_url).content
        with open(save_path, 'wb') as handler:
            handler.write(img_data)
        print(f"Downloaded image from {image_url}")
    except Exception as e:
        print(f"Failed to download image from {image_url}: {e}")

# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Failed to extract text from {image_path}: {e}")
        return ""

# Function to clean and extract entity value and unit
def extract_entity_value(text, entity_name):
    try:
        # Use regex to find the first match of a value + unit in the text
        pattern = r"([0-9]*\.?[0-9]+)\s?([a-zA-Z]+)"
        matches = re.findall(pattern, text)
        
        # Go through the matches and return the first valid one with an allowed unit
        for match in matches:
            value, unit = match
            if unit.lower() in ALLOWED_UNITS:
                return f"{float(value)} {unit.lower()}"
        return ""  # Return empty if no valid value found
    except Exception as e:
        print(f"Error in extracting entity value: {e}")
        return ""

# Main function to process dataset and generate predictions
def process_dataset(csv_file, output_file):
    # Read the dataset
    df = pd.read_csv(csv_file)
    
    predictions = []
    
    for index, row in df.iterrows():
        image_url = row['image_link']
        entity_name = row['entity_name']
        image_save_path = f"images/{index}.jpg"
        
        # Download the image
        download_image(image_url, image_save_path)
        
        # Extract text from the image
        ocr_text = extract_text_from_image(image_save_path)
        
        # Extract entity value from the OCR text
        entity_value = extract_entity_value(ocr_text, entity_name)
        
        # Append result
        predictions.append({"index": row['index'], "prediction": entity_value})
    
    # Save the predictions to the output CSV
    predictions_df = pd.DataFrame(predictions)
    predictions_df.to_csv(output_file, index=False)
    print(f"Predictions saved to {output_file}")

# Usage
# Ensure to replace 'train.csv' with the actual file path and 'output.csv' with the desired output file
process_dataset('dataset/train.csv', 'output.csv')