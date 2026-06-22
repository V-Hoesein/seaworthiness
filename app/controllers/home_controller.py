from flask import render_template
from app.repositories.kapal_repository import InspeksiRepository

class HomeController:
    def __init__(self):
        self.inspeksi_repo = InspeksiRepository()

    def index(self):
        inspeksi_list = self.inspeksi_repo.get_all()
        return render_template('dashboard.html', inspeksi_list=inspeksi_list)
