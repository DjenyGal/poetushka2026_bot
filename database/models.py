import os
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func

# Если существует директория /data (на сервере Amvera) — используем её,
# иначе (локальный запуск) — используем текущую папку проекта
DB_DIR = "/data" if os.path.exists("/data") else "."
DB_PATH = os.path.join(DB_DIR, "orders.db")

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]

    name: Mapped[str] = mapped_column(default="")
    age: Mapped[str] = mapped_column(default="")
    relationship: Mapped[str] = mapped_column(default="")
    occasion: Mapped[str] = mapped_column(default="")
    tone: Mapped[str] = mapped_column(default="")
    length: Mapped[str] = mapped_column(default="")
    price: Mapped[int] = mapped_column(default=0)
    details: Mapped[str] = mapped_column(default="")
    secrets: Mapped[str] = mapped_column(default="")
    signature: Mapped[str] = mapped_column(default="")

    delivery_method: Mapped[str] = mapped_column(default="")
    email: Mapped[str] = mapped_column(nullable=True)

    variant_1: Mapped[str] = mapped_column(default="")
    variant_2: Mapped[str] = mapped_column(default="")
    chosen_variant: Mapped[int] = mapped_column(nullable=True)

    is_paid: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)