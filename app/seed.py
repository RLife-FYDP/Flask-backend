import random

from faker import Faker

from app.models import *
from app.utils.constants import CANVAS_BLOB

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

    address = faker.street_address()
    suite = Suite(
        active=faker.boolean(),
        canvas=CANVAS_BLOB,
        location=location,
        name=address,
        address=address,
        messages=[]
    )

    db.session.add(suite)

for i in range(4 * num_suites):
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
        rating=random.uniform(0, 1),
        location=location,
        setting=setting,
        suite_id=(i % num_suites) + 1
    )
    db.session.add(user)

all_tasks = []
for i in range(5 * num_suites):
    task = Task(
        title=faker.text(max_nb_chars=random.randrange(10, 20)),
        description=faker.text(max_nb_chars=random.randrange(20, 50)),
        tags=faker.text(max_nb_chars=random.randrange(5, 15)),
        points=random.randrange(1, 10),
        start_time=faker.date(),
        last_completed=faker.date(),
        rrule_option="RRULE:FREQ=WEEKLY;INTERVAL=1;UNTIL=20220407T040000Z;BYDAY=TU,TH,SA",
        messages=[],
    )
    all_tasks.append(task)

    db.session.add(task)

suites = Suite.query.all()
for suite in suites:
    users = suite.users
    for _ in range(5):
        task = all_tasks.pop()
        for i in range(random.randrange(len(users))):
            task.assignments.append(
                Assignment(user=users[i], task=task, completed_at=faker.date() if bool(random.getrandbits(1)) else None)
            )
        task.messages.append(
            TaskMessage(content=faker.text(), from_user=users[random.randint(0, len(users)-1)].id)
        )
        suite.messages.append(
            SuiteMessage(content=faker.text(), from_user=users[random.randint(0, len(users)-1)].id)
        )

for suite in suites:
    users = suite.users
    for _ in range(5):
        expense_item = ExpenseItem(
            total_amount=random.randrange(1, 1000),
            paid_by_id=random.choice(users).id,
            description=faker.text(),
            receipt_img_link=faker.image_url(),
        )
        for i in range(random.randrange(len(users))):
            expense_item.user_expenses.append(
                UserExpense(
                    user=users[i], expense_items=expense_item, amount=random.randrange(1, expense_item.total_amount),
                    paid_at=faker.date() if bool(random.getrandbits(1)) else None
                )
            )
        db.session.add(expense_item)

for suite in suites:
    users = suite.users
    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            peer_rating_i_j = PeerRating(
                suite_id=suite.id,
                rater_user_id=users[i].id,
                ratee_user_id=users[j].id,
                rating=random.randint(0,1)
            )

            peer_rating_j_i = PeerRating(
                suite_id=suite.id,
                rater_user_id=users[j].id,
                ratee_user_id=users[i].id,
                rating=random.randint(0,1)
            )
            db.session.add(peer_rating_i_j)
            db.session.add(peer_rating_j_i)

db.session.commit()
db.session.close()
