class ScoringService:
    @staticmethod
    def hitung_skor(svm_result, apar, radio, jaket, mesin):
        """
        Menghitung skor kelayakan kapal berdasarkan rule:
        - Lambung Baik = 35 (Rusak = 0)
        - APAR = 25
        - Jaket = 20
        - Radio = 10
        - Mesin = 10
        Total = 100
        Jika >= 80 -> Layak, else Tidak Layak
        """
        skor = 0
        
        if svm_result == "Baik":
            skor += 35
            
        skor += apar * 25
        skor += radio * 10
        skor += jaket * 20
        skor += mesin * 10
        
        status = "Layak" if skor >= 80 else "Tidak Layak"
        
        return skor, status
