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

db.session.commit()
db.session.close()
