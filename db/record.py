from sqlalchemy import Column, Integer, DateTime, func, Text, String

from db import Base


class Record(Base):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    winner = Column(String(10), nullable=False, comment="胜者")
    black = Column(String(20), nullable=False, comment="黑棋玩家")
    white = Column(String(20), nullable=False, comment="白棋玩家")
    data = Column(Text, nullable=False, comment="对局数据")
    like = Column(Integer, default=0, nullable=True, comment="获赞数")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=False, comment="结束时间")

    create_time = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="修改时间")

    def __init__(self, winner=None, black=None, white=None, data=None):
        self.winner = winner
        self.black = black
        self.white = white
        self.data = data

    def __repr__(self):
        return f'<Record {self.id!r}>'

    def serialize(self):
        return {
            'id': self.id,
            'winner': self.winner,
            'black': self.black,
            'white': self.white,
            'data': self.data,
            'like': self.like,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'create_time': self.create_time,
            'update_time': self.update_time,
        }
