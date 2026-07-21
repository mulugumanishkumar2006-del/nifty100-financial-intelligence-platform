from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Text

from app.database import Base


class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    company_name = Column(String)

    symbol = Column(String)

    sector = Column(String)

    website = Column(String)

    about_company = Column(Text)

    face_value = Column(Float)

    book_value = Column(Float)

    roce_percentage = Column(Float)

    roe_percentage = Column(Float)