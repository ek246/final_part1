from app.database import Base, engine
from app.models.users import Users


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()