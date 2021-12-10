from db import *
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

class Accs(db.Model):
    __tablename__ = 'accs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    timecreated = db.Column(db.Integer)
    profileurl = db.Column(db.String)
    profilestate = db.Column(db.Integer)

    def __init__(self, i, n, t, pu, ps):
        self.id = i
        self.name = n
        self.timecreated = t
        self.profileurl = pu
        self.profilestate = ps

    def __repr__(self):
        return f""

class Apps(db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.String)
    title = db.Column(db.String)
    dlc = db.Column(db.Boolean)
    parent = db.Column(db.Integer)

    def __init__(self, i, n, a, d, t, dl, p):
        self.id = i
        self.name = n
        self.author = a
        self.date = d
        self.title = t
        self.dlc = dl
        self.parent = p

    def __repr__(self):
        return f''

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(postgresql.UUID, primary_key=True)
    appid = db.Column(db.Integer, db.ForeignKey('apps.id'))
    playtime = db.Column(postgresql.UUID)
    user_id = db.Column(db.Integer, db.ForeignKey('accs.id'))
    gifted = db.Column(db.Integer)
    price = db.Column(db.Integer)

    user_inv = relationship('Accs', foreign_keys=[user_id])

    def __init__(self, i, a, p, u , g, pr):
        self.id = i
        self.appid = a
        self.playtime = p
        self.user_id = u
        self.gifted = g
        self.price = pr
    
    def __repr__(self):
        return f''
