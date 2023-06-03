from tg_bot import db


class User(db.Model):
    first_name = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    is_bot = db.Column(db.String)
    language_code = db.Column(db.String)
    username = db.Column(db.String)


class PhoneBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')
    name = db.Column(db.String)
    phone_number = db.Column(db.Unicode)
    __table_args__ = (db.UniqueConstraint('user_id', 'phone_number', name='unique_user_phones'),
                      db.UniqueConstraint('user_id', 'name', name='unique_user_names'))
