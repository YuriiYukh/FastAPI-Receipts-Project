# # app/core/config.py
# import os

# from pydantic_settings import BaseSettings

# from dotenv import load_dotenv

# load_dotenv()


# class Settings(BaseSettings):
#     DATABASE_URL: str = os.environ.get('DATABASE_URL')
#     JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY')
#     JWT_ALGORITHM: str = os.environ.get('JWT_ALGORITHM')
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
#         os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

#     class Config:
#         env_file = '.env'


# settings = Settings()
