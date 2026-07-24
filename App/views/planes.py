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
    
@plane_views.route('/api/create_plane',methods=['GET'])
@jwt_required()
def create_plane_page():
    if not jwt_current_user.is_admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    return render_template('Plane Creation.html')

@plane_views.route('/api/plane_creation',methods=['POST'])
def create_plane_action():
    plane_model = request.form.get('model')
    plane_capacity = request.form.get('capacity')
    success = create_Plane(plane_model,plane_capacity)
    if not success:
        flash("Plane could not be created")
    flash("Plane created!")
    return redirect(url_for('index_views.home_page'))

@plane_views.route('/api/update_plane/<int:plane_id>',methods=['GET'])
def plane_update_page(plane_id):
    plane = Plane.query.get(plane_id)
    if not plane:
        flash("Plane not found")
        return redirect(url_for('index_views.home_page'))
    return render_template('Plane Updates.html',plane=plane)

@plane_views.route('/api/update_plane',methods=['POST'])
def update_plane_action():
    plane_id = request.form.get('plane_id')
    plane_id = int(plane_id)
    plane_model = request.form.get('model')
    plane_capacity = request.form.get('capacity')
    success = update_plane(plane_id,plane_model,plane_capacity)
    if not success:
        flash("Plane could not be updated")
    flash("Plane updated!")
    return redirect(url_for('index_views.home_page'))