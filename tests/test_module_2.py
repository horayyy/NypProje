"""
Module 2 Kapsamlı Test Suite
Modül 2'ün tüm fonksiyonlarının doğru çalıştığını otomatik olarak kontrol eder.
Kod değişikliklerinden sonra hızlıca doğrulama sağlar.
"""
import unittest
import sys
import os
from datetime import datetime
from typing import List

# --- IMPORT AYARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, root_dir)

try:
    from app.modules.module_2.base import AntrenmanOturumuTemel
    from app.modules.module_2.implementations import (
        IndividualTrainingSession,
        TeamTrainingSession,
        RehabTrainingSession,
        TrainingManager,
        TrainingPlan,
        TrainingSchedule,
        TrainingStatistics
    )
    from app.modules.module_2.repository import TrainingRepository
    from app.modules.module_2.exceptions import (
        TakvimCakismasiHatasi,
        OturumBulunamadiHatasi,
        DuplicateOturumHatasi,
        GecersizOturumIdHatasi,
        GecersizSporcuIdHatasi,
        GecersizSureHatasi,
        GecersizOturumTipiHatasi,
        GecersizOturumDurumuHatasi,
        GecersizSahaIdHatasi
    )
except ImportError as e:
    print(f"HATA: Modüller bulunamadı. Python Path: {sys.path}")
    raise e


class TestBaseClass(unittest.TestCase):
    """Base class metodlarını test eder."""
    
    def test_gecerli_oturum_tipleri_getir(self):
        """Base class'tan geçerli oturum tiplerini getirir."""
        tipler = AntrenmanOturumuTemel.gecerli_oturum_tipleri_getir()
        self.assertIsInstance(tipler, list)
        self.assertIn("kondisyon", tipler)
        self.assertIn("teknik", tipler)
        self.assertIn("taktik", tipler)
        self.assertIn("rehabilitasyon", tipler)
    
    def test_gecerli_durumlar_getir(self):
        """Base class'tan geçerli durumları getirir."""
        durumlar = AntrenmanOturumuTemel.gecerli_durumlar_getir()
        self.assertIsInstance(durumlar, list)
        self.assertIn("planlandı", durumlar)
        self.assertIn("tamamlandi", durumlar)
        self.assertIn("iptal_edildi", durumlar)
    
    def test_oturum_tipi_gecerli_mi(self):
        """Oturum tipi geçerliliğini kontrol eder."""
        self.assertTrue(AntrenmanOturumuTemel.oturum_tipi_gecerli_mi("kondisyon"))
        self.assertTrue(AntrenmanOturumuTemel.oturum_tipi_gecerli_mi("teknik"))  # Case insensitive
        self.assertTrue(AntrenmanOturumuTemel.oturum_tipi_gecerli_mi("Taktik"))  # Case insensitive
        self.assertFalse(AntrenmanOturumuTemel.oturum_tipi_gecerli_mi("geçersiz"))
    
    def test_sure_dakikadan_saat_dakikaya(self):
        """Dakikayı saat ve dakikaya çevirir."""
        saat, dakika = AntrenmanOturumuTemel.sure_dakikadan_saat_dakikaya(90)
        self.assertEqual(saat, 1)
        self.assertEqual(dakika, 30)
        
        saat, dakika = AntrenmanOturumuTemel.sure_dakikadan_saat_dakikaya(125)
        self.assertEqual(saat, 2)
        self.assertEqual(dakika, 5)
    
    def test_tarih_cakismasi_kontrol(self):
        """Tarih çakışması kontrolü yapar."""
        tarih1 = datetime(2025, 6, 1, 10, 0)
        tarih2 = datetime(2025, 6, 1, 10, 30)
        tarih3 = datetime(2025, 6, 1, 12, 0)
        
        # Çakışma var (10:00-11:00 ile 10:30-11:30)
        self.assertTrue(AntrenmanOturumuTemel.tarih_cakismasi_kontrol(tarih1, 60, tarih2, 60))
        
        # Çakışma yok (10:00-11:00 ile 12:00-13:00)
        self.assertFalse(AntrenmanOturumuTemel.tarih_cakismasi_kontrol(tarih1, 60, tarih3, 60))


