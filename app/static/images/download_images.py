import requests
import os

def download_image(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

# URLs for the images
robot_url = "https://cdn.pixabay.com/photo/2017/05/10/19/29/robot-2301646_1280.jpg"
books_url = "https://cdn.pixabay.com/photo/2016/09/08/22/43/books-1655783_1280.jpg"

# Ensure the directory exists
os.makedirs("app/static/images", exist_ok=True)

# Download the images
download_image(robot_url, "app/static/images/robot-bg.jpg")
download_image(books_url, "app/static/images/books-bg.jpg") 