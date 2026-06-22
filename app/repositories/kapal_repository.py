from app.repositories.base import BaseRepository
from app.models.kapal import Kapal
from app.models.gambar_kapal import GambarKapal
from app.models.inspeksi import Inspeksi

class KapalRepository(BaseRepository):
    def __init__(self):
        super().__init__(Kapal)

class GambarKapalRepository(BaseRepository):
    def __init__(self):
        super().__init__(GambarKapal)

class InspeksiRepository(BaseRepository):
    def __init__(self):
        super().__init__(Inspeksi)
