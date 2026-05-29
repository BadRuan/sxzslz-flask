from asyncio import run
from app.services import init_db_, insert_init_data, test_get_latest_article, test_get_public_categories

if __name__ == "__main__":
    # run(init_db_())
    # run(test_get_latest_article())
    run(test_get_public_categories())
    # run(insert_init_data())