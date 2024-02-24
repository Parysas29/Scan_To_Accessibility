import fitz  # PyMuPDF
from PIL import Image
import subprocess

def pdf_to_ppm(input_pdf, output_folder, dpi=300):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf)

    # Iterate through each page
    for page_number in range(pdf_document.page_count):
        # Get the current page
        page = pdf_document[page_number]

        # Render the page as an image with higher DPI
        image = page.get_pixmap(matrix=fitz.Matrix(dpi / 72.0, dpi / 72.0))

        # Convert the image to a PIL Image
        pil_image = Image.frombytes("RGB", (image.width, image.height), image.samples)

        # Save the PIL Image as a PPM file with higher DPI
        output_file_path = f"{output_folder}/page_{page_number + 1}.ppm"
        pil_image.save(output_file_path, format="ppm", dpi=(dpi, dpi))

        print(f"Page {page_number + 1} saved as {output_file_path}")

    # Close the PDF file
    pdf_document.close()

def run_img2pdf(input_folder, output_pdf):
    # Construct the img2pdf command
    img2pdf_command = [
        "img2pdf",
        f"{input_folder}/*.ppm",
        "-o", f"{output_pdf}/out.pdf"
    ]

    # Run the img2pdf command
    process = subprocess.run(img2pdf_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check for errors
    if process.returncode != 0:
        print(f"Error executing img2pdf command: {process.stderr.decode()}")
    else:
        print(f"PDF saved as {output_pdf}")

def run_unpaper(input_folder, output_folder):
    # Construct the unpaper command
    unpaper_command = [
        "unpaper",
        "--layout", "double",
        "--input-pages", "1",
        "--output-pages", "2",
        f"{input_folder}/page_%d.ppm",
        f"{output_folder}/output%03d.ppm"
    ]

    # Run the unpaper command
    process = subprocess.run(unpaper_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check for errors
    if process.returncode != 0:
        print(f"Error executing unpaper command: {process.stderr.decode()}")
    else:
        print("Unpaper command executed successfully.")

def run_tesseract(output_unpaper):
    tesseract_command = [ 
        "tesseract",
         f"{output_unpaper}/sorted_files.txt",
        "../output-prefix pdf"
    ]

    subprocess.run(tesseract_command)

def create_sorted_text_file(output_folder):
    # Get a list of all the files in the output folder
    file_list = os.listdir(output_folder)

    # Sort the file list alphabetically
    sorted_file_list = sorted(file_list)

    # Create a new text file to store the sorted file names
    output_file_path = f"{output_folder}/sorted_files.txt"
    with open(output_file_path, "w") as output_file:
        # Write each file name to the text file
        for file_name in sorted_file_list:
            output_file.write(f"{output_folder}/{file_name}\n")

    print(f"Sorted file list saved as {output_file_path}")

# Call the function to create the sorted text file


if __name__ == "__main__":
    # Provide the input PDF file and output folder
    input_pdf_file = "../input.pdf"
    output_folder_path = "../output_high_quality_ppm_files"
    output_unpaper = "../output_unpaper_files"

    # Create the output folder if it doesn't exist
    import os
    os.makedirs(output_folder_path, exist_ok=True)
    os.makedirs(output_unpaper, exist_ok=True)

    # Convert PDF to PPM with higher DPI for better quality
    pdf_to_ppm(input_pdf_file, output_folder_path, dpi=300)

    # Run unpaper on the generated PPM files
    run_unpaper(output_folder_path, output_unpaper)
    run_img2pdf(output_unpaper, output_unpaper)
    #create_sorted_text_file(output_unpaper)
    #run_tesseract(output_unpaper)
