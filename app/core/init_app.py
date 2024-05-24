from datetime import datetime

import httpx
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.expressions import Q
from app.api import api_router
from app.controllers.user import UserCreate, user_controller
from app.controllers.monitor import MonitorSetCreate, monitorset_controller, monitor_controller
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
from ..api.v1.monitor.monitor import fetch_monitor_data
from ..log import logger
from ..schemas.monitor import MonitorCreate


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
                enable="true"
            )
        )
        await monitorset_controller.create(
            MonitorSetCreate(
                sn="JX000001",
                api_url="https://app.autosort.cn/api/dpc/realtime/mg",
                fetch_interval=30,
                enable="true"
            )
        )
    logger.info(f"默认监控配置已存在,启动后台任务")
    await run_monitor_task()


async def run_monitor_task():
    logger.info(f"Interval Background Task scheduling")

    q = Q(enable="true")
    monitor_sets = await monitorset_controller.model.filter(q).all()
    for m_set in monitor_sets:
        logger.info(f"定时任务: {m_set}")
        interval_int = int(m_set.fetch_interval)
        IntervalTaskScheduler.add_job(fetch_monitor_data, IntervalTrigger(seconds=interval_int), id=str(m_set.id),
                                      args=[m_set])
    IntervalTaskScheduler.start()


async def fetch_monitor_data(m_set: MonitorSet):
    url = f"{m_set.api_url}?sn={m_set.sn}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/124.0.0.0 Safari/537.36'
    }
    # Corrected the query parameter syntax
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            text = response.text
            logger.error(f"Error fetching monitor data: {response.status_code}, {text}")
            return None
        logger.info(f"Job excute at: {datetime.now()}, url:{url}, response: {response.json()['data']}")

        data = response.json()['data']
        if isinstance(data, list):
            for d in data:
                sn = d.get('sn')
                content = d.get('content')
                report_time = d.get('reportTime')
                start_time = d.get('startTime')
                end_time = d.get('endTime')
                monitor_his = await monitor_controller.model.filter(sn=sn, content=content,
                                                                    report_time=report_time, start_time=start_time,
                                                                    end_time=end_time).exists()

                if not monitor_his:
                    logger.info(f"发现新监控记录,保存更新中...{d}")

                    await monitor_controller.create(MonitorCreate(
                        sn=d['sn'],
                        content=d['content'],
                        report_time=d['reportTime'],
                        start_time=d['startTime'],
                        end_time=d['endTime']
                    ))
        elif isinstance(data, dict):
            sn = data.get('sn')
            content = data.get('content')
            report_time = data.get('reportTime')
            start_time = data.get('startTime')
            end_time = data.get('endTime')
            monitor_his = await monitor_controller.model.filter(sn=sn, content=content,
                                                                report_time=report_time, start_time=start_time,
                                                                end_time=end_time).exists()

            if not monitor_his:
                logger.info(f"发现新监控记录,保存更新中...{data}")

                await monitor_controller.create(MonitorCreate(
                    sn=data['sn'],
                    content=data['content'],
                    report_time=data['reportTime'],
                    start_time=data['startTime'],
                    end_time=data['endTime']
                ))


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
