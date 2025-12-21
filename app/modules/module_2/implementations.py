"""
Antrenman ve Program modülü için implementasyon sınıfları.
Subclass'lar, entity/model sınıfları ve service katmanı burada yer alır.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List

from base import AntrenmanOturumuTemel
from exceptions import (
    GecersizSporcuIdHatasi,
    GecersizTakimIdHatasi,
    GecersizTarihSaatHatasi,
    GecersizSahaIdHatasi,
    SahaDoluHatasi,
    AntrenmanHatasi,
    TakvimCakismasiHatasi,
    OturumBulunamadiHatasi
)


class IndividualTrainingSession(AntrenmanOturumuTemel):
    """
    Bireysel antrenman oturumu subclass'ı.
    Tek bir sporcu için özel antrenman seanslarını temsil eder.
    """
    
    MIN_PERFORMANS_NOTU = 0
    MAX_PERFORMANS_NOTU = 10
    GECERLI_ODAK_ALANLARI = ["hız", "güç", "dayanıklılık", "esneklik", "koordinasyon"]
    
    def __init__(
        self,
        oturum_id: int,
        sure: int,
        athlete_id: int,
        antrenor_id: int,
        odak_alani: str = "hız",
        oturum_tipi: str = "kondisyon",
        tarih_saat: Optional[datetime] = None,
        durum: str = "planlandı",
        performans_notu: Optional[float] = None
    ):
        """
        Bireysel antrenman oturumu örneğini başlatır.
        """
        super().__init__(
            oturum_id=oturum_id,
            sure=sure,
            athlete_id=athlete_id,
            oturum_tipi=oturum_tipi,
            tarih_saat=tarih_saat,
            durum=durum
        )
        
        self._antrenor_id = None
        self._odak_alani = None
        self._performans_notu = None
        
        self.antrenor_id = antrenor_id
        self.odak_alani = odak_alani
        if performans_notu is not None:
            self.performans_notu = performans_notu

    @property
    def antrenor_id(self) -> int:
        """Antrenör ID'sini döndürür."""
        return self._antrenor_id

    @antrenor_id.setter
    def antrenor_id(self, value: Any) -> None:
        """Antrenör ID'sini doğrulama ile ayarlar."""
        if not isinstance(value, int):
            raise GecersizSporcuIdHatasi(f"Antrenör ID'si tam sayı olmalıdır, alınan: {type(value).__name__}")
        if value <= 0:
            raise GecersizSporcuIdHatasi(f"Antrenör ID'si pozitif tam sayı olmalıdır, alınan: {value}")
        self._antrenor_id = value

    @property
    def odak_alani(self) -> str:
        """Odak alanını döndürür."""
        return self._odak_alani

    @odak_alani.setter
    def odak_alani(self, value: Any) -> None:
        """Odak alanını geçerli alanlar listesine göre ayarlar."""
        if not isinstance(value, str):
            raise ValueError(f"Odak alanı string olmalıdır, alınan: {type(value).__name__}")
        
        alan_formatted = value.lower().strip()
        if alan_formatted not in self.GECERLI_ODAK_ALANLARI:
            raise ValueError(
                f"Odak alanı {self.GECERLI_ODAK_ALANLARI} değerlerinden biri olmalıdır, alınan: '{value}'"
            )
        self._odak_alani = alan_formatted

    @property
    def performans_notu(self) -> Optional[float]:
        """Performans notunu döndürür."""
        return self._performans_notu

    @performans_notu.setter
    def performans_notu(self, value: Any) -> None:
        """Performans notunu doğrulama ile ayarlar."""
        if value is not None:
            try:
                notu = float(value)
            except (ValueError, TypeError):
                raise ValueError(f"Performans notu sayısal bir değer olmalıdır, alınan: {type(value).__name__}")
            
            if not (self.MIN_PERFORMANS_NOTU <= notu <= self.MAX_PERFORMANS_NOTU):
                raise ValueError(
                    f"Performans notu {self.MIN_PERFORMANS_NOTU} ile {self.MAX_PERFORMANS_NOTU} arasında olmalıdır, alınan: {notu}"
                )
            self._performans_notu = round(notu, 1)
        else:
            self._performans_notu = None

    def oturum_detaylari_getir(self) -> Dict[str, Any]:
        """Bireysel antrenman oturumunun detaylı bilgilerini döndürür."""
        detaylar = {
            "oturum_id": self.oturum_id,
            "oturum_tipi": self.oturum_tipi,
            "sure": self.sure,
            "athlete_id": self.athlete_id,
            "antrenor_id": self.antrenor_id,
            "odak_alani": self.odak_alani,
            "durum": self.durum,
            "tarih_saat": self.tarih_saat.isoformat() if self.tarih_saat else None,
            "performans_notu": self.performans_notu,
            "oturum_turu": "bireysel"
        }
        return detaylar

    def oturum_maliyeti_hesapla(self) -> float:
        """Bireysel antrenman oturumunun maliyetini hesaplar."""
        SAATLIK_ANTRENOR_UCRETI = 150.0
        
        saat = self.sure / 60.0
        maliyet = SAATLIK_ANTRENOR_UCRETI * saat
        
        if self.odak_alani == "koordinasyon":
            maliyet *= 1.2
        
        return round(maliyet, 2)

    def performans_notu_guncelle(self, yeni_not: float) -> None:
        """Sporcu performans notunu günceller."""
        self.performans_notu = yeni_not

    def bireysel_rapor_olustur(self) -> str:
        """Bireysel antrenman oturumu için detaylı rapor oluşturur."""
        rapor = f"=== BİREYSEL ANTRENMAN RAPORU ===\n"
        rapor += f"Oturum ID: {self.oturum_id}\n"
        rapor += f"Sporcu ID: {self.athlete_id}\n"
        rapor += f"Antrenör ID: {self.antrenor_id}\n"
        rapor += f"Odak Alanı: {self.odak_alani.upper()}\n"
        rapor += f"Oturum Tipi: {self.oturum_tipi.upper()}\n"
        rapor += f"Süre: {self.sure} dakika ({self.sure // 60} saat {self.sure % 60} dakika)\n"
        
        if self.tarih_saat:
            rapor += f"Tarih/Saat: {self.tarih_saat.strftime('%d.%m.%Y %H:%M')}\n"
        
        rapor += f"Durum: {self.durum.upper()}\n"
        
        if self.performans_notu is not None:
            rapor += f"Performans Notu: {self.performans_notu}/10\n"
            if self.performans_notu >= 8:
                rapor += "Değerlendirme: Mükemmel performans!\n"
            elif self.performans_notu >= 6:
                rapor += "Değerlendirme: İyi performans.\n"
            else:
                rapor += "Değerlendirme: Geliştirilmesi gereken alanlar var.\n"
        else:
            rapor += "Performans Notu: Henüz değerlendirilmedi\n"
        
        rapor += f"Tahmini Maliyet: {self.oturum_maliyeti_hesapla()} TL\n"
        rapor += "=" * 35
        
        return rapor

    @classmethod
    def bireysel_antrenman_olustur(
        cls,
        oturum_id: int,
        sure: int,
        athlete_id: int,
        antrenor_id: int,
        odak_alani: str = "hız",
        oturum_tipi: str = "kondisyon"
    ) -> 'IndividualTrainingSession':
        """Yeni bir bireysel antrenman oturumu oluşturur."""
        return cls(
            oturum_id=oturum_id,
            sure=sure,
            athlete_id=athlete_id,
            antrenor_id=antrenor_id,
            odak_alani=odak_alani,
            oturum_tipi=oturum_tipi,
            tarih_saat=None,
            durum="planlandı"
        )

    @classmethod
    def odak_alani_gecerli_mi(cls, alan: str) -> bool:
        """Verilen odak alanının geçerli olup olmadığını kontrol eder."""
        if not isinstance(alan, str):
            return False
        return alan.lower().strip() in cls.GECERLI_ODAK_ALANLARI

    @staticmethod
    def performans_notu_dogrula(notu: Any) -> bool:
        """Performans notunun geçerli aralıkta olup olmadığını kontrol eder."""
        try:
            notu_float = float(notu)
            return IndividualTrainingSession.MIN_PERFORMANS_NOTU <= notu_float <= IndividualTrainingSession.MAX_PERFORMANS_NOTU
        except (ValueError, TypeError):
            return False

    @staticmethod
    def performans_notu_karsilastir(not1: float, not2: float) -> int:
        """İki performans notunu karşılaştırır."""
        if not IndividualTrainingSession.performans_notu_dogrula(not1):
            raise ValueError(f"İlk not geçersiz: {not1}")
        if not IndividualTrainingSession.performans_notu_dogrula(not2):
            raise ValueError(f"İkinci not geçersiz: {not2}")
        
        if not1 < not2:
            return -1
        elif not1 > not2:
            return 1
        else:
            return 0


