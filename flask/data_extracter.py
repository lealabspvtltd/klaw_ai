# all the functions to extract datas from pdfs and other files



######################## ########################   OCR    ######################## ######################## ######################## 

# Import the easyocr Reader class
import easyocr

def extract_text_from_image(image_path):
    """
    Extracts text from an image using EasyOCR and returns it as a full sentence.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The extracted text as a complete sentence.
    """
    
    # Initialize the EasyOCR Reader with English language
    reader = easyocr.Reader(['en'])

    # Read text from the image
    result = reader.readtext(image_path, detail=0)  # detail=0 returns only text, not boxes/confidence

    # Join the extracted text list into a sentence
    sentence = ' '.join(result)


    return sentence


#sample usage of the above function

"""

image_path = 'documents/quote.jpg'

text_output = extract_text_from_image(image_path)

print("Extracted Text:", text_output)

"""


######################## ########################   OCR    ######################## ######################## ######################## 



######################## ########################   TXT     ######################## ######################## ######################## 

def extract_text_from_txt(file_path):
    """
    Reads text from a .txt file and returns it as a single string.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The content of the text file as a single string.
    """
    try:
        # Open the file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Return the stripped content (removes leading/trailing spaces/newlines)
        return content.strip()

    except FileNotFoundError:
        return f"Error: File not found at path '{file_path}'"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# sample usage

"""

file_path = 'documents/Nikola_Tesla.txt'

text = extract_text_from_txt(file_path)

print("Extracted Text:\n", text)

"""

######################## ########################   TXT    ######################## ######################## ######################## 




######################## ########################   PDF    ######################## ######################## ######################## 




import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts and returns all text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: All text content extracted from the PDF.
    """
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)

        # Store all extracted text here
        all_text = ""

        # Iterate through each page and extract text
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)      # Load page
            text = page.get_text()              # Extract text
            all_text += text + "\n"             # Add to final string

        doc.close()
        
        return all_text.strip()  # Remove extra whitespace

    except FileNotFoundError:
        return f"Error: File not found at path '{pdf_path}'"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# sample usage

"""

pdf_path = 'documents/Nikola_Tesla.pdf'

pdf_text = extract_text_from_pdf(pdf_path)

print("Extracted PDF Text:\n", pdf_text)

"""


######################## ########################   PDF    ######################## ######################## ######################## 
