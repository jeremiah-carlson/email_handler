from sqlalchemy import create_engine, Column, ForeignKey, Sequence, select, delete
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.dialects.postgresql import *
import psycopg2

from scripts.setup import secrets

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' % tuple(secrets['db'].values()))


class pdf_template(Base):
    __tablename__ = 'pdf_template'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(100))
    description = Column(VARCHAR(100))
    parameters = Column(VARCHAR(2000))
    full_text = Column(VARCHAR(100000))


Base.metadata.create_all(engine)

def new_pdf_template(name, description, parameters, full_text):
    with Session(engine) as session:

        duplicate = select(pdf_template).where(pdf_template.name == name)

        if session.scalar(duplicate) == None:


            template = pdf_template(name=name,
                                    description=description,
                                    parameters= parameters,
                                    full_text=full_text)

            session.add_all([template])
            session.commit()

            return 'Template %s created successfully!' % name
        
        else:

            return 'Template with name %s already exists.' % name





