import random
from app.models import Base, User, Breed, Food, Pet, Reminder, Supplement
from db_manager import DBManager
from faker import Faker

fake = Faker()


def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)


def create_user():
    profile = fake.simple_profile()
    tokens = profile["name"].split(" ")
    first_name = tokens.pop(0)
    last_name = " ".join(tokens)
    username = "{0}_{1}".format(first_name, last_name.replace(" ", "_")).lower()
    provider = profile["mail"].split("@")[1]
    email = "{0}@{1}".format(username, provider)
    user = User(
        email=email,
        password='12345',
    )
    return user


def create_fake_users(session, n=5):
    users = []
    for _ in range(n):
        user = create_user()
        users.append(user)
        session.add(user)
    session.commit()
    return users


def create_fake_reminders(session):
    med_reminder = Reminder(user_id=1, type='Medication', start='2023-12-10T07:00', end='2023-12-10T08:30')
    play_reminder = Reminder(user_id=1, type='play', start='2023-12-05', end='2023-12-05')
    exercise_reminder = Reminder(user_id=2, type='exercise', start='2023-12-21', end='2023-12-23')
    session.add(med_reminder)
    session.add(play_reminder)
    session.add(exercise_reminder)
    session.commit()


def create_fake_pets(session):
    boo = Pet(user_id=1, breed_id=2, name='Boo', age=11, weight='25', birthday='2012-10-05')
    session.add(boo)
    miles = Pet(user_id=1, breed_id=1, name='Miles', age=8, weight='75', birthday='2015-03-15')
    session.add(miles)
    flare = Pet(user_id=1, breed_id=1, name='Flare', age=7, weight='67', birthday='2016-08-21')
    session.add(flare)
    session.commit()


# def create_fake_foods(session):
#     orijen_senior_dry = Food(type='dry', name='Orijen: Senior', ingredients=None, crude_protein=38, crude_fat=15, crude_fiber=8, moisture=12, dietary_starch=17, epa=0.2, calcium=1.3, phosphorus=0.9, vitamin_e=750, omega_6=3, omega_3=0.8, glucosamine=600, microorganisms=1000000)
#     session.add(orijen_senior_dry)
#     session.commit()
    
def create_fake_supplements(session):
    test = Supplement(name='Tester', description='This is a test', ailment='Hip/Joint')
    session.add(test)
    session.commit()


def create_fake_breeds(session):
    husky = Breed(name='Husky', suggested_supplements=None, suggested_exercise="walks")
    session.add(husky)
    american_eskimo = Breed(name='American Eskimo', suggested_supplements=None, suggested_exercise="running")
    session.add(american_eskimo)
    bulldog = Breed(name='Bulldog', suggested_supplements=None, suggested_exercise="swimming")
    session.add(bulldog)
    session.commit()


def trigger_fastapi_reload():
    # Sneaky trick: triggering a hot reload, which releases
    # database sessions and allows database to be rebuilt:
    import subprocess

    subprocess.call(["touch", "server.py"])


def generate_data():
    print("\n1. Using touch command to trigger server reload...")
    trigger_fastapi_reload()

    print("\n2. Rebuilding database...")
    db_manager = DBManager()
    engine = db_manager.get_engine()
    session = db_manager.get_session()
    print(session)

    # drop all tables:
    step = 1
    print("{0}. Dropping all tables...".format(step))
    drop_tables(engine)
    step += 1

    # create all tables:
    print("{0}. creating DB tables (if they don't already exist)...".format(step))
    create_tables(engine)
    step += 1

    # fake users:
    print("{0}. creating some fake users...".format(step))
    users = create_fake_users(session, 5)
    step += 1

    #fake breeds
    print("{0}. creating some fake breeds...".format(step))
    breeds = create_fake_breeds(session)
    step += 1

    #fake foods
    # print("{0}. creating some fake foods...".format(step))
    # foods = create_fake_foods(session)
    # step += 1

    #fake supplements
    print("{0}. creating some fake supplements...".format(step))
    supplements = create_fake_supplements(session)
    step += 1

    #fake pets
    print("{0}. creating some fake pets...".format(step))
    pets = create_fake_pets(session)
    step += 1

    #fake reminders
    print("{0}. creating some fake reminders...".format(step))
    reminders = create_fake_reminders(session)


    # cleanup
    db_manager.cleanup()


if __name__ == "__main__":
    generate_data()
