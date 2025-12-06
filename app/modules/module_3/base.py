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