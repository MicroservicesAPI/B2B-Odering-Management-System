import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PROJECT_NAME = os.getenv("PROJECT_NAME")
    VERSION = os.getenv("VERSION")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


class LocalRunConfig(Config):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"


class ProdRunConfig(Config):
    SQLALCHEMY_DATABASE_URL = os.getenv("PROD_DATABASE_URL")


# will be use depending on the run-context
app_config = Config()
local_run_config = LocalRunConfig()
prod_run_config = ProdRunConfig()