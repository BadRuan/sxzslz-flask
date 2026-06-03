from asyncio import run
from app.database import init_db

async def main() -> None:
    await init_db()

if __name__ == "__main__":
    run(main())