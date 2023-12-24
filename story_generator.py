# story_generator.py
from pydantic import BaseModel
import requests

CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = "sk3"

class StoryRequest(BaseModel):
    theme: str

def generate_story(request: StoryRequest):
    # Constructing a prompt that guides the model to generate a long story
    prompt = f"Write a detailed story about {request.theme}. The story should be engaging and approximately 15 words in English."
    print(prompt)
    response = requests.post(
        CHATGPT_API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "gpt-4-1106-preview",
            "messages": [{"role": "system", "content": prompt}],  # Correct request format
            "temperature": 0.8,
            "max_tokens": 15  # Maximum token limit, adjust as needed
        }
    )
    print(response.json())
    # Error handling
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    return response.json()

# Example usage
if __name__ == "__main__":
    theme = input("Enter the theme for the story: ")
    request_data = StoryRequest(theme=theme)
    story_response = generate_story(request_data)

    # 打印整个响应内容，以便检查结构
    print(story_response)

    # 如果返回的结构是预期的，打印故事
    if 'choices' in story_response and story_response['choices']:
        story = story_response['choices'][0].get('message', {}).get('content')
        if story:
            print(story)
        else:
            print("No story content found in the response.")
    else:
        print("Unexpected response structure.")
