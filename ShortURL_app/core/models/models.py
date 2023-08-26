from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP

from ShortURL_app.core.database.database import Base

# from pydantic import HttpUrl as PydanticHttpUrl
#
#
# # class HttpUrl(PydanticHttpUrl):
# #     pass
#

metadata = Base.metadata


class LinkTable(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    # link = Column(HttpUrl, index=True)
    link = Column(String, index=True)
    short_link = Column(String, index=True)
    total_clicks = Column(Integer, default=0, index=True)
    creation_date = Column(TIMESTAMP, default=datetime.utcnow)
