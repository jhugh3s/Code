import os
import json
import requests

def truncate_folder_name(folder_name, max_length):
    if len(folder_name) > max_length:
        return folder_name[:max_length].strip()
    return folder_name

def download_images_from_json(json_file, save_directory):
    # Create save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Initialize counters for images with no text
    no_text_count = 1

    # Extract image URLs and download images
    for item in data:
        if 'media' in item:
            media = item['media']
            for media_item in media:
                if 'media_url' in media_item:
                    image_url = media_item['media_url']
                    image_filename = image_url.split('/')[-1]
                    full_text = item.get('full_text', '')
                    words = full_text.split()
                    if len(words) > 0 and not words[0].startswith('https://'):
                        folder_name = ' '.join([word for word in words if not word.startswith('https://')])
                        folder_name = folder_name.replace('/', '_').strip()
                        folder_name = truncate_folder_name(folder_name, 200)
                    else:
                        folder_name = f"No_title{no_text_count}"
                        no_text_count += 1
                    save_folder = os.path.join(save_directory, folder_name)

                    try:
                        # Create a folder for the image
                        os.makedirs(save_folder, exist_ok=True)

                        # Download the image
                        response = requests.get(image_url)
                        response.raise_for_status()

                        # Save the image to disk
                        image_path = os.path.join(save_folder, image_filename)
                        with open(image_path, 'wb') as image_file:
                            image_file.write(response.content)

                        print(f"Downloaded image: {image_filename}")

                        # Save additional information as a text file
                        info_filename = f"{image_filename.split('.')[0]}.txt"
                        info_path = os.path.join(save_folder, info_filename)

                        additional_info = {
                            'full_text': full_text,
                            'reply_count': item.get('reply_count', 0),
                            'retweet_count': item.get('retweet_count', 0),
                            'favorite_count': item.get('favorite_count', 0)
                        }

                        with open(info_path, 'w') as info_file:
                            json.dump(additional_info, info_file, indent=4)

                        print(f"Saved additional information: {info_filename}")
                    except requests.exceptions.RequestException as e:
                        print(f"Error downloading image: {image_filename}")
                        print(e)

# Usage example
json_file_path = '/Users/jerryhughes/Desktop/twitter_dataset/dataset_twitter-scraper_2023-06-16_09-11-51-226.json'
save_directory_path = '/Users/jerryhughes/Desktop/twitter_scrape'

download_images_from_json(json_file_path, save_directory_path)
