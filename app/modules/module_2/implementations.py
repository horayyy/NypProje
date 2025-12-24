"""
Antrenman ve Program modülü için implementasyon sınıfları.
Subclass'lar, entity/model sınıfları ve service katmanı burada yer alır.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List

from .base import AntrenmanOturumuTemel
from .exceptions import (
    GecersizSporcuIdHatasi,
    GecersizTakimIdHatasi,
    GecersizTarihSaatHatasi,
    GecersizSahaIdHatasi,
    SahaDoluHatasi,
    AntrenmanHatasi,
    TakvimCakismasiHatasi,
    OturumBulunamadiHatasi
)


# Bireysel antrenman oturumu subclass'ı - tek sporcu için özel antrenman seansları
class IndividualTrainingSession(AntrenmanOturumuTemel):
    
    MIN_PERFORMANS_NOTU = 0
    MAX_PERFORMANS_NOTU = 10
    GECERLI_ODAK_ALANLARI = ["hız", "güç", "dayanıklılık", "esneklik", "koordinasyon"]
    
    # Maliyet hesaplama sabitleri (class-level, dinamik olarak dışarıdan ayarlanabilir)
    SAATLIK_ANTRENOR_UCRETI: float = 150.0
    
    # Bireysel antrenman oturumu örneğini başlatır
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

    # Antrenör ID'sini döndürür
    @property
    def antrenor_id(self) -> int:
        return self._antrenor_id

    # Antrenör ID'sini doğrulama ile ayarlar
    @antrenor_id.setter
    def antrenor_id(self, value: Any) -> None:
        if not isinstance(value, int):
            raise GecersizSporcuIdHatasi(f"Antrenör ID'si tam sayı olmalıdır, alınan: {type(value).__name__}")
        if value <= 0:
            raise GecersizSporcuIdHatasi(f"Antrenör ID'si pozitif tam sayı olmalıdır, alınan: {value}")
        self._antrenor_id = value

    # Odak alanını döndürür
    @property
    def odak_alani(self) -> str:
        return self._odak_alani

    # Odak alanını doğrulama ile ayarlar
    @odak_alani.setter
    def odak_alani(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Odak alanı string olmalıdır, alınan: {type(value).__name__}")
        
        alan_formatted = value.lower().strip()
        if alan_formatted not in self.GECERLI_ODAK_ALANLARI:
            raise ValueError(
                f"Odak alanı {self.GECERLI_ODAK_ALANLARI} değerlerinden biri olmalıdır, alınan: '{value}'"
            )
        self._odak_alani = alan_formatted

    # Performans notunu döndürür
    @property
    def performans_notu(self) -> Optional[float]:
        return self._performans_notu

    # Performans notunu doğrulama ile ayarlar
    @performans_notu.setter
    def performans_notu(self, value: Any) -> None:
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

    # Bireysel antrenman oturumunun detaylı bilgilerini döndürür
    def oturum_detaylari_getir(self) -> Dict[str, Any]:
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
        saat = self.sure / 60.0
        maliyet = self.SAATLIK_ANTRENOR_UCRETI * saat
        
        if self.odak_alani == "koordinasyon":
            maliyet *= 1.2
        
        return round(maliyet, 2)

    # Sporcu performans notunu günceller
    def performans_notu_guncelle(self, yeni_not: float) -> None:
        self.performans_notu = yeni_not

    # Bireysel antrenman oturumu için detaylı rapor oluşturur
    def bireysel_rapor_olustur(self) -> str:
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

    # Yeni bir bireysel antrenman oturumu oluşturur
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

    # Verilen odak alanının geçerli olup olmadığını kontrol eder
    @classmethod
    def odak_alani_gecerli_mi(cls, alan: str) -> bool:
        if not isinstance(alan, str):
            return False
        return alan.lower().strip() in cls.GECERLI_ODAK_ALANLARI

    # Performans notunun geçerli aralıkta olup olmadığını kontrol eder
    @staticmethod
    def performans_notu_dogrula(notu: Any) -> bool:
        try:
            notu_float = float(notu)
            return IndividualTrainingSession.MIN_PERFORMANS_NOTU <= notu_float <= IndividualTrainingSession.MAX_PERFORMANS_NOTU
        except (ValueError, TypeError):
            return False

    # İki performans notunu karşılaştırır
    @staticmethod
    def performans_notu_karsilastir(not1: float, not2: float) -> int:
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


# Takım antrenman oturumu subclass'ı - birden fazla sporcu için antrenman seansları
class TeamTrainingSession(AntrenmanOturumuTemel):
    
    MIN_KATILIMCI = 2
    MAX_KATILIMCI = 30
    MIN_SAHA_ID = 1
    MAX_SAHA_ID = 5
    GECERLI_ANTRENMAN_PLANLARI = ["taktik", "kondisyon", "teknik", "maç_hazırlığı"]
    
    # Maliyet hesaplama sabitleri (class-level, dinamik olarak dışarıdan ayarlanabilir)
    SAHA_KIRASI_SAATLIK: float = 200.0
    ANTRENOR_UCRETI_SAATLIK: float = 250.0
    
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

    # Saha ID'sini döndürür
    @property
    def saha_id(self) -> int:
        return self._saha_id

    # Saha ID'sini doğrulama ile ayarlar 1-5 arası
    @saha_id.setter
    def saha_id(self, value: Any) -> None:
        if not isinstance(value, int):
            raise GecersizSahaIdHatasi(f"Saha ID'si tam sayı olmalıdır, alınan: {type(value).__name__}")
        if not (self.MIN_SAHA_ID <= value <= self.MAX_SAHA_ID):
            raise GecersizSahaIdHatasi(
                f"Saha ID'si {self.MIN_SAHA_ID} ile {self.MAX_SAHA_ID} arasında olmalıdır (Mevcut sahalar: 1-5), alınan: {value}"
            )
        self._saha_id = value

    # Katılımcı sayısını döndürür
    @property
    def katilimci_sayisi(self) -> int:
        return self._katilimci_sayisi

    # Katılımcı sayısını doğrulama ile ayarlar
    @katilimci_sayisi.setter
    def katilimci_sayisi(self, value: Any) -> None:
        if not isinstance(value, int):
            raise ValueError(f"Katılımcı sayısı tam sayı olmalıdır, alınan: {type(value).__name__}")
        if not (self.MIN_KATILIMCI <= value <= self.MAX_KATILIMCI):
            raise ValueError(
                f"Katılımcı sayısı {self.MIN_KATILIMCI} ile {self.MAX_KATILIMCI} arasında olmalıdır, alınan: {value}"
            )
        self._katilimci_sayisi = value

    # Antrenman planını döndürür
    @property
    def antrenman_plani(self) -> str:
        return self._antrenman_plani

    # Antrenman planını doğrulama ile ayarlar
    @antrenman_plani.setter
    def antrenman_plani(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Antrenman planı string olmalıdır, alınan: {type(value).__name__}")
        
        plan_formatted = value.lower().strip()
        if plan_formatted not in self.GECERLI_ANTRENMAN_PLANLARI:
            raise ValueError(
                f"Antrenman planı {self.GECERLI_ANTRENMAN_PLANLARI} değerlerinden biri olmalıdır, alınan: '{value}'"
            )
        self._antrenman_plani = plan_formatted

    # Takım antrenman oturumunun detaylı bilgilerini döndürür
    def oturum_detaylari_getir(self) -> Dict[str, Any]:
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

    # Takım antrenman oturumunun maliyetini hesaplar
    def oturum_maliyeti_hesapla(self) -> float:
        saat = self.sure / 60.0
        saha_maliyeti = self.SAHA_KIRASI_SAATLIK * saat
        antrenor_maliyeti = self.ANTRENOR_UCRETI_SAATLIK * saat
        
        if self.antrenman_plani == "maç_hazırlığı":
            antrenor_maliyeti *= 1.3
        
        toplam_maliyet = saha_maliyeti + antrenor_maliyeti
        
        if self.katilimci_sayisi > 15:
            toplam_maliyet *= 1.1
        
        return round(toplam_maliyet, 2)

    # Antrenmana katılımcı ekler
    def katilimci_ekle(self, eklenen_sayisi: int) -> None:
        yeni_toplam = self.katilimci_sayisi + eklenen_sayisi
        if yeni_toplam > self.MAX_KATILIMCI:
            raise ValueError(f"Maksimum katılımcı sayısı {self.MAX_KATILIMCI}, yeni toplam: {yeni_toplam}")
        self.katilimci_sayisi = yeni_toplam

    # Sahanın belirtilen tarih ve saatte müsait olup olmadığını kontrol eder
    def saha_rezervasyon_kontrol(self, mevcut_rezervasyonlar: List[Dict[str, Any]]) -> bool:
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

    # Yeni bir takım antrenman oturumu oluşturur
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
        if not isinstance(plan, str):
            return False
        return plan.lower().strip() in cls.GECERLI_ANTRENMAN_PLANLARI

    # Katılımcı sayısının geçerli aralıkta olup olmadığını kontrol eder
    @staticmethod
    def katilimci_sayisi_dogrula(sayi: int) -> bool:
        return TeamTrainingSession.MIN_KATILIMCI <= sayi <= TeamTrainingSession.MAX_KATILIMCI

    # Saha boyutuna göre maksimum katılımcı kapasitesini hesaplar
    @staticmethod
    def saha_kapasitesi_hesapla(saha_boyutu: str) -> int:
        kapasiteler = {
            "küçük": 10,
            "orta": 20,
            "büyük": 30
        }
        return kapasiteler.get(saha_boyutu.lower(), 20)


# Rehabilitasyon antrenman oturumu subclass'ı - sakatlık sonrası rehabilitasyon seansları
class RehabTrainingSession(AntrenmanOturumuTemel):
    
    GECERLI_SAKATLIK_TIPLERI = ["kas", "eklem", "kırık", "burkulma", "yırtık", "diğer"]
    MIN_ILERLEME_NOTU = 0
    MAX_ILERLEME_NOTU = 10
    
    # Maliyet hesaplama sabitleri (class-level, dinamik olarak dışarıdan ayarlanabilir)
    FIZYOTERAPIST_UCRETI_SAATLIK: float = 300.0
    EKIPMAN_MALIYETI_SAATLIK: float = 50.0
    
    # Rehabilitasyon antrenman oturumu örneğini başlatır
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

    # Fizyoterapist ID'sini döndürür
    @property
    def fizyoterapist_id(self) -> int:
        return self._fizyoterapist_id

    # Fizyoterapist ID'sini doğrulama ile ayarlar
    @fizyoterapist_id.setter
    def fizyoterapist_id(self, value: Any) -> None:

        if not isinstance(value, int):
            raise GecersizSporcuIdHatasi(f"Fizyoterapist ID'si tam sayı olmalıdır, alınan: {type(value).__name__}")
        if value <= 0:
            raise GecersizSporcuIdHatasi(f"Fizyoterapist ID'si pozitif tam sayı olmalıdır, alınan: {value}")
        self._fizyoterapist_id = value

    # Sakatlık tipini döndürür
    @property
    def sakatlik_tipi(self) -> str:
        return self._sakatlik_tipi

    # Sakatlık tipini geçerli tipler listesine göre ayarlar
    @sakatlik_tipi.setter
    def sakatlik_tipi(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Sakatlık tipi string olmalıdır, alınan: {type(value).__name__}")
        
        tip_formatted = value.lower().strip()
        if tip_formatted not in self.GECERLI_SAKATLIK_TIPLERI:
            raise ValueError(
                f"Sakatlık tipi {self.GECERLI_SAKATLIK_TIPLERI} değerlerinden biri olmalıdır, alınan: '{value}'"
            )
        self._sakatlik_tipi = tip_formatted

    # Rehabilitasyon programını döndürür
    @property
    def rehab_programi(self) -> str:
        return self._rehab_programi

    # Rehabilitasyon programını ayarlar
    @rehab_programi.setter
    def rehab_programi(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Rehabilitasyon programı string olmalıdır, alınan: {type(value).__name__}")
        if len(value.strip()) == 0:
            raise ValueError("Rehabilitasyon programı boş olamaz")
        self._rehab_programi = value.strip()

    # İlerleme notunu döndürür
    @property
    def ilerleme_notu(self) -> Optional[float]:
        return self._ilerleme_notu

    # İlerleme notunu doğrulama ile ayarlar
    @ilerleme_notu.setter
    def ilerleme_notu(self, value: Any) -> None:
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

    # Rehabilitasyon antrenman oturumunun detaylı bilgilerini döndürür
    def oturum_detaylari_getir(self) -> Dict[str, Any]:
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

    # Rehabilitasyon antrenman oturumunun maliyetini hesaplar
    def oturum_maliyeti_hesapla(self) -> float:
        saat = self.sure / 60.0
        fizyoterapist_maliyeti = self.FIZYOTERAPIST_UCRETI_SAATLIK * saat
        ekipman_maliyeti = self.EKIPMAN_MALIYETI_SAATLIK * saat
        
        if self.sakatlik_tipi in ["kırık", "yırtık"]:
            ekipman_maliyeti *= 1.5
        
        toplam_maliyet = fizyoterapist_maliyeti + ekipman_maliyeti
        
        return round(toplam_maliyet, 2)

    # Verilen sakatlık tipinin geçerli olup olmadığını kontrol eder
    @classmethod
    def sakatlik_tipi_gecerli_mi(cls, tip: str) -> bool:
        if not isinstance(tip, str):
            return False
        return tip.lower().strip() in cls.GECERLI_SAKATLIK_TIPLERI


# Bir sporcunun belirli bir dönem için antrenman planını temsil eden entity sınıfı - Plan; tarih aralığı, hedef ve ilişkilendirilmiş sporcu bilgisini içerir
class TrainingPlan:

    # TrainingPlan örneğini başlatır
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

    # Plan ID bilgisini döndürür
    @property
    def plan_id(self) -> int:
        return self._plan_id

    @plan_id.setter
    def plan_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Plan ID pozitif bir tam sayı olmalıdır")
        self._plan_id = value

    # Plana bağlı sporcunun ID bilgisini döndürür
    @property
    def sporcu_id(self) -> int:
        return self._sporcu_id

    @sporcu_id.setter
    def sporcu_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise GecersizSporcuIdHatasi()
        self._sporcu_id = value

    # Plan başlangıç tarihini döndürür
    @property
    def baslangic_tarihi(self) -> datetime:
        return self._baslangic_tarihi

    @baslangic_tarihi.setter
    def baslangic_tarihi(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise GecersizTarihSaatHatasi("Başlangıç tarihi datetime olmalıdır")
        self._baslangic_tarihi = value

    # Plan bitiş tarihini döndürür
    @property
    def bitis_tarihi(self) -> datetime:
        return self._bitis_tarihi

    @bitis_tarihi.setter
    def bitis_tarihi(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise GecersizTarihSaatHatasi("Bitiş tarihi datetime olmalıdır")
        if hasattr(self, "_baslangic_tarihi") and value < self._baslangic_tarihi:
            raise ValueError("Bitiş tarihi başlangıç tarihinden önce olamaz")
        self._bitis_tarihi = value

    # Planın temel hedef açıklamasını döndürür
    @property
    def hedef(self) -> str:
        return self._hedef

    @hedef.setter
    def hedef(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Hedef metni string olmalıdır")
        temiz = value.strip()
        if not temiz:
            raise ValueError("Hedef metni boş olamaz")
        self._hedef = temiz

    # Planın tüm detaylarını sözlük olarak döndürür
    def plan_detaylari(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "sporcu_id": self.sporcu_id,
            "baslangic_tarihi": self.baslangic_tarihi.isoformat(),
            "bitis_tarihi": self.bitis_tarihi.isoformat(),
            "hedef": self.hedef,
            "gun_sayisi": self.plan_suresi_hesapla(),
        }

    # Plan süresini gün cinsinden hesaplar
    def plan_suresi_hesapla(self) -> int:
        fark = self.bitis_tarihi.date() - self.baslangic_tarihi.date()
        return fark.days + 1

    # Varsayılan olarak 4 haftalık kısa vadeli antrenman planı oluşturur
    @classmethod
    def kisa_vadeli_plan_olustur(
        cls,
        plan_id: int,
        sporcu_id: int,
        baslangic: datetime,
        hedef: str,
    ) -> "TrainingPlan":
        from datetime import timedelta

        bitis = baslangic + timedelta(weeks=4)
        return cls(
            plan_id=plan_id,
            sporcu_id=sporcu_id,
            baslangic_tarihi=baslangic,
            bitis_tarihi=bitis,
            hedef=hedef,
        )

    # Verilen iki tarih arasındaki gün sayısını hesaplayan yardımcı static metot
    @staticmethod
    def tarih_araligindan_gun_sayisi(baslangic: datetime, bitis: datetime) -> int:
        if not isinstance(baslangic, datetime) or not isinstance(bitis, datetime):
            raise ValueError("Başlangıç ve bitiş datetime olmalıdır")
        if bitis < baslangic:
            raise ValueError("Bitiş tarihi başlangıç tarihinden önce olamaz")
        return (bitis.date() - baslangic.date()).days + 1


# Haftalık antrenman programını ve bu programa bağlı oturum listesini temsil eder
class TrainingSchedule:

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

    # Program ID bilgisini döndürür
    @property
    def program_id(self) -> int:
        return self._program_id

    @program_id.setter
    def program_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Program ID pozitif bir tam sayı olmalıdır")
        self._program_id = value

    # Haftalık program seviyesini döndürür (düşük/orta/yüksek)
    @property
    def haftalik_program(self) -> str:
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

    # Programa bağlı antrenman oturumu listesini döndürür
    @property
    def oturumlar(self) -> List[AntrenmanOturumuTemel]:
        return list(self._oturumlar)

    # Programa yeni bir antrenman oturumu ekler
    def oturum_ekle(self, oturum: AntrenmanOturumuTemel) -> None:
        if not isinstance(oturum, AntrenmanOturumuTemel):
            raise TypeError("Yalnızca AntrenmanOturumuTemel tipinden nesneler eklenebilir")
        self._oturumlar.append(oturum)

    # Tüm oturumların sürelerini toplayarak haftalık antrenman yükünü dakika cinsinden hesaplar
    def haftalik_yuk_hesapla(self) -> int:
        return sum(oturum.sure for oturum in self._oturumlar)

    # Programın özet bilgilerini sözlük olarak döndürür
    def program_ozeti(self) -> Dict[str, Any]:
        return {
            "program_id": self.program_id,
            "haftalik_program": self.haftalik_program,
            "oturum_sayisi": len(self._oturumlar),
            "toplam_sure_dakika": self.haftalik_yuk_hesapla(),
        }

    # Verilen seviye ile boş bir antrenman programı oluşturur
    @classmethod
    def bos_program_olustur(cls, program_id: int, seviye: str = "orta") -> "TrainingSchedule":
        return cls(program_id=program_id, haftalik_program=seviye, oturumlar=None)

    # Haftalık program seviyesine göre önerilen maksimum antrenman süresini (dakika) döndürür
    @staticmethod
    def onerilen_maksimum_haftalik_sure(seviye: str) -> int:
        seviye = seviye.lower().strip()
        harita = {"düşük": 240, "orta": 360, "yüksek": 540}
        return harita.get(seviye, 360)


# Bir sporcunun antrenman istatistiklerini tutan entity sınıfı - Toplam oturum sayısı, tamamlanan ve iptal edilen oturumlar gibi temel metrikleri içerir
class TrainingStatistics:

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

    # Verilen duruma göre istatistikleri günceller
    def istatistik_guncelle(self, yeni_durum: str) -> None:
        self.toplam_oturum += 1
        durum = yeni_durum.lower().strip()

        if durum == "tamamlandi":
            self.tamamlanan += 1
        elif durum == "iptal_edildi":
            self.iptal_edilen += 1

    # Tamamlanan oturum sayısına göre başarı oranını yüzde olarak hesaplar
    def basari_orani_hesapla(self) -> float:
        if self.toplam_oturum == 0:
            return 0.0
        oran = (self.tamamlanan / self.toplam_oturum) * 100
        return round(oran, 2)

    # İstatistiklerin özetini sözlük olarak döndürür
    def istatistik_ozeti(self) -> Dict[str, Any]:
        return {
            "sporcu_id": self.sporcu_id,
            "toplam_oturum": self.toplam_oturum,
            "tamamlanan": self.tamamlanan,
            "iptal_edilen": self.iptal_edilen,
            "basari_orani": self.basari_orani_hesapla(),
        }

    # Verilen sporcuya ait oturum listesinden istatistik nesnesi oluşturur
    @classmethod
    def oturumlardan_olustur(
        cls,
        sporcu_id: int,
        oturumlar: List[AntrenmanOturumuTemel],
    ) -> "TrainingStatistics":
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

    # Verilen oturum listesi için durumlara göre sayım yapan yardımcı static metot
    @staticmethod
    def durum_sayim(oturumlar: List[AntrenmanOturumuTemel]) -> Dict[str, int]:
        sayim: Dict[str, int] = {}
        for oturum in oturumlar:
            durum = oturum.durum
            sayim[durum] = sayim.get(durum, 0) + 1
        return sayim


# Antrenman modülü için Servis (Service) katmanı - iş mantığı kurallarını uygular ve Repository ile haberleşir
class TrainingManager:
    
    # TrainingManager örneğini başlatır
    def __init__(self, repository):
        self.repo = repository
    
    # Yeni bir TrainingManager örneği oluşturur (class method)
    @classmethod
    def yeni_manager_olustur(cls, repository) -> 'TrainingManager':
        return cls(repository)

    # Yeni bir oturum oluşturur ve çakışma kontrolü yapar
    def oturum_olustur(self, oturum: AntrenmanOturumuTemel) -> None:
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

    # Bir oturumu iptal eder
    def oturum_iptal_et(self, oturum_id: int) -> None:
        oturum = self.repo.id_ile_bul(oturum_id)
        if not oturum:
            raise OturumBulunamadiHatasi()
        
        oturum.oturum_iptal_et()
        self.repo.guncelle(oturum) 
        print(f"Bilgi: {oturum_id} ID'li oturum iptal edildi.")

    # Bir oturumu tamamlandı olarak işaretler
    def oturum_tamamla(self, oturum_id: int) -> None:
        oturum = self.repo.id_ile_bul(oturum_id)
        if not oturum:
            raise OturumBulunamadiHatasi()
        
        oturum.oturum_tamamla()
        self.repo.guncelle(oturum)
        print(f"Bilgi: {oturum_id} ID'li oturum tamamlandı olarak işaretlendi.")

    # Sporcunun antrenman geçmişini ve gelecek programını raporlar
    def sporcu_programi_getir(self, athlete_id: int) -> List[Dict[str, Any]]:
        oturumlar = self.repo.sporcuya_gore_filtrele(athlete_id)
        rapor = []
        for o in oturumlar:
            rapor.append(o.oturum_detaylari_getir())
        return rapor

    # Belirli aralıklarla tekrar eden antrenmanlar oluşturur
    def toplu_program_olustur(self, baslangic_id: int, template_oturum: AntrenmanOturumuTemel, tekrar_sayisi: int, aralik_gun: int):
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
    
    # Verilen oturum durumunun geçerli olup olmadığını kontrol eden static metot
    @staticmethod
    def oturum_durumu_gecerli_mi(durum: str) -> bool:
        gecerli_durumlar = ["planlandı", "tamamlandi", "iptal_edildi"]
        return isinstance(durum, str) and durum.lower() in gecerli_durumlar