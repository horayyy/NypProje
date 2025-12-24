"""
Antrenman ve Program modülü için özel exception sınıfları.
Tüm exception'lar AntrenmanHatasi temel sınıfından türer.
"""


# Tüm antrenman ve program ile ilgili hatalar için temel exception sınıfı
class AntrenmanHatasi(Exception):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Bir antrenman hatası oluştu"):
        self.mesaj = mesaj
        super().__init__(self.mesaj)


# Sistemde bulunmayan bir antrenman oturumuna erişmeye çalışıldığında fırlatılan exception
class OturumBulunamadiHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Antrenman oturumu sistemde bulunamadı"):
        super().__init__(mesaj)


# Antrenman oturumu ID'si geçersiz olduğunda fırlatılan exception
class GecersizOturumIdHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Antrenman oturumu ID'si geçerli pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)


# Sporcu ID'si geçersiz olduğunda fırlatılan exception
class GecersizSporcuIdHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Sporcu ID'si geçerli pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)


# Takım ID'si geçersiz olduğunda fırlatılan exception
class GecersizTakimIdHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Takım ID'si geçerli pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)


# Antrenman oturumu tipi geçersiz olduğunda fırlatılan exception
class GecersizOturumTipiHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Antrenman oturumu tipi şunlardan biri olmalıdır: kondisyon, teknik, taktik, rehabilitasyon"):
        super().__init__(mesaj)


# Antrenman oturumu durumu geçersiz olduğunda fırlatılan exception
class GecersizOturumDurumuHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Oturum durumu şunlardan biri olmalıdır: planlandı, tamamlandi, iptal_edildi"):
        super().__init__(mesaj)


# Tarih ve saat formatı geçersiz olduğunda fırlatılan exception
class GecersizTarihSaatHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Tarih ve saat geçerli formatta olmalıdır ve geçmiş bir tarih olamaz"):
        super().__init__(mesaj)


# Antrenman oturumu çakışması olduğunda fırlatılan exception
class TakvimCakismasiHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Antrenman oturumu mevcut planlanmış bir oturum ile çakışıyor"):
        super().__init__(mesaj)


# Antrenman oturumu doğrulaması başarısız olduğunda fırlatılan exception
class OturumDogrulamaHatasi(AntrenmanHatasi):

    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Antrenman oturumu doğrulaması başarısız: bir veya daha fazla zorunlu alan geçersiz"):
        super().__init__(mesaj)


# Aynı ID'ye sahip antrenman oturumu mevcut olduğunda fırlatılan exception
class DuplicateOturumHatasi(AntrenmanHatasi):

    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Bu ID'ye sahip bir antrenman oturumu zaten sistemde mevcut"):
        super().__init__(mesaj)


# Saha ID'si geçersiz olduğunda fırlatılan exception
class GecersizSahaIdHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Saha ID'si geçerli pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)


# Saha belirtilen tarih ve saatte dolu olduğunda fırlatılan exception
class SahaDoluHatasi(AntrenmanHatasi):
    
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Seçilen saha belirtilen tarih ve saatte zaten dolu"):
        super().__init__(mesaj)


# Antrenman oturumu süresi geçersiz olduğunda fırlatılan exception
class GecersizSureHatasi(AntrenmanHatasi):
        
    # Exception örneğini başlatır
    def __init__(self, mesaj: str = "Antrenman oturumu süresi 1 ile 480 dakika arasında pozitif bir tam sayı olmalıdır"):
        super().__init__(mesaj)

