import os
import random
import shutil

# Source directory where the images are located
source_directory = '/Users/jerryhughes/Desktop/pol_clean'

# Destination directory on the desktop to store the selected images
destination_directory = '/Users/jerryhughes/Desktop/pol_random_sample'

# Number of images to select
num_images_to_select = 500

# Get a list of all image files in the source directory
image_files = [
    file for file in os.listdir(source_directory)
    if file.lower().endswith(('.jpg', '.jpeg', '.png'))
]

# Randomly select 500 images from the list
selected_images = random.sample(image_files, num_images_to_select)

# Create the destination directory if it doesn't exist
os.makedirs(destination_directory, exist_ok=True)

# Copy and paste the selected images to the destination directory
for image in selected_images:
    source_path = os.path.join(source_directory, image)
    destination_path = os.path.join(destination_directory, image)
    shutil.copy(source_path, destination_path)

print("Images have been successfully copied to the destination folder.")
