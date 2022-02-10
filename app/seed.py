import random

from faker import Faker

from app.models import *

faker = Faker()

db.drop_all()
db.create_all()

SIZE_FACTOR = 1
num_suites = 5 * SIZE_FACTOR
for i in range(num_suites):
    location = SuiteLocation(
        latitude=faker.latitude(),
        longitude=faker.longitude(),
    )

    messages = []
    for _ in range(3):
        messages.append(SuiteMessage(
            content=faker.text(),
        ))

    suite = Suite(
        active=faker.boolean(),
        canvas=faker.json(
            data_columns={
                'top_left': random.randrange(1, 100),
                'top_right': random.randrange(1, 100),
                'bottom_left': random.randrange(1, 100),
                'bottom_right': random.randrange(1, 100),
                'message': 'text'
            },
            num_rows=3
        ),
        location=location,
        messages=messages
    )

    db.session.add(suite)

for i in range(10 * SIZE_FACTOR):
    location = UserLocation(
        latitude=faker.latitude(),
        longitude=faker.longitude(),
    )

    setting = Setting(
        setting=faker.json(
            data_columns={
                'Version': '@1.0.1',
                'Spec': {'theme': 'hex_color', 'language': 'language_name'}
            },
            num_rows=1)
    )
    user = User(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.ascii_email() if i != 0 else 'tyler1@gmail.com',
        age=random.randrange(18, 30),
        profile_img_link=faker.image_url(),
        gender="Male" if i % 2 == 0 else "Female",
        birthday=faker.date_of_birth(),
        password_digest="$2b$12$nVLkz8wKCwT6tVBjhc7JxOSFwtHjHiuEhsxun4E.aQFC7n.YkwAoa",  # password,
        rating=random.randrange(1, 10),
        location=location,
        setting=setting,
        suite_id=(i % num_suites) + 1
    )

    db.session.add(user)

for i in range(5 * SIZE_FACTOR):
    messages = []
    for _ in range(3):
        messages.append(TaskMessage(
            content=faker.text(),
        ))

    task = Task(
        title=faker.text(max_nb_chars=random.randrange(10, 20)),
        description=faker.text(max_nb_chars=random.randrange(20, 50)),
        tags=faker.text(max_nb_chars=random.randrange(5, 15)),
        points=random.randrange(1, 10),
        start_time=faker.date(),
        last_completed=faker.date(),
        rrule_option="RRULE:FREQ=WEEKLY;INTERVAL=1;UNTIL=20220407T040000Z;BYDAY=TU,TH,SA",
        messages=messages,
    )

    db.session.add(task)

tasks = Task.query.all()
users = User.query.all()
for task in tasks:
    for i in range(random.randrange(len(users))):
        task.assignments.append(
            Assignment(user=users[i], task=task, completed_at=faker.date() if bool(random.getrandbits(1)) else None)
        )

for _ in range(5 * SIZE_FACTOR):
    expense_item = ExpenseItem(
        total_amount=random.randrange(1, 1000),
        paid_by_id=random.choice(users).id,
        description=faker.text(),
        receipt_img_link=faker.image_url(),
    )

    db.session.add(expense_item)

expense_items = ExpenseItem.query.all()
for expense_item in expense_items:
    for i in range(random.randrange(len(users))):
        expense_item.user_expenses.append(
            UserExpense(
                user=users[i], expense_items=expense_item, amount=random.randrange(1, expense_item.total_amount),
                paid_at=faker.date() if bool(random.getrandbits(1)) else None
            )
        )

db.session.commit()
db.session.close()
