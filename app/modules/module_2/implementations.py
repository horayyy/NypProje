"""
Antrenman ve Program modülü için implementasyon sınıfları.
Subclass'lar, entity/model sınıfları ve service katmanı burada yer alır.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.modules.module_2.base import AntrenmanOturumuTemel
from app.modules.module_2.exceptions import (
    GecersizSporcuIdHatasi,
    GecersizTarihSaatHatasi,
    AntrenmanHatasi
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
        
        Args:
            oturum_id: Antrenman oturumu için benzersiz tanımlayıcı
            sure: Antrenman süresi (dakika)
            athlete_id: Sporcu ID'si (zorunlu)
            antrenor_id: Antrenör ID'si
            odak_alani: Antrenmanın odaklandığı alan (hız, güç, dayanıklılık, esneklik, koordinasyon)
            oturum_tipi: Antrenman oturumu tipi
            tarih_saat: Oturum için planlanan tarih ve saat
            durum: Oturumun mevcut durumu
            performans_notu: Sporcu performans notu (0-10 arası, opsiyonel)
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
        """
        Bireysel antrenman oturumunun detaylı bilgilerini döndürür.
        Abstract metot implementasyonu.
        """
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
        """
        Bireysel antrenman oturumunun maliyetini hesaplar.
        Abstract metot implementasyonu.
        Bireysel antrenmanlar için saatlik antrenör ücreti × süre (saat) hesaplanır.
        """
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
        """
        Yeni bir bireysel antrenman oturumu oluşturur.
        Class metodu ile kolay oluşturma sağlar.
        """
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
        """
        İki performans notunu karşılaştırır.
        Returns: -1 (not1 < not2), 0 (not1 == not2), 1 (not1 > not2)
        """
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
