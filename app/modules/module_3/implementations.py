from datetime import datetime
from .base import MacBase, TurnuvaHatasi

class HazirlikMaci(MacBase):
    
    _toplam_hazirlik_maci = 0
    _min_bilet_fiyati = 50.0

    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, organizasyon_adi):

        super().__init__(ev_sahibi, deplasman, tarih_saat, mac_id)
        self._organizasyon_adi = organizasyon_adi
        self._bilet_fiyati = 100.0 # Varsayılan
        self._seyirci_sayisi = 0
        self._yardim_maci_mi = False

    def puan_hesapla(self):
        pass

    def mac_detay_getir(self):
        pass