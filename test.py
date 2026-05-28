from asyncio import run
from app.services import init_db_, insert_init_data,test_get_latest_article

if __name__ == "__main__":
    # run(init_db_())
    run(test_get_latest_article())
    # run(insert_init_data())