import asyncio

import httpx
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.expressions import Q
from app.api import api_router
from app.controllers.user import UserCreate, user_controller
from app.controllers.monitor import MonitorSetCreate, monitorset_controller
from apscheduler.triggers.interval import IntervalTrigger

from app.core.exceptions import (
    DoesNotExist,
    DoesNotExistHandle,
    HTTPException,
    HttpExcHandle,
    IntegrityError,
    IntegrityHandle,
    RequestValidationError,
    RequestValidationHandle,
    ResponseValidationError,
    ResponseValidationHandle,
)
from app.models.admin import Menu, MonitorSet
from app.schemas.menus import MenuType
from app.settings.config import settings
from .bgtask import IntervalTaskScheduler

from .middlewares import BackGroundTaskMiddleware
from ..log import logger


def make_middlewares():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
        ),
        Middleware(BackGroundTaskMiddleware),
    ]
    return middleware


def register_db(app: FastAPI, db_url=None):
    register_tortoise(
        app,
        # db_url='sqlite://db.sqlite3',
        # modules={'models':['app.models', "aerich.models"]},
        config=settings.TORTOISE_ORM,
        generate_schemas=True,
    )


def register_exceptions(app: FastAPI):
    app.add_exception_handler(DoesNotExist, DoesNotExistHandle)
    app.add_exception_handler(HTTPException, HttpExcHandle)
    app.add_exception_handler(IntegrityError, IntegrityHandle)
    app.add_exception_handler(RequestValidationError, RequestValidationHandle)
    app.add_exception_handler(ResponseValidationError, ResponseValidationHandle)


def register_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)


async def init_superuser():
    user = await user_controller.model.exists()
    if not user:
        await user_controller.create(
            UserCreate(
                username="admin",
                email="admin@admin.com",
                password="123456",
                is_active=True,
                is_superuser=True,
            )
        )


async def init_fetch_monitor_data():
    monitor_set = await monitorset_controller.model.exists()
    if not monitor_set:
        logger.info(f"默认监控配置不存在,初始化监控配置")

        await monitorset_controller.create(
            MonitorSetCreate(
                sn="JX000001",
                api_url="https://app.autosort.cn/api/dpc/history/mg",
                fetch_interval=30,
                enable=True
            )
        )
        await monitorset_controller.create(
            MonitorSetCreate(
                sn="JX000001",
                api_url="https://app.autosort.cn/api/dpc/realtime/mg",
                fetch_interval=30,
                enable=True
            )
        )
    logger.info(f"默认监控配置已存在,启动后台任务")
    await run_monitor_task()


async def run_monitor_task():
    logger.info(f"Interval Background Task scheduling")

    q = Q(enable=True)
    monitor_sets = await monitorset_controller.model.filter(q).all()
    for m_set in monitor_sets:
        # job = IntervalTaskScheduler.get_job(str(m_set.id))
        # if job:
        #     # Remove the job from the scheduler
        #     logger.info(f"Task ID: {m_set.id} is running, and do cancel for next check.")
        #     IntervalTaskScheduler.remove_job(m_set.id)
        #     continue
        logger.info(f"定时任务: {m_set}")
        IntervalTaskScheduler.add_job(fetch_monitor_data, IntervalTrigger(seconds=30), id=str(m_set.id), args=[m_set])
    IntervalTaskScheduler.start()


async def fetch_monitor_data(m_set: MonitorSet):
    url = f"{m_set.api_url}?sn={m_set.sn}"  # Corrected the query parameter syntax
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            text = response.text
            logger.error(f"Error fetching monitor data: {response.status_code}, {text}")
            return None
        print(response.json())
        return response.json()


async def init_menus():
    menus = await Menu.exists()
    if not menus:
        parent_menu = await Menu.create(
            menu_type=MenuType.CATALOG,
            name="系统管理",
            path="system",
            order=1,
            parent_id=0,
            icon="carbon:gui-management",
            is_hidden=False,
            component="Layout",
            keepalive=True,
            redirect="/system/user",
        )
        children_menu = [
            Menu(
                menu_type=MenuType.MENU,
                name="用户管理",
                path="user",
                order=1,
                parent_id=parent_menu.id,
                icon="material-symbols:person-outline-rounded",
                is_hidden=False,
                component="/system/user",
                keepalive=True,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="角色管理",
                path="role",
                order=2,
                parent_id=parent_menu.id,
                icon="carbon:user-role",
                is_hidden=False,
                component="/system/role",
                keepalive=True,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="菜单管理",
                path="menu",
                order=3,
                parent_id=parent_menu.id,
                icon="material-symbols:list-alt-outline",
                is_hidden=False,
                component="/system/menu",
                keepalive=True,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="API管理",
                path="api",
                order=4,
                parent_id=parent_menu.id,
                icon="ant-design:api-outlined",
                is_hidden=False,
                component="/system/api",
                keepalive=True,
            ),
        ]
        await Menu.bulk_create(children_menu)
