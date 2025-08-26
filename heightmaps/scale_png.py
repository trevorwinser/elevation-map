import imageio.v3 as iio
import numpy as np

def contrast_stretch(input_path, output_path):
    # Load image and convert to grayscale if needed
    image = iio.imread(input_path)

    # If image has 3 channels (RGB), convert to grayscale using luminance
    if image.ndim == 3:
        # Standard luminance conversion
        image = 0.299 * image[..., 0] + 0.587 * image[..., 1] + 0.114 * image[..., 2]

    # Convert to float32 for processing
    image = image.astype(np.float32)

    # Find min and max
    min_val = np.min(image)
    max_val = np.max(image)

    print(f"Darkest pixel value: {min_val}")
    print(f"Brightest pixel value: {max_val}")

    if max_val == min_val:
        raise ValueError("Image has no contrast to stretch (all pixels same value).")

    # Apply contrast stretching
    stretched = (image - min_val) * (255.0 / (max_val - min_val))
    stretched = np.clip(stretched, 0, 255).astype(np.uint8)

    # Save output
    iio.imwrite(output_path, stretched)

# Run the function
contrast_stretch("input_image.png", "output_image.png")
