import requests
import openai
import os
def generate_audio(text):
    openai.api_key = '你的APIkey'

    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {openai.api_key}",
        },
        json={
            "model": "tts-1-1106",
            "input": text,  # 使用传入的故事文本
            "voice": "onyx",
        },
    )
    # 检查响应状态并处理数据
   
    if response.status_code == 200:
        audio_filename = "output.mp3"
        audio_filepath = os.path.join("static", audio_filename)
        with open(audio_filepath, "wb") as audio_file:
            audio_file.write(response.content)
        return f"/static/{audio_filename}"  # 返回音频文件的相对 URL
    else:
        print("Error:", response.status_code, response.text)
        return None
