import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, delete_gate, delete_plane, delete_pilot )
from App.models.Gates import Gate


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

@user_cli.command("show flights",help="Shows all flights in the database")
def show_flights_command():
    from App.controllers.user import get_all_flights_json
    print(get_all_flights_json())

@user_cli.command("show gates",help="Shows all gates in the database")
def show_gates_command():
    from App.controllers.user import get_all_gates_json
    print(get_all_gates_json())

@user_cli.command("show planes",help="Shows all planes in the database")
def show_planes_command():
    from App.controllers.user import get_all_planes_json
    print(get_all_planes_json())

@user_cli.command("show pilots",help="Shows all pilots in the database")
def show_pilots_command():
    from App.controllers.user import get_all_pilots_json
    print(get_all_pilots_json())

@user_cli.command("show admins",help="Shows all admins in the database")
def show_admins_command():
    from App.controllers.user import get_all_admins_json
    print(get_all_admins_json())
    
@user_cli.command("create flight", help="Creates a flight")
@click.argument("departure_time", default="2024-06-01 12:00:00")
@click.argument("arrival_time", default="2024-06-01 15:00:00")
@click.argument("plane_id", default=1)
@click.argument("pilot_id", default=1)
@click.argument("departure_destination", default="JFK")
@click.argument("destination", default="LAX")
def create_flight_command(departure_time, arrival_time, plane_id, pilot_id, departure_destination, destination):
    from App.controllers.user import create_Flight
    flight = create_Flight(departure_time, arrival_time, plane_id, pilot_id, departure_destination, destination)
    if flight:
        print(f"Flight created with id {flight.id}")
    else:
        print("Failed to create flight. Please check the provided IDs.")

@user_cli.command("delete flight", help="Deletes a flight")
@click.argument("flight_id", type=int)
def delete_flight_command(flight_id):
    from App.controllers.user import delete_flight
    success = delete_flight(flight_id)
    if success:
        print(f"Flight with id {flight_id} deleted")
    else:
        print(f"Flight with id {flight_id} not found")
        
@user_cli.command("delete gate", help="Deletes a gate")
@click.argument("gate_id", type=int)
def delete_gate_command(gate_id):
    success = delete_gate(gate_id)
    if success:
        print(f"Gate with id {gate_id} deleted")
    else:
        print(f"Gate with id {gate_id} not found")

@user_cli.command("delete plane", help="Deletes a plane")
@click.argument("plane_id", type=int)
def delete_plane_command(plane_id):
    success = delete_plane(plane_id)
    if success:
        print(f"Plane with id {plane_id} deleted")
    else:
        print(f"Plane with id {plane_id} not found")
        
@user_cli.command("delete pilot", help="Deletes a pilot")
@click.argument("pilot_id", type=int)
def delete_pilot_command(pilot_id):
    success = delete_pilot(pilot_id)
    if success:
        print(f"Pilot with id {pilot_id} deleted")
    else:
        print(f"Pilot with id {pilot_id} not found")

@user_cli.command("create gate", help="Creates a gate")
@click.argument("terminal", default="A1")
@click.argument("flight_id", type=int, default=1)
def create_gate_command(terminal, flight_id):
    from App.controllers.user import create_Gate
    success = create_Gate(terminal, flight_id)
    if success:
        print(f"Gate created for flight id {flight_id} at terminal {terminal}")
    else:
        print(f"Failed to create gate. Flight id {flight_id} may not exist.")

@user_cli.command("create plane", help="Creates a plane")
@click.argument("model", default="Boeing 737")
@click.argument("capacity", type=int, default=180)
def create_plane_command(model, capacity):
    from App.controllers.user import create_Plane
    plane = create_Plane(model, capacity)
    if plane:
        print(f"Plane created with id {plane.id}")
    else:
        print("Failed to create plane.")

@user_cli.command("create pilot", help="Creates a pilot")
@click.argument("name", default="John Doe")
def create_pilot_command(name):
    from App.controllers.user import create_Pilot
    pilot = create_Pilot(name)
    if pilot:
        print(f"Pilot created with id {pilot.id}")
    else:
        print("Failed to create pilot.")
        
#commands to update
@user_cli.command("update plane",help="Updates plane info")
@click.argument("plane_id", type=int)
@click.argument("model", default=None)
@click.argument("capacity", type=int, default=None)
def update_plane_command(plane_id, model, capacity):
    from App.controllers.user import update_plane
    success = update_plane(plane_id, model, capacity)
    if success:
        print(f"Plane with id {plane_id} updated")
    else:
        print(f"Plane with id {plane_id} not found or no changes made")

@user_cli.command("update pilot",help="Updates pilot info")
@click.argument("pilot_id", type=int)
@click.argument("name", default=None)
def update_pilot_command(pilot_id, name):
    from App.controllers.user import update_pilot
    success = update_pilot(pilot_id, name)
    if success:
        print(f"Pilot with id {pilot_id} updated")
    else:
        print(f"Pilot with id {pilot_id} not found or no changes made")

@user_cli.command("update gate",help="Updates gate info")
@click.argument("gate_id", type=int)
@click.argument("terminal", default=None)
@click.argument("flight_id", type=int, default=None)
def update_gate_command(gate_id, terminal, flight_id):
    from App.controllers.user import update_gate
    success = update_gate(gate_id, terminal, flight_id)
    if success:
        print(f"Gate with id {gate_id} updated")
    else:
        print(f"Gate with id {gate_id} not found or no changes made")
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)