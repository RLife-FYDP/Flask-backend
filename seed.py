from models import *
from faker import Faker
import random

faker = Faker()

db.drop_all()
db.create_all()

for i in range(10):
    location = Location(
        latitude=faker.latitude(),
        longitude=faker.longitude(),
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
        location=location
    )

    db.session.add(user)

db.session.commit()