class TestIndividualTrainingSession(unittest.TestCase):
    """IndividualTrainingSession sınıfını test eder."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.session = IndividualTrainingSession(
            oturum_id=1,
            sure=60,
            athlete_id=101,
            antrenor_id=5,
            odak_alani="hız",
            oturum_tipi="kondisyon",
            tarih_saat=datetime(2025, 6, 1, 10, 0)
        )
    
    def test_olusturma(self):
        """Bireysel antrenman oturumu oluşturulur."""
        self.assertEqual(self.session.oturum_id, 1)
        self.assertEqual(self.session.athlete_id, 101)
        self.assertEqual(self.session.antrenor_id, 5)
        self.assertEqual(self.session.odak_alani, "hız")
        self.assertEqual(self.session.durum, "planlandı")
    
    def test_odak_alani_gecerli_mi(self):
        """Odak alanı geçerliliğini kontrol eder."""
        self.assertTrue(IndividualTrainingSession.odak_alani_gecerli_mi("hız"))
        self.assertTrue(IndividualTrainingSession.odak_alani_gecerli_mi("güç"))
        self.assertFalse(IndividualTrainingSession.odak_alani_gecerli_mi("geçersiz"))
    
    def test_performans_notu_dogrula(self):
        """Performans notu doğrulaması yapar."""
        self.assertTrue(IndividualTrainingSession.performans_notu_dogrula(5.5))
        self.assertTrue(IndividualTrainingSession.performans_notu_dogrula(0))
        self.assertTrue(IndividualTrainingSession.performans_notu_dogrula(10))
        self.assertFalse(IndividualTrainingSession.performans_notu_dogrula(11))
        self.assertFalse(IndividualTrainingSession.performans_notu_dogrula(-1))
    
    def test_performans_notu_karsilastir(self):
        """Performans notlarını karşılaştırır."""
        self.assertEqual(IndividualTrainingSession.performans_notu_karsilastir(5, 5), 0)
        self.assertEqual(IndividualTrainingSession.performans_notu_karsilastir(7, 5), 1)
        self.assertEqual(IndividualTrainingSession.performans_notu_karsilastir(5, 7), -1)
    
    def test_oturum_detaylari_getir(self):
        """Oturum detaylarını getirir."""
        detaylar = self.session.oturum_detaylari_getir()
        self.assertEqual(detaylar["oturum_turu"], "bireysel")
        self.assertEqual(detaylar["athlete_id"], 101)
        self.assertEqual(detaylar["antrenor_id"], 5)
        self.assertIn("performans_notu", detaylar)
    
    def test_oturum_maliyeti_hesapla(self):
        """Oturum maliyetini hesaplar."""
        maliyet = self.session.oturum_maliyeti_hesapla()
        # 60 dakika = 1 saat, 150 TL/saat
        self.assertEqual(maliyet, 150.0)
    
    def test_bireysel_antrenman_olustur(self):
        """Class method ile bireysel antrenman oluşturur."""
        session = IndividualTrainingSession.bireysel_antrenman_olustur(
            oturum_id=2,
            sure=90,
            athlete_id=102,
            antrenor_id=6,
            odak_alani="güç"
        )
        self.assertIsInstance(session, IndividualTrainingSession)
        self.assertEqual(session.oturum_id, 2)
        self.assertEqual(session.durum, "planlandı")


class TestTeamTrainingSession(unittest.TestCase):
    """TeamTrainingSession sınıfını test eder."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.session = TeamTrainingSession(
            oturum_id=1,
            sure=90,
            team_id=10,
            saha_id=3,
            katilimci_sayisi=15,
            antrenman_plani="taktik",
            tarih_saat=datetime(2025, 6, 1, 14, 0)
        )
    
    def test_olusturma(self):
        """Takım antrenman oturumu oluşturulur."""
        self.assertEqual(self.session.team_id, 10)
        self.assertEqual(self.session.saha_id, 3)
        self.assertEqual(self.session.katilimci_sayisi, 15)
        self.assertEqual(self.session.antrenman_plani, "taktik")
    
    def test_antrenman_plani_gecerli_mi(self):
        """Antrenman planı geçerliliğini kontrol eder."""
        self.assertTrue(TeamTrainingSession.antrenman_plani_gecerli_mi("taktik"))
        self.assertTrue(TeamTrainingSession.antrenman_plani_gecerli_mi("kondisyon"))
        self.assertFalse(TeamTrainingSession.antrenman_plani_gecerli_mi("geçersiz"))
    
    def test_katilimci_sayisi_dogrula(self):
        """Katılımcı sayısı doğrulaması yapar."""
        self.assertTrue(TeamTrainingSession.katilimci_sayisi_dogrula(10))
        self.assertTrue(TeamTrainingSession.katilimci_sayisi_dogrula(2))
        self.assertTrue(TeamTrainingSession.katilimci_sayisi_dogrula(30))
        self.assertFalse(TeamTrainingSession.katilimci_sayisi_dogrula(1))
        self.assertFalse(TeamTrainingSession.katilimci_sayisi_dogrula(31))
    
    def test_saha_kapasitesi_hesapla(self):
        """Saha kapasitesini hesaplar."""
        self.assertEqual(TeamTrainingSession.saha_kapasitesi_hesapla("küçük"), 10)
        self.assertEqual(TeamTrainingSession.saha_kapasitesi_hesapla("orta"), 20)
        self.assertEqual(TeamTrainingSession.saha_kapasitesi_hesapla("büyük"), 30)
    
    def test_oturum_detaylari_getir(self):
        """Oturum detaylarını getirir."""
        detaylar = self.session.oturum_detaylari_getir()
        self.assertEqual(detaylar["oturum_turu"], "takım")
        self.assertEqual(detaylar["team_id"], 10)
        self.assertEqual(detaylar["saha_id"], 3)
        self.assertEqual(detaylar["katilimci_sayisi"], 15)
    
    def test_oturum_maliyeti_hesapla(self):
        """Oturum maliyetini hesaplar."""
        maliyet = self.session.oturum_maliyeti_hesapla()
        # 90 dakika = 1.5 saat
        # Saha: 200 TL/saat * 1.5 = 300 TL
        # Antrenör: 250 TL/saat * 1.5 = 375 TL
        # Toplam: 675 TL
        self.assertGreater(maliyet, 0)
        self.assertIsInstance(maliyet, float)
    
    def test_saha_id_validasyon(self):
        """Saha ID validasyonu çalışır."""
        with self.assertRaises(GecersizSahaIdHatasi):
            session = TeamTrainingSession(
                oturum_id=2,
                sure=60,
                team_id=10,
                saha_id=6,  # Geçersiz (1-5 arası olmalı)
                katilimci_sayisi=10
            )


