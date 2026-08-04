import requests
import os

# Create folder if not exists
folder = "static/images"
os.makedirs(folder, exist_ok=True)

images = {
    "logo.png": "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
    "hero.png": "https://cdn-icons-png.flaticon.com/512/4712/4712027.png",
    "ai.png": "https://cdn-icons-png.flaticon.com/512/4712/4712100.png",
    "result.png": "https://cdn-icons-png.flaticon.com/512/1828/1828640.png",
    "bg.jpg": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3"
}

for filename, url in images.items():
    try:
        response = requests.get(url)

        if response.status_code == 200:
            path = os.path.join(folder, filename)

            with open(path, "wb") as file:
                file.write(response.content)

            print(f"Downloaded: {filename}")

        else:
            print(f"Failed: {filename}")

    except Exception as e:
        print(filename, e)

print("All images downloaded!")