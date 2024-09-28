from PIL import Image
import pytesseract
import re


# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path if different


# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Failed to extract text from {image_path}: {e}")
        return ""

# Function to extract entity value from OCR text
def extract_entity_value(text):
    try:
        # Simple regex to capture value and unit from the text
        pattern = r"([0-9]*\.?[0-9]+)\s?([a-zA-Z]+)"
        matches = re.findall(pattern, text)
        
        # List of allowed units
        ALLOWED_UNITS = ["gram", "milligram", "kilogram", "cup", "ounce", "litre", "millilitre", 
                         "centimetre", "metre", "foot", "kilovolt", "kilowatt", "ton", "volt", "watt"]
        
        # Go through matches and find valid ones
        for match in matches:
            value, unit = match
            if unit.lower() in ALLOWED_UNITS:
                return f"{float(value)} {unit.lower()}"
        return ""
    except Exception as e:
        print(f"Error in extracting entity value: {e}")
        return ""

# Main function to process the already downloaded image
def process_downloaded_image(image_path):
    # Extract text from the image
    ocr_text = extract_text_from_image(image_path)
    print("Extracted Text: ", ocr_text)
    
    # Extract entity value from the OCR text
    entity_value = extract_entity_value(ocr_text)
    print("Extracted Entity Value: ", entity_value)

# Test with the local downloaded image
image_path = "1.jpg"  # Replace this with the actual path of your downloaded image
process_downloaded_image(image_path)