from app import db, ma
from marshmallow import Schema, fields, ValidationError, validate, ValidationError


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    profile_img_link = db.Column(db.String(255))
    gender = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.DateTime())
    password_digest = db.Column(db.String(255))
    rating = db.Column(db.Integer, nullable=False)

    suite_id = db.Column(db.Integer, db.ForeignKey('suites.id'))

    location = db.relationship('UserLocation', backref='user', lazy=True, uselist=False)
    setting = db.relationship('Setting', backref='user', lazy=True, uselist=False)
    tasks = db.relationship("Task", secondary="assignments", viewonly=True)
    expense_items = db.relationship("ExpenseItem", secondary="user_expenses", viewonly=True)


class Location(Base):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20))

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


class Setting(Base):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    setting = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Suite(Base):
    __tablename__ = 'suites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    canvas = db.Column(db.Text)
    address = db.Column(db.String(255))

    users = db.relationship('User', backref='suite', lazy=True)
    messages = db.relationship('SuiteMessage', backref='suite', lazy=True)
    location = db.relationship('SuiteLocation', backref='suite', lazy=True, uselist=False)


class Message(Base):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20))
    from_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'message',
        "polymorphic_on": type
    }


class SuiteMessage(Message):
    suite_id = db.Column(db.Integer, db.ForeignKey('suites.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'suite_message'
    }


class TaskMessage(Message):
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'task_message'
    }


class Assignment(Base):
    __tablename__ = 'assignments'
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    completed_at = db.Column(db.DateTime)

    user = db.relationship('User', backref='assignments')


class Task(Base):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    points = db.Column(db.Integer, nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    last_completed = db.Column(db.DateTime, nullable=True)
    rrule_option = db.Column(db.String(255), nullable=True)

    messages = db.relationship('TaskMessage', backref='task', lazy=True, cascade="all, delete")
    assignments = db.relationship('Assignment', backref='task', cascade="all, delete")
    users = db.relationship("User", secondary="assignments", viewonly=True)


class ExpenseItem(Base):
    __tablename__ = 'expense_items'
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    receipt_img_link = db.Column(db.String(255), nullable=True)
    paid_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user_expenses = db.relationship('UserExpense', backref='expense_items', cascade="all, delete")
    users = db.relationship("User", secondary="user_expenses", viewonly=True)


class UserExpense(Base):
    __tablename__ = 'user_expenses'
    expense_item_id = db.Column(db.Integer, db.ForeignKey('expense_items.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    paid_at = db.Column(db.DateTime)

    user = db.relationship('User', backref='user_expenses')


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location


class SuiteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SuiteLocation


class UserLocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserLocation


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Setting


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message


class SuiteMessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SuiteMessage
    from_user = fields.Int()


class TaskMessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskMessage


class AssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment


class ExpenseItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExpenseItem
        include_fk = True

    totalAmount = fields.Float()
    paidByID = fields.Int()
    receiptImgLink = fields.String()
    userOwe = fields.List(fields.Dict(keys=fields.Str(), values=fields.Float()))

    users = ma.Nested(lambda: UserSchema(only=["id"]), many=True)

class UserExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserExpense

    expense_item_id = fields.Int()
    user_id = fields.Int()
    amount = fields.Float()
    paid_at = fields.DateTime()


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

    title = fields.String()
    points = fields.Int(validate=[validate.Range(min=0)])
    tags = fields.String()
    description = fields.String()
    startTime = fields.DateTime()
    lastCompleted = fields.DateTime(allow_none=True)
    rruleOption = fields.String()
    assignee = fields.List(fields.Int)

    messages = ma.Nested(TaskMessageSchema, many=True)
    users = ma.Nested(lambda: UserSchema(only=["id"]), many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    location = ma.Nested(LocationSchema)
    setting = ma.Nested(SettingSchema)
    suite = ma.Nested(SuiteSchema)
    expense_items = ma.Nested(ExpenseItemSchema, many=True)


class SuiteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Suite

    messages = ma.Nested(SuiteMessageSchema, many=True)
    location = ma.Nested(LocationSchema)
