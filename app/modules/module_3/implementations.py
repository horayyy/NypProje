from datetime import datetime
from .base import MacBase, TurnuvaHatasi

class HazirlikMaci(MacBase):
    
    _toplam_hazirlik_maci = 0
    _min_bilet_fiyati = 50.0

    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, organizasyon_adi, sport_type='futbol'):
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat, match_type='friendly', sport_type=sport_type)
        
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

    def bilet_geliri_hesapla(self):
        return self._seyirci_sayisi * self._bilet_fiyati

    def organizasyon_bilgisi(self):
        return {
            "organizasyon": self._organizasyon_adi,
            "bilet_fiyati": self._bilet_fiyati,
            "seyirci": self._seyirci_sayisi,
            "yardim_maci": self._yardim_maci_mi,
            "spor_dali": self.sport_type
        }

    def spor_dali_ozel_bilgi(self):
        if self.sport_type == 'futbol':
            return {"sure": "90 dakika", "devre": 2, "oyuncu_sayisi": 11}
        elif self.sport_type == 'basketbol':
            return {"sure": "40 dakika", "devre": 4, "oyuncu_sayisi": 5}
        elif self.sport_type == 'voleybol':
            return {"sure": "Set bazlı", "devre": "Set", "oyuncu_sayisi": 6}
        elif self.sport_type == 'hentbol':
            return {"sure": "60 dakika", "devre": 2, "oyuncu_sayisi": 7}
        elif self.sport_type == 'tenis':
            return {"sure": "Set bazlı", "devre": "Set", "oyuncu_sayisi": 1}
        return {}
   
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

class LigMaci(MacBase):
    
    _kazanan_puan = 3
    _beraberlik_puan = 1
    _maglubiyet_puan = 0
    _toplam_lig_maci = 0

    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, lig_adi, hafta_no, sport_type='futbol'):
       
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat, match_type='league', sport_type=sport_type)
        
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

    def lig_bilgisi(self):
        return {
            "lig": self.lig_adi,
            "sezon": self._sezon,
            "hafta": self.hafta_no,
            "tarih": self.tarih_saat.strftime("%Y-%m-%d %H:%M")
        }

    def puan_sistemi_bilgisi(self):
        return LigMaci.puan_sistemi_getir()

    def spor_dali_skor_format(self):
        if self.sport_type == 'futbol':
            return f"{self._skor_ev}-{self._skor_dep} (Gol)"
        elif self.sport_type == 'basketbol':
            return f"{self._skor_ev}-{self._skor_dep} (Sayı)"
        elif self.sport_type == 'voleybol':
            return f"{self._skor_ev}-{self._skor_dep} (Set)"
        elif self.sport_type == 'hentbol':
            return f"{self._skor_ev}-{self._skor_dep} (Gol)"
        elif self.sport_type == 'tenis':
            return f"{self._skor_ev}-{self._skor_dep} (Set)"
        return self.skor

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

import random 

class ElemeMaci(MacBase):
    _toplam_eleme_maci = 0
    _gecerli_turler = ['Son 16', 'Çeyrek Final', 'Yarı Final', 'Final', 'İlk Tur', 'İkinci Tur']

    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, tur_adi, sport_type='futbol'):
        super().__init__(mac_id, ev_sahibi, deplasman, tarih_saat, match_type='tournament', sport_type=sport_type)
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

    def turnuva_detay(self):
        return {
            "turnuva": self._turnuva_adi,
            "tur": self._tur_adi,
            "kurallar": self._eleme_kurallari,
            "penalti_var": self._penalti_skoru is not None,
            "kazanan": self.kazanan_takim_belirle()
        }

    def penalti_gerekli_mi(self):
        return self._skor_girildi_mi and self._skor_ev == self._skor_dep

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

