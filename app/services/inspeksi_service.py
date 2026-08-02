from app.repositories.kapal_repository import KapalRepository, InspeksiRepository
from app.models.kapal import Kapal
from app.models.inspeksi import Inspeksi
from app.services.scoring_service import ScoringService

class InspeksiService:
    def __init__(self):
        self.kapal_repo = KapalRepository()
        self.inspeksi_repo = InspeksiRepository()
        self.scoring_service = ScoringService()

    def create_inspeksi(self, data, svm_result):
        # 1. Simpan Data Kapal
        kapal = Kapal(
            nama_kapal=data['nama_kapal'],
            pemilik=data['pemilik'],
            nomor_registrasi=data['nomor_registrasi']
        )
        self.kapal_repo.save(kapal)

        # 2. Hitung Skor
        apar = int(data.get('apar', 0))
        jaket = int(data.get('jaket', 0))
        mesin = int(data.get('mesin', 0))

        skor, status = self.scoring_service.hitung_skor(
            svm_result, apar, jaket, mesin
        )

        # 3. Simpan Inspeksi
        inspeksi = Inspeksi(
            kapal_id=kapal.id,
            apar=apar,
            jaket=jaket,
            mesin=mesin,
            skor=skor,
            status_kelayakan=status
        )
        self.inspeksi_repo.save(inspeksi)

        return kapal, inspeksi
