import requests
import base64

url = "http://127.0.0.1:5000/generate"

# Example message (one dialog)
messages = [
    {"role": "user", "content": "I am going to Paris, what should I see?"},
#    {"role": "assistant", "content": "Visit the Eiffel Tower and the Louvre Museum."},
#    {"role": "user", "content": "What is so great about #1?"}
]

data = {"messages": messages}

response = requests.post(url, json=data)

print(response.json())  # Print the response from the server


# Load and encode image
with open("models/scripts/resources/dog.jpg", "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

# Example messages (one dialog)
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "data": img_base64},
            {"type": "text", "text": "Describe this image in two sentences."}
        ]
    }
]

data = {"messages": messages}

response = requests.post(url, json=data)

print(response.json())  # Print the response from the server
