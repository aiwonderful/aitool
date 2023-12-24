from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from story_generator import generate_story, StoryRequest
from audio_generator import generate_audio
from image_generator import generate_image
import openai
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# 挂载静态文件夹
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", { "request": request })


@app.post("/generate_story")
async def handle_generate_story(request: StoryRequest):
    return generate_story(request)


@app.post("/generate_audio")
async def handle_generate_audio(request: Request):
    story_text = await request.body()
    story_text = story_text.decode("utf-8")  # 将字节流解码为字符串
    # 使用 story_text 生成音频
    # 返回音频文件的路径或URL等...
    audio_url = generate_audio(story_text)
    if audio_url:
        return {"audioUrl": audio_url}
    else:
        return {"error": "音频生成失败"}




@app.post("/generate_image")
async def handle_generate_image(request: Request):
    prompt = await request.text()
    return generate_image(prompt)


if __name__ == "__main__":
    
    uvicorn.run("main:app", port=8000, reload=True, log_level="debug")
