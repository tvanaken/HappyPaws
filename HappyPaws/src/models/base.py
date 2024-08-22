from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Convert the object to a dictionary representation.

    Returns:
        dict: A dictionary representation of the object.
    """
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
