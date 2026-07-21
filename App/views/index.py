from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize, get_all_pilots, get_all_planes, get_all_gates

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/home', methods=['GET'])
def home_page():
    pilots = get_all_pilots()
    planes = get_all_planes()
    return render_template('home.html',pilots=pilots,planes=planes)