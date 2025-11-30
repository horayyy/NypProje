"""
Antrenman ve Program modülü için özel exception sınıfları.
Tüm exception'lar AntrenmanHatasi temel sınıfından türer.
"""


class AntrenmanHatasi(Exception):
    """Tüm antrenman ve program ile ilgili hatalar için temel exception sınıfı."""
    
    def __init__(self, mesaj: str = "Bir antrenman hatası oluştu"):
        self.mesaj = mesaj
        super().__init__(self.mesaj)


class OturumBulunamadiHatasi(AntrenmanHatasi):
    """Sistemde bulunmayan bir antrenman oturumuna erişmeye veya değiştirmeye çalışıldığında fırlatılır."""
    
    def __init__(self, mesaj: str = "Antrenman oturumu sistemde bulunamadı"):
        super().__init__(mesaj)


class GecersizOturumIdHatasi(AntrenmanHatasi):
    """Antrenman oturumu ID'si geçersiz, eksik veya negatif olduğunda fırlatılır."""
    
    def __init__(self, mesaj: str = "Antrenman oturumu ID'si geçerli pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)


class GecersizSporcuIdHatasi(AntrenmanHatasi):
    """Sporcu ID'si geçersiz, eksik veya sistemde bulunmadığında fırlatılır."""
    
    def __init__(self, mesaj: str = "Sporcu ID'si geçerli pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)


class GecersizTakimIdHatasi(AntrenmanHatasi):
    """Takım ID'si geçersiz, eksik veya sistemde bulunmadığında fırlatılır."""
    
    def __init__(self, mesaj: str = "Takım ID'si geçerli pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)


class GecersizOturumTipiHatasi(AntrenmanHatasi):
    """Antrenman oturumu tipi tanınmadığında veya geçersiz olduğunda fırlatılır."""
    
    def __init__(self, mesaj: str = "Antrenman oturumu tipi şunlardan biri olmalıdır: kondisyon, teknik, taktik, rehabilitasyon"):
        super().__init__(mesaj)


class GecersizOturumDurumuHatasi(AntrenmanHatasi):
    """Antrenman oturumu durumu geçerli bir durum değeri olmadığında fırlatılır."""
    
    def __init__(self, mesaj: str = "Oturum durumu şunlardan biri olmalıdır: planlandı, tamamlandi, iptal_edildi"):
        super().__init__(mesaj)


class GecersizTarihSaatHatasi(AntrenmanHatasi):
    """Tarih ve saat formatı geçersiz olduğunda veya geçmiş bir tarih için oturum planlanmaya çalışıldığında fırlatılır."""
    
    def __init__(self, mesaj: str = "Tarih ve saat geçerli formatta olmalıdır ve geçmiş bir tarih olamaz"):
        super().__init__(mesaj)


class TakvimCakismasiHatasi(AntrenmanHatasi):
    """Bir antrenman oturumu mevcut planlanmış bir oturum ile çakıştığında fırlatılır."""
    
    def __init__(self, mesaj: str = "Antrenman oturumu mevcut planlanmış bir oturum ile çakışıyor"):
        super().__init__(mesaj)


class OturumDogrulamaHatasi(AntrenmanHatasi):
    """Antrenman oturumu doğrulaması birden fazla veya kritik doğrulama hatası nedeniyle başarısız olduğunda fırlatılır."""
    
    def __init__(self, mesaj: str = "Antrenman oturumu doğrulaması başarısız: bir veya daha fazla zorunlu alan geçersiz"):
        super().__init__(mesaj)


class DuplicateOturumHatasi(AntrenmanHatasi):
    """Aynı ID'ye sahip bir antrenman oturumu zaten sistemde mevcut olduğunda fırlatılır."""
    
    def __init__(self, mesaj: str = "Bu ID'ye sahip bir antrenman oturumu zaten sistemde mevcut"):
        super().__init__(mesaj)


class GecersizSahaIdHatasi(AntrenmanHatasi):
    """Saha ID'si geçersiz, eksik veya sistemde bulunmadığında fırlatılır."""
    
    def __init__(self, mesaj: str = "Saha ID'si geçerli pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)


class SahaDoluHatasi(AntrenmanHatasi):
    """Seçilen saha belirtilen tarih ve saatte zaten dolu olduğunda fırlatılır."""
    
    def __init__(self, mesaj: str = "Seçilen saha belirtilen tarih ve saatte zaten dolu"):
        super().__init__(mesaj)


class GecersizSureHatasi(AntrenmanHatasi):
    """Antrenman oturumu süresi geçersiz olduğunda (negatif, sıfır veya maksimum değeri aştığında) fırlatılır."""
    
    def __init__(self, mesaj: str = "Antrenman oturumu süresi 1 ile 480 dakika arasında pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)

