# from pydantic import BaseSettings
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str


    class Config:
        env_file = '.env'


settings = Settings()
# print(settings.dict())
# postgres://eclipse:jDMmNpxz1u2EhnK0iIBn0BiUjKlxDtNy@dpg-chos72qk728ivvull1f0-a.oregon-postgres.render.com/eclipse_fastapi