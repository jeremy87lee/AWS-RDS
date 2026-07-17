from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers.user import get_all_flights_json, create_Flight, delete_flight, get_all_flights
from App.models.Planes import Plane
from App.models.flights import Flight
from App.models.pilots import Pilot
from App.views.user import user_views
from App.database import db

flight_views = Blueprint('flight_views', __name__, template_folder='../templates')


@flight_views.route('/api/flights', methods=['GET'])
@jwt_required()
def get_flights_action():
    is_admin = jwt_current_user.is_admin 
    flights = get_all_flights()
    return render_template('flights.html', flights=flights,is_admin=is_admin)
    #return jsonify(flights)

@flight_views.route('/api/new_flight', methods=['POST'])
def create_flight_action():
    flight_data = request.form
    departure_time = flight_data.get('departure_time')
    arrival_time = flight_data.get('arrival_time')
    plane_id = flight_data.get('plane_id')
    pilot_id = flight_data.get('pilot_id')
    departure_destination = flight_data.get('departure_destination')
    destination = flight_data.get('destination')

    # Validate the plane and pilot IDs
    plane = Plane.query.get(plane_id)
    pilot = Pilot.query.get(pilot_id)
    if not plane or not pilot:
        flash("Invalid plane or pilot ID", "error")
        return redirect(url_for('flight_views.create_flight_page'))

    new_flight = create_Flight(departure_time, arrival_time, plane_id, pilot_id, departure_destination, destination)
    if not new_flight:
        flash("Failed to create flight. Please check the provided data for flight clashes or wrong IDs.", "error")
        return redirect(url_for('flight_views.create_flight_page'))
    db.session.add(new_flight)
    db.session.commit()
    flash("Flight created successfully!", "success")
    return redirect(url_for('flight_views.get_flights_action'))
 
@flight_views.route('/api/delete_flight', methods=['POST'])
def delete_flight_action():
    flight_id = request.form.get('flight_id')
    flight = Flight.query.get(flight_id)
    if flight:
        success = delete_flight(flight_id)
        if success:
            return redirect(url_for('flight_views.get_flights_action'))
    else:
        return redirect(url_for('flight_views.get_flights_action', message=f"Flight with id {flight_id} not found"))

@flight_views.route('/api/update_flight', methods=['POST'])
def update_flight_action():
   flight_id = request.form.get('flight_id')
   flight = Flight.query.get(flight_id)
   if flight:
    new_departure_time = request.form.get('departure_time')
    new_arrival_time = request.form.get('arrival_time')
    new_plane_id = request.form.get('plane_id')
    new_pilot_id = request.form.get('pilot_id')
    Pla = Plane.query.get(new_plane_id)
    Pil = Pilot.query.get(new_pilot_id)
    if not Pla or not Pil:
        flash("Invalid plane or pilot ID", "error")
        return redirect(url_for('flight_views.get_flights_action'))
    new_departure_destination = request.form.get('departure_destination')
    new_destination = request.form.get('destination')
    if new_departure_time >= new_arrival_time:
        flash("Departure time must be before arrival time.", "error")
        return redirect(url_for('flight_views.get_flights_action'))
    new_plane_id = int(new_plane_id)
    new_pilot_id = int(new_pilot_id)
    Flights = Flight.query.all()
    for f in Flights:
        if f.id == int(flight_id):
            continue
        if (new_departure_time < f.arrival_time and new_arrival_time > f.departure_time) and new_pilot_id == f.pilot_id:
            flash(f"Pilot {new_pilot_id} already has another flight at that time!")
            return redirect(url_for('flight_views.get_flights_action'))
        if (new_departure_time < f.arrival_time and new_arrival_time > f.departure_time) and new_plane_id == f.plane_id:
            flash(f"Plane {new_plane_id} already has another flight at that time!")
            return redirect(url_for('flight_views.get_flights_action'))
        
    flight.departure_time = new_departure_time
    flight.arrival_time = new_arrival_time
    flight.plane_id = new_plane_id
    flight.pilot_id = new_pilot_id
    flight.departure_destination = new_departure_destination
    flight.destination = new_destination
    db.session.commit()
    return redirect(url_for('flight_views.get_flights_action'))
   else:
    flash(f"Flight with id {flight_id} not found", "error")
    return redirect(url_for('flight_views.get_flights_action'))

@flight_views.route('/api/update_flight/<int:flight_id>', methods=['GET'])
def update_flight_page(flight_id):
    flight = Flight.query.get(flight_id)
    if flight:
        return render_template('Flight Updates.html', flight=flight)
    else:
        return jsonify({'message': f"Flight with id {flight_id} not found"}), 404

@flight_views.route('/api/create_flight', methods=['GET'])
@jwt_required()
def create_flight_page():
    current_user = jwt_current_user
    if not current_user.is_admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    return render_template('Flight Creation.html')