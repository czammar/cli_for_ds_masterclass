from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DETERMINISTIC_ANS: bool
    BOT_DATA_PATH: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
        )


# Instantiate the settings class to load values from .env
bot_config = Config()  # type: ignore
