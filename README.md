# Локальный AI чат-бот (Модель Saiga 8B Q3_K_S)
Полная реализация локального чат-бота с веб-интерфейсом для модели Saiga 8B Q3_K_S, оптимизированная под Ubuntu 24, Intel N100 + 8GB RAM + NVMe.

# Структура проекта

~/llm/  
├── chatbot_web.py            # FastAPI сервер + логика генерации  
├── saiga_8b.Q3_K_S.gguf      # Квантованная модель 3.5GB  
└── templates / chat.html     # Интерфейс на HTML/JS  

# Установка
ssh ваш_пользователь@ip_адрес
mkdir -p ~/llm && cd ~/llm
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv wget git build-essential
python3 -m venv venv
source venv/bin/activate
pip install llama-cpp-python fastapi uvicorn sse-starlette pydantic

# Скачать модель (3.5GB)
wget https://huggingface.co/IlyaGusev/saiga_yandexgpt_8b_gguf/resolve/main/saiga_yandexgpt_8b.Q3_K_S.gguf -O saiga_8b.Q3_K_S.gguf

# Установка зависимостей (CPU-only)
pip install fastapi uvicorn jinja2 python-multipart
mkdir -p templates static

python3 chatbot_web.py --workers 1 --limit-max-requests 100

После запуска откройте: http://localhost:8000

Ключевые параметры модели
python
llm = Llama(
    model_path="saiga_8b.Q3_K_S.gguf",
    n_ctx=2048,          # Макс. длина контекста
    n_threads=4,         # По количеству ядер N100
    n_batch=512,         # Для баланса скорости/памяти
    use_mlock=True,      # Фикс модели в RAM
    n_gpu_layers=0       # Только CPU
)

Особенности работы
Генерация: ~2-5 токенов/сек на N100
Память: ~5GB RAM в пике
Поддержка русского: Оптимизирована для диалогов
Артефакты: Возможны из-за агрессивного квантования
