from datetime import datetime
from .base import MacBase, TurnuvaHatasi, SporTipi, PuanKurallari, MacTipi

# Hazırlık maçı sınıfı - hazırlık ve dostluk maçları için özel özellikler
class HazirlikMaci(MacBase):

    # Hazırlık maçı objesi oluşturur - organizasyon ve bilet bilgileri ile
    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, organizasyon_adi, min_bilet_fiyati=50.0, bilet_fiyati=None):
        """
        Hazırlık maçı oluşturur.
        
        Args:
            mac_id: Maç ID'si
            ev_sahibi: Ev sahibi takım adı
            deplasman: Deplasman takım adı
            tarih_saat: Maç tarihi ve saati
            organizasyon_adi: Organizasyon adı
            min_bilet_fiyati: Minimum bilet fiyatı (varsayılan: 50.0)
            bilet_fiyati: Bilet fiyatı (varsayılan: 100.0)
        """
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat, MacTipi.FRIENDLY)
        
        self._organizasyon_adi = organizasyon_adi
        self._min_bilet_fiyati = min_bilet_fiyati
        self._bilet_fiyati = bilet_fiyati if bilet_fiyati is not None else 100.0
        self._seyirci_sayisi = 0
        self._yardim_maci_mi = False

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
        if deger < self._min_bilet_fiyati:
            raise TurnuvaHatasi(f"Bilet fiyatı {self._min_bilet_fiyati} TL altında olamaz.")
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

    # Hasılat hesaplama metodu - seyirci sayısı ve bilet fiyatına göre
    def hasilat_hesapla(self):
        gelir = self._seyirci_sayisi * self._bilet_fiyati
        if self._yardim_maci_mi:
            return 0.0
        return gelir

    # Polymorphism örneği - abstract metot override edilir
    def mac_sonucu(self):
        if not self.skor_girildi_mi:
            return "Maç oynanmadı"
        return {"ev_sahibi": 0, "deplasman": 0, "not": "Hazırlık maçı puan etkilemez"}

    # Polymorphism örneği - abstract metot override edilir, hazırlık maçı formatında
    def mac_detay_getir(self):
        ozet = f"[Hazirlik] {self.ev_sahibi} vs {self.deplasman}"
        ozet += f" | Org: {self.organizasyon_adi}"
        ozet += f" | Skor: {self.skor}"
        return ozet

    # Statik metot - organizasyon adı formatını kontrol eder
    @staticmethod
    def organizasyon_adi_kontrol(isim):
        """
        Organizasyon adı formatını kontrol eder (static method).
        
        Args:
            isim: Kontrol edilecek organizasyon adı
        
        Returns:
            bool: True ise geçerli format, False ise geçersiz
        """
        if isinstance(isim, str) and len(isim) >= 5:
            return True
        return False
    
    # Class metot - factory pattern ile hazırlık maçı oluşturur
    @classmethod
    def hazirlik_maci_olustur(cls, mac_id, ev_sahibi, deplasman, tarih_saat, organizasyon_adi, min_bilet_fiyati=50.0, bilet_fiyati=None):
        """
        Yeni bir hazırlık maçı oluşturur (class method - factory pattern).
        
        Args:
            mac_id: Maç ID'si
            ev_sahibi: Ev sahibi takım adı
            deplasman: Deplasman takım adı
            tarih_saat: Maç tarihi ve saati
            organizasyon_adi: Organizasyon adı
            min_bilet_fiyati: Minimum bilet fiyatı (varsayılan: 50.0)
            bilet_fiyati: Bilet fiyatı (varsayılan: 100.0)
        
        Returns:
            HazirlikMaci: Yeni oluşturulmuş hazırlık maçı
        """
        return cls(mac_id, ev_sahibi, deplasman, tarih_saat, organizasyon_adi, min_bilet_fiyati, bilet_fiyati)
    
    


# LİG MAÇI SINIFI 


