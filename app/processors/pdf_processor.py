from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_folder, dpi=300):
    """
    Converts a PDF file into images, one image per page.
    Args:
        pdf_path (str): Path to the input PDF file.
        output_folder (str): Folder to save the output images.
        dpi (int): Dots per inch (quality of the output images).
    Returns:
        list: List of paths to the generated images.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to images
    pages = convert_from_path(pdf_path, dpi=dpi)

    image_paths = []
    for idx, page in enumerate(pages):
        image_filename = os.path.join(output_folder, f"page_{idx + 1}.png")
        page.save(image_filename, 'PNG')
        image_paths.append(image_filename)

    return image_paths
