from openai import OpenAI
import base64
import requests


class DVAI:
    """
    Digital Vision Artificial Intelligence
    """

    def __init__(self, key: str):
        self.api_key = key

        self.client = OpenAI(
            api_key=key,
        )

    def gpt_with_vision_by_url(self, image_url, context: str):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": context},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
        )

        return response.choices[0].message.content

    def gpt_with_vision_by_base64(self, image_path: str, context: str):
        base64_image = self.encode_image(image_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": context},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 1000,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )

        return response.json()["choices"][0]["message"]["content"]

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")