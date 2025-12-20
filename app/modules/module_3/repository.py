from .base import MacBase, TurnuvaHatasi
from datetime import datetime

class MacRepository:
    def __init__(self):
        self._maclar = {}
        self._son_id = 0

    def kaydet(self, mac):
        if not isinstance(mac, MacBase):
            raise TurnuvaHatasi("Sadece MacBase türevi nesneler kaydedilebilir.")
        if mac.mac_id in self._maclar:
            raise TurnuvaHatasi(f"Maç zaten kayıtlı: {mac.mac_id}")
        self._maclar[mac.mac_id] = mac
        if mac.mac_id > self._son_id:
            self._son_id = mac.mac_id

    def id_ile_bul(self, mac_id):
        return self._maclar.get(mac_id)

    def tarihe_gore_filtrele(self, baslangic, bitis):
        if not isinstance(baslangic, datetime) or not isinstance(bitis, datetime):
            raise TypeError("Tarih parametreleri datetime olmalıdır.")
        return [mac for mac in self._maclar.values() if baslangic <= mac.tarih_saat <= bitis]

    def lige_gore_filtrele(self, lig_adi):
        from .implementations import LigMaci
        return [mac for mac in self._maclar.values() if isinstance(mac, LigMaci) and mac.lig_adi == lig_adi]

    def turnuvaya_gore_filtrele(self, turnuva_adi):
        from .implementations import ElemeMaci
        return [mac for mac in self._maclar.values() if isinstance(mac, ElemeMaci) and mac.turnuva_adi == turnuva_adi]

    def spor_dalina_gore_filtrele(self, sport_type):
        return [mac for mac in self._maclar.values() if mac.sport_type == sport_type]

    def takima_gore_filtrele(self, takim_adi):
        return [mac for mac in self._maclar.values() if mac.ev_sahibi == takim_adi or mac.deplasman == takim_adi]

    def duruma_gore_filtrele(self, durum):
        return [mac for mac in self._maclar.values() if mac.durum == durum]

    def tumunu_getir(self):
        return list(self._maclar.values())

    def sil(self, mac_id):
        if mac_id not in self._maclar:
            raise TurnuvaHatasi(f"Maç bulunamadı: {mac_id}")
        return self._maclar.pop(mac_id)

    def guncelle(self, mac_id, yeni_mac):
        if mac_id not in self._maclar:
            raise TurnuvaHatasi(f"Maç bulunamadı: {mac_id}")
        if not isinstance(yeni_mac, MacBase):
            raise TurnuvaHatasi("Sadece MacBase türevi nesneler güncellenebilir.")
        self._maclar[mac_id] = yeni_mac
        return yeni_mac

    def toplam_mac_sayisi(self):
        return len(self._maclar)

    def bos_mu(self):
        return len(self._maclar) == 0

    @classmethod
    def yeni_repository(cls):
        return cls()

    def mac_tipine_gore_filtrele(self, match_type):
        return [mac for mac in self._maclar.values() if mac.match_type == match_type]

    def yaklasan_maclar(self, gun_sayisi=7):
        from datetime import timedelta
        bugun = datetime.now()
        hedef = bugun + timedelta(days=gun_sayisi)
        return [mac for mac in self._maclar.values() if bugun <= mac.tarih_saat <= hedef and mac.durum == "scheduled"]

    def gecmis_maclar(self):
        bugun = datetime.now()
        return [mac for mac in self._maclar.values() if mac.tarih_saat < bugun]

    def takim_ev_sahibi_maclar(self, takim_adi):
        return [mac for mac in self._maclar.values() if mac.ev_sahibi == takim_adi]

    def takim_deplasman_maclar(self, takim_adi):
        return [mac for mac in self._maclar.values() if mac.deplasman == takim_adi]

    def istatistik_getir(self):
        return {
            "toplam_mac": len(self._maclar),
            "tamamlanan": len(self.duruma_gore_filtrele("finished")),
            "planlanan": len(self.duruma_gore_filtrele("scheduled")),
            "iptal": len(self.duruma_gore_filtrele("cancelled")),
            "devam_ediyor": len(self.duruma_gore_filtrele("in_progress"))
        }

    def temizle(self):
        self._maclar.clear()
        self._son_id = 0

    def toplu_kaydet(self, mac_listesi):
        for mac in mac_listesi:
            self.kaydet(mac)

    @classmethod
    def repository_olustur(cls):
        return cls()

    @staticmethod
    def mac_id_gecerli_mi(mac_id):
        return isinstance(mac_id, int) and mac_id > 0

    def en_son_mac(self):
        if len(self._maclar) == 0:
            return None
        return max(self._maclar.values(), key=lambda m: m.tarih_saat)

    def en_eski_mac(self):
        if len(self._maclar) == 0:
            return None
        return min(self._maclar.values(), key=lambda m: m.tarih_saat)

    def takim_istatistik(self, takim_adi):
        maclar = self.takima_gore_filtrele(takim_adi)
        return {
            "takim": takim_adi,
            "toplam_mac": len(maclar),
            "ev_sahibi": len(self.takim_ev_sahibi_maclar(takim_adi)),
            "deplasman": len(self.takim_deplasman_maclar(takim_adi)),
            "tamamlanan": len([m for m in maclar if m.durum == "finished"])
        }

    def mac_tipi_istatistik(self):
        from .implementations import HazirlikMaci, LigMaci, ElemeMaci
        return {
            "hazirlik": len([m for m in self._maclar.values() if isinstance(m, HazirlikMaci)]),
            "lig": len([m for m in self._maclar.values() if isinstance(m, LigMaci)]),
            "eleme": len([m for m in self._maclar.values() if isinstance(m, ElemeMaci)])
        }

    @staticmethod
    def tarih_araligi_gecerli_mi(baslangic, bitis):
        return isinstance(baslangic, datetime) and isinstance(bitis, datetime) and baslangic <= bitis

