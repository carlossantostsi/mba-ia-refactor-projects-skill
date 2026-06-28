import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "minha-chave-super-secreta-123")
    DEBUG = os.getenv("DEBUG", "True").lower() in {"1", "true", "yes", "on"}
    DB_PATH = os.getenv("DB_PATH", "loja.db")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
