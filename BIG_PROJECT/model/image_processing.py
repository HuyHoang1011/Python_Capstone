import cv2
import numpy as np
import os
from pyzbar import pyzbar
import tkinter as tk
from tkinter import messagebox

# Global variable to store detected MSSVs
mssv_list = []
current_mssv = None

# Resize image to a manageable size
def resize_image(image, width=800):
    height, original_width = image.shape[:2]
    if original_width > width:
        scale = width / original_width
        new_height = int(height * scale)
        resized_image = cv2.resize(image, (width, new_height))
        return resized_image
    return image

# Function to detect the student card region based on color
def find_card_region(image):
    """
    Tìm vùng thẻ sinh viên dựa vào màu sắc: xanh dương ở trên và trắng bên dưới.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Màu xanh dương (HSV range)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Tạo mask màu xanh dương
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Tìm contours trong mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return (x, y, w, h)  # Trả về tọa độ vùng chứa màu xanh dương
    return None

# Function to preprocess the barcode region for better detection
def preprocess_barcode(image):
    """
    Tiền xử lý ảnh để tăng khả năng phát hiện mã vạch.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Chuyển ảnh sang xám
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Làm mờ nhẹ để loại nhiễu
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Nhị phân hóa
    return thresh



# Updated function to detect MSSV and highlight fields
def detect_mssv_with_highlight(image_path):
    global current_mssv

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Unable to load the image.")

    # Resize the image
    image = resize_image(image)



    # Find the student card region based on blue color
    card_region = find_card_region(image)
    if card_region:
        x, y, w, h = card_region
        # Draw rectangle around the detected card region
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(f"Detected card region at: x={x}, y={y}, w={w}, h={h}")

        # Define ROIs relative to the detected card region
        roi_logo = (x + 20, y + 20, 100, 100)  # Logo
        roi_title = (x + 150, y + 20, 300, 50)  # Title
        roi_photo = (x + 50, y + 150, 120, 200)  # Photo
        roi_mssv = (x + 50, y + h - 70, w - 100, 50)  # MSSV near bottom

        # Highlight regions
        cv2.circle(image, (roi_logo[0] + roi_logo[2] // 2, roi_logo[1] + roi_logo[3] // 2), 50, (0, 255, 0), 2)
        cv2.rectangle(image, (roi_title[0], roi_title[1]),
                      (roi_title[0] + roi_title[2], roi_title[1] + roi_title[3]), (0, 255, 0), 2)
        cv2.rectangle(image, (roi_photo[0], roi_photo[1]),
                      (roi_photo[0] + roi_photo[2], roi_photo[1] + roi_photo[3]), (0, 255, 0), 2)
        cv2.rectangle(image, (roi_mssv[0], roi_mssv[1]),
                      (roi_mssv[0] + roi_mssv[2], roi_mssv[1] + roi_mssv[3]), (0, 255, 0), 2)

    else:
        print("Could not detect card region based on color.")

    # Detect barcodes
    barcodes = pyzbar.decode(image)
    detected_mssv = None
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        if barcode_data.isdigit() and len(barcode_data) == 10:
            detected_mssv = barcode_data
            break

    # Set current MSSV for approval
    current_mssv = detected_mssv

    # Show the highlighted image
    cv2.imshow("Highlighted Student Card", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return detected_mssv



# Function to handle user interaction for saving MSSVs
def process_image_interactive(image_path):
    global mssv_list, current_mssv

    detected_mssv = detect_mssv_with_highlight(image_path)

    def on_approve():
        if detected_mssv:
            if detected_mssv in mssv_list:
                messagebox.showwarning("Duplicate MSSV", f"MSSV {detected_mssv} is already in the list.")
            else:
                mssv_list.append(detected_mssv)
                messagebox.showinfo("Success", f"MSSV {detected_mssv} saved successfully.")
        else:
            messagebox.showerror("Error", "No valid MSSV detected.")
        root.destroy()

    def on_skip():
        messagebox.showinfo("Skipped", "Image skipped without saving.")
        root.destroy()

    # Create a Tkinter window for approval
    root = tk.Tk()
    root.title("Approve MSSV")

    tk.Label(root, text=f"Detected MSSV: {detected_mssv if detected_mssv else 'None'}", font=("Arial", 14)).pack(
        pady=10)
    tk.Button(root, text="Approve", command=on_approve, width=15).pack(pady=5)
    tk.Button(root, text="Skip", command=on_skip, width=15).pack(pady=5)

    root.mainloop()


# Function to process all images in the Resources/images folder interactively
def process_all_images_interactive(directory):
    if not os.path.exists(directory):
        raise ValueError(f"Directory {directory} does not exist.")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            print(f"Processing image: {file_path}")
            process_image_interactive(file_path)


# Function to display MSSV list
def display_mssv_list():
    global mssv_list
    if not mssv_list:
        return "No MSSVs detected yet."
    return "\n".join(mssv_list)
