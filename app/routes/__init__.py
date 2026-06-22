from flask import Blueprint
from app.controllers.home_controller import HomeController
from app.controllers.inspeksi_controller import InspeksiController

main_bp = Blueprint('main', __name__)

home_controller = HomeController()
inspeksi_controller = InspeksiController()

@main_bp.route('/')
def index():
    return home_controller.index()

@main_bp.route('/inspeksi/baru', methods=['GET'])
def create_inspeksi():
    return inspeksi_controller.create_form()

@main_bp.route('/inspeksi/baru', methods=['POST'])
def submit_inspeksi():
    return inspeksi_controller.submit_form()
