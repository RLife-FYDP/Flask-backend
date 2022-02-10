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
        receipt_img_link=expense_data['receiptImgLink']
    )
    for item in expense_data['userOwe']:
        user_id, owe_amount = item['id'], item['amount']
        user = User.query.get(user_id)
        expense_item.user_expenses.append(
            UserExpense(user=user, expense_item=expense_item, amount=owe_amount, paid_at=None)
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


#
# @expenses.route('/<int:id>', methods=['DELETE'])
# @authorize
# def delete_task(user, id):
#     task = Task.query.get_or_404(id)
#     try:
#         db.session.delete(task)
#         db.session.commit()
#         return {"message": f"task {id} deleted"}, 200
#     except Exception as err:
#         return {"message": f"Error delete record {id}", "errors": str(err)}, 500
