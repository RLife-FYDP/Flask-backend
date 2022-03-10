from datetime import datetime
from typing import List

from sqlalchemy import and_
from app.models import ExpenseItem, User, Task, Assignment, Suite
from app import db


def main():
  users = User.query.all()
  for user in users:
    suite = Suite.query.get(user.suite_id)
    room_rating = 0
    if suite != None:
      M_ts = calculate_task_share(user, suite)
      M_es = calculate_expense_share(user, suite)
      M_dr = calculate_deadline_reliability(user)
      M_pr = calculate_peer_rating_metric(user)
      room_rating = .33*M_ts + .33*M_dr + .22*M_es + .12*M_pr
    print(f'---{user.email}')
    print(f'M_ts={M_ts}, M_es={M_es}, M_dr={M_dr}, M_pr={M_pr}')
    print(f'room_rating={room_rating}')
    user.rating = room_rating
  db.session.commit()

def calculate_peer_rating_metric(user):
  return .5

def calculate_deadline_reliability(user):
  assignments = Assignment.query.filter(Assignment.user_id == user.id).all()
  unique_task_ids = {assignment.task_id for assignment in assignments}
  user_tasks_passed_deadline: List[Task] = Task.query.filter(and_(Task.id.in_(unique_task_ids), Task.start_time < datetime.utcnow())).all()
  T_user = len(user_tasks_passed_deadline)
  T_ontime = len([task for task in user_tasks_passed_deadline if task.last_completed != None and task.last_completed < task.start_time])
  return T_ontime/T_user if T_user > 0 else .5


def calculate_expense_share(user: User, suite):
  suite_expenses: List[ExpenseItem] = ExpenseItem.query.filter(ExpenseItem.paid_by_id.in_([u.id for u in suite.users])).all()
  E_total = sum([suite_expense.total_amount for suite_expense in suite_expenses])
  E_user = sum([suite_expense.total_amount for suite_expense in suite_expenses if suite_expense.paid_by_id == user.id])
  N_roommates = len(suite.users)
  return min(E_user * N_roommates / E_total, 1) if E_total > 0 else .5

def calculate_task_share(user: User, suite):
  user_assignments = Assignment.query.filter(Assignment.user_id == user.id).all()
  user_unique_task_ids = {assignment.task_id for assignment in user_assignments}
  T_user = len(Task.query.filter(Task.id.in_(user_unique_task_ids)).all())

  all_assignments = Assignment.query.filter(Assignment.user_id.in_([user.id for user in suite.users])).all()
  all_unique_task_ids = {assignment.task_id for assignment in all_assignments}
  T_total = len(Task.query.filter(Task.id.in_(all_unique_task_ids)).all())
  N_roommates = len(suite.users)
  return min(T_user*N_roommates/T_total, 1) if T_total > 0 else .5


if __name__ == '__main__':
  main()