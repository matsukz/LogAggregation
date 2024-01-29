# discord関連
from discordwebhook import Discord

# DB関連
from sqlalchemy import Column
from sqlalchemy import Integer,BigInteger,String,DateTime
from sqlalchemy import func

from sqlalchemy.future import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

#環境変数関連
import os
from dotenv import load_dotenv

#その他
import ping3
import requests
import datetime

#環境変数読み込み
load_dotenv()
db_name = os.environ["db_name"]
db_user = os.environ["db_user"]
db_password = os.environ["db_passwd"]
db_address = os.environ["db_address"]
#-------

#DB接続
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_address}/{db_name}?charset=utf8")
Base = declarative_base()
#-------

#テーブル情報
class NnginxLog(Base):
    __tablename__ = "nginx_access_log"
    id = Column("id",BigInteger,primary_key=True)
    time = Column("time",DateTime)
    remote_addr = Column("remote_addr",String)
    country = Column("country",String)
    status = Column("Status",Integer)
#------

#セッション作成
Session = sessionmaker(bind=engine)
session = Session()
#------

#SQL実行
last = session.query(NnginxLog).limit(3).all()
#------

#データ取り出し
for i in last:
    print(f"id={i.id} IP={i.remote_addr}")
#------

#セッション終了
session.close()
#------


print("OK")