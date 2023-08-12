from fastapi import FastAPI
from sqlmodel import SQLModel
from urllib.parse import quote

from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from fastapi_amis_admin.amis.components import Form
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.fields import Field


from pydantic import BaseModel

import sqlalchemy

app = FastAPI()


DB_USERNAME = "postgres"
DB_PASSWORD = "qwe123!@#"
DB_HOST = "localhost"
DB_PORT = 5432
DB_DATABASE = "postgres"

SQLURL = sqlalchemy.engine.URL.create(
    "postgresql+asyncpg",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
)


site = AdminSite(settings=Settings(database_url_async=str(SQLURL)))


class PageDevelopers(SQLModel, table=True):
    __tablename__ = "developers"
    __table_args__ = {"schema": "page"}
    id: int = Field(default=None, primary_key=True, nullable=False, title="Index")
    col1: str = Field(default="", title="col1")
    col2: str = Field(default="", title="col2")


@site.register_admin
class CategoryAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = "Category"
    model = PageDevelopers


site.mount_app(app)


# @app.on_event("startup")
# async def startup():
#     await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, debug=True)
