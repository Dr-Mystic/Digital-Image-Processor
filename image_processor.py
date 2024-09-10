import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, 
                             QPushButton, QComboBox, QFileDialog, QDialog, QVBoxLayout, 
                             QDialogButtonBox, QSpinBox, QDoubleSpinBox, QMessageBox, QInputDialog) # type: ignore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

def read_image(path):
    return cv2.imread(path)

def convert_to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def rotate_image(img, angle):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def scale_image(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    return cv2.resize(img, (width, height))

def edge_detection(img):
    return cv2.Canny(img, 100, 200)

def flip_image(img, axis):
    if axis == "Horizontal":
        return cv2.flip(img, 1)
    elif axis == "Vertical":
        return cv2.flip(img, 0)
    elif axis == "Both":
        return cv2.flip(img, -1)
    else:
        return img  # No flip

def blur_image(img):
    return cv2.GaussianBlur(img, (5, 5), 0)

def sharpen_image(img):
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    sharpened_img = cv2.filter2D(img, -1, kernel)
    return sharpened_img

def save_image(path, img):
    cv2.imwrite(path, img)

class ImageProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processor")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Buttons
        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_image)
        self.layout.addWidget(self.open_button)

        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self.process_image)
        self.layout.addWidget(self.process_button)

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo_last_action)
        self.layout.addWidget(self.undo_button)

        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_button)

        # ComboBox for image processing options
        self.process_options = QComboBox()
        self.process_options.addItems(["Select Option", "Convert to Grayscale", "Rotate Image", 
                                        "Scale Image", "Edge Detection", "Flip Image", "Blur Image", 
                                        "Sharpen Image"])
        self.layout.addWidget(self.process_options)

        # QLabel for displaying the image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.image = None  # Placeholder for the loaded image
        self.history = []  # Stack to store the history of images

    def open_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            self.image = read_image(filename)
            self.history = [self.image.copy()]  # Initialize history with the original image
            self.display_image()

    def process_image(self):
        if self.image is not None:
            selected_option = self.process_options.currentText()
            processed_image = None
            if selected_option == "Convert to Grayscale":
                processed_image = convert_to_grayscale(self.image)
            elif selected_option == "Rotate Image":
                angle = self.get_rotation_angle()
                processed_image = rotate_image(self.image, angle)
            elif selected_option == "Scale Image":
                scale = self.get_scaling_factor()
                processed_image = scale_image(self.image, scale)
            elif selected_option == "Edge Detection":
                processed_image = edge_detection(self.image)
            elif selected_option == "Flip Image":
                axis = self.get_flip_axis()  # Get the selected flip axis
                processed_image = flip_image(self.image, axis)
            elif selected_option == "Blur Image":
                processed_image = blur_image(self.image)
            elif selected_option == "Sharpen Image":
                processed_image = sharpen_image(self.image)

            if processed_image is not None:
                self.image = processed_image
                self.history.append(self.image.copy())
                self.display_image()

    def save_image(self):
        if self.image is not None:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if filename:
                if len(self.image.shape) == 2:  # If grayscale, convert to BGR
                    img = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
                else:
                    img = self.image  # If
                    img = self.image
                save_image(filename, img)
                QMessageBox.information(self, "Success", "Image saved successfully.")

    def undo_last_action(self):
        if len(self.history) > 1:  # Ensure there is an action to undo
            self.history.pop()  # Remove the last processed image
            self.image = self.history[-1].copy()  # Set current image to the last in history
            self.display_image()
        else:
            QMessageBox.warning(self, "Warning", "No more actions to undo.")

    def get_rotation_angle(self):
        angle, _ = QInputDialog.getDouble(self, "Rotation Angle", "Enter rotation angle (degrees):", 0, -180, 180, 1)
        return angle

    def get_scaling_factor(self):
        scale, _ = QInputDialog.getDouble(self, "Scaling Factor", "Enter scaling factor:", 1.0, 0.1, 10.0, 1)
        return scale

    def get_flip_axis(self):
        axis, _ = QInputDialog.getItem(self, "Flip Image", "Select flip axis:", ["Horizontal", "Vertical", "Both"])
        return axis

    def display_image(self):
        if self.image is not None:
            h, w = self.image.shape[:2]  # Extract height and width
            ch = self.image.shape[2] if len(self.image.shape) > 2 else 1  # Check number of channels
            bytes_per_line = ch * w
            
            if ch == 1:
                q_img = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
            else:
                q_img = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            
            pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessorApp()
    window.show()
    sys.exit(app.exec_())