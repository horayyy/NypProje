from datetime import datetime
from .base import MacBase, TurnuvaHatasi

# Hazırlık maçı sınıfı
class HazirlikMaci(MacBase):
    
    _toplam_hazirlik_maci = 0
    _min_bilet_fiyati = 50.0

    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, organizasyon_adi):
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat, match_type='friendly')
        
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

    def mac_sonucu(self):
        if not self._skor_girildi_mi:
            return "Maç oynanmadı"
        return {"ev_sahibi": 0, "deplasman": 0, "not": "Hazırlık maçı puan etkilemez"}

    def puan_hesapla(self):
        return {"ev_sahibi_puan": 0, "deplasman_puan": 0, "aciklama": "Hazırlık maçı puan etkilemez"}

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
    
    


# LİG MAÇI SINIFI 


class LigMaci(MacBase):
    
    # Lig kuralları 
    _kazanan_puan = 3
    _beraberlik_puan = 1
    _maglubiyet_puan = 0
    _toplam_lig_maci = 0

    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, lig_adi, hafta_no):
       
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat, match_type='league')
        
        self.lig_adi = lig_adi
        self.hafta_no = hafta_no
        self._sezon = f"{tarih_saat.year}-{tarih_saat.year+1} Sezonu"
        self._gol_farki_ev = 0
        self._gol_farki_dep = 0
        
        LigMaci.lig_sayaci_artir()

    
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
    def sezon(self):
        return self._sezon

    @property
    def gol_farki_ev(self):
        return self._gol_farki_ev

    @property
    def gol_farki_dep(self):
        return self._gol_farki_dep

    def gol_farki_hesapla(self):
        if not self._skor_girildi_mi:
            return {"ev_sahibi": 0, "deplasman": 0}
        self._gol_farki_ev = self._skor_ev - self._skor_dep
        self._gol_farki_dep = self._skor_dep - self._skor_ev
        return {"ev_sahibi": self._gol_farki_ev, "deplasman": self._gol_farki_dep}

    def mac_sonucu(self):
        if not self._skor_girildi_mi:
            return "Maç henüz tamamlanmadı, puan hesaplanamaz."

        puan_ev = 0
        puan_dep = 0

        
        if self._skor_ev > self._skor_dep:
            puan_ev = self._kazanan_puan
            puan_dep = self._maglubiyet_puan
        elif self._skor_dep > self._skor_ev:
            puan_ev = self._maglubiyet_puan
            puan_dep = self._kazanan_puan
        else:
            puan_ev = self._beraberlik_puan
            puan_dep = self._beraberlik_puan

        return {
            "ev_sahibi_puan": puan_ev, 
            "deplasman_puan": puan_dep,
            "lig": self.lig_adi,
            "hafta": self.hafta_no
        }

    def puan_hesapla(self):
        sonuc = self.mac_sonucu()
        if isinstance(sonuc, str):
            return {"ev_sahibi_puan": 0, "deplasman_puan": 0, "durum": "henuz_oynanmadi"}
        gol_farki = self.gol_farki_hesapla()
        return {
            "ev_sahibi_puan": sonuc["ev_sahibi_puan"],
            "deplasman_puan": sonuc["deplasman_puan"],
            "gol_farki_ev": gol_farki["ev_sahibi"],
            "gol_farki_dep": gol_farki["deplasman"]
        }

    def mac_detay_getir(self):
        durum_ikonu = "✅" if self.durum == "finished" else "⏳"
        return f"{durum_ikonu} [Lig: {self.lig_adi}] {self.ev_sahibi} vs {self.deplasman} ({self.hafta_no}. Hafta)"

    @classmethod
    def lig_sayaci_artir(cls):
        cls._toplam_lig_maci += 1

    @classmethod
    def toplam_lig_maci_getir(cls):
        return cls._toplam_lig_maci

    @classmethod
    def puan_sistemi_getir(cls):
        return {
            "kazanan": cls._kazanan_puan,
            "beraberlik": cls._beraberlik_puan,
            "maglubiyet": cls._maglubiyet_puan
        }

    @staticmethod
    def hafta_no_gecerli_mi(hafta_no):
        return isinstance(hafta_no, int) and hafta_no > 0

    @staticmethod
    def lig_adi_gecerli_mi(lig_adi):
        return isinstance(lig_adi, str) and len(lig_adi) >= 3



