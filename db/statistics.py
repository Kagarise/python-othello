from sqlalchemy import Column, Integer, String, DateTime, func

from db import Base


class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="统计ID")

    player_type = Column(String(20), nullable=False, comment="游玩类型")
    total = Column(Integer, default=0, nullable=False, comment="总计数")
    win = Column(Integer, default=0, nullable=False, comment="胜场计数")
    draw = Column(Integer, default=0, nullable=False, comment="平局计数")
    
    create_time = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="修改时间")

    def __init__(self, player_type=None):
        self.player_type = player_type
        self.total = 0
        self.win = 0
        self.draw = 0

    def __repr__(self):
        return f'<Statistics {self.player_type!r}>'

    def serialize(self):
        return {
            'player_type': self.player_type,
            'total': self.total,
            'win': self.win,
            'draw': self.draw
        }
