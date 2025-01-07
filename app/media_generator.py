import openai
from PIL import Image
from io import BytesIO
import requests

openai.api_key = "openai-api-key"

def generate_image(article_text: str) -> Image:
    prompt = f"Create an image based on this article content:\n\n{article_text}"
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))
    return image
