import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Orderservice of the B2B ordering system")
    VERSION = os.getenv("VERSION", "0.1.0")


class LocalRunConfig(Config):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test_order.db"


class ProdRunConfig(Config):
    SQLALCHEMY_DATABASE_URL = os.getenv("PROD_DATABASE_URL")


# will be use depending on the run-context
app_config = Config()
local_run_config = LocalRunConfig()
prod_run_config = ProdRunConfig()