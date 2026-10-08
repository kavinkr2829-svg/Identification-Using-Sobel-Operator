**Multi-Object Boundary Identification**  
Multi-Object Boundary Identification Using Sobel Operator  
This project identifies the boundaries of multiple objects in a real-world image using the **Sobel edge detection operator**.  
It also analyzes how the detected boundaries change when the input image is first smoothed using **Gaussian filtering** with different sigma (σ) values.  
The project provides both **visual and quantitative comparisons** between:  
- Raw Image + Sobel  
- Gaussian Filtering + Sobel  
- Thresholded Boundary Maps  
- Morphologically Cleaned Boundary Maps  
**Features**  
- Detects object boundaries using the Sobel operator.  
- Calculates horizontal and vertical image gradients.  
- Computes Sobel gradient magnitude and direction.  
- Applies Gaussian smoothing before Sobel detection.  
- Supports multiple Gaussian sigma values.  
- Converts gradient magnitude into binary boundary maps.  
- Uses morphological closing to clean detected boundaries.  
- Calculates edge density.  
- Estimates image noise.  
- Generates a visual comparison of all processing stages.  
- Saves intermediate output images automatically.  
- Provides command-line arguments for easy configuration.  
**Technologies Used**  
- **Python**  
- **OpenCV**  
- **NumPy**  
- **Matplotlib**  
**Requirements**  
Install the required Python packages:  
pip install opencv-python numpy matplotlib  
   
**Project Structure**  
Multi-Object-Boundary-Identification/  
 │  
 ├── Multi-Object Boundary Identification.py  
 ├── README.md  
 │  
 ├── input/  
 │   └── objects.jpg  
 │  
 └── output/  
     ├── 00_original.png  
     ├── 01_sobel_raw_mag.png  
     ├── 02_sobel_raw_binary.png  
     ├── 03_sobel_raw_clean.png  
     ├── 04_gauss_s1_blur.png  
     ├── 05_gauss_s1_mag.png  
     ├── 06_gauss_s1_binary.png  
     ├── 07_gauss_s1_clean.png  
     ├── ...  
     └── comparison.png  
   
**Methodology**  
**1. Input Image**  
The program accepts a real-world image containing multiple objects.  
The image is loaded using OpenCV and resized while maintaining its aspect ratio for consistent visualization. It is then converted to grayscale.  
**2. Sobel Edge Detection**  
The Sobel operator calculates image gradients in two directions:  
- **X direction (** **Gx** **)** — detects vertical changes.  
- **Y direction (** **Gy** **)** — detects horizontal changes.  
The gradient magnitude is calculated as:  
Magnitude = √(Gx² + Gy²)  
   
The gradient direction is calculated using:  
Direction = atan2(Gy, Gx)  
   
The project uses a Sobel kernel size of 3 × 3.  
**3. Boundary Magnitude**  
The gradient magnitude represents the strength of the detected boundary.  
Strong intensity changes produce stronger boundary responses.  
The magnitude is normalized to the range:  
0 – 255  
   
**4. Thresholding**  
A threshold is applied to the Sobel magnitude to obtain a binary boundary map.  
Default threshold:  
80  
   
Pixels above the threshold are considered significant boundaries.  
**5. Morphological Cleanup**  
Morphological closing is applied to the binary boundary image.  
This helps connect nearby boundary pixels and remove small gaps in the detected object boundaries.  
The default morphological kernel size is:  
3 × 3  
   
**Gaussian Smoothing**  
Gaussian filtering is applied before Sobel edge detection.  
The purpose of Gaussian smoothing is to reduce small intensity variations and noise before detecting boundaries.  
Default sigma values:  
σ = 1, 2, 4  
   
For each sigma value:  
Original Image  
        ↓  
 Grayscale  
        ↓  
 Gaussian Blur  
        ↓  
 Sobel Operator  
        ↓  
 Gradient Magnitude  
        ↓  
 Thresholding  
        ↓  
 Morphological Cleanup  
        ↓  
 Detected Boundaries  
   
**Quantitative Analysis**  
The project calculates two metrics for comparing the different processing methods.  
**1. Edge Density**  
Edge density represents the fraction of pixels whose gradient magnitude is greater than a specified threshold.  
Edge Density =  
 Number of pixels above threshold  
 ---------------------------------  
 Total number of pixels  
   
**2. Noise Estimate**  
The project estimates noise using the mean gradient magnitude of the lowest 20% of pixels.  
This provides an approximate measurement of low-level image variation/noise.  
**Running the Project**  
**Basic Command**  
python "Multi-Object Boundary Identification.py" --image path/to/image.jpg  
   
Example:  
python "Multi-Object Boundary Identification.py" --image input/objects.jpg  
   
**Specify Gaussian Sigma Values**  
python "Multi-Object Boundary Identification.py" \  
 --image input/objects.jpg \  
 --sigma 1 2 3 4  
   
**Change the Boundary Threshold**  
The default threshold is 80.  
python "Multi-Object Boundary Identification.py" \  
 --image input/objects.jpg \  
 --thresh 100  
   
