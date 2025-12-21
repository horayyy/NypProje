import unittest
import sys
import os
from datetime import datetime

# --- IMPORT AYARI ---
# Test dosyasının bulunduğu yerden iki klasör yukarı çıkıp (root)
# 'app' klasörünü Python'ın arama yoluna ekliyoruz.
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(root_dir, 'app', 'modules', 'module_2'))

# Şimdi modülleri import edebiliriz
try:
    from implementations import IndividualTrainingSession, TrainingManager
    from repository import TrainingRepository
    from exceptions import TakvimCakismasiHatasi, OturumBulunamadiHatasi
except ImportError as e:
    print(f"HATA: Modüller bulunamadı. Python Path: {sys.path}")
    raise e

class TestModule2(unittest.TestCase):
    
    def setUp(self):
        """Her testten önce çalışır, temiz bir ortam kurar."""
        self.repo = TrainingRepository()
        self.service = TrainingManager(self.repo)

    def test_antrenman_olusturma(self):
        """PDF Madde 117: Antrenman oluşturma testi"""
        t1 = IndividualTrainingSession(
            oturum_id=1, sure=60, athlete_id=101, antrenor_id=5,
            oturum_tipi="kondisyon", tarih_saat=datetime(2025, 6, 1, 10, 0)
        )
        self.service.oturum_olustur(t1)
        
        # Kaydedildi mi kontrol et
        kayit = self.repo.id_ile_bul(1)
        self.assertIsNotNone(kayit)
        self.assertEqual(kayit.oturum_id, 1)
        self.assertEqual(kayit.durum, "planlandı")

    def test_cakisma_kontrolu(self):
        """PDF Madde 118: Tarih/zaman çakışması testi"""
        # 1. Antrenman: Sporcu 101, Saat 10:00 - 11:00
        t1 = IndividualTrainingSession(
            oturum_id=1, sure=60, athlete_id=101, antrenor_id=5,
            tarih_saat=datetime(2025, 6, 1, 10, 0)
        )
        self.service.oturum_olustur(t1)
        
        # 2. Antrenman: Aynı Sporcu (101), Saat 10:30 (Çakışmalı)
        t2 = IndividualTrainingSession(
            oturum_id=2, sure=60, athlete_id=101, antrenor_id=6,
            tarih_saat=datetime(2025, 6, 1, 10, 30)
        )
        
        # Hata fırlatmasını bekliyoruz
        with self.assertRaises(TakvimCakismasiHatasi):
            self.service.oturum_olustur(t2)

    def test_iptal_islemi(self):
        """PDF Madde 119: İptal işlemi testi"""
        t1 = IndividualTrainingSession(1, 60, 101, 5, tarih_saat=datetime(2025, 6, 1, 14, 0))
        self.service.oturum_olustur(t1)
        
        self.service.oturum_iptal_et(1)
        
        kayit = self.repo.id_ile_bul(1)
        self.assertEqual(kayit.durum, "iptal_edildi")

if __name__ == '__main__':
    unittest.main()