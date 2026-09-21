"""
Application settings, loaded from environment variables / .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Vector store ---
    vector_store_dir: str = "data/vector_store"
    collection_name: str = "documents"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    # --- LLM (Ollama) ---
    ollama_model: str = "llama3.2"
    ollama_host: str = "http://localhost:11434"

    # --- Retrieval ---
    top_k: int = 4

    # --- API / CORS ---
    frontend_origin: str = "http://localhost:8501"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
