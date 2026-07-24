from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Text

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, index=True)

    company_name = Column(String, nullable=False)

    ticker = Column(String)

    isin = Column(String)

    market_cap = Column(Float)

    company_logo = Column(String)

    chart_link = Column(String)

    about_company = Column(Text)

    website = Column(String)

    nse_profile = Column(String)

    bse_profile = Column(String)

    face_value = Column(Float)

    book_value = Column(Float)

    roce_percentage = Column(Float)

    roe_percentage = Column(Float)