class TestRehabTrainingSession(unittest.TestCase):
    """RehabTrainingSession sınıfını test eder."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.session = RehabTrainingSession(
            oturum_id=1,
            sure=45,
            athlete_id=101,
            fizyoterapist_id=8,
            sakatlik_tipi="kas",
            rehab_programi="temel",
            tarih_saat=datetime(2025, 6, 1, 16, 0)
        )
    
    def test_olusturma(self):
        """Rehabilitasyon oturumu oluşturulur."""
        self.assertEqual(self.session.athlete_id, 101)
        self.assertEqual(self.session.fizyoterapist_id, 8)
        self.assertEqual(self.session.sakatlik_tipi, "kas")
        self.assertEqual(self.session.rehab_programi, "temel")
    
    def test_sakatlik_tipi_gecerli_mi(self):
        """Sakatlık tipi geçerliliğini kontrol eder."""
        self.assertTrue(RehabTrainingSession.sakatlik_tipi_gecerli_mi("kas"))
        self.assertTrue(RehabTrainingSession.sakatlik_tipi_gecerli_mi("eklem"))
        self.assertFalse(RehabTrainingSession.sakatlik_tipi_gecerli_mi("geçersiz"))
    
    def test_oturum_detaylari_getir(self):
        """Oturum detaylarını getirir."""
        detaylar = self.session.oturum_detaylari_getir()
        self.assertEqual(detaylar["oturum_turu"], "rehabilitasyon")
        self.assertEqual(detaylar["athlete_id"], 101)
        self.assertEqual(detaylar["fizyoterapist_id"], 8)
    
    def test_oturum_maliyeti_hesapla(self):
        """Oturum maliyetini hesaplar."""
        maliyet = self.session.oturum_maliyeti_hesapla()
        self.assertGreater(maliyet, 0)
        self.assertIsInstance(maliyet, float)


class TestTrainingRepository(unittest.TestCase):
    """TrainingRepository sınıfını test eder."""
    
    def setUp(self):
        """Her testten önce çalışır, temiz bir ortam kurar."""
        self.repo = TrainingRepository()
    
    def test_bos_repository_olustur(self):
        """Boş repository oluşturur."""
        repo = TrainingRepository.bos_repository_olustur()
        self.assertIsInstance(repo, TrainingRepository)
        self.assertEqual(len(repo.tumunu_listele()), 0)
    
    def test_gecerli_oturum_id_mi(self):
        """Geçerli oturum ID kontrolü yapar."""
        self.assertTrue(TrainingRepository.gecerli_oturum_id_mi(1))
        self.assertTrue(TrainingRepository.gecerli_oturum_id_mi(100))
        self.assertFalse(TrainingRepository.gecerli_oturum_id_mi(0))
        self.assertFalse(TrainingRepository.gecerli_oturum_id_mi(-1))
    
    def test_kaydet(self):
        """Oturum kaydeder."""
        session = IndividualTrainingSession(1, 60, 101, 5, tarih_saat=datetime(2025, 6, 1, 10, 0))
        self.repo.kaydet(session)
        
        kayit = self.repo.id_ile_bul(1)
        self.assertIsNotNone(kayit)
        self.assertEqual(kayit.oturum_id, 1)
    
    def test_duplicate_kayit_hatasi(self):
        """Aynı ID ile tekrar kayıt yapılamaz."""
        session1 = IndividualTrainingSession(1, 60, 101, 5)
        session2 = IndividualTrainingSession(1, 90, 102, 6)
        
        self.repo.kaydet(session1)
        
        with self.assertRaises(DuplicateOturumHatasi):
            self.repo.kaydet(session2)
    
    def test_id_ile_bul(self):
        """ID ile oturum bulur."""
        session = IndividualTrainingSession(1, 60, 101, 5)
        self.repo.kaydet(session)
        
        bulunan = self.repo.id_ile_bul(1)
        self.assertIsNotNone(bulunan)
        self.assertEqual(bulunan.oturum_id, 1)
        
        bulunamayan = self.repo.id_ile_bul(999)
        self.assertIsNone(bulunamayan)
    
    def test_guncelle(self):
        """Oturum günceller."""
        session = IndividualTrainingSession(1, 60, 101, 5)
        self.repo.kaydet(session)
        
        session.performans_notu = 8.5
        self.repo.guncelle(session)
        
        guncellenen = self.repo.id_ile_bul(1)
        self.assertEqual(guncellenen.performans_notu, 8.5)
    
    def test_sil(self):
        """Oturum siler."""
        session = IndividualTrainingSession(1, 60, 101, 5)
        self.repo.kaydet(session)
        
        self.repo.sil(1)
        
        silinen = self.repo.id_ile_bul(1)
        self.assertIsNone(silinen)
    
    def test_tumunu_listele(self):
        """Tüm oturumları listeler."""
        session1 = IndividualTrainingSession(1, 60, 101, 5)
        session2 = TeamTrainingSession(2, 90, 10, 3, 15)
        
        self.repo.kaydet(session1)
        self.repo.kaydet(session2)
        
        liste = self.repo.tumunu_listele()
        self.assertEqual(len(liste), 2)
    
    def test_sporcuya_gore_filtrele(self):
        """Sporcuya göre filtreler."""
        session1 = IndividualTrainingSession(1, 60, 101, 5)
        session2 = IndividualTrainingSession(2, 60, 102, 5)
        session3 = IndividualTrainingSession(3, 60, 101, 6)
        
        self.repo.kaydet(session1)
        self.repo.kaydet(session2)
        self.repo.kaydet(session3)
        
        sonuclar = self.repo.sporcuya_gore_filtrele(101)
        self.assertEqual(len(sonuclar), 2)
        self.assertTrue(all(s.athlete_id == 101 for s in sonuclar))
    
    def test_takima_gore_filtrele(self):
        """Takıma göre filtreler."""
        session1 = TeamTrainingSession(1, 60, 10, 1, 10)
        session2 = TeamTrainingSession(2, 60, 20, 2, 15)
        session3 = TeamTrainingSession(3, 60, 10, 3, 12)
        
        self.repo.kaydet(session1)
        self.repo.kaydet(session2)
        self.repo.kaydet(session3)
        
        sonuclar = self.repo.takima_gore_filtrele(10)
        self.assertEqual(len(sonuclar), 2)
        self.assertTrue(all(s.team_id == 10 for s in sonuclar))
    
    def test_tarih_araligina_gore_filtrele(self):
        """Tarih aralığına göre filtreler."""
        tarih1 = datetime(2025, 6, 1, 10, 0)
        tarih2 = datetime(2025, 6, 5, 14, 0)
        tarih3 = datetime(2025, 6, 10, 16, 0)
        
        session1 = IndividualTrainingSession(1, 60, 101, 5, tarih_saat=tarih1)
        session2 = IndividualTrainingSession(2, 60, 102, 5, tarih_saat=tarih2)
        session3 = IndividualTrainingSession(3, 60, 103, 5, tarih_saat=tarih3)
        
        self.repo.kaydet(session1)
        self.repo.kaydet(session2)
        self.repo.kaydet(session3)
        
        baslangic = datetime(2025, 6, 1, 0, 0)
        bitis = datetime(2025, 6, 6, 23, 59)
        
        sonuclar = self.repo.tarih_araligina_gore_filtrele(baslangic, bitis)
        self.assertEqual(len(sonuclar), 2)
    
    def test_detayli_cakisma_kontrol_sporcu(self):
        """Sporcu çakışması kontrolü yapar."""
        tarih = datetime(2025, 6, 1, 10, 0)
        session1 = IndividualTrainingSession(1, 60, 101, 5, tarih_saat=tarih)
        self.repo.kaydet(session1)
        
        # Aynı sporcu, çakışan saat
        cakisma = self.repo.detayli_cakisma_kontrol(
            tarih=datetime(2025, 6, 1, 10, 30),
            sure_dk=60,
            haric_id=-1,
            athlete_id=101
        )
        self.assertTrue(cakisma)
        
        # Farklı sporcu, çakışan saat (çakışma olmamalı)
        cakisma = self.repo.detayli_cakisma_kontrol(
            tarih=datetime(2025, 6, 1, 10, 30),
            sure_dk=60,
            haric_id=-1,
            athlete_id=102
        )
        self.assertFalse(cakisma)
    
    def test_detayli_cakisma_kontrol_saha(self):
        """Saha çakışması kontrolü yapar."""
        tarih = datetime(2025, 6, 1, 14, 0)
        session1 = TeamTrainingSession(1, 90, 10, 3, 15, tarih_saat=tarih)
        self.repo.kaydet(session1)
        
        # Aynı saha, çakışan saat
        cakisma = self.repo.detayli_cakisma_kontrol(
            tarih=datetime(2025, 6, 1, 14, 30),
            sure_dk=60,
            haric_id=-1,
            saha_id=3
        )
        self.assertTrue(cakisma)
        
        # Farklı saha, çakışan saat (çakışma olmamalı)
        cakisma = self.repo.detayli_cakisma_kontrol(
            tarih=datetime(2025, 6, 1, 14, 30),
            sure_dk=60,
            haric_id=-1,
            saha_id=4
        )
        self.assertFalse(cakisma)


class TestTrainingManager(unittest.TestCase):
    """TrainingManager servis katmanını test eder."""
    
    def setUp(self):
        """Her testten önce çalışır, temiz bir ortam kurar."""
        self.repo = TrainingRepository()
        self.service = TrainingManager(self.repo)
    
    def test_yeni_manager_olustur(self):
        """Class method ile manager oluşturur."""
        manager = TrainingManager.yeni_manager_olustur(self.repo)
        self.assertIsInstance(manager, TrainingManager)
    
    def test_oturum_durumu_gecerli_mi(self):
        """Oturum durumu geçerliliğini kontrol eder."""
        self.assertTrue(TrainingManager.oturum_durumu_gecerli_mi("planlandı"))
        self.assertTrue(TrainingManager.oturum_durumu_gecerli_mi("tamamlandi"))
        self.assertTrue(TrainingManager.oturum_durumu_gecerli_mi("iptal_edildi"))
        self.assertFalse(TrainingManager.oturum_durumu_gecerli_mi("geçersiz"))
    
    def test_antrenman_olusturma(self):
        """Antrenman oluşturma testi"""
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
        """Tarih/zaman çakışması testi"""
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
        """İptal işlemi testi"""
        t1 = IndividualTrainingSession(1, 60, 101, 5, tarih_saat=datetime(2025, 6, 1, 14, 0))
        self.service.oturum_olustur(t1)
        
        self.service.oturum_iptal_et(1)
        
        kayit = self.repo.id_ile_bul(1)
        self.assertEqual(kayit.durum, "iptal_edildi")
    
    def test_oturum_tamamla(self):
        """Oturum tamamlama testi"""
        t1 = IndividualTrainingSession(1, 60, 101, 5, tarih_saat=datetime(2025, 6, 1, 14, 0))
        self.service.oturum_olustur(t1)
        
        self.service.oturum_tamamla(1)
        
        kayit = self.repo.id_ile_bul(1)
        self.assertEqual(kayit.durum, "tamamlandi")
    
    def test_sporcu_programi_getir(self):
        """Sporcu programı getirme testi"""
        t1 = IndividualTrainingSession(1, 60, 101, 5, tarih_saat=datetime(2025, 6, 1, 10, 0))
        t2 = IndividualTrainingSession(2, 60, 101, 5, tarih_saat=datetime(2025, 6, 2, 14, 0))
        t3 = IndividualTrainingSession(3, 60, 102, 5, tarih_saat=datetime(2025, 6, 1, 16, 0))
        
        self.repo.kaydet(t1)
        self.repo.kaydet(t2)
        self.repo.kaydet(t3)
        
        program = self.service.sporcu_programi_getir(101)
        self.assertEqual(len(program), 2)
        self.assertTrue(all(p["athlete_id"] == 101 for p in program))
    
    def test_toplu_program_olustur(self):
        """Toplu program oluşturma testi"""
        template = IndividualTrainingSession(
            1, 60, 101, 5,
            tarih_saat=datetime(2025, 6, 1, 10, 0)
        )
        
        self.service.toplu_program_olustur(
            baslangic_id=10,
            template_oturum=template,
            tekrar_sayisi=3,
            aralik_gun=7
        )
        
        # 3 oturum oluşturulmuş olmalı
        liste = self.repo.tumunu_listele()
        self.assertGreaterEqual(len(liste), 3)
        
        # ID'ler kontrol
        oturum10 = self.repo.id_ile_bul(10)
        oturum11 = self.repo.id_ile_bul(11)
        oturum12 = self.repo.id_ile_bul(12)
        
        self.assertIsNotNone(oturum10)
        self.assertIsNotNone(oturum11)
        self.assertIsNotNone(oturum12)
    
    def test_iptal_bulunamayan_oturum(self):
        """Bulunamayan oturumu iptal etmeye çalışır."""
        with self.assertRaises(OturumBulunamadiHatasi):
            self.service.oturum_iptal_et(999)
    
    def test_tamamla_bulunamayan_oturum(self):
        """Bulunamayan oturumu tamamlamaya çalışır."""
        with self.assertRaises(OturumBulunamadiHatasi):
            self.service.oturum_tamamla(999)


class TestTrainingStatistics(unittest.TestCase):
    """TrainingStatistics sınıfını test eder."""
    
    def test_durum_sayim(self):
        """Durum sayımı yapar."""
        oturumlar = [
            IndividualTrainingSession(1, 60, 101, 5, durum="planlandı"),
            IndividualTrainingSession(2, 60, 101, 5, durum="tamamlandi"),
            IndividualTrainingSession(3, 60, 101, 5, durum="tamamlandi"),
            IndividualTrainingSession(4, 60, 101, 5, durum="iptal_edildi"),
        ]
        
        sayim = TrainingStatistics.durum_sayim(oturumlar)
        
        self.assertEqual(sayim["planlandı"], 1)
        self.assertEqual(sayim["tamamlandi"], 2)
        self.assertEqual(sayim["iptal_edildi"], 1)
    
    def test_oturumlardan_olustur(self):
        """Oturum listesinden istatistik oluşturur."""
        oturumlar = [
            IndividualTrainingSession(1, 60, 101, 5, durum="planlandı"),
            IndividualTrainingSession(2, 60, 101, 5, durum="tamamlandi"),
            IndividualTrainingSession(3, 60, 101, 5, durum="tamamlandi"),
            IndividualTrainingSession(4, 60, 102, 5, durum="tamamlandi"),  # Farklı sporcu
        ]
        
        stats = TrainingStatistics.oturumlardan_olustur(101, oturumlar)
        
        self.assertEqual(stats.sporcu_id, 101)
        self.assertEqual(stats.toplam_oturum, 3)
        self.assertEqual(stats.tamamlanan, 2)
        self.assertEqual(stats.iptal_edilen, 0)
    
    def test_basari_orani_hesapla(self):
        """Başarı oranını hesaplar."""
        stats = TrainingStatistics(sporcu_id=101, toplam_oturum=10, tamamlanan=7, iptal_edilen=1)
        
        oran = stats.basari_orani_hesapla()
        self.assertEqual(oran, 70.0)
        
        # Hiç oturum yoksa
        stats2 = TrainingStatistics(sporcu_id=102, toplam_oturum=0, tamamlanan=0, iptal_edilen=0)
        oran2 = stats2.basari_orani_hesapla()
        self.assertEqual(oran2, 0.0)


class TestExceptionHandling(unittest.TestCase):
    """Exception handling'i test eder."""
    
    def test_gecersiz_oturum_id(self):
        """Geçersiz oturum ID hatası fırlatır."""
        with self.assertRaises(GecersizOturumIdHatasi):
            session = IndividualTrainingSession(0, 60, 101, 5)  # ID 0 geçersiz
    
    def test_gecersiz_sure(self):
        """Geçersiz süre hatası fırlatır."""
        with self.assertRaises(GecersizSureHatasi):
            session = IndividualTrainingSession(1, 0, 101, 5)  # Süre 0 geçersiz
    
    def test_gecersiz_oturum_tipi(self):
        """Geçersiz oturum tipi hatası fırlatır."""
        with self.assertRaises(GecersizOturumTipiHatasi):
            session = IndividualTrainingSession(1, 60, 101, 5, oturum_tipi="geçersiz")
    
    def test_gecersiz_durum(self):
        """Geçersiz durum hatası fırlatır."""
        session = IndividualTrainingSession(1, 60, 101, 5)
        with self.assertRaises(GecersizOturumDurumuHatasi):
            session.durum = "geçersiz_durum"


if __name__ == '__main__':
    # Test suite'i çalıştır
    unittest.main(verbosity=2)
