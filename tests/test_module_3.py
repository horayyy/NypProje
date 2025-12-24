"""
Module 3 Test Suite
Maç, lig ve turnuva organizasyonlarının yönetimi testleri
"""

import unittest
from datetime import datetime, timedelta
import sys
import os

# Proje root dizinini path'e ekle
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.modules.module_3.base import SporTipi, TurnuvaHatasi, MacTipi
from app.modules.module_3.implementations import LigMaci, HazirlikMaci, ElemeMaci
from app.modules.module_3.repository import (
    LigYonetimi, 
    FiksturOlusturucu, 
    PuanTablosu, 
    LigRepository,
    MacRepository
)


# ============================================================================
# MAÇ OLUŞTURMA TESTLERİ
# ============================================================================

class TestMacOlusturma(unittest.TestCase):
    """Maç oluşturma testleri"""
    
    def test_lig_maci_olusturma(self):
        """Lig maçı oluşturma testi"""
        tarih = datetime(2024, 9, 15, 15, 0)
        mac = LigMaci(
            mac_id=1,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=tarih,
            lig_adi="Süper Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        self.assertEqual(mac.mac_id, 1)
        self.assertEqual(mac.ev_sahibi, "Galatasaray")
        self.assertEqual(mac.deplasman, "Fenerbahçe")
        self.assertEqual(mac.lig_adi, "Süper Lig")
        self.assertEqual(mac.hafta_no, 1)
        self.assertEqual(mac.mac_tipi, MacTipi.LEAGUE)
        self.assertEqual(mac.durum, "planlandi")
    
    def test_hazirlik_maci_olusturma(self):
        """Hazırlık maçı oluşturma testi"""
        tarih = datetime(2024, 8, 10, 19, 0)
        mac = HazirlikMaci(
            mac_id=2,
            ev_sahibi="Beşiktaş",
            deplasman="Trabzonspor",
            tarih_saat=tarih,
            organizasyon_adi="Yaz Hazırlık Turnuvası"
        )
        
        self.assertEqual(mac.mac_id, 2)
        self.assertEqual(mac.ev_sahibi, "Beşiktaş")
        self.assertEqual(mac.deplasman, "Trabzonspor")
        self.assertEqual(mac.organizasyon_adi, "Yaz Hazırlık Turnuvası")
        self.assertEqual(mac.mac_tipi, MacTipi.FRIENDLY)
    
    def test_eleme_maci_olusturma(self):
        """Eleme maçı oluşturma testi"""
        tarih = datetime(2024, 10, 5, 20, 0)
        mac = ElemeMaci(
            mac_id=3,
            ev_sahibi="Real Madrid",
            deplasman="Barcelona",
            tarih_saat=tarih,
            tur_adi="Çeyrek Final"
        )
        
        self.assertEqual(mac.mac_id, 3)
        self.assertEqual(mac.ev_sahibi, "Real Madrid")
        self.assertEqual(mac.deplasman, "Barcelona")
        self.assertEqual(mac.tur_adi, "Çeyrek Final")
        self.assertEqual(mac.mac_tipi, MacTipi.TOURNAMENT)
    
    def test_gecersiz_mac_id(self):
        """Geçersiz maç ID testi"""
        tarih = datetime(2024, 9, 15, 15, 0)
        with self.assertRaises(TurnuvaHatasi):
            LigMaci(
                mac_id=-1,  # Negatif ID
                ev_sahibi="Galatasaray",
                deplasman="Fenerbahçe",
                tarih_saat=tarih,
                lig_adi="Süper Lig",
                hafta_no=1
            )
    
    def test_gecersiz_takim_adi(self):
        """Geçersiz takım adı testi"""
        tarih = datetime(2024, 9, 15, 15, 0)
        with self.assertRaises(TurnuvaHatasi):
            LigMaci(
                mac_id=1,
                ev_sahibi="AB",  # 3 karakterden kısa
                deplasman="Fenerbahçe",
                tarih_saat=tarih,
                lig_adi="Süper Lig",
                hafta_no=1
            )


# ============================================================================
# SONUÇ GİRİŞ TESTLERİ
# ============================================================================

class TestSonucGirisi(unittest.TestCase):
    """Sonuç giriş testleri"""
    
    def setUp(self):
        """Test öncesi hazırlık"""
        self.tarih = datetime(2024, 9, 15, 15, 0)
        self.mac = LigMaci(
            mac_id=1,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="Süper Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
    
    def test_skor_girisi_futbol(self):
        """Futbol skor girişi testi"""
        self.mac.skor_belirle(3, 1)
        
        self.assertTrue(self.mac.skor_girildi_mi)
        self.assertEqual(self.mac.skor_ev, 3)
        self.assertEqual(self.mac.skor_deplasman, 1)
        self.assertEqual(self.mac.skor, "3-1")
        self.assertEqual(self.mac.durum, "planlandi")  # Durum otomatik değişmez
    
    def test_skor_girisi_beraberlik_futbol(self):
        """Futbol beraberlik skoru testi"""
        self.mac.skor_belirle(2, 2)
        
        self.assertEqual(self.mac.skor_ev, 2)
        self.assertEqual(self.mac.skor_deplasman, 2)
    
    def test_skor_girisi_voleybol(self):
        """Voleybol skor girişi testi (set skorları)"""
        voleybol_mac = LigMaci(
            mac_id=2,
            ev_sahibi="Eczacıbaşı",
            deplasman="Vakıfbank",
            tarih_saat=self.tarih,
            lig_adi="Sultanlar Ligi",
            hafta_no=1,
            spor_tipi=SporTipi.VOLEYBOL
        )
        
        voleybol_mac.skor_belirle(3, 1)  # 3 set - 1 set
        
        self.assertEqual(voleybol_mac.skor_ev, 3)
        self.assertEqual(voleybol_mac.skor_deplasman, 1)
    
    def test_skor_girisi_basketbol(self):
        """Basketbol skor girişi testi"""
        basketbol_mac = LigMaci(
            mac_id=3,
            ev_sahibi="Anadolu Efes",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="BSL",
            hafta_no=1,
            spor_tipi=SporTipi.BASKETBOL
        )
        
        basketbol_mac.skor_belirle(95, 88)
        
        self.assertEqual(basketbol_mac.skor_ev, 95)
        self.assertEqual(basketbol_mac.skor_deplasman, 88)
    
    def test_beraberlik_gecersiz_voleybol(self):
        """Voleybol için beraberlik geçersiz testi"""
        voleybol_mac = LigMaci(
            mac_id=4,
            ev_sahibi="Eczacıbaşı",
            deplasman="Vakıfbank",
            tarih_saat=self.tarih,
            lig_adi="Sultanlar Ligi",
            hafta_no=1,
            spor_tipi=SporTipi.VOLEYBOL
        )
        
        with self.assertRaises(TurnuvaHatasi):
            voleybol_mac.skor_belirle(3, 3)  # Beraberlik olamaz
    
    def test_negatif_skor(self):
        """Negatif skor testi"""
        with self.assertRaises(TurnuvaHatasi):
            self.mac.skor_belirle(-1, 2)
    
    def test_durum_guncelleme(self):
        """Maç durumu güncelleme testi"""
        self.mac.skor_belirle(2, 1)
        self.mac.durum = "tamamlandi"
        
        self.assertEqual(self.mac.durum, "tamamlandi")


# ============================================================================
# PUAN HESAPLAMA TESTLERİ
# ============================================================================

class TestPuanHesaplama(unittest.TestCase):
    """Puan hesaplama testleri"""
    
    def setUp(self):
        """Test öncesi hazırlık"""
        self.tarih = datetime(2024, 9, 1)
        self.lig = LigYonetimi("Test Lig", SporTipi.FUTBOL, self.tarih)
        self.lig.takim_ekle("Galatasaray")
        self.lig.takim_ekle("Fenerbahçe")
        self.lig.takim_ekle("Beşiktaş")
        self.puan_tablosu = PuanTablosu(self.lig)
    
    def test_galibiyet_puani_futbol(self):
        """Futbol galibiyet puanı testi"""
        mac = LigMaci(
            mac_id=1,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="Test Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        mac.skor_belirle(3, 1)
        mac.durum = "tamamlandi"
        self.puan_tablosu.mac_sonucu_gir(mac)
        
        gs_istatistik = self.puan_tablosu.takim_istatistikleri_getir("Galatasaray")
        self.assertEqual(gs_istatistik["puan"], 3)  # Futbol galibiyet = 3 puan
        self.assertEqual(gs_istatistik["galibiyet"], 1)
        self.assertEqual(gs_istatistik["atilan"], 3)
        self.assertEqual(gs_istatistik["yenilen"], 1)
        self.assertEqual(gs_istatistik["averaj"], 2)
    
    def test_beraberlik_puani_futbol(self):
        """Futbol beraberlik puanı testi"""
        mac = LigMaci(
            mac_id=2,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="Test Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        mac.skor_belirle(2, 2)
        mac.durum = "tamamlandi"
        self.puan_tablosu.mac_sonucu_gir(mac)
        
        gs_istatistik = self.puan_tablosu.takim_istatistikleri_getir("Galatasaray")
        fb_istatistik = self.puan_tablosu.takim_istatistikleri_getir("Fenerbahçe")
        
        self.assertEqual(gs_istatistik["puan"], 1)  # Futbol beraberlik = 1 puan
        self.assertEqual(fb_istatistik["puan"], 1)
        self.assertEqual(gs_istatistik["beraberlik"], 1)
        self.assertEqual(fb_istatistik["beraberlik"], 1)
    
    def test_maglubiyet_puani_futbol(self):
        """Futbol mağlubiyet puanı testi"""
        mac = LigMaci(
            mac_id=3,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="Test Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        mac.skor_belirle(0, 2)
        mac.durum = "tamamlandi"
        self.puan_tablosu.mac_sonucu_gir(mac)
        
        gs_istatistik = self.puan_tablosu.takim_istatistikleri_getir("Galatasaray")
        self.assertEqual(gs_istatistik["puan"], 0)  # Futbol mağlubiyet = 0 puan
        self.assertEqual(gs_istatistik["maglubiyet"], 1)
    
    def test_galibiyet_puani_voleybol(self):
        """Voleybol galibiyet puanı testi"""
        voleybol_lig = LigYonetimi("Voleybol Lig", SporTipi.VOLEYBOL, self.tarih)
        voleybol_lig.takim_ekle("Eczacıbaşı")
        voleybol_lig.takim_ekle("Vakıfbank")
        voleybol_puan = PuanTablosu(voleybol_lig)
        
        mac = LigMaci(
            mac_id=4,
            ev_sahibi="Eczacıbaşı",
            deplasman="Vakıfbank",
            tarih_saat=self.tarih,
            lig_adi="Voleybol Lig",
            hafta_no=1,
            spor_tipi=SporTipi.VOLEYBOL
        )
        
        mac.skor_belirle(3, 1)
        mac.durum = "tamamlandi"
        voleybol_puan.mac_sonucu_gir(mac)
        
        eczacibasi_istatistik = voleybol_puan.takim_istatistikleri_getir("Eczacıbaşı")
        self.assertEqual(eczacibasi_istatistik["puan"], 3)  # Voleybol galibiyet = 3 puan
        self.assertEqual(eczacibasi_istatistik["galibiyet"], 1)
    
    def test_puan_tablosu_siralama(self):
        """Puan tablosu sıralama testi"""
        # İlk maç: Galatasaray kazandı
        mac1 = LigMaci(
            mac_id=5,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="Test Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        mac1.skor_belirle(3, 1)
        mac1.durum = "tamamlandi"
        self.puan_tablosu.mac_sonucu_gir(mac1)
        
        # İkinci maç: Beşiktaş kazandı
        mac2 = LigMaci(
            mac_id=6,
            ev_sahibi="Beşiktaş",
            deplasman="Galatasaray",
            tarih_saat=self.tarih + timedelta(days=7),
            lig_adi="Test Lig",
            hafta_no=2,
            spor_tipi=SporTipi.FUTBOL
        )
        mac2.skor_belirle(2, 0)
        mac2.durum = "tamamlandi"
        self.puan_tablosu.mac_sonucu_gir(mac2)
        
        tablo = self.puan_tablosu.puan_tablosu_getir()
        
        # Beşiktaş 3 puan, Galatasaray 3 puan (ama averaj daha iyi)
        # Sıralama: puan, sonra averaj
        self.assertGreaterEqual(len(tablo), 2)
        # İlk sırada en yüksek puanlı takım olmalı
        self.assertIn(tablo[0]["takim"], ["Beşiktaş", "Galatasaray"])


# ============================================================================
# REPOSİTORY TESTLERİ
# ============================================================================

class TestRepository(unittest.TestCase):
    """Repository testleri"""
    
    def setUp(self):
        """Test öncesi hazırlık"""
        self.mac_repo = MacRepository()
        self.lig_repo = LigRepository()
        self.tarih = datetime(2024, 9, 15, 15, 0)
    
    def test_mac_kaydet(self):
        """Maç kaydetme testi"""
        mac = LigMaci(
            mac_id=1,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="Süper Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        self.mac_repo.mac_kaydet(mac)
        
        self.assertEqual(self.mac_repo.toplam_mac_sayisi(), 1)
    
    def test_mac_getir_id_ile(self):
        """ID'ye göre maç getirme testi"""
        mac = LigMaci(
            mac_id=10,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="Süper Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        self.mac_repo.mac_kaydet(mac)
        
        bulunan_mac = self.mac_repo.mac_getir_id_ile(10)
        self.assertIsNotNone(bulunan_mac)
        self.assertEqual(bulunan_mac.mac_id, 10)
        self.assertEqual(bulunan_mac.ev_sahibi, "Galatasaray")
    
    def test_mac_getir_id_ile_bulunamadi(self):
        """ID ile maç bulunamadı testi"""
        bulunan_mac = self.mac_repo.mac_getir_id_ile(999)
        self.assertIsNone(bulunan_mac)
    
    def test_maclari_tarihe_gore_filtrele(self):
        """Tarihe göre filtreleme testi"""
        # Farklı tarihlerde maçlar oluştur
        mac1 = LigMaci(
            mac_id=1,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=datetime(2024, 9, 10, 15, 0),
            lig_adi="Süper Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        mac2 = LigMaci(
            mac_id=2,
            ev_sahibi="Beşiktaş",
            deplasman="Trabzonspor",
            tarih_saat=datetime(2024, 9, 20, 15, 0),
            lig_adi="Süper Lig",
            hafta_no=2,
            spor_tipi=SporTipi.FUTBOL
        )
        
        mac3 = LigMaci(
            mac_id=3,
            ev_sahibi="Başakşehir",
            deplasman="Konyaspor",
            tarih_saat=datetime(2024, 9, 30, 15, 0),
            lig_adi="Süper Lig",
            hafta_no=3,
            spor_tipi=SporTipi.FUTBOL
        )
        
        self.mac_repo.mac_kaydet(mac1)
        self.mac_repo.mac_kaydet(mac2)
        self.mac_repo.mac_kaydet(mac3)
        
        # 15 Eylül - 25 Eylül arası maçları filtrele
        filtrelenmis = self.mac_repo.maclari_tarihe_gore_filtrele(
            baslangic_tarihi=datetime(2024, 9, 15),
            bitis_tarihi=datetime(2024, 9, 25)
        )
        
        self.assertEqual(len(filtrelenmis), 1)
        self.assertEqual(filtrelenmis[0].mac_id, 2)  # Sadece mac2 bu aralıkta
    
    def test_maclari_lig_adi_ile_filtrele(self):
        """Lig adına göre filtreleme testi"""
        mac1 = LigMaci(
            mac_id=1,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="Süper Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        mac2 = LigMaci(
            mac_id=2,
            ev_sahibi="Eczacıbaşı",
            deplasman="Vakıfbank",
            tarih_saat=self.tarih,
            lig_adi="Sultanlar Ligi",
            hafta_no=1,
            spor_tipi=SporTipi.VOLEYBOL
        )
        
        hazirlik_mac = HazirlikMaci(
            mac_id=3,
            ev_sahibi="Beşiktaş",
            deplasman="Trabzonspor",
            tarih_saat=self.tarih,
            organizasyon_adi="Yaz Turnuvası"
        )
        
        self.mac_repo.mac_kaydet(mac1)
        self.mac_repo.mac_kaydet(mac2)
        self.mac_repo.mac_kaydet(hazirlik_mac)
        
        # Süper Lig maçlarını filtrele
        filtrelenmis = self.mac_repo.maclari_lig_turnuva_adi_ile_filtrele("Süper Lig")
        
        self.assertEqual(len(filtrelenmis), 1)
        self.assertEqual(filtrelenmis[0].mac_id, 1)
        self.assertEqual(filtrelenmis[0].lig_adi, "Süper Lig")
    
    def test_maclari_turnuva_adi_ile_filtrele(self):
        """Turnuva adına göre filtreleme testi"""
        eleme_mac = ElemeMaci(
            mac_id=1,
            ev_sahibi="Real Madrid",
            deplasman="Barcelona",
            tarih_saat=self.tarih,
            tur_adi="Çeyrek Final"
        )
        
        hazirlik_mac = HazirlikMaci(
            mac_id=2,
            ev_sahibi="Beşiktaş",
            deplasman="Trabzonspor",
            tarih_saat=self.tarih,
            organizasyon_adi="Yaz Turnuvası"
        )
        
        self.mac_repo.mac_kaydet(eleme_mac)
        self.mac_repo.mac_kaydet(hazirlik_mac)
        
        # Çeyrek Final maçlarını filtrele
        filtrelenmis = self.mac_repo.maclari_lig_turnuva_adi_ile_filtrele("Çeyrek Final")
        
        self.assertEqual(len(filtrelenmis), 1)
        self.assertEqual(filtrelenmis[0].mac_id, 1)
        self.assertEqual(filtrelenmis[0].tur_adi, "Çeyrek Final")
    
    def test_tum_maclari_getir(self):
        """Tüm maçları getirme testi"""
        mac1 = LigMaci(
            mac_id=1,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=datetime(2024, 9, 10, 15, 0),
            lig_adi="Süper Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        mac2 = LigMaci(
            mac_id=2,
            ev_sahibi="Beşiktaş",
            deplasman="Trabzonspor",
            tarih_saat=datetime(2024, 9, 20, 15, 0),
            lig_adi="Süper Lig",
            hafta_no=2,
            spor_tipi=SporTipi.FUTBOL
        )
        
        self.mac_repo.mac_kaydet(mac1)
        self.mac_repo.mac_kaydet(mac2)
        
        tum_maclar = self.mac_repo.tum_maclari_getir()
        
        self.assertEqual(len(tum_maclar), 2)
        # Tarih sırasına göre sıralanmış olmalı
        self.assertEqual(tum_maclar[0].mac_id, 1)
        self.assertEqual(tum_maclar[1].mac_id, 2)
    
    def test_mac_sil(self):
        """Maç silme testi"""
        mac = LigMaci(
            mac_id=1,
            ev_sahibi="Galatasaray",
            deplasman="Fenerbahçe",
            tarih_saat=self.tarih,
            lig_adi="Süper Lig",
            hafta_no=1,
            spor_tipi=SporTipi.FUTBOL
        )
        
        self.mac_repo.mac_kaydet(mac)
        self.assertEqual(self.mac_repo.toplam_mac_sayisi(), 1)
        
        self.mac_repo.mac_sil(1)
        self.assertEqual(self.mac_repo.toplam_mac_sayisi(), 0)
        
        with self.assertRaises(TurnuvaHatasi):
            self.mac_repo.mac_sil(1)  # Zaten silinmiş
    
    def test_lig_repository(self):
        """Lig repository testi"""
        tarih = datetime(2024, 9, 1)
        lig = LigYonetimi("Test Lig", SporTipi.FUTBOL, tarih)
        lig.takim_ekle("Galatasaray")
        lig.takim_ekle("Fenerbahçe")
        
        self.lig_repo.lig_kaydet(lig)
        
        bulunan_lig = self.lig_repo.lig_getir("Test Lig")
        self.assertIsNotNone(bulunan_lig)
        self.assertEqual(bulunan_lig.lig_adi, "Test Lig")
        
        tum_ligler = self.lig_repo.tum_ligler_getir()
        self.assertEqual(len(tum_ligler), 1)
        
        self.lig_repo.lig_sil("Test Lig")
        bulunan_lig = self.lig_repo.lig_getir("Test Lig")
        self.assertIsNone(bulunan_lig)


# ============================================================================
# FİKSTÜR OLUŞTURMA TESTLERİ
# ============================================================================

class TestFiksturOlusturma(unittest.TestCase):
    """Fikstür oluşturma testleri"""
    
    def test_fikstur_olustur(self):
        """Fikstür oluşturma testi"""
        tarih = datetime(2024, 9, 1)
        lig = LigYonetimi("Test Lig", SporTipi.FUTBOL, tarih)
        lig.takim_ekle("Galatasaray")
        lig.takim_ekle("Fenerbahçe")
        lig.takim_ekle("Beşiktaş")
        lig.takim_ekle("Trabzonspor")
        
        fikstur = lig.fikstur_olustur()
        
        self.assertIsNotNone(fikstur)
        self.assertGreater(fikstur.toplam_hafta_sayisi(), 0)
    
    def test_haftalik_maclar_getir(self):
        """Haftalık maçlar getirme testi"""
        tarih = datetime(2024, 9, 1)
        lig = LigYonetimi("Test Lig", SporTipi.FUTBOL, tarih)
        lig.takim_ekle("Galatasaray")
        lig.takim_ekle("Fenerbahçe")
        
        lig.fikstur_olustur()
        maclar = lig.haftalik_maclar_getir(1)
        
        self.assertGreater(len(maclar), 0)
        self.assertIsInstance(maclar[0], LigMaci)


if __name__ == '__main__':
    unittest.main()

