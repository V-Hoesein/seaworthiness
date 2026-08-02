class ScoringService:
    @staticmethod
    def hitung_skor(svm_result, apar, jaket, mesin):
        """
        Menghitung skor kelayakan kapal berdasarkan rule:
        - Lambung Baik = 40 (Rusak = 0)
        - APAR = 25
        - Jaket = 20
        - Mesin = 15
        Total = 100
        Jika >= 80 -> Layak, else Tidak Layak
        """
        skor = 0
        
        if svm_result == "Baik":
            skor += 40
            
        skor += apar * 25
        skor += jaket * 20
        skor += mesin * 15
        
        status = "Layak" if skor >= 80 else "Tidak Layak"
        
        return skor, status
