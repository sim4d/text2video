import requests
from bs4 import BeautifulSoup
import os

def save_images(url, save_dir="images"):
    """
    Fetches the wechat article content, extracts image URL, and saves them to a directory.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch webpage: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all img tags
    images = soup.findAll('img', {'class': 'rich_pages wxw-img'})

    # Create the save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    for filename in os.listdir(save_dir):
        file_path = os.path.join(save_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f'Deleted file: {file_path}')

    # loop through each image and download it
    iter = 1
    saved_image = False
    for image in images:
        image_url = image.get('src')
        image_url2 = image.get('data-src')
        if not image_url:
            if not image_url2:
                print("ERR: both urls are NONE")
                continue # skip if image URL is missing
            image_url = image_url2

        # print(image_url)
        data_type = str(image.get('data-type'))
        filename = str(iter) + "." + data_type
        iter = iter + 1

        # download the image and save it
        image_response = requests.get(image_url, stream=True)
        if image_response.status_code == 200:
            with open(os.path.join(save_dir, filename), 'wb') as f:
                for chunk in image_response.iter_content(1024):
                    f.write(chunk)

            print(f"Image saved: {filename}")
            saved_image = True
        else:
            print(f"Failed to download image: {image_url}")

    return saved_image


if __name__ == "__main__":
    # Replace with target webpage URL
    url = 'https://mp.weixin.qq.com/s/t8c07-3gKjKXW4MOIwW5aQ'

    # Replace with the desired save directory
    save_dir = "images"

    try:
        save_images(url, save_dir)
    except Exception as e:
        print(f"Error: {e}")



