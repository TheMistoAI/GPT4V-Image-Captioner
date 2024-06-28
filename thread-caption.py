import os
import threading
from lib.Api_Utils import use_gpt_model, use_claude_model  # Assuming these functions are defined in Api_Utils

# Hardcoded API configurations
API_KEY_GPT = 'your_gpt_api_key'
API_URL_GPT = 'your_gpt_api_url'
API_KEY_CLAUDE = 'your_claude_api_key'
API_URL_CLAUDE = 'your_claude_api_url'

def process_image(image_path, model_type):
    """Process an image and save the caption to a text file."""
    output_filename = f"{os.path.splitext(image_path)[0]}.txt"
    if model_type == 'gpt':
        caption = use_gpt_model(image_path, API_KEY_GPT, API_URL_GPT)
    else:
        caption = use_claude_model(image_path, API_KEY_CLAUDE, API_URL_CLAUDE)
    with open(output_filename, 'w') as file:
        file.write(caption)
    print(f"Processed {image_path} using {model_type} model.")

def process_directory(directory_path):
    """Process all images in the directory using multithreading."""
    images = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith(('.png', '.jpg', '.jpeg'))]
    i = 0
    while i < len(images):
        threads = []
        # Process two images at a time, one with GPT and one with Claude
        if i < len(images):
            thread_gpt = threading.Thread(target=process_image, args=(images[i], 'gpt'))
            threads.append(thread_gpt)
            thread_gpt.start()
            i += 1
        if i < len(images):
            thread_claude = threading.Thread(target=process_image, args=(images[i], 'claude'))
            threads.append(thread_claude)
            thread_claude.start()
            i += 1
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        process_directory(sys.argv[1])
    else:
        print("Please provide the directory path as an argument.")
