from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    profile_link = db.Column(db.String(255))
    gender = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.DateTime())
    password_digest = db.Column(db.String(255))
    rating = db.Column(db.Integer, nullable=False)

    suite_id = db.Column(db.Integer, db.ForeignKey('suites.id'))

    location = db.relationship('UserLocation', backref='user', lazy=True, uselist=False)
    setting = db.relationship('Setting', backref='user', lazy=True, uselist=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20))

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    __mapper_args__ = {
        'polymorphic_identity': 'location',
        "polymorphic_on": type
    }


class SuiteLocation(Location):
    suite_id = db.Column(db.Integer, db.ForeignKey('suites.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'suite_location'
    }


class UserLocation(Location):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'user_location'
    }


class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    setting = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Suite(db.Model):
    __tablename__ = 'suites'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    canvas = db.Column(db.Text)

    users = db.relationship('User', backref='suite', lazy=True)
    messages = db.relationship('SuiteMessage', backref='suite', lazy=True)
    location = db.relationship('SuiteLocation', backref='suite', lazy=True, uselist=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20))

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    __mapper_args__ = {
        'polymorphic_identity': 'message',
        "polymorphic_on": type
    }


class SuiteMessage(Message):
    suite_id = db.Column(db.Integer, db.ForeignKey('suites.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'suite_message'
    }

# class TaskMessage(db.Model):
