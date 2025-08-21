import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-change-this-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///text_analysis.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here-change-this-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 60 * 60  # 24小时
    
    # LLM配置
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'ollama')  # ollama, openai, local
    
    # Ollama配置
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5:7b')  # 推荐使用qwen2.5:7b或llama3.1:8b
    
    # OpenAI配置（备用）
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # 本地模型配置
    LOCAL_MODEL_PATH = os.getenv('LOCAL_MODEL_PATH', './models')
    LOCAL_MODEL_NAME = os.getenv('LOCAL_MODEL_NAME', 'chatglm3-6b')
    
    # 分析配置
    MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', '10000'))
    DEFAULT_SUMMARY_LENGTH = int(os.getenv('DEFAULT_SUMMARY_LENGTH', '200'))
    DEFAULT_KEYWORDS_COUNT = int(os.getenv('DEFAULT_KEYWORDS_COUNT', '10'))
