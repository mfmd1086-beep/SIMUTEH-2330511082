# SIMUTEH - Praktikum P5-P6 Computer Vision
Nama: Muhammad Fahmi | NIM: 2330511082 | Kelas: TI-7B | SEED: 1986

## Cara menjalankan
1. `pip install -r requirements.txt`
2. Dari folder utama: `python src/buat_dataset_sintetis.py`
3. Simpan parameter praproses (`hasil/param_praproses.json`, konfigurasi E dari Evaluasi P1-P4).
4. Jalankan `notebook/P5_tepi.ipynb` lalu `notebook/P6_morfologi.ipynb` dengan Restart & Run All.

## Ringkasan hasil
- P5: Canny kanal R sesudah praproses (sigma 2, ambang 30/90) F1 tepi 0,972. Ambang otomatis dari median gagal pada Gray kontras rendah; ambang persentil (q = 98) berhasil (F1 R 0,988).
- Keputusan: tepi dipakai sebagai pemeriksa batas, bukan untuk luas bercak.
- P6: opening + closing elips 5x5, komponen terhubung konektivitas 8, filter luas >= 20, kebulatan >= 0,5, rasio aspek <= 1,8.
- Evaluasi 60 citra: akurasi kelas 0,983, galat persen 0,335 poin, korelasi 0,967 (1 kesalahan: teh_025).

## Cara memakai analisis_daun
```python
from praproses import praproses
from bercak import analisis_daun
h = analisis_daun(praproses(img_bgr, PARAM))   # img_bgr: citra BGR
h["jumlah_bercak"], h["persen_bercak"], h["kelas"], h["bercak"]
```

## Git
```
git add . && git commit -m "P5: deteksi tepi dan keputusan pemakaian"
git tag v0.2-tepi
git add . && git commit -m "P6: morfologi dan bercak.py"
git tag v0.3-morfologi && git push && git push --tags
```