class TeamTrainingSession(AntrenmanOturumuTemel):
    """
    Takım antrenman oturumu subclass'ı.
    Birden fazla sporcunun birlikte antrenman yaptığı seansları temsil eder.
    """
    
    MIN_KATILIMCI = 2
    MAX_KATILIMCI = 30
    GECERLI_ANTRENMAN_PLANLARI = ["taktik", "kondisyon", "teknik", "maç_hazırlığı"]
    
    def __init__(
        self,
        oturum_id: int,
        sure: int,
        team_id: int,
        saha_id: int,
        katilimci_sayisi: int,
        antrenman_plani: str = "taktik",
        oturum_tipi: str = "taktik",
        tarih_saat: Optional[datetime] = None,
        durum: str = "planlandı"
    ):
        """Takım antrenman oturumu örneğini başlatır."""
        super().__init__(
            oturum_id=oturum_id,
            sure=sure,
            team_id=team_id,
            oturum_tipi=oturum_tipi,
            tarih_saat=tarih_saat,
            durum=durum
        )
        
        self._saha_id = None
        self._katilimci_sayisi = None
        self._antrenman_plani = None
        
        self.saha_id = saha_id
        self.katilimci_sayisi = katilimci_sayisi
        self.antrenman_plani = antrenman_plani

    @property
    def saha_id(self) -> int:
        """Saha ID'sini döndürür."""
        return self._saha_id

    @saha_id.setter
    def saha_id(self, value: Any) -> None:
        """Saha ID'sini doğrulama ile ayarlar."""
        if not isinstance(value, int):
            raise GecersizSahaIdHatasi(f"Saha ID'si tam sayı olmalıdır, alınan: {type(value).__name__}")
        if value <= 0:
            raise GecersizSahaIdHatasi(f"Saha ID'si pozitif tam sayı olmalıdır, alınan: {value}")
        self._saha_id = value

    @property
    def katilimci_sayisi(self) -> int:
        """Katılımcı sayısını döndürür."""
        return self._katilimci_sayisi

    @katilimci_sayisi.setter
    def katilimci_sayisi(self, value: Any) -> None:
        """Katılımcı sayısını doğrulama ile ayarlar."""
        if not isinstance(value, int):
            raise ValueError(f"Katılımcı sayısı tam sayı olmalıdır, alınan: {type(value).__name__}")
        if not (self.MIN_KATILIMCI <= value <= self.MAX_KATILIMCI):
            raise ValueError(
                f"Katılımcı sayısı {self.MIN_KATILIMCI} ile {self.MAX_KATILIMCI} arasında olmalıdır, alınan: {value}"
            )
        self._katilimci_sayisi = value

    @property
    def antrenman_plani(self) -> str:
        """Antrenman planını döndürür."""
        return self._antrenman_plani

    @antrenman_plani.setter
    def antrenman_plani(self, value: Any) -> None:
        """Antrenman planını geçerli planlar listesine göre ayarlar."""
        if not isinstance(value, str):
            raise ValueError(f"Antrenman planı string olmalıdır, alınan: {type(value).__name__}")
        
        plan_formatted = value.lower().strip()
        if plan_formatted not in self.GECERLI_ANTRENMAN_PLANLARI:
            raise ValueError(
                f"Antrenman planı {self.GECERLI_ANTRENMAN_PLANLARI} değerlerinden biri olmalıdır, alınan: '{value}'"
            )
        self._antrenman_plani = plan_formatted

    def oturum_detaylari_getir(self) -> Dict[str, Any]:
        """Takım antrenman oturumunun detaylı bilgilerini döndürür."""
        detaylar = {
            "oturum_id": self.oturum_id,
            "oturum_tipi": self.oturum_tipi,
            "sure": self.sure,
            "team_id": self.team_id,
            "saha_id": self.saha_id,
            "katilimci_sayisi": self.katilimci_sayisi,
            "antrenman_plani": self.antrenman_plani,
            "durum": self.durum,
            "tarih_saat": self.tarih_saat.isoformat() if self.tarih_saat else None,
            "oturum_turu": "takım"
        }
        return detaylar

    def oturum_maliyeti_hesapla(self) -> float:
        """Takım antrenman oturumunun maliyetini hesaplar."""
        SAHA_KIRASI_SAATLIK = 200.0
        ANTRENOR_UCRETI_SAATLIK = 250.0
        
        saat = self.sure / 60.0
        saha_maliyeti = SAHA_KIRASI_SAATLIK * saat
        antrenor_maliyeti = ANTRENOR_UCRETI_SAATLIK * saat
        
        if self.antrenman_plani == "maç_hazırlığı":
            antrenor_maliyeti *= 1.3
        
        toplam_maliyet = saha_maliyeti + antrenor_maliyeti
        
        if self.katilimci_sayisi > 15:
            toplam_maliyet *= 1.1
        
        return round(toplam_maliyet, 2)

    def katilimci_ekle(self, eklenen_sayisi: int) -> None:
        """Antrenmana katılımcı ekler."""
        yeni_toplam = self.katilimci_sayisi + eklenen_sayisi
        if yeni_toplam > self.MAX_KATILIMCI:
            raise ValueError(f"Maksimum katılımcı sayısı {self.MAX_KATILIMCI}, yeni toplam: {yeni_toplam}")
        self.katilimci_sayisi = yeni_toplam

    def saha_rezervasyon_kontrol(self, mevcut_rezervasyonlar: List[Dict[str, Any]]) -> bool:
        """Sahanın belirtilen tarih ve saatte müsait olup olmadığını kontrol eder."""
        if self.tarih_saat is None:
            return True
        
        from datetime import timedelta
        oturum_bitis = self.tarih_saat + timedelta(minutes=self.sure)
        
        for rezervasyon in mevcut_rezervasyonlar:
            rez_baslangic = rezervasyon.get("baslangic")
            rez_sure = rezervasyon.get("sure", 0)
            rez_saha_id = rezervasyon.get("saha_id")
            
            if rez_saha_id != self.saha_id:
                continue
            
            if rez_baslangic is None:
                continue
            
            if isinstance(rez_baslangic, str):
                from datetime import datetime
                rez_baslangic = datetime.fromisoformat(rez_baslangic)
            
            rez_bitis = rez_baslangic + timedelta(minutes=rez_sure)
            
            if not (oturum_bitis <= rez_baslangic or self.tarih_saat >= rez_bitis):
                return False
        
        return True

    @classmethod
    def takim_antrenman_olustur(
        cls,
        oturum_id: int,
        sure: int,
        team_id: int,
        saha_id: int,
        katilimci_sayisi: int,
        antrenman_plani: str = "taktik"
    ) -> 'TeamTrainingSession':
        """Yeni bir takım antrenman oturumu oluşturur."""
        return cls(
            oturum_id=oturum_id,
            sure=sure,
            team_id=team_id,
            saha_id=saha_id,
            katilimci_sayisi=katilimci_sayisi,
            antrenman_plani=antrenman_plani,
            oturum_tipi="taktik",
            tarih_saat=None,
            durum="planlandı"
        )

    @classmethod
    def antrenman_plani_gecerli_mi(cls, plan: str) -> bool:
        """Verilen antrenman planının geçerli olup olmadığını kontrol eder."""
        if not isinstance(plan, str):
            return False
        return plan.lower().strip() in cls.GECERLI_ANTRENMAN_PLANLARI

    @staticmethod
    def katilimci_sayisi_dogrula(sayi: int) -> bool:
        """Katılımcı sayısının geçerli aralıkta olup olmadığını kontrol eder."""
        return TeamTrainingSession.MIN_KATILIMCI <= sayi <= TeamTrainingSession.MAX_KATILIMCI

    @staticmethod
    def saha_kapasitesi_hesapla(saha_boyutu: str) -> int:
        """Saha boyutuna göre maksimum katılımcı kapasitesini hesaplar."""
        kapasiteler = {
            "küçük": 10,
            "orta": 20,
            "büyük": 30
        }
        return kapasiteler.get(saha_boyutu.lower(), 20)


