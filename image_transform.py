import cv2
import os
import numpy as np


def crop_image(img):
  # Convert to gray, and threshold
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

  # remove noise
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
  morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

  # Find the max-area contour
  cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
  if not cnts:
        print("No contour found.")
        return None

  cnt = sorted(cnts, key=cv2.contourArea)[-1]

  # Crop and save it
  x,y,w,h = cv2.boundingRect(cnt)
  dst = img[y:y+h, x:x+w]
  return dst

def resize_image(img, max_w=200, max_h=90):
    h, w = img.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

def rotate_image(img):
    return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)



input_folder =  "/images"
output_folder = "/processed_images"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png")):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        if img is None:
            print(f"Failed to load {filename}")
            continue

        cropped = crop_image(img)
        resized = resize_image(cropped)
        rotated = rotate_image(resized)

        save_path = os.path.join(output_folder, filename)
        cv2.imwrite(save_path, rotated)
        print(f"Processed and saved: {save_path}")