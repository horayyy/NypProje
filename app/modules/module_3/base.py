from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

# Projeye özgü temel hata sınıfı - turnuva işlemlerinde hata yönetimi
class TurnuvaHatasi(Exception):
    pass

# Spor tipi enum'ı - desteklenen spor dallarını tanımlar
class SporTipi(Enum):
    FUTBOL = "futbol"
    VOLEYBOL = "voleybol"
    BASKETBOL = "basketbol"

# Maç tipi enum'ı - maç organizasyon tiplerini tanımlar
class MacTipi(Enum):
    FRIENDLY = "friendly"
    LEAGUE = "league"
    CUP = "cup"
    TOURNAMENT = "tournament"

# Puan kuralları sınıfı - spor tipine göre puan hesaplama kurallarını yönetir
class PuanKurallari:
    """Her spor tipi için puan kurallarını yönetir."""
    
    # Puan kuralları objesi oluşturur - dinamik puan değerleri ile
    def __init__(self, futbol_galibiyet=3, futbol_beraberlik=1, futbol_maglubiyet=0, voleybol_galibiyet=3, voleybol_maglubiyet=0):
        """
        Puan kuralları oluşturur.
        
        Args:
            futbol_galibiyet: Futbol galibiyet puanı (varsayılan: 3)
            futbol_beraberlik: Futbol beraberlik puanı (varsayılan: 1)
            futbol_maglubiyet: Futbol mağlubiyet puanı (varsayılan: 0)
            voleybol_galibiyet: Voleybol/Basketbol galibiyet puanı (varsayılan: 3)
            voleybol_maglubiyet: Voleybol/Basketbol mağlubiyet puanı (varsayılan: 0)
        """
        self._futbol_galibiyet = futbol_galibiyet
        self._futbol_beraberlik = futbol_beraberlik
        self._futbol_maglubiyet = futbol_maglubiyet
        self._voleybol_galibiyet = voleybol_galibiyet
        self._voleybol_maglubiyet = voleybol_maglubiyet
    
    # Spor tipine göre puan değerini hesaplar
    def puan_al(self, spor_tipi, sonuc):
        """
        Spor tipine göre puan döndürür.
        
        Args:
            spor_tipi: SporTipi enum değeri
            sonuc: "galibiyet", "beraberlik", "maglubiyet"
        
        Returns:
            int: Puan değeri
        """
        if spor_tipi == SporTipi.FUTBOL:
            if sonuc == "galibiyet":
                return self._futbol_galibiyet
            elif sonuc == "beraberlik":
                return self._futbol_beraberlik
            elif sonuc == "maglubiyet":
                return self._futbol_maglubiyet
        elif spor_tipi in [SporTipi.VOLEYBOL, SporTipi.BASKETBOL]:
            if sonuc == "galibiyet":
                return self._voleybol_galibiyet
            elif sonuc == "maglubiyet":
                return self._voleybol_maglubiyet
        
        return 0
    
    # Statik metod ile varsayılan kurallarla puan hesaplar
    @staticmethod
    def puan_al_static(spor_tipi, sonuc):
        """
        Statik metod - varsayılan puan kuralları ile çalışır (geriye dönük uyumluluk için).
        
        Args:
            spor_tipi: SporTipi enum değeri
            sonuc: "galibiyet", "beraberlik", "maglubiyet"
        
        Returns:
            int: Puan değeri
        """
        varsayilan_kurallar = PuanKurallari()
        return varsayilan_kurallar.puan_al(spor_tipi, sonuc)
    
    # Class metod ile varsayılan puan kuralları objesi oluşturur
    @classmethod
    def varsayilan_kurallar_olustur(cls):
        """
        Varsayılan puan kuralları ile yeni bir PuanKurallari instance'ı oluşturur (class method).
        
        Returns:
            PuanKurallari: Varsayılan kurallarla oluşturulmuş instance
        """
        return cls()
    
    # Statik metod ile spor tipine göre beraberlik geçerliliğini kontrol eder
    @staticmethod
    def beraberlik_gecerli_mi(spor_tipi):
        """
        Spor tipine göre beraberliğin geçerli olup olmadığını kontrol eder.
        
        Args:
            spor_tipi: SporTipi enum değeri
        
        Returns:
            bool: True ise beraberlik geçerli, False ise geçersiz
        """
        return spor_tipi == SporTipi.FUTBOL

