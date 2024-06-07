"""
given a graph like the attached, could you generate a program that obtains the Y values of N values evently distributed

Load the image: Read the image file into a format that we can process.
Preprocess the image: Convert it to grayscale and apply any necessary filtering.
Extract the graph line: Detect the line in the graph and extract its coordinates.
Map pixel coordinates to graph coordinates: Convert the pixel coordinates of the detected line to the actual data values using the axis limits.
Interpolate values: Generate N evenly spaced X values and interpolate the corresponding Y values from the extracted data.

Install opencv:
pip install opencv-python-headless numpy matplotlib


"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters, measure
from scipy.interpolate import interp1d

# Load the image
image_path = '/content/truflation.JPG'
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a Gaussian filter to reduce noise and improve edge detection
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use the Sobel filter to detect edges
edges = filters.sobel(blurred)

# Find contours in the edge-detected image
contours = measure.find_contours(edges, level=0.1)

# Assuming the largest contour is the graph line
largest_contour = max(contours, key=len)

# Extract the x and y coordinates of the contour points
x_coords = largest_contour[:, 1]
y_coords = largest_contour[:, 0]

# Sort coordinates by x value
sorted_indices = np.argsort(x_coords)
x_coords = x_coords[sorted_indices]
y_coords = y_coords[sorted_indices]

# Define the axis limits based on the graph
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = 1.8, 3.4  # Y-axis limits based on the given graph

# Normalize pixel coordinates to data coordinates
data_x = (x_coords - x_min) / (x_max - x_min)
data_y = (y_max - y_min) * (1 - (y_coords - min(y_coords)) / (max(y_coords) - min(y_coords))) + y_min

# Define the number of points to sample
N = 100
sampled_x = np.linspace(0, 1, N)
interpolator = interp1d(data_x, data_y, kind='linear', fill_value="extrapolate")
sampled_y = interpolator(sampled_x)

# Plot the extracted data
plt.figure(figsize=(10, 6))
plt.plot(data_x, data_y, label='Extracted Data')
plt.scatter(sampled_x, sampled_y, color='red', label='Sampled Points')
plt.xlabel('Normalized X')
plt.ylabel('Y Value')
plt.title('Extracted and Sampled Data from Graph')
plt.legend()
plt.show()

# Print the sampled Y values
print(sampled_y)
