import os
import threading
from lib.Api_Utils import openai_api, claude_api  # Assuming these functions are defined in Api_Utils

# Hardcoded API configurations
API_KEY = 'sk-W39pXOPIBceb804110faT3BlBKFJ8c8F0987355E47908C93'
API_URL_GPT = 'https://apic.ohmygpt.com/v1/chat/completions'
API_URL_CLAUDE = 'https://apic.ohmygpt.com/v1/messages'

def process_image(image_path, model_type):
    """Process an image and save the caption to a text file."""
    prompt = "As an AI image tagging expert, please provide precise tags for these images to enhance the CLIP model's understanding of the content. Employ succinct keywords or phrases, steering clear of elaborate sentences and extraneous conjunctions. Prioritize the tags by relevance. Your tags should capture key elements such as the image type(such as photo, render, paint, etc.), the main subject, setting, artistic style, composition, image quality, color tone, filter, camera specifications, shot angle, photography techniques, light, lens language, picture texture, perspective, and any other tags crucial for the image. If the main object is humans,  be sure to include the following specific details: skin color, gender, race, attire, actions, pose, expressions, accessories, makeup, composition type, and age. For example: 'two dark/Brown/light skinned Asian/African/Latin young women standing on a rock with an angry facial expression.' For other image categories, apply appropriate and common descriptive tags as well. Recognize and tag any celebrities, well-known landmarks, or IPs if featured in the image. Your tags should be accurate, and non-duplicative. Try to re-organize your response into one brief description of the image followed by other tags (don't include tags already in the previous sentence). Make the response within 77 tokens. An example response is: 'A dark-skinned man wearing sunglasses and a grey oversized shirt with red text on the sleeve, standing against a gradient blue and white background. photo, male, dark skin, sunglasses, grey shirt, oversized clothing, red text, gradient background, blue, white, fashion, modern, casual, studio shot, minimalistic, cool tone, standing, serious expression.' Exceptional tagging will be rewarded with $10 per image."
    if model_type == 'gpt':
        # image_path, prompt, api_key, api_url, quality=None, timeout=10, model="claude-3-5-sonnet-20240620"
        openai_api(image_path, prompt, API_KEY, API_URL_GPT, quality="low", model="gpt-4o-2024-05-13")
    else:
        claude_api(image_path, prompt, API_KEY, API_URL_CLAUDE, quality="low", model="claude-3-5-sonnet-20240620")

def process_directory(directory_path):
    """Process all images in the directory using multithreading."""
    images = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith(('.png', '.jpg', '.jpeg'))]
    i = 0
    while i < len(images):
        threads = []
        # Process two images at a time, one with GPT and one with Claude
        if i < len(images):
            output_filename = f"{os.path.splitext(images[i])[0]}.txt"
            if not os.path.exists(output_filename):  # Check if the txt file already exists
                thread_gpt = threading.Thread(target=process_image, args=(images[i], 'gpt'))
                threads.append(thread_gpt)
                thread_gpt.start()
            i += 1
        if i < len(images):
            output_filename = f"{os.path.splitext(images[i])[0]}.txt"
            if not os.path.exists(output_filename):  # Check if the txt file already exists
                thread_claude = threading.Thread(target=process_image, args=(images[i], 'claude'))
                threads.append(thread_claude)
                thread_claude.start()
            i += 1
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    directory_path = r'C:\Users\yuhan\Downloads\prompt_test'
    process_directory(directory_path)
