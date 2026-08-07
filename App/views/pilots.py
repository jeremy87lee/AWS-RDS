from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers.user import get_all_flights_json, delete_pilot,update_pilot,create_Pilot
from App.models.Planes import Plane
from App.models.flights import Flight
from App.models.pilots import Pilot
from App.views.user import user_views
from App.database import db
from App.views.index import index_views

pilot_views = Blueprint('pilot_views', __name__, template_folder='../templates')

@pilot_views.route('/api/delete_pilot',methods=['POST'])
def delete_pilot_action():
    pilot_id = request.form.get('pilot_id')
    pilot_id = int(pilot_id)
    success = delete_pilot(pilot_id)
    if success:
        flash("Pilot deleted!")
        return redirect(url_for('index_views.home_page'))
    flash("Pilot could not be deleted!")
    return redirect(url_for('index_views.home_page'))

@pilot_views.route('/api/create_pilot',methods=['GET'])
def pilot_creation_page():
    return render_template('Pilot Creation.html')

@pilot_views.route('/api/pilot_creation', methods=['POST'])
def create_pilot_action():
    pilot_name = request.form.get('pilot_name')
    if not pilot_name:
        flash("Missing required fields")
        return redirect(url_for('index_views.home_page'))
    success = create_Pilot(pilot_name)
    if success:
        flash("Pilot created!")
    else:
        flash("Pilot could not be created!")
    return redirect(url_for('index_views.home_page'))

@pilot_views.route('/api/pilot_updates/<int:pilot_id>',methods=['GET'])
def pilot_update_page(pilot_id):
    pilot = Pilot.query.get(pilot_id)
    return render_template('Pilot Updates.html',pilot=pilot)

@pilot_views.route('/api/update_pilot',methods=['POST'])
def update_pilot_action():
    pilot_id = request.form.get('pilot_id')
    pilot_id = int(pilot_id)
    pilot_name = request.form.get('pilot_name')
    if not pilot_id or not pilot_name:
        flash("Missing required fields")
        return redirect(url_for('index_views.home_page'))
    success = update_pilot(pilot_id,pilot_name)
    if success:
        flash("Pilot updated!")
        return redirect(url_for('index_views.home_page'))
    flash("Pilot could not be updated!")
    return redirect(url_for('index_views.home_page'))