import json
import requests
import os
import os
import requests
from pathlib import Path

# Configuration
IMAGE_FOLDER = "mcqImage"
START_INDEX_FILE = "start_index.txt"
CAPTION_TEMPLATE = (
    """🚨 Disclaimer: This content is designed for learning English through MCQ practice for exams. It follows Facebook's community guidelines and aims to educate, not offend."""

)
FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v17.0/me/photos"

def get_access_token():
    """Fetch the Facebook access token from environment variables."""
    token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

    if not token:
        raise ValueError("Facebook access token not found. Set it as an environment variable.")
    return token

def get_images():
    """Fetch all image paths from the designated folder."""
    return sorted(Path(IMAGE_FOLDER).glob("*.png"))

def load_start_index():
    """Load the index of the next image to post."""
    if not Path(START_INDEX_FILE).exists():
        return 0
    with open(START_INDEX_FILE, "r") as file:
        return int(file.read().strip())

def save_start_index(index):
    """Save the updated index for the next image to post."""
    with open(START_INDEX_FILE, "w") as file:
        file.write(str(index))

def post_mcq_to_facebook(token, image_path):
    """Post an image with a caption to Facebook using requests."""
    with open(image_path, "rb") as image:
        payload = {
            'caption': CAPTION_TEMPLATE,
            'access_token': token
        }
        files = {
            'source': image
        }
        response = requests.post(FACEBOOK_GRAPH_URL, data=payload, files=files)

    if response.status_code == 200:
        print(f"Successfully posted: {image_path}")
    else:
        print(f"Failed to post image. Status: {response.status_code}, Response: {response.text}")

def main():
    """Main function to handle the posting logic."""
    token = get_access_token()
    images = get_images()
    if not images:
        print("No images found in the folder.")
        return

    start_index = load_start_index()
    if start_index >= len(images):
        start_index = 0  # Wrap around if all images are posted

    image_path = images[start_index]
    print(f"Posting image: {image_path}")
    post_mcq_to_facebook(token, image_path)

    save_start_index(start_index + 1)

if __name__ == "__main__":
    main()