class RehabTrainingSession(AntrenmanOturumuTemel):
    """
    Rehabilitasyon antrenman oturumu subclass'ı.
    Sakatlık sonrası rehabilitasyon seanslarını temsil eder.
    """
    
    GECERLI_SAKATLIK_TIPLERI = ["kas", "eklem", "kırık", "burkulma", "yırtık", "diğer"]
    MIN_ILERLEME_NOTU = 0
    MAX_ILERLEME_NOTU = 10
    
    def __init__(
        self,
        oturum_id: int,
        sure: int,
        athlete_id: int,
        fizyoterapist_id: int,
        sakatlik_tipi: str,
        rehab_programi: str = "temel",
        oturum_tipi: str = "rehabilitasyon",
        tarih_saat: Optional[datetime] = None,
        durum: str = "planlandı",
        ilerleme_notu: Optional[float] = None
    ):
        """Rehabilitasyon antrenman oturumu örneğini başlatır."""
        super().__init__(
            oturum_id=oturum_id,
            sure=sure,
            athlete_id=athlete_id,
            oturum_tipi=oturum_tipi,
            tarih_saat=tarih_saat,
            durum=durum
        )
        
        self._fizyoterapist_id = None
        self._sakatlik_tipi = None
        self._rehab_programi = None
        self._ilerleme_notu = None
        
        self.fizyoterapist_id = fizyoterapist_id
        self.sakatlik_tipi = sakatlik_tipi
        self.rehab_programi = rehab_programi
        if ilerleme_notu is not None:
            self.ilerleme_notu = ilerleme_notu

    @property
    def fizyoterapist_id(self) -> int:
        """Fizyoterapist ID'sini döndürür."""
        return self._fizyoterapist_id

    @fizyoterapist_id.setter
    def fizyoterapist_id(self, value: Any) -> None:
        """Fizyoterapist ID'sini doğrulama ile ayarlar."""
        if not isinstance(value, int):
            raise GecersizSporcuIdHatasi(f"Fizyoterapist ID'si tam sayı olmalıdır, alınan: {type(value).__name__}")
        if value <= 0:
            raise GecersizSporcuIdHatasi(f"Fizyoterapist ID'si pozitif tam sayı olmalıdır, alınan: {value}")
        self._fizyoterapist_id = value

    @property
    def sakatlik_tipi(self) -> str:
        """Sakatlık tipini döndürür."""
        return self._sakatlik_tipi

    @sakatlik_tipi.setter
    def sakatlik_tipi(self, value: Any) -> None:
        """Sakatlık tipini geçerli tipler listesine göre ayarlar."""
        if not isinstance(value, str):
            raise ValueError(f"Sakatlık tipi string olmalıdır, alınan: {type(value).__name__}")
        
        tip_formatted = value.lower().strip()
        if tip_formatted not in self.GECERLI_SAKATLIK_TIPLERI:
            raise ValueError(
                f"Sakatlık tipi {self.GECERLI_SAKATLIK_TIPLERI} değerlerinden biri olmalıdır, alınan: '{value}'"
            )
        self._sakatlik_tipi = tip_formatted

    @property
    def rehab_programi(self) -> str:
        """Rehabilitasyon programını döndürür."""
        return self._rehab_programi

    @rehab_programi.setter
    def rehab_programi(self, value: Any) -> None:
        """Rehabilitasyon programını ayarlar."""
        if not isinstance(value, str):
            raise ValueError(f"Rehabilitasyon programı string olmalıdır, alınan: {type(value).__name__}")
        if len(value.strip()) == 0:
            raise ValueError("Rehabilitasyon programı boş olamaz")
        self._rehab_programi = value.strip()

    @property
    def ilerleme_notu(self) -> Optional[float]:
        """İlerleme notunu döndürür."""
        return self._ilerleme_notu

    @ilerleme_notu.setter
    def ilerleme_notu(self, value: Any) -> None:
        """İlerleme notunu doğrulama ile ayarlar."""
        if value is not None:
            try:
                notu = float(value)
            except (ValueError, TypeError):
                raise ValueError(f"İlerleme notu sayısal bir değer olmalıdır, alınan: {type(value).__name__}")
            
            if not (self.MIN_ILERLEME_NOTU <= notu <= self.MAX_ILERLEME_NOTU):
                raise ValueError(
                    f"İlerleme notu {self.MIN_ILERLEME_NOTU} ile {self.MAX_ILERLEME_NOTU} arasında olmalıdır, alınan: {notu}"
                )
            self._ilerleme_notu = round(notu, 1)
        else:
            self._ilerleme_notu = None

    def oturum_detaylari_getir(self) -> Dict[str, Any]:
        """Rehabilitasyon antrenman oturumunun detaylı bilgilerini döndürür."""
        detaylar = {
            "oturum_id": self.oturum_id,
            "oturum_tipi": self.oturum_tipi,
            "sure": self.sure,
            "athlete_id": self.athlete_id,
            "fizyoterapist_id": self.fizyoterapist_id,
            "sakatlik_tipi": self.sakatlik_tipi,
            "rehab_programi": self.rehab_programi,
            "durum": self.durum,
            "tarih_saat": self.tarih_saat.isoformat() if self.tarih_saat else None,
            "ilerleme_notu": self.ilerleme_notu,
            "oturum_turu": "rehabilitasyon"
        }
        return detaylar

    def oturum_maliyeti_hesapla(self) -> float:
        """Rehabilitasyon antrenman oturumunun maliyetini hesaplar."""
        FIZYOTERAPIST_UCRETI_SAATLIK = 300.0
        EKIPMAN_MALIYETI_SAATLIK = 50.0
        
        saat = self.sure / 60.0
        fizyoterapist_maliyeti = FIZYOTERAPIST_UCRETI_SAATLIK * saat
        ekipman_maliyeti = EKIPMAN_MALIYETI_SAATLIK * saat
        
        if self.sakatlik_tipi in ["kırık", "yırtık"]:
            ekipman_maliyeti *= 1.5
        
        toplam_maliyet = fizyoterapist_maliyeti + ekipman_maliyeti
        
        return round(toplam_maliyet, 2)

    def ilerleme_kaydet(self, yeni_not: float) -> None:
        """Sporcu rehabilitasyon ilerleme notunu kaydeder."""
        self.ilerleme_notu = yeni_not

    def rehab_raporu_olustur(self) -> str:
        """Rehabilitasyon antrenman oturumu için detaylı rapor oluşturur."""
        rapor = f"=== REHABİLİTASYON ANTRENMAN RAPORU ===\n"
        rapor += f"Oturum ID: {self.oturum_id}\n"
        rapor += f"Sporcu ID: {self.athlete_id}\n"
        rapor += f"Fizyoterapist ID: {self.fizyoterapist_id}\n"
        rapor += f"Sakatlık Tipi: {self.sakatlik_tipi.upper()}\n"
        rapor += f"Rehabilitasyon Programı: {self.rehab_programi}\n"
        rapor += f"Oturum Tipi: {self.oturum_tipi.upper()}\n"
        rapor += f"Süre: {self.sure} dakika ({self.sure // 60} saat {self.sure % 60} dakika)\n"
        
        if self.tarih_saat:
            rapor += f"Tarih/Saat: {self.tarih_saat.strftime('%d.%m.%Y %H:%M')}\n"
        
        rapor += f"Durum: {self.durum.upper()}\n"
        
        if self.ilerleme_notu is not None:
            rapor += f"İlerleme Notu: {self.ilerleme_notu}/10\n"
            if self.ilerleme_notu >= 8:
                rapor += "Değerlendirme: Mükemmel ilerleme!\n"
            elif self.ilerleme_notu >= 6:
                rapor += "Değerlendirme: İyi ilerleme kaydediliyor.\n"
            elif self.ilerleme_notu >= 4:
                rapor += "Değerlendirme: Orta seviye ilerleme.\n"
            else:
                rapor += "Değerlendirme: Daha fazla çalışma gerekiyor.\n"
        else:
            rapor += "İlerleme Notu: Henüz değerlendirilmedi\n"
        
        rapor += f"Tahmini Maliyet: {self.oturum_maliyeti_hesapla()} TL\n"
        rapor += "=" * 40
        
        return rapor

    @classmethod
    def rehab_oturumu_olustur(
        cls,
        oturum_id: int,
        sure: int,
        athlete_id: int,
        fizyoterapist_id: int,
        sakatlik_tipi: str,
        rehab_programi: str = "temel"
    ) -> 'RehabTrainingSession':
        """Yeni bir rehabilitasyon oturumu oluşturur."""
        return cls(
            oturum_id=oturum_id,
            sure=sure,
            athlete_id=athlete_id,
            fizyoterapist_id=fizyoterapist_id,
            sakatlik_tipi=sakatlik_tipi,
            rehab_programi=rehab_programi,
            oturum_tipi="rehabilitasyon",
            tarih_saat=None,
            durum="planlandı"
        )

    @classmethod
    def sakatlik_tipi_gecerli_mi(cls, tip: str) -> bool:
        """Verilen sakatlık tipinin geçerli olup olmadığını kontrol eder."""
        if not isinstance(tip, str):
            return False
        return tip.lower().strip() in cls.GECERLI_SAKATLIK_TIPLERI

    @staticmethod
    def ilerleme_notu_dogrula(notu: Any) -> bool:
        """İlerleme notunun geçerli aralıkta olup olmadığını kontrol eder."""
        try:
            notu_float = float(notu)
            return RehabTrainingSession.MIN_ILERLEME_NOTU <= notu_float <= RehabTrainingSession.MAX_ILERLEME_NOTU
        except (ValueError, TypeError):
            return False

    @staticmethod
    def sakatlik_onceligi_hesapla(sakatlik_tipi: str) -> int:
        """Sakatlık tipine göre öncelik seviyesini hesaplar."""
        oncelikler = {
            "kırık": 5,
            "yırtık": 4,
            "burkulma": 3,
            "eklem": 2,
            "kas": 1,
            "diğer": 1
        }
        return oncelikler.get(sakatlik_tipi.lower(), 1)