**Change Output Directory**  
By default, results are saved inside output/.  
python "Multi-Object Boundary Identification.py" \  
 --image input/objects.jpg \  
 --out results  
   
**Output Files**  
The program automatically creates several output images.  
**Original Image**  
00_original.png  
   
**Raw Sobel Magnitude**  
01_sobel_raw_mag.png  
   
**Raw Binary Boundary**  
02_sobel_raw_binary.png  
   
**Raw Cleaned Boundary**  
03_sobel_raw_clean.png  
   
**Gaussian Results**  
For each sigma value:  
04_gauss_sX_blur.png  
 05_gauss_sX_mag.png  
 06_gauss_sX_binary.png  
 07_gauss_sX_clean.png  
   
For example:  
04_gauss_s1_blur.png  
 05_gauss_s1_mag.png  
 06_gauss_s1_binary.png  
 07_gauss_s1_clean.png  
   
**Comparison Visualization**  
The project generates:  
comparison.png  
   
This provides a side-by-side comparison of the original image, raw Sobel result, Gaussian + Sobel results, and cleaned boundary maps.  
**Sample Output**  
The terminal displays a quantitative report similar to:  
========== Quantitative Report ==========  
 Pipeline                         Edge density    Noise est.  
 ----------------------------------------------------------  
 Raw + Sobel                           0.xxxx          xx.xx  
 Gaussian σ=1 + Sobel                  0.xxxx          xx.xx  
 Gaussian σ=2 + Sobel                  0.xxxx          xx.xx  
 Gaussian σ=4 + Sobel                  0.xxxx          xx.xx  
 ==========================================================  
   
The actual values depend on the input image.  
**Effect of Gaussian Filtering**  
Gaussian smoothing reduces small-scale intensity variations before the Sobel operation.  
**Without Gaussian Filtering**  
Image  
   ↓  
 Sobel  
   ↓  
 Edges + Fine Details + Noise  
   
**With Gaussian Filtering**  
Image  
   ↓  
 Gaussian Blur  
   ↓  
 Sobel  
   ↓  
 More Stable Boundaries  
   
As the Gaussian sigma increases, stronger smoothing is applied.  
| | |  
|-|-|  
| **Processing** | **Expected Result** |   
| Raw + Sobel | More fine details and possible noise |   
| Gaussian σ=1 + Sobel | Slight smoothing |   
| Gaussian σ=2 + Sobel | More noise suppression |   
| Gaussian σ=4 + Sobel | Stronger smoothing and fewer fine details |   
   
The exact result depends on the image and threshold selected.  
**Algorithm**  
START  
   │  
   ▼  
 Load Input Image  
   │  
   ▼  
 Resize Image  
   │  
   ▼  
 Convert to Grayscale  
   │  
   ├───────────────┐  
   │               │  
   ▼               ▼  
 Raw Image      Gaussian Blur  
   │               │  
   ▼               ▼  
 Sobel           Sobel  
   │               │  
   ▼               ▼  
 Gradient        Gradient  
 Magnitude       Magnitude  
   │               │  
   ▼               ▼  
 Threshold       Threshold  
   │               │  
   ▼               ▼  
 Morphological   Morphological  
 Cleanup         Cleanup  
   │               │  
   └───────┬───────┘  
           ▼  
 Quantitative Comparison  
           │  
           ▼  
 Visualization  
           │  
           ▼  
 Save Results  
           │  
           ▼  
          END  
   
**Applications**  
- Computer Vision  
- Object Detection  
- Image Segmentation  
- Industrial Inspection  
- Medical Image Processing  
- Shape Detection  
- Robotics  
- Autonomous Systems  
- Image Analysis  
**Advantages**  
- Simple and computationally efficient.  
- Uses a standard Sobel edge detector.  
- Supports multiple objects in a single image.  
- Allows comparison between different Gaussian smoothing levels.  
- Provides both visual and numerical analysis.  
- Automatically saves intermediate processing results.  
- Command-line parameters make experimentation easy.  
**Limitations**  
- Sobel detects intensity changes rather than understanding object semantics.  
- Strong texture can produce unwanted boundaries.  
- The selected threshold affects the final boundary map.  
- Excessive Gaussian smoothing can remove fine object details.  
- Edge density and noise estimate are proxy metrics rather than ground-truth accuracy measures.  
**Conclusion**  
The project demonstrates **multi-object boundary identification using the Sobel operator** and investigates the effect of  **Gaussian pre-smoothing**.  
The raw Sobel method can preserve fine image details but may also detect unwanted small variations. Applying Gaussian filtering before Sobel detection can suppress these variations and produce cleaner boundaries. Increasing the Gaussian sigma increases the amount of smoothing, which can reduce fine details along with noise.  
Therefore, the appropriate Gaussian sigma and threshold should be selected according to the characteristics of the input image and the required boundary detail.  
# Identification-Using-Sobel-Operator
