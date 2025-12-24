from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any, Dict


from .exceptions import (
    GecersizOturumIdHatasi,
    GecersizSporcuIdHatasi,
    GecersizTakimIdHatasi,
    GecersizOturumTipiHatasi,
    GecersizOturumDurumuHatasi,
    GecersizTarihSaatHatasi,
    GecersizSureHatasi,
    OturumDogrulamaHatasi
)


# Tüm antrenman oturumu tipleri için soyut temel sınıf
class AntrenmanOturumuTemel(ABC):

    
    GECERLI_OTURUM_TIPLERI = ["kondisyon", "teknik", "taktik", "rehabilitasyon"]
    GECERLI_DURUMLAR = ["planlandı", "tamamlandi", "iptal_edildi"]
    MIN_SURE = 1
    MAX_SURE = 480
    
    # Antrenman oturumu örneğini başlatır
    def __init__(
        self,
        oturum_id: int,
        sure: int,
        athlete_id: Optional[int] = None,
        team_id: Optional[int] = None,
        oturum_tipi: str = "kondisyon",
        tarih_saat: Optional[datetime] = None,
        durum: str = "planlandı"
    ):
        
        # Özel nitelikler (Private attributes)
        self._oturum_id = None
        self._sure = None
        self._athlete_id = None
        self._team_id = None
        self._oturum_tipi = None
        self._tarih_saat = None
        self._durum = None
        
        # Property setter'ları üzerinden değer ataması
        self.oturum_id = oturum_id
        self.sure = sure
        
        if athlete_id is not None:
            self.athlete_id = athlete_id
        if team_id is not None:
            self.team_id = team_id
            
        self.oturum_tipi = oturum_tipi
        
        if tarih_saat is not None:
            self.tarih_saat = tarih_saat
            
        self.durum = durum

    # Oturum ID'sini döndürür
    @property
    def oturum_id(self) -> int:
        return self._oturum_id

    # Oturum ID'sini doğrulama ile ayarlar
    @oturum_id.setter
    def oturum_id(self, value: Any) -> None:
        if not isinstance(value, int):
            raise GecersizOturumIdHatasi(f"Oturum ID'si tam sayı olmalıdır, alınan: {type(value).__name__}")
        if value <= 0:
            raise GecersizOturumIdHatasi(f"Oturum ID'si pozitif tam sayı olmalıdır, alınan: {value}")
        self._oturum_id = value

    # Antrenman süresini dakika cinsinden döndürür
    @property
    def sure(self) -> int:
        return self._sure

    # Antrenman süresini doğrulama ile ayarlar
    @sure.setter
    def sure(self, value: Any) -> None:
        if not isinstance(value, int):
            raise GecersizSureHatasi(f"Süre tam sayı olmalıdır, alınan: {type(value).__name__}")
        if not (self.MIN_SURE <= value <= self.MAX_SURE):
            raise GecersizSureHatasi(f"Süre {self.MIN_SURE} ile {self.MAX_SURE} dakika arasında olmalıdır, alınan: {value}")
        self._sure = value

    # Sporcu ID'sini döndürür
    @property
    def athlete_id(self) -> Optional[int]:
        return self._athlete_id

    # Sporcu ID'sini doğrulama ile ayarlar
    @athlete_id.setter
    def athlete_id(self, value: Any) -> None:
        if not isinstance(value, int):
            raise GecersizSporcuIdHatasi(f"Sporcu ID'si tam sayı olmalıdır, alınan: {type(value).__name__}")
        if value <= 0:
            raise GecersizSporcuIdHatasi(f"Sporcu ID'si pozitif tam sayı olmalıdır, alınan: {value}")
        self._athlete_id = value

    # Takım ID'sini döndürür
    @property
    def team_id(self) -> Optional[int]:
        return self._team_id

    # Takım ID'sini doğrulama ile ayarlar
    @team_id.setter
    def team_id(self, value: Any) -> None:
        if not isinstance(value, int):
            raise GecersizTakimIdHatasi(f"Takım ID'si tam sayı olmalıdır, alınan: {type(value).__name__}")
        if value <= 0:
            raise GecersizTakimIdHatasi(f"Takım ID'si pozitif tam sayı olmalıdır, alınan: {value}")
        self._team_id = value

    # Oturum tipini döndürür
    @property
    def oturum_tipi(self) -> str:
        return self._oturum_tipi

    # Oturum tipini doğrulama ile ayarlar
    @oturum_tipi.setter
    def oturum_tipi(self, value: Any) -> None:
        if not isinstance(value, str):
            raise GecersizOturumTipiHatasi(f"Oturum tipi string olmalıdır, alınan: {type(value).__name__}")
        
        tip_formatted = value.lower().strip()
        if tip_formatted not in self.GECERLI_OTURUM_TIPLERI:
            raise GecersizOturumTipiHatasi(
                f"Oturum tipi {self.GECERLI_OTURUM_TIPLERI} değerlerinden biri olmalıdır, alınan: '{value}'"
            )
        self._oturum_tipi = tip_formatted

    # Tarih ve saati döndürür
    @property
    def tarih_saat(self) -> Optional[datetime]:
        return self._tarih_saat

    # Tarih ve saati doğrulama ile ayarlar
    @tarih_saat.setter
    def tarih_saat(self, value: Any) -> None:
        if value is not None:
            if not isinstance(value, datetime):
                raise GecersizTarihSaatHatasi(f"Tarih ve saat datetime objesi olmalıdır, alınan: {type(value).__name__}")
        self._tarih_saat = value

    # Oturum durumunu döndürür
    @property
    def durum(self) -> str:
        return self._durum

    # Oturum durumunu doğrulama ile ayarlar
    @durum.setter
    def durum(self, value: Any) -> None:
        if not isinstance(value, str):
            raise GecersizOturumDurumuHatasi(f"Durum string olmalıdır, alınan: {type(value).__name__}")
        
        durum_formatted = value.lower().strip()
        if durum_formatted not in self.GECERLI_DURUMLAR:
            raise GecersizOturumDurumuHatasi(
                f"Durum {self.GECERLI_DURUMLAR} değerlerinden biri olmalıdır, alınan: '{value}'"
            )
        self._durum = durum_formatted

    # Antrenman oturumunun detaylı bilgilerini döndürür (abstract method)
    @abstractmethod
    def oturum_detaylari_getir(self) -> Dict[str, Any]:
        pass

    # Antrenman oturumunun maliyetini hesaplar (abstract method)
    @abstractmethod
    def oturum_maliyeti_hesapla(self) -> float:
        pass

    # Antrenman oturumunun temel bilgilerini string olarak döndürür
    def oturum_bilgisi_al(self) -> str:
        bilgi = f"Oturum ID: {self.oturum_id}, Tip: {self.oturum_tipi}, Süre: {self.sure} dakika"
        if self.athlete_id:
            bilgi += f", Sporcu ID: {self.athlete_id}"
        if self.team_id:
            bilgi += f", Takım ID: {self.team_id}"
        if self.tarih_saat:
            bilgi += f", Tarih: {self.tarih_saat.strftime('%Y-%m-%d %H:%M')}"
        bilgi += f", Durum: {self.durum}"
        return bilgi

    # Antrenman oturumunu tamamlandı olarak işaretler
    def oturum_tamamla(self) -> None:
        self.durum = "tamamlandi"

    # Antrenman oturumunu iptal edildi olarak işaretler
    def oturum_iptal_et(self) -> None:
        self.durum = "iptal_edildi"

    # Antrenman oturumunu yeni bir tarih ve saat için planlar
    def oturum_planla(self, yeni_tarih_saat: datetime) -> None:
        if not isinstance(yeni_tarih_saat, datetime):
            raise GecersizTarihSaatHatasi(f"Tarih ve saat datetime objesi olmalıdır, alınan: {type(yeni_tarih_saat).__name__}")
        self.tarih_saat = yeni_tarih_saat
        if self.durum == "iptal_edildi":
            self.durum = "planlandı"

    # Antrenman oturumunun geçmiş bir tarihte olup olmadığını kontrol eder
    def oturum_gecmis_mi(self) -> bool:
        if self.tarih_saat is None:
            return False
        return self.tarih_saat < datetime.now()

    # Geçerli antrenman oturumu tiplerini döndürür
    @classmethod
    def gecerli_oturum_tipleri_getir(cls) -> list[str]:
        return cls.GECERLI_OTURUM_TIPLERI.copy()

    # Geçerli antrenman oturumu durumlarını döndürür
    @classmethod
    def gecerli_durumlar_getir(cls) -> list[str]:
        return cls.GECERLI_DURUMLAR.copy()

    # Verilen oturum tipinin geçerli olup olmadığını kontrol eder
    @classmethod
    def oturum_tipi_gecerli_mi(cls, tip: str) -> bool:
        if not isinstance(tip, str):
            return False
        return tip.lower().strip() in cls.GECERLI_OTURUM_TIPLERI

    # Dakika cinsinden süreyi saat ve dakika cinsine çevirir
    @staticmethod
    def sure_dakikadan_saat_dakikaya(dakika: int) -> tuple[int, int]:
        if not isinstance(dakika, int) or dakika < 0:
            raise ValueError("Dakika pozitif bir tam sayı olmalıdır")
        saat = dakika // 60
        kalan_dakika = dakika % 60
        return (saat, kalan_dakika)

    # İki tarih arasındaki tüm günleri içeren bir liste döndürür
    @staticmethod
    def tarih_araligi_olustur(baslangic: datetime, bitis: datetime) -> list[datetime]:
        if not isinstance(baslangic, datetime) or not isinstance(bitis, datetime):
            raise ValueError("Başlangıç ve bitiş tarihleri datetime objesi olmalıdır")
        if baslangic > bitis:
            raise ValueError("Başlangıç tarihi bitiş tarihinden sonra olamaz")
        
        from datetime import timedelta
        tarihler = []
        mevcut = baslangic.date()
        bitis_tarih = bitis.date()
        
        while mevcut <= bitis_tarih:
            tarihler.append(datetime.combine(mevcut, datetime.min.time()))
            mevcut += timedelta(days=1)
        
        return tarihler

    # İki antrenman oturumunun tarih ve saat açısından çakışıp çakışmadığını kontrol eder
    @staticmethod
    def tarih_cakismasi_kontrol(tarih1: datetime, sure1: int, tarih2: datetime, sure2: int) -> bool:
        if not all(isinstance(x, (datetime, int)) for x in [tarih1, sure1, tarih2, sure2]):
            raise ValueError("Tüm parametreler doğru tipte olmalıdır")
        
        from datetime import timedelta
        bitis1 = tarih1 + timedelta(minutes=sure1)
        bitis2 = tarih2 + timedelta(minutes=sure2)
        
        return not (bitis1 <= tarih2 or bitis2 <= tarih1)