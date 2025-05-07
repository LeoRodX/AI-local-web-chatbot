import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from llama_cpp import Llama
from pathlib import Path
import uvicorn

# Конфигурация
MODEL_PATH = "saiga_8b.Q3_K_S.gguf"
NVME_CACHE_DIR = os.path.expanduser("~/llm/cache")  # Новый путь
os.makedirs(NVME_CACHE_DIR, exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Инициализация модели
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    n_batch=128,
    n_gpu_layers=0,
    use_mmap=True,
    cache=True,
    cache_dir=NVME_CACHE_DIR
)

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/api/chat")
async def chat_api(request: Request):
    data = await request.json()
    prompt = f"<s>user\n{data['message']}</s>\n<s>bot\n"
    
    response = llm(
        prompt,
        max_tokens=150,
        temperature=0.7,
        stop=["</s>"]
    )
    
    return {"response": response['choices'][0]['text']}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,  # Для экономии RAM
        log_level="info"
    )