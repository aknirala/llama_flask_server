import requests
import json
from PIL import Image
import io

def send_request(role, content):
    url = "http://localhost:5000/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "role": role,
        "content": content
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Response from server:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to get response. Status code: {response.status_code}")

def main():
    content = [
        {"text": "How you doing?"}
    ]
    send_request("user", content)

    # # Example 1: Image and text
    # img_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac\xf8\xff\xff?\x00\x05\xfe\x02\xfeA\x0b\x0f\x00\x00\x00\x00IEND\xaeB`\x82'
    # content1 = [
    #     {"data": img_data},
    #     {"text": "Describe this image in two sentences"}
    # ]
    # send_request("user", content1)

    # Example 2: Text only
    content2 = [
        {"text": "what is the recipe of mayonnaise in two sentences?"}
    ]
    send_request("user", content2)

    # # Open the image using Pillow
    # with open(THIS_DIR / "resources/dog.jpg", "rb") as f:
    #     img = f.read()

    # # Optionally, process the image with Pillow
    # image = Image.open(io.BytesIO(img))
    # # You can now manipulate the image if needed, e.g., resize, convert, etc.

if __name__ == "__main__":
    main() 