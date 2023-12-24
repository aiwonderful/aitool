from openai import OpenAI
import requests

def generate_image(prompt):
    client = OpenAI(api_key="你的apikey")

    # 进行图片生成的 API 调用
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,  # 使用传入的提示
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # 从响应中提取图片 URL
    try:
        image_url = response.data[0].url
        print("Image URL:", image_url)
    except (IndexError, AttributeError):
        print("Failed to retrieve image URL from response.")
        return None

    # 定义下载图片的函数
    def download_image(url, path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download image: {response.status_code}")

    # 使用此函数下载图片
    image_path = 'downloaded_image.png'
    download_image(image_url, image_path)
    return image_path

# Example usage
if __name__ == "__main__":
    prompt = "A futuristic cityscape"
    image_path = generate_image(prompt)
    if image_path:
        print(f"Image saved to {image_path}")
