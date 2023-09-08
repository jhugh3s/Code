
import requests
from bs4 import BeautifulSoup
import os
import pathlib
from urllib.parse import urlparse, urljoin
import mimetypes

# URLs of the specific threads
thread_urls = [

   ]

# Set the target folder path on your desktop
target_folder = os.path.join(pathlib.Path.home(), 'Desktop', '4chan_images')

# Create the target folder if it doesn't exist
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# Iterate over each thread URL
for thread_url in thread_urls:
    # Send a GET request to the specific thread
    response = requests.get(thread_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the thread title from the page
    thread_title_element = soup.select_one('.subject')

    if thread_title_element is None:
        print("Thread title element not found.")
        continue

    thread_title = thread_title_element.text.strip()
    thread_title = thread_title.replace('/', '_')  # Remove slashes from title

    # Create the thread folder
    thread_folder = os.path.join(target_folder, thread_title)

    # Create the thread folder if it doesn't exist
    if not os.path.exists(thread_folder):
        os.makedirs(thread_folder)

    # Find all image links within the thread
    image_links = soup.select('a.fileThumb')

    # Download each image within the thread
    for image_link in image_links:
        image_url = urljoin(thread_url, image_link['href'])

        # Check if the URL has a scheme
        parsed_url = urlparse(image_url)
        if not parsed_url.scheme:
            # Add the 'https' scheme
            parsed_url = parsed_url._replace(scheme='https')
            image_url = parsed_url.geturl()

        # Extract the image name from the URL
        image_name = os.path.basename(parsed_url.path)

        # Check the file extension
        content_type, _ = mimetypes.guess_type(image_url)
        if content_type not in ['image/jpeg', 'image/png']:
            print(f"Skipping non-jpg/png file: {image_name}")
            continue

        image_path = os.path.join(thread_folder, image_name)

        # Download the image and save it to the thread folder
        try:
            image_response = requests.get(image_url)
            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)
            print(f"Downloaded: {image_name}")
        except Exception as e:
            print(f"Failed to download: {image_name}")
            print(f"Error: {str(e)}")