class PuanTablosu:
    def __init__(self, takim_adi):
        self._takim_adi = takim_adi
        self._oynanan = 0
        self._galibiyet = 0
        self._beraberlik = 0
        self._maglubiyet = 0
        self._atilan_gol = 0
        self._yenilen_gol = 0
        self._puan = 0

    @property
    def takim_adi(self):
        return self._takim_adi

    @property
    def oynanan(self):
        return self._oynanan

    @property
    def galibiyet(self):
        return self._galibiyet

    @property
    def beraberlik(self):
        return self._beraberlik

    @property
    def maglubiyet(self):
        return self._maglubiyet

    @property
    def atilan_gol(self):
        return self._atilan_gol

    @property
    def yenilen_gol(self):
        return self._yenilen_gol

    @property
    def puan(self):
        return self._puan

    @property
    def gol_farki(self):
        return self._atilan_gol - self._yenilen_gol

    def mac_ekle(self, atilan, yenilen, puan):
        self._oynanan += 1
        self._atilan_gol += atilan
        self._yenilen_gol += yenilen
        self._puan += puan
        if puan == 3:
            self._galibiyet += 1
        elif puan == 1:
            self._beraberlik += 1
        else:
            self._maglubiyet += 1

    def tablo_bilgisi_getir(self):
        return {
            "takim": self._takim_adi,
            "oynanan": self._oynanan,
            "galibiyet": self._galibiyet,
            "beraberlik": self._beraberlik,
            "maglubiyet": self._maglubiyet,
            "atilan": self._atilan_gol,
            "yenilen": self._yenilen_gol,
            "gol_farki": self.gol_farki,
            "puan": self._puan
        }

    def ortalama_gol_atilan(self):
        if self._oynanan == 0:
            return 0.0
        return round(self._atilan_gol / self._oynanan, 2)

    def ortalama_gol_yenilen(self):
        if self._oynanan == 0:
            return 0.0
        return round(self._yenilen_gol / self._oynanan, 2)

    def galibiyet_yuzdesi(self):
        if self._oynanan == 0:
            return 0.0
        return round((self._galibiyet / self._oynanan) * 100, 2)

    @staticmethod
    def siralama_karsilastir(takim1, takim2):
        if takim1._puan != takim2._puan:
            return takim2._puan - takim1._puan
        if takim1.gol_farki != takim2.gol_farki:
            return takim2.gol_farki - takim1.gol_farki
        return takim2._atilan_gol - takim1._atilan_gol

class Fikstur:
    def __init__(self, organizasyon_adi, baslangic_tarihi):
        self._organizasyon_adi = organizasyon_adi
        self._baslangic_tarihi = baslangic_tarihi
        self._maclar = []

    @property
    def organizasyon_adi(self):
        return self._organizasyon_adi

    @property
    def baslangic_tarihi(self):
        return self._baslangic_tarihi

    @property
    def maclar(self):
        return self._maclar.copy()

    def mac_ekle(self, mac):
        self._maclar.append(mac)

    def mac_sayisi_getir(self):
        return len(self._maclar)

    def tamamlanan_mac_sayisi(self):
        return sum(1 for mac in self._maclar if mac.durum == "finished")

    def bekleyen_mac_sayisi(self):
        return len(self._maclar) - self.tamamlanan_mac_sayisi()

    def tamamlanma_yuzdesi(self):
        if len(self._maclar) == 0:
            return 0.0
        return round((self.tamamlanan_mac_sayisi() / len(self._maclar)) * 100, 2)

    def fikstur_bilgisi_getir(self):
        return {
            "organizasyon": self._organizasyon_adi,
            "baslangic": self._baslangic_tarihi.strftime("%Y-%m-%d"),
            "toplam_mac": len(self._maclar),
            "tamamlanan": self.tamamlanan_mac_sayisi(),
            "bekleyen": self.bekleyen_mac_sayisi(),
            "tamamlanma_yuzdesi": self.tamamlanma_yuzdesi()
        }

