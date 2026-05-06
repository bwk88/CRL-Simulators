#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 14:58:33 2025

@author: crl
"""

import os
import subprocess
#from PIL import Image, ImageChops
import time
import pyautogui
import pandas as pd
from skimage.metrics import structural_similarity as ssim
import cv2 


def save_screenshot(base_name,captured):
    # Ensure the folder exists
    os.makedirs(captured,exist_ok=True)
    
    counter = 1
    while True:
        filename = f"{base_name}_{counter}.png"
        filepath = os.path.join(captured,filename)
        if not os.path.exists(filepath):
            break
        counter +=1
        
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"screenshot saved to {filepath}")
    
def compare_images(img1_path, img2_path, threshold=0.95):
    # Compare two images and return similarity score + Pass/Fail
    if not os.path.exists(img1_path) or not os.path.exists(img2_path):
        return 0, "Fail (file not found)"
    
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    
    if img1 is None or img2 is None:
        return 0, "Fail (unable to read image)"
    
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2,(img1.shape[1],img1.shape[0]))
    
    gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    
    score,_ = ssim(gray1, gray2, full=True)
    result = "Pass" if score >= threshold else "Fail"
    return score, result


def process_excel(excel_path,captured_folder,reference_folder):
    df = pd.read_excel(excel_path)
    results=[]
    for idx, row in df.iterrows():
        captured_name= str(row.get('captured_image','')).strip()
        reference_name= str(row.get('reference_image','')).strip()
        
        #skip if missing or invalid
        if not captured_name or captured_name.lower() == 'nan' or \
            not reference_name or reference_name.lower() == 'nan':
                print(f"skipping row {idx +1}(missing file name)")
                results.append("skipped")
                continue
        captured_path= os.path.join(captured_folder,captured_name)
        reference_path= os.path.join(reference_folder,reference_name)
        
        score,result = compare_images(captured_path,reference_path)
        print(f"---------------------{result,results}")
        print(f"{captured_name} vs {reference_name} -> {score:.3f} -> {result}")
        results.append(result)
    df['result'] =results
    output_file = "comparison_results.xlsx"
    df.to_excel(output_file,index=True)
    print(f"\n Results saved to {output_file}")
    
    
def main():
    captured = "/home/kuldeepsingh@Indigenous.com/Documents/ATC_TESTING/DYANAMIC_SIMULATOR/dynamic_testing_simulator_1.9.4/player/27-oct-2025_kuldeep/ATCSimulator/player/Captured_Screenshot"
    reference = "/home/kuldeepsingh@Indigenous.com/Documents/ATC_TESTING/DYANAMIC_SIMULATOR/dynamic_testing_simulator_1.9.4/player/27-oct-2025_kuldeep/ATCSimulator/player/Referenced_Screenshot"
    base_name ="Screenshot"
    save_screenshot(base_name,captured)
    process_excel("/home/kuldeepsingh@Indigenous.com/Documents/ATC_TESTING/DYANAMIC_SIMULATOR/dynamic_testing_simulator_1.9.4/player/27-oct-2025_kuldeep/ATCSimulator/player/compare.xlsx",captured,reference)


if __name__ == "__main__":
    main()