from quart import Quart, render_template
from uvicorn import run
from sqlalchemy import select
from src.utils import Logger
from src.database import AsyncSessionLocal
from src.models import Post


log = Logger(__name__)
app = Quart(__name__)


@app.route('/', methods=['GET'])
async def index():
    async with AsyncSessionLocal() as sesseion:
        result = await sesseion.execute(
            select(Post).where(Post.is_public == True).limit(5)
        )
        post = result.scalars()
        return await render_template('home.html', r=post)


if __name__ == '__main__':
    run(app="main:app", host="0.0.0.0", port=8989)
