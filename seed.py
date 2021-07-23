import random

from faker import Faker

from models import *

faker = Faker()

db.drop_all()
db.create_all()

num_suites = 5
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

for i in range(10):
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
        email=faker.ascii_email(),
        age=random.randrange(18, 30),
        profile_link=faker.image_url(),
        gender="Male" if i % 2 == 0 else "Female",
        birthday=faker.date_of_birth(),
        password_digest=faker.password(length=255),
        rating=random.randrange(1, 10),
        location=location,
        setting=setting,
        suite_id=i % num_suites + 1
    )

    db.session.add(user)

for i in range(5):
    messages = []
    for _ in range(3):
        messages.append(TaskMessage(
            content=faker.text(),
        ))

    task = Task(
        title=faker.text(max_nb_chars=random.randrange(10, 20)),
        description=faker.text(max_nb_chars=random.randrange(20, 50)),
        priority=random.randrange(1, 10),
        completed=faker.boolean(),
        tags=faker.text(max_nb_chars=random.randrange(5, 15)),
        points=random.randrange(1, 10),
        start_time=faker.date(),
        due_date=faker.date(),
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

db.session.commit()
db.session.close()
