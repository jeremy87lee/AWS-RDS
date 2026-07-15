import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
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
@click.argument("departure_time", default="2023-01-01 10:00:00")
@click.argument("arrival_time", default="2023-01-01 12:00:00")
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