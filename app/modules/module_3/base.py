from abc import ABC, abstractmethod
from datetime import datetime

#projeye özel hata sınıfı   
class TurnuvaHatasi(Exception):
    pass    

class MacBase(ABC):
    toplam_mac_sayisi = 0  
    gecerli_durumlar = ['planlandi', 'devam_ediyor', 'tamamlandi', 'iptal_edildi', 'ertelendi']

    def __init__(self, ev_sahibi, deplasman, tarih_saat, mac_id):
        self.ev_sahibi = ev_sahibi
        self.deplasman = deplasman
        self.tarih_saat = tarih_saat
        self.mac_id = mac_id
        self.durum = 'planlandi'
        self.skor_ev = 0
        self.skor_deplasman = 0
        self.skor_girildimi = False
        self. konum = "Ana Stadyum"
        self.hakem = "Atanmadı"
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
        if len(value ) < 3:
            raise TurnuvaHatasi("Ev sahibi takım adı en az 3 karakter olmalıdır.")
        self._ev_sahibi = value

    @property
    def deplasman(self):
        return self._deplasman
    @deplasman.setter
    def deplasman(self, value):
        if value == self._ev_sahibi:
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
    def durum(self):
        return self._durum
    
    @durum.setter
    def durum(self, value):
        if value not in MacBase.gecerli_durumlar:
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