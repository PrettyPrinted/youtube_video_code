from flask_sqlalchemy_lite import SQLAlchemy
from flask_alembic import Alembic

from .models import Base

db = SQLAlchemy()
alembic = Alembic(metadatas=Base.metadata)