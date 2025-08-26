import numpy as np
import imageio.v3 as iio
import sys

def convert_32bit_png_to_16bit(input_path, output_path):
    # Read the image
    img = iio.imread(input_path)

    # Convert to grayscale if it's not already
    if img.ndim == 3:
        if img.shape[2] == 3 or img.shape[2] == 4:  # RGB or RGBA
            # Use standard luminance weights
            rgb = img[..., :3].astype(np.float32)
            img_32 = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
        else:
            raise ValueError("Unsupported channel count in image.")
    elif img.ndim == 2:
        img_32 = img.astype(np.float32)
    else:
        raise ValueError("Unsupported image format.")

    # Normalize to [0, 1]
    min_val = np.min(img_32)
    max_val = np.max(img_32)
    if max_val == min_val:
        img_normalized = np.zeros_like(img_32, dtype=np.float32)
    else:
        img_normalized = (img_32 - min_val) / (max_val - min_val)

    # Convert to 16-bit grayscale
    img_16 = (img_normalized * 65535).astype(np.uint16)

    # Save output
    iio.imwrite(output_path, img_16)
    print(f"Converted and saved to {output_path}")

# Usage example
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_png.py input.png output.png")
    else:
        convert_32bit_png_to_16bit(sys.argv[1], sys.argv[2])
