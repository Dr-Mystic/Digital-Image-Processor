# Image Processor App

## Description
This is a PyQt5-based desktop application that allows users to perform various image processing tasks using OpenCV. Users can open images, apply transformations like grayscale conversion, rotation, scaling, edge detection, flipping, blurring, and sharpening, and then save the processed images.

## Features
- Open and display images
- Convert to grayscale
- Rotate images by user-defined angles
- Scale images by user-defined factors
- Perform edge detection
- Flip images horizontally, vertically, or both
- Apply blur and sharpening filters
- Undo actions and restore previous image states
- Save the processed images

## Installation
1. Clone the repository:
```bash
   git clone https://github.com/Dr-Mystic/Digital-Image-Processor.git
```
```bash
   cd Digital-Image-Processor
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Run the application:
```bash
   python image_processor.py
```

## Usage
- Use the "Open Image" button to load an image.
- Select an operation from the dropdown and click "Process Image."
- You can undo the last action using the "Undo" button.
- Save the processed image using the "Save Image" button.

## Dependencies
- PyQt5
- OpenCV

## License
This project is licensed under the MIT License.