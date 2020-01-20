from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

    def __repr__(self): # self es como el this en javascript, permite ver todo lo dentro de la clase funcion
        return '<Contact %r>' % self.name


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone
        }


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user = db.Column(db.String(50), nullable=False)

    def __repr__(self): # self es como el this en javascript, permite ver todo lo dentro de la clase funcion
        return '<Todo %r>' % self.label


    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done,
            "user": self.user
        }



