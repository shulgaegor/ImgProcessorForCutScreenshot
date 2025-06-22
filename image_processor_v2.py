#python image_processor_v2.py
import cv2
import numpy as np
import os

input_folder = "in"
output_folder = "out"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 30, 150)
        
        # Находим контуры
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            # Если контур прямоугольный (слайд)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                cropped_img = img[y:y+h, x:x+w]
                cv2.imwrite(os.path.join(output_folder, filename), cropped_img)
                break
'''
Если код не находит слайд, попробуйте:
Подобрать параметры Canny (в строке edged = cv2.Canny(blurred, 50, 150)):
Увеличить 150, если слайд сливается с фоном.
Уменьшить 50, если теряются границы.