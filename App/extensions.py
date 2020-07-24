"""扩展模块。每个扩展在app.py中的app工厂中初始化."""

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from App.commons.apispec import APISpecExt

bcrypt = Bcrypt()
db = SQLAlchemy()
cache = Cache()
cors = CORS()
apispec = APISpecExt()
migrate = Migrate(db=db)
debug_toolbar = DebugToolbarExtension()
serialize = Marshmallow()
