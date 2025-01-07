import openai
from config import config

openai.api_key = "openai-api-key"

def generate_caption(article_text: str) -> str:
    prompt = f"Summarize the following article in 2-3 sentences:\n\n{article_text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    caption = response.choices[0].text.strip()
    return caption
