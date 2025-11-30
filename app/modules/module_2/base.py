"""
Antrenman Oturumu varlıkları için soyut temel sınıf.
Tüm antrenman oturumu implementasyonlarının takip etmesi gereken sözleşmeyi tanımlar.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any
from app.modules.module_2.exceptions import (
    GecersizOturumIdHatasi,
    GecersizSporcuIdHatasi,
    GecersizTakimIdHatasi,
    GecersizOturumTipiHatasi,
    GecersizOturumDurumuHatasi,
    GecersizTarihSaatHatasi,
    TakvimCakismasiHatasi,
    OturumDogrulamaHatasi
)


class AntrenmanOturumuTemel(ABC):
    """
    Tüm antrenman oturumu tipleri için soyut temel sınıf.
    Antrenman oturumları için ortak yapı ve doğrulama sağlar.
    """
    
    GECERLI_OTURUM_TIPLERI = ["kondisyon", "teknik", "taktik", "rehabilitasyon"]
    GECERLI_DURUMLAR = ["planlandı", "tamamlandi", "iptal_edildi"]
    MIN_SURE = 1
    MAX_SURE = 480
    
    def __init__(
        self,
        oturum_id: int,
        athlete_id: Optional[int] = None,
        team_id: Optional[int] = None,
        oturum_tipi: str = "kondisyon",
        tarih_saat: Optional[datetime] = None,
        durum: str = "planlandı"
    ):
        """
        Antrenman oturumu temel örneğini başlatır.
        
        Args:
            oturum_id: Antrenman oturumu için benzersiz tanımlayıcı
            athlete_id: Bireysel sporcu için opsiyonel tanımlayıcı
            team_id: Takım için opsiyonel tanımlayıcı
            oturum_tipi: Antrenman oturumu tipi (kondisyon, teknik, taktik, rehabilitasyon)
            tarih_saat: Oturum için planlanan tarih ve saat
            durum: Oturumun mevcut durumu (planlandı, tamamlandi, iptal_edildi)
        """
        self.__oturum_id = None
        self.__athlete_id = None
        self.__team_id = None
        self.__oturum_tipi = None
        self.__tarih_saat = None
        self.__durum = None
        
        self.oturum_id_ayarla(oturum_id)
        if athlete_id is not None:
            self.athlete_id_ayarla(athlete_id)
        if team_id is not None:
            self.team_id_ayarla(team_id)
        self.oturum_tipi_ayarla(oturum_tipi)
        if tarih_saat is not None:
            self.tarih_saat_ayarla(tarih_saat)
        self.durum_ayarla(durum)
    
    def oturum_id_al(self) -> int:
        """Oturum ID'sini alır."""
        return self.__oturum_id
    
    def oturum_id_ayarla(self, oturum_id: Any) -> None:
        """Oturum ID'sini doğrulama ile ayarlar."""
        if not isinstance(oturum_id, int):
            raise GecersizOturumIdHatasi(f"Oturum ID'si tam sayı olmalıdır, alınan: {type(oturum_id).__name__}")
        oturum_id_int: int = oturum_id
        if oturum_id_int <= 0:
            raise GecersizOturumIdHatasi(f"Oturum ID'si pozitif tam sayı olmalıdır, alınan: {oturum_id_int}")
        self.__oturum_id = oturum_id_int
    
    def athlete_id_al(self) -> Optional[int]:
        """Sporcu ID'sini alır."""
        return self.__athlete_id
    
    def athlete_id_ayarla(self, athlete_id: Any) -> None:
        """Sporcu ID'sini doğrulama ile ayarlar."""
        if not isinstance(athlete_id, int):
            raise GecersizSporcuIdHatasi(f"Sporcu ID'si tam sayı olmalıdır, alınan: {type(athlete_id).__name__}")
        athlete_id_int: int = athlete_id
        if athlete_id_int <= 0:
            raise GecersizSporcuIdHatasi(f"Sporcu ID'si pozitif tam sayı olmalıdır, alınan: {athlete_id_int}")
        self.__athlete_id = athlete_id_int
    
    def team_id_al(self) -> Optional[int]:
        """Takım ID'sini alır."""
        return self.__team_id
    
    def team_id_ayarla(self, team_id: Any) -> None:
        """Takım ID'sini doğrulama ile ayarlar."""
        if not isinstance(team_id, int):
            raise GecersizTakimIdHatasi(f"Takım ID'si tam sayı olmalıdır, alınan: {type(team_id).__name__}")
        team_id_int: int = team_id
        if team_id_int <= 0:
            raise GecersizTakimIdHatasi(f"Takım ID'si pozitif tam sayı olmalıdır, alınan: {team_id_int}")
        self.__team_id = team_id_int
    
    def oturum_tipi_al(self) -> str:
        """Oturum tipini alır."""
        return self.__oturum_tipi
    
    def oturum_tipi_ayarla(self, oturum_tipi: Any) -> None:
        """Oturum tipini doğrulama ile ayarlar."""
        if not isinstance(oturum_tipi, str):
            raise GecersizOturumTipiHatasi(f"Oturum tipi string olmalıdır, alınan: {type(oturum_tipi).__name__}")
        oturum_tipi_str: str = oturum_tipi
        oturum_tipi_kucuk = oturum_tipi_str.lower().strip()
        if oturum_tipi_kucuk not in self.GECERLI_OTURUM_TIPLERI:
            raise GecersizOturumTipiHatasi(
                f"Oturum tipi {self.GECERLI_OTURUM_TIPLERI} değerlerinden biri olmalıdır, alınan: '{oturum_tipi_str}'"
            )
        self.__oturum_tipi = oturum_tipi_kucuk
    
    def tarih_saat_al(self) -> Optional[datetime]:
        """Planlanan tarih ve saati alır."""
        return self.__tarih_saat
    
    def tarih_saat_ayarla(self, tarih_saat: Any) -> None:
        """Planlanan tarih ve saati doğrulama ile ayarlar."""
        if not isinstance(tarih_saat, datetime):
            raise GecersizTarihSaatHatasi(
                f"Tarih saat datetime nesnesi olmalıdır, alınan: {type(tarih_saat).__name__}"
            )
        tarih_saat_dt: datetime = tarih_saat
        if tarih_saat_dt < datetime.now():
            raise GecersizTarihSaatHatasi(
                f"Geçmiş tarih için oturum planlanamaz: {tarih_saat_dt.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        self.__tarih_saat = tarih_saat_dt
    
    def durum_al(self) -> str:
        """Oturum durumunu alır."""
        return self.__durum
    
    def durum_ayarla(self, durum: Any) -> None:
        """Oturum durumunu doğrulama ile ayarlar."""
        if not isinstance(durum, str):
            raise GecersizOturumDurumuHatasi(f"Durum string olmalıdır, alınan: {type(durum).__name__}")
        durum_str: str = durum
        durum_kucuk = durum_str.lower().strip()
        if durum_kucuk not in self.GECERLI_DURUMLAR:
            raise GecersizOturumDurumuHatasi(
                f"Durum {self.GECERLI_DURUMLAR} değerlerinden biri olmalıdır, alınan: '{durum_str}'"
            )
        self.__durum = durum_kucuk
    
    @staticmethod
    def tarih_formati_dogrula(tarih_string: str) -> bool:
        """
        Bir tarih string'inin beklenen formata uyup uymadığını doğrular.
        
        Args:
            tarih_string: 'YYYY-MM-DD HH:MM:SS' formatında doğrulanacak string
            
        Returns:
            Format geçerliyse True, aksi halde False
        """
        if not isinstance(tarih_string, str):
            return False
        try:
            datetime.strptime(tarih_string, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
    
    @classmethod
    def bos_sablon_olustur(cls) -> dict:
        """
        Antrenman oturumu verisi için boş şablon sözlüğü oluşturur.
        
        Returns:
            Tüm oturum öznitelikleri için boş/varsayılan değerler içeren sözlük
        """
        return {
            "oturum_id": 0,
            "athlete_id": None,
            "team_id": None,
            "oturum_tipi": "kondisyon",
            "tarih_saat": None,
            "durum": "planlandı"
        }
    
    @abstractmethod
    def oturum_detaylari_al(self) -> dict:
        """
        Antrenman oturumunun kapsamlı detaylarını alır.
        Implementasyon alt sınıflar tarafından sağlanmalıdır.
        
        Returns:
            Tüm oturum detaylarını içeren sözlük
        """
        pass
    
    @abstractmethod
    def oturum_dogrula(self) -> bool:
        """
        Antrenman oturumu verisini doğrular.
        Implementasyon alt sınıflar tarafından sağlanmalıdır.
        
        Returns:
            Oturum geçerliyse True, aksi halde False
            
        Raises:
            OturumDogrulamaHatasi: Doğrulama belirli hata detayları ile başarısız olursa
        """
        pass
