# discord関連
from discordwebhook import Discord

# DB関連
from sqlalchemy import Column
from sqlalchemy import Integer,BigInteger,String,DateTime
from sqlalchemy import func
from sqlalchemy import or_,and_

from sqlalchemy.future import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

#環境変数関連
import os
from dotenv import load_dotenv

#時刻関連
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=9), "JST")

#その他
import ping3
import requests

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
#last = session.query(NnginxLog).filter(NnginxLog.time == "")
#------

#データ取り出し

#昨日の日付
yesterday = datetime.now(JST) - timedelta(days=1)
yesterday = datetime(yesterday.year, yesterday.month, yesterday.day).replace(tzinfo=None)
#一昨日の日付
twoDaysAgo = datetime.now(JST) - timedelta(days=2)
twoDaysAgo = datetime(twoDaysAgo.year, twoDaysAgo.month, twoDaysAgo.day).replace(tzinfo=None)

#検索実行
all_data = session.query(NnginxLog).filter(and_(twoDaysAgo< NnginxLog.time, NnginxLog.time < yesterday)).count()
allow_data = session.query(NnginxLog).filter(and_(twoDaysAgo< NnginxLog.time, NnginxLog.time < yesterday, NnginxLog.status == 200)).count()
deny_data = session.query(NnginxLog).filter(and_(twoDaysAgo< NnginxLog.time, NnginxLog.time < yesterday, NnginxLog.status == 403)).count()
error_data = session.query(NnginxLog).filter(and_(twoDaysAgo< NnginxLog.time, NnginxLog.time < yesterday, NnginxLog.status == 502)).count()

#msg送信準備
all_time = yesterday.strftime("%Y年%m月%d日")
msg = f"{all_time}の集計結果\n"
msg += f"許可　　　：{allow_data} ({round((allow_data/all_data)*100,3)}%)\n"
msg += f"拒否　　　：{deny_data} ({round((deny_data/all_data)*100,3)}%)\n"
msg += f"転送エラー：{error_data} ({round((error_data/all_data)*100,3)}%)\n"
msg += f"総アクセス：{all_data}\n"
print(msg)

# for i in last:
#     print(f"id={i.id} IP={i.remote_addr}")
#------

#セッション終了
session.close()
#------