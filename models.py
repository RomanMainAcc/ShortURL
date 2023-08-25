from datetime import datetime

from sqlalchemy import MetaData, Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


metadata = Base.metadata


class LinkTable(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, index=True)
    short_link = Column(String, index=True)
    total_clicks = Column(Integer, default=0, index=True)
    creation_date = Column(TIMESTAMP, default=datetime.utcnow)
