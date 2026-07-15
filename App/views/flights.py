from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers.user import get_all_flights_json, create_Flight, delete_flight
from App.models.flights import Flight
from App.views.user import user_views
from App.database import db

flight_views = Blueprint('flight_views', __name__, template_folder='../templates')


@flight_views.route('/api/flights', methods=['GET'])
@jwt_required()
def get_flights_action():
    is_admin = jwt_current_user.is_admin 
    flights = get_all_flights_json()
    return render_template('flights.html', flights=flights,is_admin=is_admin)
    #return jsonify(flights)

@flight_views.route('/api/new_flight', methods=['POST'])
def create_flight_action():
    data = request.json
    flight = create_Flight(data['departure_time'], data['arrival_time'], data['plane_id'], data['pilot_id'], data['departure_destination'], data['destination'])
    return jsonify({'message': f"Flight {flight.flight_number} created with id {flight.id}"})

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

@flight_views.route('/api/update_flight', methods=['PUT'])
def update_flight_action():
    data = request.json
    flight_id = data['flight_id']
    flight = Flight.query.get(flight_id)
    if flight:
        # Update flight attributes
        flight.departure_time = data.get('departure_time', flight.departure_time)
        flight.arrival_time = data.get('arrival_time', flight.arrival_time)
        flight.plane_id = data.get('plane_id', flight.plane_id)
        flight.pilot_id = data.get('pilot_id', flight.pilot_id)
        flight.departure_destination = data.get('departure_destination', flight.departure_destination)
        flight.destination = data.get('destination', flight.destination)
        db.session.commit()
        return jsonify({'message': f"Flight with id {flight_id} updated"})
    else:
        return jsonify({'message': f"Flight with id {flight_id} not found"}), 404