class ScoringService:
    @staticmethod
    def hitung_skor(svm_result, apar, radio, jaket, izin, mesin):
        """
        Menghitung skor kelayakan kapal berdasarkan rule:
        - Lambung Baik = 30 (Rusak = 0)
        - APAR = 20
        - Radio = 10
        - Jaket = 15
        - Izin = 15
        - Mesin = 10
        Total = 100
        Jika >= 80 -> Layak, else Tidak Layak
        """
        skor = 0
        
        if svm_result == "Baik":
            skor += 30
            
        skor += apar * 20
        skor += radio * 10
        skor += jaket * 15
        skor += izin * 15
        skor += mesin * 10
        
        status = "Layak" if skor >= 80 else "Tidak Layak"
        
        return skor, status
