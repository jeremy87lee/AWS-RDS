from .user import create_Flight, create_Pilot, create_Plane, create_admin, create_user, create_Gate
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', False)
    create_user('alice', 'alicepass', False)
    create_user('admin', 'adminpass', True)
    create_Pilot('John Doe')
    create_Plane('Boeing 737', 180)
    create_Flight('2024-06-01 10:00:00', '2024-06-01 14:00:00', 1, 1, 'New York', 'Los Angeles')
    create_Gate('A1', 1)