# Lig maçı sınıfı - lig organizasyonları için maç yönetimi
class LigMaci(MacBase):

    # Lig maçı objesi oluşturur - lig, hafta ve spor tipi bilgileri ile
    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, lig_adi, hafta_no, spor_tipi: SporTipi = SporTipi.FUTBOL):
       
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat, MacTipi.LEAGUE)
        
        self.lig_adi = lig_adi
        self.hafta_no = hafta_no
        self._spor_tipi = spor_tipi
        self._sezon = f"{tarih_saat.year}-{tarih_saat.year+1} Sezonu"

    
    @property
    def lig_adi(self):
        return self._lig_adi

    @lig_adi.setter
    def lig_adi(self, deger):
        if not deger or len(deger) < 3:
            raise TurnuvaHatasi("Lig adı en az 3 karakter olmalıdır.")
        self._lig_adi = deger

    
    @property
    def hafta_no(self):
        return self._hafta_no

    @hafta_no.setter
    def hafta_no(self, deger):
        if not isinstance(deger, int) or deger <= 0:
            raise TurnuvaHatasi("Hafta numarası pozitif tam sayı olmalıdır.")
        self._hafta_no = deger

    @property
    def spor_tipi(self):
        return self._spor_tipi

    @spor_tipi.setter
    def spor_tipi(self, deger):
        if not isinstance(deger, SporTipi):
            raise TypeError("Spor tipi SporTipi enum değeri olmalıdır.")
        self._spor_tipi = deger

    # Skor belirleme metodu - beraberlik kontrolü ile override edilir
    def skor_belirle(self, skor_ev, skor_deplasman):
        """
        Skor belirler ve beraberlik kontrolü yapar (voleybol/basketbol için).
        """
        # Beraberlik kontrolü (voleybol/basketbol için) - önce kontrol et
        if not PuanKurallari.beraberlik_gecerli_mi(self.spor_tipi) and skor_ev == skor_deplasman:
            raise TurnuvaHatasi(f"{self.spor_tipi.value} için beraberlik olamaz!")
        
        # MacBase'deki skor_belirle metodunu çağır
        super().skor_belirle(skor_ev, skor_deplasman)

    # Polymorphism örneği - abstract metot override edilir, lig maçı puan hesaplaması ile
    def mac_sonucu(self):
        if not self.skor_girildi_mi:
            return "Maç henüz tamamlanmadı, puan hesaplanamaz."

        puan_ev = 0
        puan_dep = 0

        if self.skor_ev > self.skor_deplasman:
            puan_ev = PuanKurallari.puan_al_static(self.spor_tipi, "galibiyet")
            puan_dep = PuanKurallari.puan_al_static(self.spor_tipi, "maglubiyet")
        elif self.skor_deplasman > self.skor_ev:
            puan_ev = PuanKurallari.puan_al_static(self.spor_tipi, "maglubiyet")
            puan_dep = PuanKurallari.puan_al_static(self.spor_tipi, "galibiyet")
        else:
            # Beraberlik (sadece futbol için geçerli)
            puan_ev = PuanKurallari.puan_al_static(self.spor_tipi, "beraberlik")
            puan_dep = PuanKurallari.puan_al_static(self.spor_tipi, "beraberlik")

        return {
            "ev_sahibi_puan": puan_ev, 
            "deplasman_puan": puan_dep,
            "lig": self.lig_adi,
            "hafta": self.hafta_no,
            "spor_tipi": self.spor_tipi.value
        }

    # Polymorphism örneği - abstract metot override edilir, lig maçı formatında
    def mac_detay_getir(self):
        durum_ikonu = "✅" if self.durum == "tamamlandi" else "⏳"
        return f"{durum_ikonu} [Lig: {self.lig_adi}] {self.ev_sahibi} vs {self.deplasman} ({self.hafta_no}. Hafta)"
    
    # Statik metot - lig adı formatını kontrol eder
    @staticmethod
    def lig_adi_gecerli_mi(lig_adi: str):
        """
        Lig adı formatını kontrol eder (static method).
        
        Args:
            lig_adi: Kontrol edilecek lig adı
        
        Returns:
            bool: True ise geçerli format, False ise geçersiz
        """
        return isinstance(lig_adi, str) and len(lig_adi) >= 3
    
    # Class metot - factory pattern ile lig maçı oluşturur
    @classmethod
    def lig_maci_olustur(cls, mac_id, ev_sahibi, deplasman, tarih_saat, lig_adi, hafta_no, spor_tipi: SporTipi = SporTipi.FUTBOL):
        """
        Yeni bir lig maçı oluşturur (class method - factory pattern).
        
        Args:
            mac_id: Maç ID'si
            ev_sahibi: Ev sahibi takım adı
            deplasman: Deplasman takım adı
            tarih_saat: Maç tarihi ve saati
            lig_adi: Lig adı
            hafta_no: Hafta numarası
            spor_tipi: Spor tipi (varsayılan: FUTBOL)
        
        Returns:
            LigMaci: Yeni oluşturulmuş lig maçı
        """
        return cls(mac_id, ev_sahibi, deplasman, tarih_saat, lig_adi, hafta_no, spor_tipi)



