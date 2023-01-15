import os
from pathlib import Path
import requests

PINATA_BASE_URL = "https://app.pinata.cloud/"
end_point = "pinning/pinFileToIPFS"
file_path = "img/pug.png"
file_name = file_path.split()[-1]
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET_KEY"),
}


def main():
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        pinata_response = requests.post(
            PINATA_BASE_URL + end_point,
            files={"file": (file_name, image_binary)},
            headers=headers,
        )
        print(pinata_response.json())
