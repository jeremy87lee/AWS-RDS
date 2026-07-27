from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers.user import get_all_flights_json, delete_pilot,update_pilot
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