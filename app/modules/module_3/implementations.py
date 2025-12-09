from datetime import datetime
from .base import MacBase, TurnuvaHatasi

# Hazırlık maçı sınıfı
class HazirlikMaci(MacBase):
    
    _toplam_hazirlik_maci = 0
    _min_bilet_fiyati = 50.0

    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, organizasyon_adi):
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat) # DİKKAT: Sıralama mac_id başta olacak şekilde düzeltildi
        
        self._organizasyon_adi = organizasyon_adi
        self._bilet_fiyati = 100.0 
        self._seyirci_sayisi = 0
        self._yardim_maci_mi = False
        
        HazirlikMaci.hazirlik_sayaci_artir()

    @property
    def organizasyon_adi(self):
        return self._organizasyon_adi

    @organizasyon_adi.setter
    def organizasyon_adi(self, deger):
        if not HazirlikMaci.organizasyon_adi_kontrol(deger):
            raise TurnuvaHatasi("Organizasyon adı en az 5 karakter olmalı.")
        self._organizasyon_adi = deger

    @property
    def bilet_fiyati(self):
        return self._bilet_fiyati

    @bilet_fiyati.setter
    def bilet_fiyati(self, deger):
        if not isinstance(deger, (int, float)):
            raise TypeError("Bilet fiyatı sayı olmalı.")
        if deger < HazirlikMaci._min_bilet_fiyati:
            raise TurnuvaHatasi(f"Bilet fiyatı {HazirlikMaci._min_bilet_fiyati} TL altında olamaz.")
        self._bilet_fiyati = float(deger)

    @property
    def seyirci_sayisi(self):
        return self._seyirci_sayisi

    @seyirci_sayisi.setter
    def seyirci_sayisi(self, deger):
        if not isinstance(deger, int) or deger < 0:
            raise TurnuvaHatasi("Seyirci sayısı negatif olamaz.")
        self._seyirci_sayisi = deger
    
    @property
    def yardim_maci_mi(self):
        return self._yardim_maci_mi
    
    @yardim_maci_mi.setter
    def yardim_maci_mi(self, durum):
        if not isinstance(durum, bool):
            raise TypeError("Durum True veya False olmalı.")
        self._yardim_maci_mi = durum

    def hasilat_hesapla(self):
        gelir = self._seyirci_sayisi * self._bilet_fiyati
        if self._yardim_maci_mi:
            return 0.0
        return gelir

    # --- DÜZELTİLEN KISIM BURASI ---
    # Metodun adı 'puan_hesapla' idi, 'mac_sonucu' yaptık.
    def mac_sonucu(self):
        if not self._skor_girildi_mi:
            return "Maç oynanmadı"
        return {"ev_sahibi": 0, "deplasman": 0, "not": "Hazırlık maçı puan etkilemez"}

    def mac_detay_getir(self):
        ozet = f"[Hazirlik] {self.ev_sahibi} vs {self.deplasman}"
        ozet += f" | Org: {self.organizasyon_adi}"
        ozet += f" | Skor: {self.skor}"
        return ozet

    @classmethod
    def hazirlik_sayaci_artir(cls):
        cls._toplam_hazirlik_maci += 1

    @classmethod
    def toplam_hazirlik_getir(cls):
        return cls._toplam_hazirlik_maci

    @staticmethod
    def organizasyon_adi_kontrol(isim):
        if isinstance(isim, str) and len(isim) >= 5:
            return True
        return False