from sqlalchemy.orm import DeclarativeBase, Mapped
from flask_security.models import sqla

class Model(DeclarativeBase):
    pass

sqla.FsModels.set_db_info(base_model=Model)

class Role(Model, sqla.FsRoleMixin):
    __tablename__ = "role"


class User(Model, sqla.FsUserMixin):
    __tablename__ = "user"
    name: Mapped[str]