class TakimIstatistikleri:
    def __init__(self, takim_adi):
        self._takim_adi = takim_adi
        self._mac_gecmisi = []
        self._toplam_gol = 0
        self._toplam_yenilen = 0

    @property
    def takim_adi(self):
        return self._takim_adi

    @property
    def mac_gecmisi(self):
        return self._mac_gecmisi.copy()

    def mac_ekle(self, mac):
        self._mac_gecmisi.append(mac)
        if mac._skor_girildi_mi:
            if mac.ev_sahibi == self._takim_adi:
                self._toplam_gol += mac._skor_ev
                self._toplam_yenilen += mac._skor_dep
            elif mac.deplasman == self._takim_adi:
                self._toplam_gol += mac._skor_dep
                self._toplam_yenilen += mac._skor_ev

    def galibiyet_sayisi(self):
        return sum(1 for mac in self._mac_gecmisi if mac._skor_girildi_mi and 
                   ((mac.ev_sahibi == self._takim_adi and mac._skor_ev > mac._skor_dep) or
                    (mac.deplasman == self._takim_adi and mac._skor_dep > mac._skor_ev)))

    def maglubiyet_sayisi(self):
        return sum(1 for mac in self._mac_gecmisi if mac._skor_girildi_mi and 
                   ((mac.ev_sahibi == self._takim_adi and mac._skor_ev < mac._skor_dep) or
                    (mac.deplasman == self._takim_adi and mac._skor_dep < mac._skor_ev)))

    def beraberlik_sayisi(self):
        return sum(1 for mac in self._mac_gecmisi if mac._skor_girildi_mi and mac._skor_ev == mac._skor_dep)

    def istatistik_getir(self):
        return {
            "takim": self._takim_adi,
            "toplam_mac": len(self._mac_gecmisi),
            "galibiyet": self.galibiyet_sayisi(),
            "beraberlik": self.beraberlik_sayisi(),
            "maglubiyet": self.maglubiyet_sayisi(),
            "toplam_gol": self._toplam_gol,
            "toplam_yenilen": self._toplam_yenilen,
            "gol_farki": self._toplam_gol - self._toplam_yenilen
        }

