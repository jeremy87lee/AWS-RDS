from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers.user import get_all_flights_json, delete_plane, create_Plane, update_plane
from App.models.Planes import Plane
from App.models.flights import Flight
from App.models.pilots import Pilot
from App.views.user import user_views
from App.database import db
from App.views.index import index_views

plane_views = Blueprint('plane_views', __name__, template_folder='../templates')

@plane_views.route('/api/delete_plane',methods=['POST'])
def delete_plane_action():
    plane_id = request.form.get('plane_id')
    plane_id = int(plane_id)
    plane = Plane.query.get(plane_id)
    if not plane:
       flash("Plane not found! Can't delete")
    success = delete_plane(plane_id)
    if not success:
        flash("Plane not deleted!")
    else:
        return redirect(url_for('index_views.home_page'))
    