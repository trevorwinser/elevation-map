# Introduction
This project is based on the project at [learnopengl.com](https://learnopengl.com/Guest-Articles/2021/Tessellation/Height-map)

First, let me say that this is not the optimized tessellation solution, but rather the CPU version due to complications utilizing my GPU.

This project is intended to provide a proof of concept for wildfire research. The idea is that by following the process in the above article, we can simulate terrain data and visualize a topography-based prediction model for fire spread.

## Why?

Personally, I do not like 2D graphs of terrain data. You lose a degree of information, and substitute it with something like color to depict depth. However, if we instead maintain 3 dimensions to some scale, we can use color for something equally arbitrary.

If we model fire spread chance as color, we can get a *Probability Heat Map* that provides meaningful information about what locations are more likely to burn.

Ultimately, it may not be necessary, it may not be efficient, but it may be interesting to explore the visualization of a prediction model on a particular terrain.

## How?

The primary predictor is the *slope* between two points. How this affects fire growth, I don't know! But I will try to explain how we attempt to simplify wildfire spread to get meaningful results.

In the Summer of 2025, I worked with PhD Student, Ladan Tazik, Professor John Braun, and Assistant Professor, John Thompson, in an effort to simulate wildfire spreading using small scale wildfires.

In an ideal scenario:

1. Extract a height map of our desired location, taking note of the scaling with the [Tangram Heightmapper](https://tangrams.github.io/heightmapper/).

1. Invert the image with a simple program.
    ```python
    from PIL import Image
    import numpy as np

    def invert_image(input_path, output_path):
        # Load image
        img = Image.open(input_path)

        # Convert to grayscale if not already
        if img.mode != "L":
            img = img.convert("L")

        # Convert to numpy array for fast operations
        arr = np.array(img)

        # Invert pixel values
        inverted = 255 - arr

        # Save output
        out_img = Image.fromarray(inverted.astype(np.uint8))
        out_img.save(output_path)

    if __name__ == "__main__":
        invert_image("input.png", "output.png")
    ```
1. Convert image to [STL](https://imagetostl.com/convert/file/png/to/stl#convert).

1. 3D Print the inverse of the terrain. Take note of the scale used.

1. Imprint the inverse onto clay.

1. Fire clay.

1. Place desired fuel source on terrain (more on this later).

1. Record burning of fuel source.

1. Using the Segment Anything Model [(SAM)](https://openaccess.thecvf.com/content/ICCV2023/papers/Kirillov_Segment_Anything_ICCV_2023_paper.pdf), isolate the border of the fire at each frame.

1. Train a model (I really don't know what I'm talking about here) to understand the fire spread patterns given the following parameters: the **fire border image**, the **timestamp**, and the **height of each pixel**.

1. Add UI to the program to allow the user to start fire simulations.

1. Using the current 2D array of pixels indicating unburnt, burning, and burnt as the input, output the next timestep as 2D array of confidence intervals to determine the probability. (ie. No fire at [5,5] with 99.9% CI means there is a 99.9% chance that no fire will spread to that location). I say this with very little knowledge on how to do this.

### This all sounds nice. Let me tell you what went wrong.

1. The images extracted from this elevation map are quite... **sharp**. They require smoothing with some blur. Further research necessary.

1. The inversion, conversion, and printing all depends on having access to a 3D printer, which due to poor planning on my part, our team could not use.

1. Firing the clay model (8" x 11") can be done in many ways. Without the 3D model, we opted to make an abstract terrain using clay. Furthermore, we did not think there was a way to fire the clay properly without a large enough kiln. After more recent research, methods such as [Pit Firing](https://thepotterywheel.com/how-to-fire-clay-at-home/) may have sufficed for our circumstances.

1. The biggest issue of this project is finding the right way to model fuel sources. There is [public data](https://www.arcgis.com/home/item.html?id=9a1f02ec49b84911ab06b016fbfae62e) on where certain fuel types are, but actually getting a small scale representation of this fuel to accurately depict fire spread is it's own problem. We were most interested in smoldering fires because in the presence of flames, the camera would become obscured, making data collection trickier. Our best result came from Aspen wood shavings

# Program

The OpenGL program is based on the [guest article](https://learnopengl.com/Guest-Articles/2021/Tessellation/Height-map).

For instructions on configuring the project to run, see below:

First, you will need to download your preferred version of [**Visual Studio**](https://visualstudio.microsoft.com/downloads/), not to be confused with *Visual Studio Code*. I can write what's already be said, or I can direct you in the correct place by directing you to this tutorial on setting up your environment for OpenGL programming [here](https://www.youtube.com/watch?v=XpBGwZNyUh0&list=PLPaoO-vpZnumdcb4tZc4x5Q-v7CkrQ6M-&index=1).

If you have an interest in learning OpenGL, I recommend watching the full playlist as it provides beginner insights into what it is like to program shaders, and the steps to achieve said shaders.