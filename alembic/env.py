from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config  # 🔥 Важно: async версия
from db.database import Base
import db.models
from alembic import context
import os
from dotenv import load_dotenv
import asyncio  # Для запуска асинхронного кода

load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("DATABASE_URL")

    if url:
        config.set_main_option("sqlalchemy.url", url)
        
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Новая вспомогательная функция для синхронного контекста внутри async
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


# Асинхронная версия run_migrations_online
async def run_migrations_async():
    url = os.getenv("DATABASE_URL")
    
    connectable = async_engine_from_config(
        {"sqlalchemy.url": url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        #Ключевой момент: run_sync позволяет запускать синхронный код внутри async
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Запускаем асинхронные миграции через asyncio.run()"""
    asyncio.run(run_migrations_async())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()