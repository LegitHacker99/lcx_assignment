# from huggingface_hub import InferenceClient

# import requests
# import json

# from config import config

# model_repo_id = config.MODEL_REPO_ID
# hf_key = config.HF_KEY

# llm_client = InferenceClient(
#     model=model_repo_id,
#     timeout=120,
#     token=hf_key
# )

# def call_llm(inference_client: InferenceClient, prompt: str):
#     response = inference_client.post(
#         json={
#             "imputs": prompt,
#             "parameters": {"max_new_tokens": 100, "temperature": 0.7},
#             "task": "text-generation",
#         }
#     )

#     return json.loads(response.decode())[0]["generated_text"]

# def generate_caption_with_llm(content: str) -> str:
#     """
#     Query the LLM API (Hugging Face) to generate a short caption for the given content.
    
#     Args:
#         content (str): The article content for which the caption is to be generated.
        
#     Returns:
#         str: The generated caption.
#     """
    
#     try:
#         print("BIGGGG <><><><><>>>", content)
#         content = f"Generate a short 10 word caption for the following content: {content}"
#         response = call_llm(llm_client, content)
#         print("BIGGGG <><><><><>>>", response)
    
#     except requests.exceptions.RequestException as e:
#         print(f"Error querying the LLM API: {e}")
#         return None


from huggingface_hub import InferenceClient
import json
from config import config

# Model and API setup from config
model_repo_id = config.MODEL_REPO_ID  # For example, "microsoft/Phi-3.5-mini-instruct"
hf_key = config.HF_KEY  # Your Hugging Face API key

# Initialize InferenceClient
llm_client = InferenceClient(
    model=model_repo_id,
    timeout=120,
    token=hf_key
)

def call_llm(inference_client: InferenceClient, prompt: str):
    try:
        response = inference_client.post(
            json={
                "inputs": prompt,
                "parameters": {"max_new_tokens": 100, "temperature": 0.7},
                "task": "text-generation",
            }
        )

        return json.loads(response.decode())[0]["generated_text"]
    except Exception as e:
        print(f"Error during inference: {e}")
        return None

def generate_caption_with_llm(content: str) -> str:
    """
    Query the LLM API (Hugging Face) to generate a short caption for the given content.
    
    Args:
        content (str): The article content for which the caption is to be generated.
        
    Returns:
        str: The generated caption.
    """
    
    try:
        prompt = f"Generate a short 10 word caption for the following content: {content}"
        caption = call_llm(llm_client, prompt)
        if caption:
            caption = caption.split("\n")[1] if caption.split("\n")[1] not in ("", " ") else caption.split("\n")[2]
        
        return caption
    
    except Exception as e:
        print(f"Error querying the LLM API: {e}")
        return None
