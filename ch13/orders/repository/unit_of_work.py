import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv('DB_URL')

# DBURL環境変数が設定されていない場合はアプリケーションを終了
assert DB_URL is not None, 'DB_URL environment variable needed.'

class UnitOfWork:

    def __init__(self):
        self.session_maker = sessionmaker(
            bind=create_engine(DB_URL)
        )

    def __enter__(self):
        # 新しいデータベースセッションを開く
        self.session = self.session_maker()
        # UnitOfWOrkオブジェクトのインスタンスを返す
        return self

    def __exit__(self, exc_type, exc_val, traceback):


        # 例外が発生したかチェック
        if exc_type is not None:
            # 例外が発生した場合はトランザクションをロールバック
            self.rollback()
            self.session.close()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

