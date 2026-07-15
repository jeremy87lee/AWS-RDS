from App.models import User
from App.database import db
from App.models.Gates import Gate
from App.models.Planes import Plane
from App.models.admin import Admin
from App.models.flights import Flight
from App.models.pilots import Pilot

def create_user(username, password, is_admin):
    if is_admin:
        create_admin(username, password, is_admin)
    else:
        newuser = User(username=username, password=password, is_admin=is_admin)
        db.session.add(newuser)
        db.session.commit()
        return newuser

def create_admin(username, password, is_admin):
    newadmin = Admin(username=username, password=password, is_admin=is_admin)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

def create_Pilot(name):
    new_pilot = Pilot(name=name)
    db.session.add(new_pilot)
    db.session.commit()
    return new_pilot

def create_Plane(model, capacity):
    new_plane = Plane(model=model, capacity=capacity)
    db.session.add(new_plane)
    db.session.commit()
    return new_plane

def create_Gate(terminal, flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        print(f"Flight ID {flight_id} does not exist.")
        return None  # Flight ID does not exist
    new_gate = Gate(terminal=terminal, flight=flight_id)
    db.session.add(new_gate)
    db.session.commit()
    return new_gate

def create_Flight(departure_time, arrival_time, plane_id, pilot_id, departure_destination, destination):
    plane = Plane.query.get(plane_id)
    if not plane:
        print(f"Plane ID {plane_id} does not exist.")
        return None  # Plane ID does not exist
    pilot = Pilot.query.get(pilot_id)
    if not pilot:
        print(f"Pilot ID {pilot_id} does not exist.")
        return None  # Pilot ID does not exist
    new_flight = Flight(departure_time=departure_time, arrival_time=arrival_time, plane_id=plane_id, pilot_id=pilot_id, departure_destination=departure_destination, destination=destination)
    db.session.add(new_flight)
    db.session.commit()
    return new_flight

def get_all_flights_json():
    flights = Flight.query.all()
    return [flight.get_json() for flight in flights]

def get_all_gates_json():
    gates = Gate.query.all()
    return [gate.get_json() for gate in gates]

def get_all_planes_json():
    planes = Plane.query.all()
    return [plane.get_json() for plane in planes]

def get_all_pilots_json():
    pilots = Pilot.query.all()
    return [pilot.get_json() for pilot in pilots]

def get_all_admins_json():
    admins = Admin.query.all()
    return [admin.get_json() for admin in admins]

def delete_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if flight:
        db.session.delete(flight)
        db.session.commit()
        return True
    return False

def get_all_flights():
    return Flight.query.all()
