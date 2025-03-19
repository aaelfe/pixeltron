import argparse
from PIL import Image
import os

def pixelate_image(input_path, output_path=None, width=None, height=None, pixels_per_pixel=1):
    """
    Pixelate an image with customizable dimensions and pixel size.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the output image (default: adds '_pixelated' to original filename)
        width (int): Width of the pixelated image in "big pixels" (default: calculated from original aspect ratio)
        height (int): Height of the pixelated image in "big pixels" (default: calculated from original aspect ratio)
        pixels_per_pixel (int): Number of pixels to use for each "big pixel" in the output (default: 1)
    
    Returns:
        str: Path to the saved pixelated image
    """
    # Open the image
    try:
        img = Image.open(input_path)
    except Exception as e:
        raise ValueError(f"Could not open image {input_path}: {e}")
    
    # Get original dimensions
    orig_width, orig_height = img.size
    
    # Calculate target dimensions if not provided
    if width is None and height is None:
        # Default to 32 big pixels wide if no dimensions specified
        width = 32
        height = int(orig_height * width / orig_width)
    elif width is None:
        # Calculate width to maintain aspect ratio
        width = int(orig_width * height / orig_height)
    elif height is None:
        # Calculate height to maintain aspect ratio
        height = int(orig_height * width / orig_width)
    
    # Resize image to the target size (this creates the pixelated effect)
    small_img = img.resize((width, height), Image.NEAREST)
    
    # Scale back up to get the enlarged pixelated image
    final_width = width * pixels_per_pixel
    final_height = height * pixels_per_pixel
    pixelated_img = small_img.resize((final_width, final_height), Image.NEAREST)
    
    # Determine output path if not provided
    if output_path is None:
        base_name, extension = os.path.splitext(input_path)
        output_path = f"{base_name}_pixelated{extension}"
    
    # Save the pixelated image
    pixelated_img.save(output_path)
    
    return output_path

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Pixelate an image with customizable dimensions and pixel size.')
    parser.add_argument('input_path', help='Path to the input image')
    parser.add_argument('-o', '--output', help='Path to save the output image')
    parser.add_argument('-w', '--width', type=int, help='Width of pixelated image in big pixels')
    parser.add_argument('-ht', '--height', type=int, help='Height of pixelated image in big pixels')
    parser.add_argument('-p', '--pixels-per-pixel', type=int, default=1,
                        help='Number of pixels for each big pixel in the output (default: 1)')
    
    args = parser.parse_args()
    
    try:
        output_path = pixelate_image(
            args.input_path, 
            args.output, 
            args.width, 
            args.height, 
            args.pixels_per_pixel
        )
        print(f"Pixelated image saved to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())