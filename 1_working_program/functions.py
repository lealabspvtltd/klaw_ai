# all functions to extract data from PDFs and other files

######################## ########################  OCR & PDF Processing ######################## ######################## 

import easyocr
import os
from pdf2image import convert_from_path
import numpy as np

def extract_text_from_image(file_path, output_folder="temp_images", delete_images=True):
    """
    Extracts text from image/PDF files using EasyOCR.
    
    Args:
        file_path (str): Path to image or PDF file
        output_folder (str): Temporary folder for PDF page images (default: 'temp_images')
        delete_images (bool): Whether to delete temporary images (default: True)
        
    Returns:
        str/list: Text string for images, list of page texts for PDFs
    """
    # Initialize EasyOCR reader once for all processing
    reader = easyocr.Reader(['en'])
    
    # PDF processing logic
    if file_path.lower().endswith('.pdf'):
        os.makedirs(output_folder, exist_ok=True)
        images = convert_from_path(file_path)
        extracted_texts = []
        print("1")
        for page_num, image in enumerate(images, 1):
            # Convert PIL image to numpy array for direct processing
            image_np = np.array(image)

            print("2")
            # Extract text from numpy array
            result = reader.readtext(image_np, detail=0)
            page_text = ' '.join(result)
            extracted_texts.append(page_text)
            print("3")
            
            # Optional: Save images for verification
            if not delete_images:
                image_path = os.path.join(output_folder, f"page_{page_num}.jpg")
                image.save(image_path, "JPEG")
                
        # Cleanup temporary folder if empty
        if delete_images and os.path.exists(output_folder):
            if not os.listdir(output_folder):
                os.rmdir(output_folder)
        print("4")       
        return extracted_texts
    
    # Image processing logic
    else:
        result = reader.readtext(file_path, detail=0)
        return ' '.join(result)

# Sample usage
if __name__ == "__main__":
    # Test with image
    #image_text = extract_text_from_image("/home/abin/Desktop/klaw_AI/documents/quote.jpg")
    #print("Image Text:", image_text)
    
    # Test with PDF
    pdf_texts = extract_text_from_image("/home/abin/Desktop/klaw_AI/documents/Albert_Einstein.pdf")
    for i, text in enumerate(pdf_texts, 1):
        print(f"\nPage {i} Text:")
        print(text)
        print("-" * 50)
