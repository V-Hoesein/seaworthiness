from flask import render_template, request, redirect, url_for, flash
from app.services.inspeksi_service import InspeksiService
from app.services.ml_service import MLService
import traceback

class InspeksiController:
    def __init__(self):
        self.inspeksi_service = InspeksiService()
        self.ml_service = MLService()

    def create_form(self):
        return render_template('inspeksi_form.html')

    def submit_form(self):
        try:
            # Get Form Data
            data = request.form
            file = request.files.get('foto_lambung')

            if not file or file.filename == '':
                flash('File foto lambung harus diunggah.', 'danger')
                return redirect(url_for('main.create_inspeksi'))

            # Karena flow memerlukan ID Kapal sebelum gambar disimpan,
            # Kita bisa membalik logika, atau menyimpan Kapal dulu tanpa gambar,
            # lalu mengupdate gambar. Untuk kemudahan, kita simpan Kapal & Inspeksi dulu.
            
            # Sementara kita lakukan ekstraksi dulu dan kita akan mendapatkan hasil SVM,
            # Namun MLService butuh kapal_id. 
            # Mari kita adjust flow: 
            # 1. Simpan Kapal & Hitung Skor
            # Kita butuh hasil SVM untuk dihitung skornya.
            # Jadi kita extract dan predict dulu TANPA save gambar_kapal ke DB,
            # Atau kita bisa modifikasi sedikit.
            
            # HACK: Predict first
            # We save file temporarily, predict, then we save the Kapal, Inspeksi, and Gambar
            filepath = file.filename
            import os
            from werkzeug.utils import secure_filename
            from app.config import Config
            
            filename = secure_filename(file.filename)
            temp_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(temp_path)
            
            features = self.ml_service.hog_extractor.extract_features(temp_path)
            svm_result = self.ml_service.svm_classifier.predict(features)
            
            # Create Kapal & Inspeksi
            kapal, inspeksi = self.inspeksi_service.create_inspeksi(data, svm_result)
            
            # Save GambarKapal
            from app.models.gambar_kapal import GambarKapal
            from app.repositories.kapal_repository import GambarKapalRepository
            gambar = GambarKapal(
                kapal_id=kapal.id,
                image_path=filename,
                svm_result=svm_result
            )
            GambarKapalRepository().save(gambar)
            
            flash(f'Inspeksi berhasil! Status: {inspeksi.status_kelayakan}', 'success')
            return redirect(url_for('main.index'))

        except Exception as e:
            traceback.print_exc()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('main.create_inspeksi'))
