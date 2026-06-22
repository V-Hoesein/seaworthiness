# Seaworthiness Classification System (Sistem Klasifikasi Kelayakan Kapal)

Sebuah aplikasi web berbasis Flask untuk melakukan **Klasifikasi Kelayakan Kapal Penangkap Ikan** secara hybrid. Sistem ini menggabungkan penilaian kondisi fisik kapal (lambung kapal) menggunakan pendekatan _Machine Learning_ (**HOG - Histogram of Oriented Gradients** dan **SVM - Support Vector Machine**) dengan perhitungan skoring berbasis aturan (_Rule-based Scoring System_) untuk aspek inspeksi administratif dan fungsional perlengkapan.

Aplikasi ini didesain menggunakan pola arsitektur **MVC (Model-View-Controller)** dan **Service Layer** guna memastikan kode terstruktur dengan baik (bersih), mudah dipelihara, dan setara dengan standar proyek akademis tingkat skripsi/penelitian.

---

## ✨ Fitur Utama

1. **HOG-SVM Machine Learning Model**: Mengekstraksi fitur visual pada gambar lambung kapal menggunakan HOG dan mengklasifikasikan kondisinya menjadi **Baik** atau **Rusak** menggunakan SVM.
2. **Rule-Based Scoring**: Menghitung kelayakan fungsional atau dokumen administrasi kapal berbasis aturan persentase/skoring.
3. **Penyimpanan Terstruktur (Database)**: Manajemen data kapal, gambar, dan hasil prediksi menggunakan SQLAlchemy ORM dengan dukungan relasi antar tabel database.
4. **Alur ML Terintegrasi (Pipeline)**: Tersedia file Jupyter Notebook untuk _training_, _tuning_, evaluasi model, hingga ekspor `.pkl` untuk di-_deploy_ di dalam aplikasi utama (Flask).

---

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python 3.8+
- **Web Framework**: Flask
- **Machine Learning**: Scikit-Learn, Scikit-Image, OpenCV, Numpy, Pandas
- **Database ORM**: Flask-SQLAlchemy (SQLite default)
- **Data Visualization & Notebook**: Jupyter Notebook, Matplotlib, Seaborn, Joblib

---

## 📂 Struktur Direktori Proyek

Proyek ini menggunakan pemisahan tanggung jawab (Separation of Concerns) melalui arsitektur berlapis:

```text
seaworthiness/
├── app/                        # Main Application Package
│   ├── config.py               # Konfigurasi Flask dan Path
│   ├── extensions.py           # Inisialisasi plugin seperti SQLAlchemy
│   ├── ml/                     # Modul spesifik ML (HOG Feature & SVM Predictor)
│   ├── models/                 # ORM Database Models (Model MVC)
│   ├── repositories/           # Akses Data / Queries (Data Access Layer)
│   ├── routes/                 # Controllers / Flask Blueprints (View/Controller)
│   └── services/               # Bussiness Logic & Orchestration (Service Layer)
├── dataset/                    # Dataset mentah untuk proses ML (baik/ & rusak/)
├── models/                     # Tempat hasil training disimpan (svm_model.pkl, scaler.pkl)
├── instance/                   # Direktori penyimpanan database lokal (SQLite)
├── Klasifikasi_Kelayakan_Kapal_HOG_SVM.ipynb  # Jupyter Notebook untuk training & eksperimen model
├── run.py                      # Entry point Flask App
└── requirements.txt            # Daftar library dan dependencies
```

---

## 🚀 Setup & Instalasi

### 1. Prasyarat

Pastikan komputer Anda sudah terinstal Python versi 3.8 atau yang lebih baru. Sangat direkomendasikan menggunakan _Virtual Environment_.

### 2. Langkah Instalasi

