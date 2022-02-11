import datetime

from marshmallow import ValidationError
from flask import Blueprint, jsonify, request
from app import db
from app.auth.middleware import authorize

from app.models import ExpenseItemSchema, ExpenseItem, User, UserExpense, UserExpenseSchema

expenses = Blueprint('expenses', __name__, url_prefix='/expenses')

expense_schema = ExpenseItemSchema()
user_expense_schema = UserExpenseSchema()


@expenses.route('create', methods=['POST'])
@authorize
def create_expense(user):
    expense_data = request.get_json()

    expense_item = ExpenseItem(
        total_amount=expense_data['totalAmount'],
        paid_by_id=expense_data['paidById'],
        description=expense_data['description'],
        receipt_img_link=expense_data['receiptImgLink']
    )
    for item in expense_data['userOwe']:
        user_id, owe_amount = item['id'], item['amount']
        user = User.query.get(user_id)
        expense_item.user_expenses.append(
            UserExpense(user=user, expense_items=expense_item, amount=owe_amount, paid_at=None)
        )

    db.session.add(expense_item)
    db.session.commit()
    return jsonify(expense_item=expense_schema.dump(expense_item))


@expenses.route('/pay/<int:id>', methods=['PUT'])
@authorize
def update_task(user, id):
    user_expense = UserExpense.query.filter_by(expense_item_id=id, user_id=user.id).first()
    user_expense.paid_at = datetime.datetime.now()
    try:
        db.session.commit()
        return jsonify(expense_item=user_expense_schema.dump(user_expense))
    except Exception as err:
        return {"message": "Error updating", "errors": str(err)}, 400


@expenses.route('/<int:id>', methods=['DELETE'])
@authorize
def delete_expense(user, id):
    expenseItem = ExpenseItem.query.get_or_404(id)
    try:
        db.session.delete(expenseItem)
        db.session.commit()
        return {"message": f"expense {id} deleted"}, 200
    except Exception as err:
        return {"message": f"Error delete record {id}", "errors": str(err)}, 500


@expenses.route('/<int:id>', methods=['GET'])
@authorize
def get_expense(user, id):
    expense_item = ExpenseItem.query.get_or_404(id)
    user_expenses = expense_item.user_expenses
    u_expense = []
    for user_expense in user_expenses:
        u_expense.append({
            "amount_owe": user_expense.amount,
            "paid_at": user_expense.paid_at,
            "user_id": user_expense.user_id,
        })
    return {
        "expense_item_description": expense_item.description,
        "expense_item_total_amount": expense_item.total_amount,
        "expense_item_paid_by_user_id": expense_item.paid_by_id,
        "expense_item_id": expense_item.id,
        "expense_receipt_url": expense_item.receipt_img_link,
        "expense_created_at": expense_item.created_at,
        "user_expenses": u_expense
    }

@expenses.route('/<int:id>', methods=['PUT'])
@authorize
def update_expense(user, id):
    expense_data = request.get_json()
    expense_item = ExpenseItem.query.get_or_404(id)
    expense_item.total_amount = expense_data['total_amount']
    expense_item.description = expense_data['description']
    expense_item.receipt_img_link = expense_data['receipt_img_link']
    expense_item.paid_by_id = expense_data['paid_by_id']
    expense_item.updated_at = datetime.datetime.now()
    for user_expense_data in expense_data['user_expenses']:
        user_expense = UserExpense.query.get((id, user_expense_data['user_id']))
        user_expense.amount = user_expense_data['amount_owe']
        user_expense.paid_at = user_expense_data['paid_at']
    try:
        db.session.commit()
        return {"message": f"Updated expenses id {id}"}, 200
    except Exception as err:
        return {"message": "Error updating", "errors": str(err)}, 400

