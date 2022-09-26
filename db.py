from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

# correction to SQLalchemy 1.4 and postgres
uri = getenv("DATABASE_URL")  
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app.config["SQLALCHEMY_DATABASE_URI"] = uri
db = SQLAlchemy(app)