class TrainingPlan:
    """
    Bir sporcunun belirli bir dönem için antrenman planını temsil eden entity sınıfı.
    Plan; tarih aralığı, hedef ve ilişkilendirilmiş sporcu bilgisini içerir.
    """

    def __init__(
        self,
        plan_id: int,
        sporcu_id: int,
        baslangic_tarihi: datetime,
        bitis_tarihi: datetime,
        hedef: str,
    ) -> None:
        self._plan_id: int
        self._sporcu_id: int
        self._baslangic_tarihi: datetime
        self._bitis_tarihi: datetime
        self._hedef: str

        self.plan_id = plan_id
        self.sporcu_id = sporcu_id
        self.baslangic_tarihi = baslangic_tarihi
        self.bitis_tarihi = bitis_tarihi
        self.hedef = hedef

    @property
    def plan_id(self) -> int:
        """Plan ID bilgisini döndürür."""
        return self._plan_id

    @plan_id.setter
    def plan_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Plan ID pozitif bir tam sayı olmalıdır")
        self._plan_id = value

    @property
    def sporcu_id(self) -> int:
        """Plana bağlı sporcunun ID bilgisini döndürür."""
        return self._sporcu_id

    @sporcu_id.setter
    def sporcu_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise GecersizSporcuIdHatasi()
        self._sporcu_id = value

    @property
    def baslangic_tarihi(self) -> datetime:
        """Plan başlangıç tarihini döndürür."""
        return self._baslangic_tarihi

    @baslangic_tarihi.setter
    def baslangic_tarihi(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise GecersizTarihSaatHatasi("Başlangıç tarihi datetime olmalıdır")
        self._baslangic_tarihi = value

    @property
    def bitis_tarihi(self) -> datetime:
        """Plan bitiş tarihini döndürür."""
        return self._bitis_tarihi

    @bitis_tarihi.setter
    def bitis_tarihi(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise GecersizTarihSaatHatasi("Bitiş tarihi datetime olmalıdır")
        if hasattr(self, "_baslangic_tarihi") and value < self._baslangic_tarihi:
            raise ValueError("Bitiş tarihi başlangıç tarihinden önce olamaz")
        self._bitis_tarihi = value

    @property
    def hedef(self) -> str:
        """Planın temel hedef açıklamasını döndürür."""
        return self._hedef

    @hedef.setter
    def hedef(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Hedef metni string olmalıdır")
        temiz = value.strip()
        if not temiz:
            raise ValueError("Hedef metni boş olamaz")
        self._hedef = temiz

    def plan_detaylari(self) -> Dict[str, Any]:
        """Planın tüm detaylarını sözlük olarak döndürür."""
        return {
            "plan_id": self.plan_id,
            "sporcu_id": self.sporcu_id,
            "baslangic_tarihi": self.baslangic_tarihi.isoformat(),
            "bitis_tarihi": self.bitis_tarihi.isoformat(),
            "hedef": self.hedef,
            "gun_sayisi": self.plan_suresi_hesapla(),
        }

    def plan_suresi_hesapla(self) -> int:
        """Plan süresini gün cinsinden hesaplar."""
        fark = self.bitis_tarihi.date() - self.baslangic_tarihi.date()
        return fark.days + 1

    @classmethod
    def kisa_vadeli_plan_olustur(
        cls,
        plan_id: int,
        sporcu_id: int,
        baslangic: datetime,
        hedef: str,
    ) -> "TrainingPlan":
        """Varsayılan olarak 4 haftalık kısa vadeli antrenman planı oluşturur."""
        from datetime import timedelta

        bitis = baslangic + timedelta(weeks=4)
        return cls(
            plan_id=plan_id,
            sporcu_id=sporcu_id,
            baslangic_tarihi=baslangic,
            bitis_tarihi=bitis,
            hedef=hedef,
        )

    @staticmethod
    def tarih_araligindan_gun_sayisi(baslangic: datetime, bitis: datetime) -> int:
        """Verilen iki tarih arasındaki gün sayısını hesaplayan yardımcı static metot."""
        if not isinstance(baslangic, datetime) or not isinstance(bitis, datetime):
            raise ValueError("Başlangıç ve bitiş datetime olmalıdır")
        if bitis < baslangic:
            raise ValueError("Bitiş tarihi başlangıç tarihinden önce olamaz")
        return (bitis.date() - baslangic.date()).days + 1


class TrainingSchedule:
    """
    Haftalık antrenman programını ve bu programa bağlı oturum listesini temsil eder.
    """

    GECERLI_PROGRAM_SEVIYELERI = ["düşük", "orta", "yüksek"]

    def __init__(
        self,
        program_id: int,
        haftalik_program: str,
        oturumlar: Optional[List[AntrenmanOturumuTemel]] = None,
    ) -> None:
        self._program_id: int
        self._haftalik_program: str
        self._oturumlar: List[AntrenmanOturumuTemel] = []

        self.program_id = program_id
        self.haftalik_program = haftalik_program
        if oturumlar:
            for oturum in oturumlar:
                self.oturum_ekle(oturum)

    @property
    def program_id(self) -> int:
        """Program ID bilgisini döndürür."""
        return self._program_id

    @program_id.setter
    def program_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Program ID pozitif bir tam sayı olmalıdır")
        self._program_id = value

    @property
    def haftalik_program(self) -> str:
        """Haftalık program seviyesini döndürür (düşük/orta/yüksek)."""
        return self._haftalik_program

    @haftalik_program.setter
    def haftalik_program(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Haftalık program string olmalıdır")
        seviye = value.lower().strip()
        if seviye not in self.GECERLI_PROGRAM_SEVIYELERI:
            raise ValueError(
                f"Haftalık program {self.GECERLI_PROGRAM_SEVIYELERI} değerlerinden biri olmalıdır"
            )
        self._haftalik_program = seviye

    @property
    def oturumlar(self) -> List[AntrenmanOturumuTemel]:
        """Programa bağlı antrenman oturumu listesini döndürür."""
        return list(self._oturumlar)

    def oturum_ekle(self, oturum: AntrenmanOturumuTemel) -> None:
        """Programa yeni bir antrenman oturumu ekler."""
        if not isinstance(oturum, AntrenmanOturumuTemel):
            raise TypeError("Yalnızca AntrenmanOturumuTemel tipinden nesneler eklenebilir")
        self._oturumlar.append(oturum)

    def haftalik_yuk_hesapla(self) -> int:
        """Tüm oturumların sürelerini toplayarak haftalık antrenman yükünü dakika cinsinden hesaplar."""
        return sum(oturum.sure for oturum in self._oturumlar)

    def program_ozeti(self) -> Dict[str, Any]:
        """Programın özet bilgilerini sözlük olarak döndürür."""
        return {
            "program_id": self.program_id,
            "haftalik_program": self.haftalik_program,
            "oturum_sayisi": len(self._oturumlar),
            "toplam_sure_dakika": self.haftalik_yuk_hesapla(),
        }

    @classmethod
    def bos_program_olustur(cls, program_id: int, seviye: str = "orta") -> "TrainingSchedule":
        """Verilen seviye ile boş bir antrenman programı oluşturur."""
        return cls(program_id=program_id, haftalik_program=seviye, oturumlar=None)

    @staticmethod
    def onerilen_maksimum_haftalik_sure(seviye: str) -> int:
        """Haftalık program seviyesine göre önerilen maksimum antrenman süresini (dakika) döndürür."""
        seviye = seviye.lower().strip()
        harita = {"düşük": 240, "orta": 360, "yüksek": 540}
        return harita.get(seviye, 360)


class TrainingStatistics:
    """
    Bir sporcunun antrenman istatistiklerini tutan entity sınıfı.
    Toplam oturum sayısı, tamamlanan ve iptal edilen oturumlar gibi temel metrikleri içerir.
    """

    def __init__(
        self,
        sporcu_id: int,
        toplam_oturum: int = 0,
        tamamlanan: int = 0,
        iptal_edilen: int = 0,
    ) -> None:
        if not isinstance(sporcu_id, int) or sporcu_id <= 0:
            raise GecersizSporcuIdHatasi()

        self.sporcu_id: int = sporcu_id
        self.toplam_oturum: int = max(0, toplam_oturum)
        self.tamamlanan: int = max(0, tamamlanan)
        self.iptal_edilen: int = max(0, iptal_edilen)

    def istatistik_guncelle(self, yeni_durum: str) -> None:
        """Verilen duruma göre istatistikleri günceller."""
        self.toplam_oturum += 1
        durum = yeni_durum.lower().strip()

        if durum == "tamamlandi":
            self.tamamlanan += 1
        elif durum == "iptal_edildi":
            self.iptal_edilen += 1

    def basari_orani_hesapla(self) -> float:
        """Tamamlanan oturum sayısına göre başarı oranını yüzde olarak hesaplar."""
        if self.toplam_oturum == 0:
            return 0.0
        oran = (self.tamamlanan / self.toplam_oturum) * 100
        return round(oran, 2)

    def istatistik_ozeti(self) -> Dict[str, Any]:
        """İstatistiklerin özetini sözlük olarak döndürür."""
        return {
            "sporcu_id": self.sporcu_id,
            "toplam_oturum": self.toplam_oturum,
            "tamamlanan": self.tamamlanan,
            "iptal_edilen": self.iptal_edilen,
            "basari_orani": self.basari_orani_hesapla(),
        }

    @classmethod
    def oturumlardan_olustur(
        cls,
        sporcu_id: int,
        oturumlar: List[AntrenmanOturumuTemel],
    ) -> "TrainingStatistics":
        """Verilen sporcuya ait oturum listesinden istatistik nesnesi oluşturur."""
        toplam = 0
        tamamlanan = 0
        iptal_edilen = 0

        for oturum in oturumlar:
            if oturum.athlete_id != sporcu_id:
                continue
            toplam += 1
            if oturum.durum == "tamamlandi":
                tamamlanan += 1
            elif oturum.durum == "iptal_edildi":
                iptal_edilen += 1

        return cls(
            sporcu_id=sporcu_id,
            toplam_oturum=toplam,
            tamamlanan=tamamlanan,
            iptal_edilen=iptal_edilen,
        )

    @staticmethod
    def durum_sayim(oturumlar: List[AntrenmanOturumuTemel]) -> Dict[str, int]:
        """Verilen oturum listesi için durumlara göre sayım yapan yardımcı static metot."""
        sayim: Dict[str, int] = {}
        for oturum in oturumlar:
            durum = oturum.durum
            sayim[durum] = sayim.get(durum, 0) + 1
        return sayim


class TrainingManager:
    """
    Antrenman modülü için Servis (Service) katmanı.
    İş mantığı kurallarını uygular ve Repository ile haberleşir.
    """
    
    def __init__(self, repository):
        self.repo = repository

    def oturum_olustur(self, oturum: AntrenmanOturumuTemel) -> None:
        """
        Yeni bir oturum oluşturur. Çakışma kontrolü yapar.
        """
        # 1. Çakışma Kontrolü (GÜNCELLENMİŞ KISIM)
        if oturum.tarih_saat:
            # Oturum tipine göre ID'leri güvenli şekilde alıyoruz
            ath_id = getattr(oturum, 'athlete_id', None)
            saha_id = getattr(oturum, 'saha_id', None)
            
            # Yeni repository metodunu çağırıyoruz: detayli_cakisma_kontrol
            cakisma_var = self.repo.detayli_cakisma_kontrol(
                tarih=oturum.tarih_saat, 
                sure_dk=oturum.sure, 
                haric_id=oturum.oturum_id,
                athlete_id=ath_id,  # Sporcu kontrolü için
                saha_id=saha_id     # Saha kontrolü için
            )
            
            if cakisma_var:
                raise TakvimCakismasiHatasi(f"Bu tarih ve saatte ({oturum.tarih_saat}) planlanan kaynak (sporcu veya saha) dolu!")

        # 2. Kayıt
        self.repo.kaydet(oturum)
        print(f"Bilgi: {oturum.oturum_id} ID'li oturum başarıyla oluşturuldu.")

    def oturum_iptal_et(self, oturum_id: int) -> None:
        """
        Bir oturumu iptal eder.
        """
        oturum = self.repo.id_ile_bul(oturum_id)
        if not oturum:
            raise OturumBulunamadiHatasi()
        
        oturum.oturum_iptal_et()
        self.repo.guncelle(oturum) 
        print(f"Bilgi: {oturum_id} ID'li oturum iptal edildi.")

    def sporcu_programi_getir(self, athlete_id: int) -> List[Dict[str, Any]]:
        """
        Sporcunun antrenman geçmişini ve gelecek programını raporlar.
        """
        oturumlar = self.repo.sporcuya_gore_filtrele(athlete_id)
        rapor = []
        for o in oturumlar:
            rapor.append(o.oturum_detaylari_getir())
        return rapor

    def toplu_program_olustur(self, baslangic_id: int, template_oturum: AntrenmanOturumuTemel, tekrar_sayisi: int, aralik_gun: int):
        """
        Belirli aralıklarla tekrar eden antrenmanlar oluşturur.
        """
        from datetime import timedelta
        import copy
        
        mevcut_tarih = template_oturum.tarih_saat
        mevcut_id = baslangic_id
        
        for _ in range(tekrar_sayisi):
            yeni_oturum = copy.deepcopy(template_oturum)
            yeni_oturum.oturum_id = mevcut_id
            yeni_oturum.tarih_saat = mevcut_tarih
            
            try:
                self.oturum_olustur(yeni_oturum)
            except Exception as e:
                print(f"Hata: {mevcut_id} ID'li periyodik oturum oluşturulamadı. Sebep: {e}")
            
            mevcut_tarih += timedelta(days=aralik_gun)
            mevcut_id += 1