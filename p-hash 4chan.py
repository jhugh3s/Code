import os
import shutil
from PIL import Image, UnidentifiedImageError
import imagehash

def calculate_phash(image_path):
    try:
        with Image.open(image_path) as img:
            # Resize the image for faster processing (optional)
            img = img.resize((8, 8), Image.ANTIALIAS)
            # Compute the p-hash value
            phash = imagehash.phash(img)
            return phash
    except (OSError, UnidentifiedImageError):
        return None

def remove_duplicates(source_folder, destination_folder, similarity_threshold):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Dictionary to store the hash values and corresponding image paths
    hash_dict = {}

    # Counter for the total number of images and duplicates removed
    total_images = 0
    duplicates_removed = 0

    # Traverse through all folders and subfolders in the source directory
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            image_path = os.path.join(root, file_name)

            # Calculate the p-hash for the image
            phash = calculate_phash(image_path)

            if phash is None:
                # Skip if the file is not a valid image
                continue

            # Check if the hash value already exists in the dictionary
            if phash in hash_dict:
                # Check the similarity with the existing image
                existing_image_path = hash_dict[phash]
                existing_similarity = phash - calculate_phash(existing_image_path)
                if existing_similarity <= similarity_threshold:
                    # Duplicate found, skip this image
                    print(f"Duplicate image found: {image_path}")
                    duplicates_removed += 1
                    continue

            # Add the image to the dictionary with its hash value
            hash_dict[phash] = image_path

            # Copy the image to the destination folder
            new_image_path = os.path.join(destination_folder, "4chan_data", file_name)
            os.makedirs(os.path.dirname(new_image_path), exist_ok=True)
            shutil.copy2(image_path, new_image_path)

            total_images += 1
            print(f"Processed image: {image_path}")

    # Write statistics to the statistics.txt file
    statistics_file = os.path.join(destination_folder, "4chan_data", "statistics.txt")
    with open(statistics_file, "w") as file:
        file.write(f"Total Images: {total_images}\n")
        file.write(f"Duplicates Removed: {duplicates_removed}\n")

# Specify the source folder where your images are stored
source_folder = '/Users/jerryhughes/Desktop/Cleaned_data/4chan_data1'

# Specify the destination folder for cleaned data
destination_folder = '/Users/jerryhughes/Desktop/Cleaned_data'

# Set the similarity threshold (lower values indicate stricter similarity)
similarity_threshold = 0

# Call the function to remove duplicates for the 4chan_scrape folder
remove_duplicates(source_folder, destination_folder, similarity_threshold)
