from abc import ABC, abstractmethod
from datetime import datetime

class TurnuvaHatasi(Exception):
    pass

class MacBase(ABC):
    
    _toplam_mac_sayisi = 0
    _gecerli_durumlar = ['scheduled', 'in_progress', 'finished', 'cancelled', 'postponed']
    _gecerli_mac_tipleri = ['friendly', 'league', 'cup', 'tournament']
    _gecerli_spor_dallari = ['futbol', 'basketbol', 'voleybol', 'hentbol', 'tenis']

    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, match_type='friendly', sport_type='futbol'):
        self.mac_id = mac_id
        self.ev_sahibi = ev_sahibi
        self.deplasman = deplasman
        self.tarih_saat = tarih_saat
        self.match_type = match_type
        self.sport_type = sport_type
        
        self._durum = "scheduled"
        self._skor_ev = 0
        self._skor_dep = 0
        self._skor_girildi_mi = False
        self._konum = "Ana Stadyum"
        self._hakem = "Atanmadi"
        
        MacBase.sayac_artir()

    @property 
    def mac_id(self):
        return self._mac_id
    
    @mac_id.setter
    def mac_id(self, value):
        if not MacBase.id_format_kontrol(value):
            raise TurnuvaHatasi("Geçersiz ID Formatı. Pozitif tam sayı bekleniyor.")
        self._mac_id = value

    @property
    def ev_sahibi(self):
        return self._ev_sahibi
    
    @ev_sahibi.setter
    def ev_sahibi(self, value):
        if not isinstance(value, str):
            raise TypeError("Ev sahibi takımı geçerli bir string olarak giriniz.")
        if len(value) < 3:
            raise TurnuvaHatasi("Ev sahibi takım adı en az 3 karakter olmalıdır.")
        self._ev_sahibi = value

    @property
    def deplasman(self):
        return self._deplasman

    @deplasman.setter
    def deplasman(self, value):
        if hasattr(self, '_ev_sahibi') and value == self._ev_sahibi:
            raise TurnuvaHatasi("Ev sahibi ve deplasman takımları aynı olamaz.")
        self._deplasman = value
    
    @property
    def tarih_saat(self):
        return self._tarih_saat
    
    @tarih_saat.setter
    def tarih_saat(self, value):
        if not isinstance(value, datetime):
            raise TypeError("Tarih objesi datetime tipinde olmalı.")
        self._tarih_saat = value

    @property
    def match_type(self):
        return self._match_type
    
    @match_type.setter
    def match_type(self, value):
        if value not in MacBase._gecerli_mac_tipleri:
            gecerli_str = ", ".join(MacBase._gecerli_mac_tipleri)
            raise TurnuvaHatasi(f"Geçersiz maç tipi. Beklenenler: {gecerli_str}")
        self._match_type = value

    @property
    def sport_type(self):
        return self._sport_type
    
    @sport_type.setter
    def sport_type(self, value):
        if value not in MacBase._gecerli_spor_dallari:
            gecerli_str = ", ".join(MacBase._gecerli_spor_dallari)
            raise TurnuvaHatasi(f"Geçersiz spor dalı. Beklenenler: {gecerli_str}")
        self._sport_type = value

    @property
    def durum(self):
        return self._durum
    
    @durum.setter
    def durum(self, value):
        if value not in MacBase._gecerli_durumlar:
            gecerli_str = ", ".join(MacBase._gecerli_durumlar)
            raise TurnuvaHatasi(f"Geçersiz durum bilgisi. Beklenenler: {gecerli_str}")
        self._durum = value

    @property
    def konum(self):
        return self._konum

    @konum.setter
    def konum(self, value):
        if len(value) < 3:
            raise TurnuvaHatasi("Lokasyon bilgisi yetersiz.")
        self._konum = value 

    @property
    def hakem(self):    
        return self._hakem

    @hakem.setter
    def hakem(self, value):
        if any(karakter.isdigit() for karakter in value):
            raise TurnuvaHatasi("Hakem isminde sayi olamaz.")
        self._hakem = value

    @property
    def skor(self):
        return str(self._skor_ev) + "-" + str(self._skor_dep)

    def skor_belirle(self, skor_ev, skor_deplasman):
        if not isinstance(skor_ev, int) or not isinstance(skor_deplasman, int):
            raise TypeError("Skorlar tam sayı olmalıdır.")
        if skor_ev < 0 or skor_deplasman < 0:
            raise TurnuvaHatasi("Skorlar negatif olamaz.")
        
        self._skor_ev = skor_ev
        self._skor_dep = skor_deplasman
        self._skor_girildi_mi = True

    @abstractmethod
    def mac_sonucu(self):
        pass

    @abstractmethod
    def mac_detay_getir(self):
        pass

    @abstractmethod
    def puan_hesapla(self):
        pass

    @classmethod
    def sayac_artir(cls):
        cls._toplam_mac_sayisi += 1
        
    @classmethod
    def toplam_sayi_getir(cls):
        return cls._toplam_mac_sayisi

    @classmethod
    def gecerli_durumlar_getir(cls):
        return cls._gecerli_durumlar.copy()

    @classmethod
    def gecerli_mac_tipleri_getir(cls):
        return cls._gecerli_mac_tipleri.copy()

    @staticmethod
    def id_format_kontrol(id_value):
        if isinstance(id_value, int) and id_value > 0:
            return True
        return False

    @staticmethod
    def durum_gecerli_mi(durum):
        return durum in MacBase._gecerli_durumlar

    @staticmethod
    def mac_tipi_gecerli_mi(mac_tipi):
        return mac_tipi in MacBase._gecerli_mac_tipleri

    def mac_bilgisi_al(self):
        return {
            "id": self.mac_id,
            "ev_sahibi": self.ev_sahibi,
            "deplasman": self.deplasman,
            "tarih": self.tarih_saat.strftime("%Y-%m-%d %H:%M"),
            "durum": self.durum,
            "match_type": self.match_type,
            "sport_type": self.sport_type,
            "skor": self.skor if self._skor_girildi_mi else "Henüz girilmedi"
        }

    def mac_gecmis_mi(self):
        from datetime import datetime
        return self.tarih_saat < datetime.now()

    def mac_yaklasan_mi(self, gun_sayisi=7):
        from datetime import datetime, timedelta
        bugun = datetime.now()
        hedef = bugun + timedelta(days=gun_sayisi)
        return bugun <= self.tarih_saat <= hedef

    def mac_tamamlanabilir_mi(self):
        return self.durum in ["scheduled", "in_progress"]

    def mac_iptal_edilebilir_mi(self):
        return self.durum in ["scheduled", "in_progress"]

    @classmethod
    def durum_listesi_getir(cls):
        return cls._gecerli_durumlar.copy()

    @classmethod
    def mac_tipi_listesi_getir(cls):
        return cls._gecerli_mac_tipleri.copy()

    @classmethod
    def spor_dali_listesi_getir(cls):
        return cls._gecerli_spor_dallari.copy()

    @staticmethod
    def takim_adi_gecerli_mi(takim_adi):
        return isinstance(takim_adi, str) and len(takim_adi) >= 3

    @staticmethod
    def tarih_gecmis_mi(tarih):
        from datetime import datetime
        return isinstance(tarih, datetime) and tarih < datetime.now()

    @staticmethod
    def spor_dali_gecerli_mi(sport_type):
        return sport_type in MacBase._gecerli_spor_dallari

    def skor_girildi_mi(self):
        return self._skor_girildi_mi

    def skor_sifirla(self):
        self._skor_ev = 0
        self._skor_dep = 0
        self._skor_girildi_mi = False

    def mac_baslat(self):
        if self.durum != "scheduled":
            raise TurnuvaHatasi("Sadece planlanmış maçlar başlatılabilir.")
        self.durum = "in_progress"

    def mac_bitir(self, skor_ev, skor_dep):
        if self.durum != "in_progress":
            raise TurnuvaHatasi("Sadece devam eden maçlar bitirilebilir.")
        self.skor_belirle(skor_ev, skor_dep)
        self.durum = "finished"

    @classmethod
    def durum_degistir(cls, mac, yeni_durum):
        if yeni_durum not in cls._gecerli_durumlar:
            raise TurnuvaHatasi(f"Geçersiz durum: {yeni_durum}")
        mac.durum = yeni_durum
        return mac