```bash
# 1. Clone atau masuk ke dalam folder direktori
cd d:/Programming/seaworthiness

# 2. Buat virtual environment (Direkomendasikan)
python -m venv .venv

# 3. Aktifkan virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 🧠 Alur Kerja Sistem (App Flow & Mechanism)

Sistem bekerja melalui 2 bagian utama yang saling terintegrasi: **Model Training (Offline)** dan **Flask Web Application (Online/Real-time)**.

### Bagian 1: Machine Learning Flow (Jupyter Notebook)

Flow ini mengatur bagaimana sistem mempelajari visualisasi lambung kapal untuk menghasilkan model pintar (AI).

1. **Load Data**: Gambar dibaca dari direktori `dataset/baik` dan `dataset/rusak`.
2. **Preprocessing Image**: Setiap gambar akan di-resize menjadi 128x128 piksel dan diubah ke dalam format Grayscale (_hitam putih_).
3. **HOG Feature Extraction**: Gambar diubah menjadi kumpulan matriks angka (fitur HOG) berdasarkan orientasi sudut tekstur dan tepian gambar (Parameter: `orientations=9`, `pixels_per_cell=(8,8)`, `cells_per_block=(2,2)`).
4. **Scaling**: Fitur yang didapat dinormalisasi (Z-score) menggunakan `StandardScaler`. Standar (_scaler_) ini kemudian disimpan sebagai `models/scaler.pkl`.
5. **SVM Training**: Fitur yang telah dinormalisasi dimasukkan ke Support Vector Machine. Dilakukan _Hyperparameter Tuning_ (GridSearchCV) dengan mencoba model Linear dan RBF.
6. **Save Model**: Model dengan akurasi terbaik diekspor dalam bentuk file _pickle_ dan disimpan di `models/svm_model.pkl`.

### Bagian 2: Web Application Flow (Flask)

Ketika _user_ mengakses web dan mencoba melakukan evaluasi kelayakan kapal:

1. **User Request**: User membuka aplikasi web, memilih kapal, dan mengunggah (_upload_) gambar lambung kapal. File tersebut masuk ke jalur HTTP di dalam `app/routes/`.
2. **Service Layer Execution**: Request akan dilempar dari _Controller (Route)_ menuju _Service Layer_ (`ml_service.py`).
3. **Feature Extraction & Scaling**:
   - Web memanggil kelas _HOGExtractor_ (`app/ml/hog_extractor.py`) untuk memproses gambar yang diunggah secara otomatis (Resize, Grayscale, dan HOG).
   - Fitur diserahkan kepada `SVMClassifier` (`app/ml/svm_model.py`) lalu dinormalisasi ulang menggunakan memori `scaler.pkl` agar sesuai skala fitur saat di-_training_.
4. **Prediction**: Model `svm_model.pkl` yang sudah termuat (`load`) di aplikasi Flask akan menerima fitur normalisasi tersebut, memprediksinya (Angka 1/0), dan menerjemahkannya ke dalam string **"Baik"** atau **"Rusak"**.
5. **Database Saving**: Hasil prediksi beserta informasi kapal disimpan ke tabel _Database_ (`app/models/gambar_kapal.py`) via perantara _Repository Pattern_.
6. **Response View**: Hasil dipulangkan ke _Controller_, kemudian dirender dan dimunculkan kembali ke tampilan layar User.

---

## 📐 Rumus Matematis & Metrik Evaluasi

Sistem ini secara konseptual bekerja menggunakan beberapa pondasi perhitungan berikut:

### 1. Standard Scaler (Z-Score Normalization)

Digunakan untuk menormalkan fitur HOG agar memiliki mean = 0 dan variansi = 1.

$$ z = \frac{x - \mu}{\sigma} $$

- $x$: Nilai fitur asli
- $\mu$: Rata-rata dari fitur data _training_
- $\sigma$: Standar deviasi dari fitur data _training_

### 2. Support Vector Machine (SVM)

Model mencoba menemukan _hyperplane_ optimal yang memaksimalkan margin antar dua kelas (Baik dan Rusak).

Fungsi prediksinya adalah:

$$ f(x) = \text{sign}\left(\sum\_{i=1}^{n} \alpha_i y_i K(x_i, x) + b\right) $$

- $\alpha_i$: Pengali Lagrange
- $y_i$: Label kelas (misal: 1 atau -1)
- $K(x_i, x)$: Fungsi Kernel (Linear atau Radial Basis Function / RBF)
- $b$: Bias

### 3. Metrik Evaluasi Confusion Matrix

Digunakan untuk mengukur performa model pada data _Testing_:

- **Accuracy**: Persentase tebakan benar secara keseluruhan.
  $$ \text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} $$
- **Precision**: Rasio tebakan "Baik" yang memang benar "Baik".
  $$ \text{Precision} = \frac{TP}{TP + FP} $$
- **Recall**: Seberapa mampu model menemukan semua kasus "Baik" (Sensitivitas).
  $$ \text{Recall} = \frac{TP}{TP + FN} $$
- **F1-Score**: Rata-rata harmonik dari Precision dan Recall.
  $$ F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} $$

_(Keterangan: TP = True Positive, TN = True Negative, FP = False Positive, FN = False Negative)_

---

## 🏃‍♂️ Menjalankan Aplikasi

**1. Training Model (Optional)**  
Jika Anda telah memasukkan data gambar terbaru ke `dataset/`, Anda perlu melatih ulang model sebelum menjalankan aplikasi web. Buka _Jupyter Notebook_ atau _VS Code_ dan jalankan seluruh baris (_Run All_) pada file `Klasifikasi_Kelayakan_Kapal_HOG_SVM.ipynb`.

**2. Menjalankan Server Web (Flask)**  
Jalankan perintah ini di dalam terminal:

```bash
python run.py
```

Aplikasi web dapat diakses melalui web browser Anda pada alamat: **http://127.0.0.1:5000** atau **http://localhost:5000**.
