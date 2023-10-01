import asyncio
from typing import List, Optional

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship

from sqlorm.core import Base

engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=True)
AsyncSession = async_sessionmaker(engine)


@Base.to_pydantic()
@Base.to_pydantic(exclude=["id"], namespace="UserPublic")
@Base.to_pydantic(exclude=["addresses"], namespace="UserOnly")
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


@Base.to_pydantic()
class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


Base.prepare()


class AddressPublic(Address.model()):
    new_address: str = None


async def async_main() -> None:

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession() as session:
        async with session.begin():
            spongebob = User(
                name="spongebob",
                fullname="Spongebob Squarepants",
                addresses=[Address(email_address="spongebob@sqlalchemy.org")],
            )
            sandy = User(
                name="sandy",
                fullname="Sandy Cheeks",
                addresses=[
                    Address(email_address="sandy@sqlalchemy.org"),
                    Address(email_address="sandy@squirrelpower.org"),
                ],
            )
            patrick = User(name="patrick", fullname="Patrick Star")

            session.add_all([spongebob, sandy, patrick])
        stmt = select(User, Address).options(joinedload(User.addresses))
        results = await session.execute(stmt)
        results = results.unique()
        results = [r for r in results]
        print(results[0][0].orm("UserOnly"))


if __name__ == "__main__":
    asyncio.run(async_main())
