from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship

# compat
text_type = str
binary_type = bytes
string_types = (str,)
unicode = str
basestring = (str, bytes)


class CRUDMixin(object):
    """为CRUD(创建、读取、更新、删除)操作添加了方便的方法."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """包含CRUD方便方法的基本模型类."""

    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """将一个名为“id”的代理整数“主键”列添加到任何声明映射类的mixin."""

    __table_args__ = {"extend_existing": True}

    id = Column(db.Integer, primary_key=True)

    @classmethod
    def getById(cls, record_id):
        """Get record by ID."""
        if any((isinstance(record_id, basestring) and record_id.isdigit(), isinstance(record_id, (int, float)))):
            return cls.query.get(int(record_id))
        return None


def referenceCol(tablename, nullable=False, pk_name="id", **kwargs):
    """添加主键外键引用的列.
    Usage: ::
        category_id = referenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return Column(db.ForeignKey("{0}.{1}".format(tablename, pk_name)), nullable=nullable, **kwargs)