# Maç ve Turnuva yönetimi için soyut temel sınıf - tüm maç tiplerinin ortak özelliklerini tanımlar
class MacBase(ABC):

    # Maç objesi oluşturur - tüm maç tipleri için ortak başlatma
    def __init__(self, mac_id, ev_sahibi, deplasman, tarih_saat, mac_tipi=None, gecerli_durumlar=None, konum=None, hakem=None):
        """
        Maç base sınıfı oluşturur.
        
        Args:
            mac_id: Maç ID'si
            ev_sahibi: Ev sahibi takım adı
            deplasman: Deplasman takım adı
            tarih_saat: Maç tarihi ve saati
            mac_tipi: Maç tipi (MacTipi enum)
            gecerli_durumlar: Geçerli durumlar listesi (varsayılan: ['planlandi', 'devam_ediyor', 'tamamlandi', 'iptal_edildi', 'ertelendi'])
            konum: Maç konumu (varsayılan: "Ana Stadyum")
            hakem: Hakem adı (varsayılan: "Atanmadi")
        """
        self.mac_id = mac_id          # ID en başta atanır
        self.ev_sahibi = ev_sahibi
        self.deplasman = deplasman
        self.tarih_saat = tarih_saat
        
        # Dinamik değerler
        if gecerli_durumlar is None:
            gecerli_durumlar = ['planlandi', 'devam_ediyor', 'tamamlandi', 'iptal_edildi', 'ertelendi']
        self._gecerli_durumlar = gecerli_durumlar
        
        self._durum = "planlandi"
        self._skor_ev = 0
        self._skor_dep = 0
        self._skor_girildi_mi = False
        self._konum = konum if konum is not None else "Ana Stadyum"
        self._hakem = hakem if hakem is not None else "Atanmadi"
        self._mac_tipi = mac_tipi  # friendly, league, cup, tournament

    # Maç ID'sini döndüren property - kapsüllenmiş erişim
    @property 
    def mac_id(self):
        return self._mac_id
    
    # Maç ID'sini ayarlayan setter - validasyon ile
    @mac_id.setter
    def mac_id(self, value):
        if not MacBase.id_format_kontrol(value):
            raise TurnuvaHatasi("Geçersiz ID Formatı. Pozitif tam sayı bekleniyor.")
        self._mac_id = value

    # Ev sahibi takım adını döndüren property
    @property
    def ev_sahibi(self):
        return self._ev_sahibi
    
    # Ev sahibi takım adını ayarlayan setter - validasyon ile
    @ev_sahibi.setter
    def ev_sahibi(self, value):
        if not isinstance(value, str):
            raise TypeError("Ev sahibi takımı geçerli bir string olarak giriniz.")
        if len(value) < 3:
            raise TurnuvaHatasi("Ev sahibi takım adı en az 3 karakter olmalıdır.")
        self._ev_sahibi = value

    # Deplasman takım adını döndüren property
    @property
    def deplasman(self):
        return self._deplasman

    # Deplasman takım adını ayarlayan setter - validasyon ile
    @deplasman.setter
    def deplasman(self, value):
        # Henüz ev sahibi atanmadıysa hata vermemesi için kontrol
        if hasattr(self, '_ev_sahibi') and value == self._ev_sahibi:
            raise TurnuvaHatasi("Ev sahibi ve deplasman takımları aynı olamaz.")
        self._deplasman = value
    
    # Maç tarih ve saatini döndüren property
    @property
    def tarih_saat(self):
        return self._tarih_saat
    
    # Maç tarih ve saatini ayarlayan setter - validasyon ile
    @tarih_saat.setter
    def tarih_saat(self, value):
        if not isinstance(value, datetime):
            raise TypeError("Tarih objesi datetime tipinde olmalı.")
        self._tarih_saat = value

    # Maç durumunu döndüren property
    @property
    def durum(self):
        return self._durum
    
    # Maç durumunu ayarlayan setter - geçerli durum kontrolü ile
    @durum.setter
    def durum(self, value):
        if value not in self._gecerli_durumlar:
            gecerli_str = ", ".join(self._gecerli_durumlar)
            raise TurnuvaHatasi(f"Geçersiz durum bilgisi. Beklenenler: {gecerli_str}")
        self._durum = value

    # Maç konumunu döndüren property
    @property
    def konum(self):
        return self._konum

    # Maç konumunu ayarlayan setter - validasyon ile
    @konum.setter
    def konum(self, value):
        if len(value) < 3:
            raise TurnuvaHatasi("Lokasyon bilgisi yetersiz.")
        self._konum = value 

    # Hakem adını döndüren property
    @property
    def hakem(self):    
        return self._hakem

    # Hakem adını ayarlayan setter - validasyon ile
    @hakem.setter
    def hakem(self, value):
        if any(karakter.isdigit() for karakter in value):
            raise TurnuvaHatasi("Hakem isminde sayi olamaz.")
        self._hakem = value
    
    # Maç tipini döndüren property
    @property
    def mac_tipi(self):
        """Maç tipini döndürür (friendly, league, cup, tournament)."""
        return self._mac_tipi
    
    # Maç tipini ayarlayan setter - validasyon ile
    @mac_tipi.setter
    def mac_tipi(self, value):
        if value is not None and not isinstance(value, MacTipi):
            raise TypeError("Maç tipi MacTipi enum değeri olmalıdır.")
        self._mac_tipi = value

    # --- İŞTE EKSİK OLAN KISIM (SKOR PROPERTY) ---
    # Skor bilgisini string formatında döndüren property
    @property
    def skor(self):
        """Skor bilgisini '2-1' formatında string olarak döner."""
        return str(self._skor_ev) + "-" + str(self._skor_dep)
    
    # Ev sahibi takım skorunu döndüren property
    @property
    def skor_ev(self):
        """Ev sahibi takımın skorunu döndürür."""
        return self._skor_ev
    
    # Deplasman takım skorunu döndüren property
    @property
    def skor_deplasman(self):
        """Deplasman takımın skorunu döndürür."""
        return self._skor_dep
    
    # Skor girilme durumunu döndüren property
    @property
    def skor_girildi_mi(self):
        """Skorun girilip girilmediğini kontrol eder."""
        return self._skor_girildi_mi

    # Skor değerlerini belirleyen metot - validasyon ile
    def skor_belirle(self, skor_ev, skor_deplasman):
        if not isinstance(skor_ev, int) or not isinstance(skor_deplasman, int):
            raise TypeError("Skorlar tam sayı olmalıdır.")
        if skor_ev < 0 or skor_deplasman < 0:
            raise TurnuvaHatasi("Skorlar negatif olamaz.")
        
        self._skor_ev = skor_ev
        self._skor_dep = skor_deplasman # Değişken adı düzeltildi (_skor_dep)
        self._skor_girildi_mi = True

    # Abstract metot - maç sonucunu hesaplar (polymorphism için)
    @abstractmethod
    def mac_sonucu(self):
        pass

    # Abstract metot - maç detaylarını döndürür (polymorphism için)
    @abstractmethod
    def mac_detay_getir(self):
        pass

    # Statik metot - ID formatını kontrol eder
    @staticmethod
    def id_format_kontrol(id_value):
        """
        ID formatını kontrol eder (static method).
        
        Args:
            id_value: Kontrol edilecek ID değeri
        
        Returns:
            bool: True ise geçerli format, False ise geçersiz
        """
        if isinstance(id_value, int) and id_value > 0:
            return True
        return False
    
    # Class metot - geçerli maç durumlarını döndürür
    @classmethod
    def gecerli_durumlar_getir(cls):
        """
        Geçerli maç durumlarını döndürür (class method).
        
        Returns:
            list: Geçerli durumlar listesi
        """
        return ['planlandi', 'devam_ediyor', 'tamamlandi', 'iptal_edildi', 'ertelendi']
    
    # Class metot - durum geçerliliğini kontrol eder
    @classmethod
    def durum_gecerli_mi(cls, durum: str):
        """
        Bir durumun geçerli olup olmadığını kontrol eder (class method).
        
        Args:
            durum: Kontrol edilecek durum
        
        Returns:
            bool: True ise geçerli, False ise geçersiz
        """
        return durum in cls.gecerli_durumlar_getir()