class MacServisi:
    def __init__(self, repository=None):
        self._repository = repository
        self._puan_tablolari = {}

    def mac_olustur(self, match_type, mac_id, ev_sahibi, deplasman, tarih_saat, sport_type='futbol', **kwargs):
        if match_type == 'friendly':
            if 'organizasyon_adi' not in kwargs:
                raise TurnuvaHatasi("Hazırlık maçı için organizasyon adı gereklidir.")
            return HazirlikMaci(mac_id, ev_sahibi, deplasman, tarih_saat, kwargs['organizasyon_adi'], sport_type)
        elif match_type == 'league':
            if 'lig_adi' not in kwargs or 'hafta_no' not in kwargs:
                raise TurnuvaHatasi("Lig maçı için lig adı ve hafta numarası gereklidir.")
            return LigMaci(mac_id, ev_sahibi, deplasman, tarih_saat, kwargs['lig_adi'], kwargs['hafta_no'], sport_type)
        elif match_type == 'tournament':
            if 'tur_adi' not in kwargs:
                raise TurnuvaHatasi("Eleme maçı için tur adı gereklidir.")
            return ElemeMaci(mac_id, ev_sahibi, deplasman, tarih_saat, kwargs['tur_adi'], sport_type)
        else:
            raise TurnuvaHatasi(f"Geçersiz maç tipi: {match_type}")

    def spor_dalina_gore_filtrele(self, sport_type):
        if self._repository is None:
            raise TurnuvaHatasi("Repository tanımlı değil.")
        return [mac for mac in self._repository.tumunu_getir() if mac.sport_type == sport_type]

    def spor_dali_istatistik(self, sport_type):
        maclar = self.spor_dalina_gore_filtrele(sport_type)
        return {
            "spor_dali": sport_type,
            "toplam_mac": len(maclar),
            "tamamlanan": len([m for m in maclar if m.durum == "finished"]),
            "planlanan": len([m for m in maclar if m.durum == "scheduled"])
        }

    def fikstur_olustur(self, takimlar, baslangic_tarihi, organizasyon_adi="Lig"):
        if len(takimlar) < 2:
            raise TurnuvaHatasi("Fikstür için en az 2 takım gereklidir.")
        fikstur = Fikstur(organizasyon_adi, baslangic_tarihi)
        mac_id = 1
        from datetime import timedelta
        tarih = baslangic_tarihi
        for i in range(len(takimlar)):
            for j in range(i + 1, len(takimlar)):
                mac = self.mac_olustur('league', mac_id, takimlar[i], takimlar[j], tarih, lig_adi=organizasyon_adi, hafta_no=1)
                fikstur.mac_ekle(mac)
                mac_id += 1
                tarih += timedelta(days=1)
        return fikstur

    def sonuc_gir(self, mac_id, skor_ev, skor_dep):
        if self._repository is None:
            raise TurnuvaHatasi("Repository tanımlı değil.")
        mac = self._repository.id_ile_bul(mac_id)
        if mac is None:
            raise TurnuvaHatasi(f"Maç bulunamadı: {mac_id}")
        mac.skor_belirle(skor_ev, skor_dep)
        mac.durum = "finished"
        if isinstance(mac, LigMaci):
            self.puan_tablosu_guncelle(mac.lig_adi, mac)
        return mac

    def puan_tablosu_guncelle(self, lig_adi, mac):
        if lig_adi not in self._puan_tablolari:
            self._puan_tablolari[lig_adi] = {}
        puan_sonuc = mac.puan_hesapla()
        if isinstance(puan_sonuc, dict) and "ev_sahibi_puan" in puan_sonuc:
            if mac.ev_sahibi not in self._puan_tablolari[lig_adi]:
                self._puan_tablolari[lig_adi][mac.ev_sahibi] = PuanTablosu(mac.ev_sahibi)
            if mac.deplasman not in self._puan_tablolari[lig_adi]:
                self._puan_tablolari[lig_adi][mac.deplasman] = PuanTablosu(mac.deplasman)
            ev_tablo = self._puan_tablolari[lig_adi][mac.ev_sahibi]
            dep_tablo = self._puan_tablolari[lig_adi][mac.deplasman]
            ev_tablo.mac_ekle(mac._skor_ev, mac._skor_dep, puan_sonuc["ev_sahibi_puan"])
            dep_tablo.mac_ekle(mac._skor_dep, mac._skor_ev, puan_sonuc["deplasman_puan"])

    def puan_tablosu_getir(self, lig_adi):
        if lig_adi not in self._puan_tablolari:
            return []
        tablolar = list(self._puan_tablolari[lig_adi].values())
        tablolar.sort(key=lambda x: (-x.puan, -x.gol_farki, -x.atilan_gol))
        return [tablo.tablo_bilgisi_getir() for tablo in tablolar]

    def takim_gecmisi_listele(self, takim_adi):
        if self._repository is None:
            raise TurnuvaHatasi("Repository tanımlı değil.")
        maclar = self._repository.takima_gore_filtrele(takim_adi)
        istatistik = TakimIstatistikleri(takim_adi)
        for mac in maclar:
            istatistik.mac_ekle(mac)
        return istatistik.istatistik_getir()

    def mac_iptal_et(self, mac_id):
        if self._repository is None:
            raise TurnuvaHatasi("Repository tanımlı değil.")
        mac = self._repository.id_ile_bul(mac_id)
        if mac is None:
            raise TurnuvaHatasi(f"Maç bulunamadı: {mac_id}")
        mac.durum = "cancelled"
        return mac

    def mac_ertele(self, mac_id, yeni_tarih):
        if self._repository is None:
            raise TurnuvaHatasi("Repository tanımlı değil.")
        mac = self._repository.id_ile_bul(mac_id)
        if mac is None:
            raise TurnuvaHatasi(f"Maç bulunamadı: {mac_id}")
        mac.tarih_saat = yeni_tarih
        mac.durum = "scheduled"
        return mac

    @classmethod
    def servis_olustur(cls, repository):
        return cls(repository)

    def mac_listesi_getir(self, match_type=None):
        if self._repository is None:
            raise TurnuvaHatasi("Repository tanımlı değil.")
        if match_type is None:
            return self._repository.tumunu_getir()
        return [mac for mac in self._repository.tumunu_getir() if mac.match_type == match_type]

    def yaklasan_maclar(self, gun_sayisi=7):
        if self._repository is None:
            raise TurnuvaHatasi("Repository tanımlı değil.")
        from datetime import datetime, timedelta
        bugun = datetime.now()
        hedef_tarih = bugun + timedelta(days=gun_sayisi)
        return self._repository.tarihe_gore_filtrele(bugun, hedef_tarih)

    def takim_istatistik_detay(self, takim_adi):
        if self._repository is None:
            raise TurnuvaHatasi("Repository tanımlı değil.")
        maclar = self._repository.takima_gore_filtrele(takim_adi)
        istatistik = TakimIstatistikleri(takim_adi)
        for mac in maclar:
            istatistik.mac_ekle(mac)
        detay = istatistik.istatistik_getir()
        detay["mac_listesi"] = [mac.mac_detay_getir() for mac in maclar]
        return detay

    def fikstur_olustur_round_robin(self, takimlar, baslangic_tarihi, organizasyon_adi="Lig"):
        if len(takimlar) < 2:
            raise TurnuvaHatasi("Fikstür için en az 2 takım gereklidir.")
        fikstur = Fikstur(organizasyon_adi, baslangic_tarihi)
        mac_id = self._repository._son_id + 1 if self._repository else 1
        from datetime import timedelta
        tarih = baslangic_tarihi
        for i in range(len(takimlar)):
            for j in range(i + 1, len(takimlar)):
                mac = self.mac_olustur('league', mac_id, takimlar[i], takimlar[j], tarih, lig_adi=organizasyon_adi, hafta_no=1)
                fikstur.mac_ekle(mac)
                if self._repository:
                    self._repository.kaydet(mac)
                mac_id += 1
                tarih += timedelta(days=1)
        return fikstur

    def toplu_sonuc_gir(self, sonuclar):
        if self._repository is None:
            raise TurnuvaHatasi("Repository tanımlı değil.")
        guncellenen_maclar = []
        for mac_id, skor_ev, skor_dep in sonuclar:
            try:
                mac = self.sonuc_gir(mac_id, skor_ev, skor_dep)
                guncellenen_maclar.append(mac)
            except Exception as e:
                print(f"Maç {mac_id} için hata: {e}")
        return guncellenen_maclar

    def puan_tablosu_sifirla(self, lig_adi):
        if lig_adi in self._puan_tablolari:
            self._puan_tablolari[lig_adi].clear()

    def tum_ligler(self):
        return list(self._puan_tablolari.keys())

    def lig_istatistik(self, lig_adi):
        if lig_adi not in self._puan_tablolari:
            return None
        tablolar = self._puan_tablolari[lig_adi]
        return {
            "lig": lig_adi,
            "takim_sayisi": len(tablolar),
            "toplam_mac": sum(tablo.oynanan for tablo in tablolar.values()) // 2
        }

    def en_cok_gol_atilan_takim(self, lig_adi):
        if lig_adi not in self._puan_tablolari:
            return None
        tablolar = self._puan_tablolari[lig_adi]
        if len(tablolar) == 0:
            return None
        return max(tablolar.values(), key=lambda t: t.atilan_gol).takim_adi

    def en_az_gol_yenilen_takim(self, lig_adi):
        if lig_adi not in self._puan_tablolari:
            return None
        tablolar = self._puan_tablolari[lig_adi]
        if len(tablolar) == 0:
            return None
        return min(tablolar.values(), key=lambda t: t.yenilen_gol).takim_adi

    @staticmethod
    def mac_tipi_gecerli_mi(match_type):
        return match_type in ['friendly', 'league', 'tournament']