# ELEME MAÇI SINIFI 

import random 

# Eleme maçı sınıfı - turnuva eleme maçları için özel özellikler
class ElemeMaci(MacBase):
    # Eleme maçı objesi oluşturur - tur bilgisi ile
    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, tur_adi):
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat, MacTipi.TOURNAMENT)
        self.tur_adi = tur_adi
    
    @property
    def tur_adi(self):
        return self._tur_adi
    
    @tur_adi.setter
    def tur_adi(self, value):
        if not isinstance(value, str) or len(value) < 3:
            raise TurnuvaHatasi("Tur adı en az 3 karakter olmalıdır.")
        self._tur_adi = value

    # Polymorphism örneği - abstract metot override edilir, eleme maçı kazanan belirleme ile
    def mac_sonucu(self):
        if not self.skor_girildi_mi:
            return "Maç oynanmadı."

        if self.skor_ev > self.skor_deplasman:
            kazanan = self.ev_sahibi
        elif self.skor_deplasman > self.skor_ev:
            kazanan = self.deplasman
        else:
            # Eleme maçlarında beraberlik olamaz
            return "Maç berabere bitti! Eleme maçlarında beraberlik olamaz."

        return {
            "tur": self.tur_adi,
            "kazanan": kazanan,
            "skor": self.skor
        }

    # Polymorphism örneği - abstract metot override edilir, eleme maçı formatında
    def mac_detay_getir(self):
        return f"🏆 [{self.tur_adi}] {self.ev_sahibi} vs {self.deplasman}"
    
    # Statik metot - tur adı formatını kontrol eder
    @staticmethod
    def tur_adi_gecerli_mi(tur_adi: str):
        """
        Tur adı formatını kontrol eder (static method).
        
        Args:
            tur_adi: Kontrol edilecek tur adı
        
        Returns:
            bool: True ise geçerli format, False ise geçersiz
        """
        return isinstance(tur_adi, str) and len(tur_adi) >= 3
    
    # Class metot - factory pattern ile eleme maçı oluşturur
    @classmethod
    def eleme_maci_olustur(cls, mac_id, ev_sahibi, deplasman, tarih_saat, tur_adi):
        """
        Yeni bir eleme maçı oluşturur (class method - factory pattern).
        
        Args:
            mac_id: Maç ID'si
            ev_sahibi: Ev sahibi takım adı
            deplasman: Deplasman takım adı
            tarih_saat: Maç tarihi ve saati
            tur_adi: Tur adı
        
        Returns:
            ElemeMaci: Yeni oluşturulmuş eleme maçı
        """
        return cls(mac_id, ev_sahibi, deplasman, tarih_saat, tur_adi)