# ELEME MAÇI SINIFI 

import random 

class ElemeMaci(MacBase):
    _toplam_eleme_maci = 0
    _gecerli_turler = ['Son 16', 'Çeyrek Final', 'Yarı Final', 'Final', 'İlk Tur', 'İkinci Tur']

    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, tur_adi):
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat, match_type='tournament')
        self.tur_adi = tur_adi
        self._penalti_skoru = None
        self._turnuva_adi = "Genel Turnuva"
        self._eleme_kurallari = "Tek maç eleme"
        
        ElemeMaci.eleme_sayaci_artir()

    @property
    def tur_adi(self):
        return self._tur_adi

    @tur_adi.setter
    def tur_adi(self, deger):
        if not isinstance(deger, str) or len(deger) < 3:
            raise TurnuvaHatasi("Tur adı geçerli bir string olmalıdır.")
        self._tur_adi = deger

    @property
    def turnuva_adi(self):
        return self._turnuva_adi

    @turnuva_adi.setter
    def turnuva_adi(self, deger):
        if not isinstance(deger, str) or len(deger) < 3:
            raise TurnuvaHatasi("Turnuva adı en az 3 karakter olmalıdır.")
        self._turnuva_adi = deger

    @property
    def eleme_kurallari(self):
        return self._eleme_kurallari

    @eleme_kurallari.setter
    def eleme_kurallari(self, deger):
        if not isinstance(deger, str):
            raise TypeError("Eleme kuralları string olmalıdır.")
        self._eleme_kurallari = deger

    def penalti_skoru_belirle(self, ev_p, dep_p):
        if ev_p == dep_p:
            raise TurnuvaHatasi("Penaltılarda beraberlik olamaz!")
        if not isinstance(ev_p, int) or not isinstance(dep_p, int):
            raise TypeError("Penaltı skorları tam sayı olmalıdır.")
        if ev_p < 0 or dep_p < 0:
            raise TurnuvaHatasi("Penaltı skorları negatif olamaz.")
        self._penalti_skoru = (ev_p, dep_p)

    def kazanan_takim_belirle(self):
        if not self._skor_girildi_mi:
            return None
        if self._skor_ev > self._skor_dep:
            return self.ev_sahibi
        elif self._skor_dep > self._skor_ev:
            return self.deplasman
        else:
            if self._penalti_skoru is None:
                return None
            p_ev, p_dep = self._penalti_skoru
            return self.ev_sahibi if p_ev > p_dep else self.deplasman

    def mac_sonucu(self):
        if not self._skor_girildi_mi:
            return "Maç oynanmadı."

        kazanan = self.kazanan_takim_belirle()
        if kazanan is None:
            return "Maç berabere bitti ama penaltılar atılmadı! Kazanan belirsiz."

        if self._skor_ev == self._skor_dep and self._penalti_skoru:
            kazanan += " (Penaltılarla)"

        return {
            "tur": self._tur_adi,
            "kazanan": kazanan,
            "skor": self.skor,
            "penalti_skoru": self._penalti_skoru
        }

    def puan_hesapla(self):
        sonuc = self.mac_sonucu()
        if isinstance(sonuc, str):
            return {"kazanan": None, "durum": "henuz_oynanmadi"}
        return {
            "kazanan": sonuc["kazanan"],
            "skor": sonuc["skor"],
            "penalti_ile": "penalti_skoru" in sonuc and sonuc["penalti_skoru"] is not None
        }

    def mac_detay_getir(self):
        return f"🏆 [{self._tur_adi}] {self.ev_sahibi} vs {self.deplasman} - {self._turnuva_adi}"

    @classmethod
    def eleme_sayaci_artir(cls):
        cls._toplam_eleme_maci += 1

    @classmethod
    def toplam_eleme_maci_getir(cls):
        return cls._toplam_eleme_maci

    @classmethod
    def gecerli_turler_getir(cls):
        return cls._gecerli_turler.copy()

    @staticmethod
    def tur_gecerli_mi(tur_adi):
        return isinstance(tur_adi, str) and len(tur_adi) >= 3

    @staticmethod
    def penalti_skoru_gecerli_mi(ev_p, dep_p):
        return isinstance(ev_p, int) and isinstance(dep_p, int) and ev_p >= 0 and dep_p >= 0 and ev_p != dep_p