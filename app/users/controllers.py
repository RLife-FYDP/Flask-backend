from flask import Blueprint, jsonify

from app.auth.middleware import authorize
from app.models import User, UserSchema, TaskSchema, UserExpense, ExpenseItem

# Define the blueprint: 'users', set its url prefix: app.url/users
users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
def get_all_users():
    users = User.query.all()
    users_schema = UserSchema(many=True, exclude=['password_digest'])
    return jsonify(users_schema.dump(users))


@users.route('/<int:id>')
def get_user(id):
    user = User.query.get(id)
    user_schema = UserSchema(exclude=['password_digest'])
    return jsonify(user_schema.dump(user))


@users.route('/tasks')
@authorize
def get_user_tasks(user):
    user = User.query.get(user.id)
    tasks = user.tasks
    task_schema = TaskSchema(many=True)
    return jsonify(task_schema.dump(tasks))


@users.route('/expenses')
@authorize
def get_user_expenses(user):
    res = []
    user_expenses = UserExpense.query.filter_by(user_id=user.id).all()
    for user_expense in user_expenses:
        expense_item = user_expense.expense_items
        res.append({
            "amount_owe": user_expense.amount,
            "paid_at": user_expense.paid_at,
            "expense_item_description": expense_item.description,
            "expense_item_total_amount": expense_item.total_amount,
            "expense_item_paid_by_user_id": expense_item.paid_by_id,
            "expense_item_id": expense_item.id,
            "expense_receipt_url": expense_item.receipt_img_link,
            "expense_created_at": expense_item.created_at,
        })

    return jsonify(res)
