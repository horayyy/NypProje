from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
from .base import TurnuvaHatasi, SporTipi, PuanKurallari, MacBase
from .implementations import LigMaci, HazirlikMaci, ElemeMaci

# ============================================================================
# LİG YÖNETİMİ SINIFI
# ============================================================================

# Lig yönetimi sınıfı - lig oluşturma, takım yönetimi ve fikstür oluşturma işlemleri
class LigYonetimi:
    """Lig oluşturma, takım yönetimi ve fikstür oluşturma sınıfı."""
    
    # Lig yönetimi objesi oluşturur - lig adı, spor tipi ve sezon bilgileri ile
    def __init__(self, lig_adi: str, spor_tipi: SporTipi, sezon_baslangic: datetime):
        """
        Lig oluşturur.
        
        Args:
            lig_adi: Lig adı (minimum 3 karakter)
            spor_tipi: SporTipi enum değeri
            sezon_baslangic: Sezon başlangıç tarihi
        """
        if not isinstance(lig_adi, str) or len(lig_adi) < 3:
            raise TurnuvaHatasi("Lig adı en az 3 karakter olmalıdır.")
        if not isinstance(spor_tipi, SporTipi):
            raise TypeError("Spor tipi SporTipi enum değeri olmalıdır.")
        if not isinstance(sezon_baslangic, datetime):
            raise TypeError("Sezon başlangıç tarihi datetime objesi olmalıdır.")
        
        self._lig_adi = lig_adi
        self._spor_tipi = spor_tipi
        self._sezon_baslangic = sezon_baslangic
        self._takimlar = []
        self._fikstur = None
        self._maclar = []  # LigMaci objelerini saklar
    
    @property
    def lig_adi(self):
        return self._lig_adi
    
    @property
    def spor_tipi(self):
        return self._spor_tipi
    
    @property
    def sezon_baslangic(self):
        return self._sezon_baslangic
    
    # Lige takım ekleme metodu - validasyon ve benzersizlik kontrolü ile
    def takim_ekle(self, takim_adi: str):
        """
        Lige takım ekler.
        
        Args:
            takim_adi: Takım adı (minimum 3 karakter, benzersiz olmalı)
        """
        if not isinstance(takim_adi, str) or len(takim_adi) < 3:
            raise TurnuvaHatasi("Takım adı en az 3 karakter olmalıdır.")
        if takim_adi in self._takimlar:
            raise TurnuvaHatasi(f"'{takim_adi}' takımı zaten ligde mevcut.")
        
        self._takimlar.append(takim_adi)
    
    # Ligden takım çıkarma metodu - fikstür sıfırlama ile
    def takim_cikar(self, takim_adi: str):
        """
        Ligden takım çıkarır.
        
        Args:
            takim_adi: Çıkarılacak takım adı
        """
        if takim_adi not in self._takimlar:
            raise TurnuvaHatasi(f"'{takim_adi}' takımı ligde bulunamadı.")
        
        self._takimlar.remove(takim_adi)
        # Fikstür varsa sıfırla
        if self._fikstur:
            self._fikstur = None
            self._maclar = []
    
    # Takım listesini döndüren metot - kopya döndürür
    def takim_listesi_getir(self) -> List[str]:
        """Tüm takımları listeler."""
        return self._takimlar.copy()
    
    # Lig bilgilerini döndüren metot - detaylı bilgi dictionary'si
    def lig_bilgisi_getir(self) -> Dict:
        """Lig detaylarını döndürür."""
        return {
            "lig_adi": self._lig_adi,
            "spor_tipi": self._spor_tipi.value,
            "sezon_baslangic": self._sezon_baslangic.strftime("%Y-%m-%d"),
            "takim_sayisi": len(self._takimlar),
            "takimlar": self._takimlar.copy()
        }
    
    # Fikstür oluşturma metodu - double round-robin algoritması ile
    def fikstur_olustur(self) -> 'FiksturOlusturucu':
        """
        Fikstür oluşturur.
        
        Returns:
            FiksturOlusturucu: Oluşturulan fikstür objesi
        """
        if len(self._takimlar) < 2:
            raise TurnuvaHatasi("Fikstür oluşturmak için en az 2 takım gereklidir.")
        
        self._fikstur = FiksturOlusturucu(self._takimlar, self._sezon_baslangic, self._spor_tipi)
        return self._fikstur
    
    # Belirli haftanın maçlarını getiren metot
    def haftalik_maclar_getir(self, hafta_no: int) -> List[LigMaci]:
        """
        Belirli haftanın maçlarını getirir.
        
        Args:
            hafta_no: Hafta numarası
        
        Returns:
            List[LigMaci]: O haftanın maçları
        """
        if not self._fikstur:
            raise TurnuvaHatasi("Önce fikstür oluşturulmalıdır.")
        
        return self._fikstur.hafta_maclarini_getir(hafta_no, self._lig_adi)
    
    # Takımın tüm maç geçmişini getiren metot - tarih sıralı
    def takim_mac_gecmisi_getir(self, takim_adi: str) -> List[LigMaci]:
        """
        Belirli takımın tüm maç geçmişini getirir.
        
        Args:
            takim_adi: Takım adı
        
        Returns:
            List[LigMaci]: Takımın oynadığı tüm maçlar (tarih sırasına göre)
        """
        if not self._fikstur:
            raise TurnuvaHatasi("Önce fikstür oluşturulmalıdır.")
        
        if takim_adi not in self._takimlar:
            raise TurnuvaHatasi(f"'{takim_adi}' takımı ligde bulunamadı.")
        
        takim_maclari = []
        toplam_hafta = self._fikstur.toplam_hafta_sayisi()
        
        # Tüm haftalardaki maçları kontrol et
        for hafta_no in range(1, toplam_hafta + 1):
            hafta_maclari = self._fikstur.hafta_maclarini_getir(hafta_no, self._lig_adi)
            
            # Takımın oynadığı maçları bul
            for mac in hafta_maclari:
                if mac.ev_sahibi == takim_adi or mac.deplasman == takim_adi:
                    takim_maclari.append(mac)
        
        # Tarih sırasına göre sırala
        takim_maclari.sort(key=lambda m: m.tarih_saat)
        
        return takim_maclari
    
    @staticmethod
    def takim_adi_gecerli_mi(takim_adi: str):
        """
        Takım adı formatını kontrol eder (static method).
        
        Args:
            takim_adi: Kontrol edilecek takım adı
        
        Returns:
            bool: True ise geçerli format, False ise geçersiz
        """
        return isinstance(takim_adi, str) and len(takim_adi) >= 3
    
    @classmethod
    def lig_olustur(cls, lig_adi: str, spor_tipi: SporTipi, sezon_baslangic: datetime):
        """
        Yeni bir lig oluşturur (class method - factory pattern).
        
        Args:
            lig_adi: Lig adı
            spor_tipi: Spor tipi
            sezon_baslangic: Sezon başlangıç tarihi
        
        Returns:
            LigYonetimi: Yeni oluşturulmuş lig yönetimi objesi
        """
        return cls(lig_adi, spor_tipi, sezon_baslangic)


# ============================================================================
# FİKSTÜR OLUŞTURUCU SINIFI
# ============================================================================

# Fikstür oluşturucu sınıfı - double round-robin algoritması ile fikstür oluşturur
class FiksturOlusturucu:
    """Double round-robin algoritması ile fikstür oluşturur."""
    
    # Fikstür oluşturucu objesi oluşturur - takım listesi, tarih ve spor tipi ile
    def __init__(self, takim_listesi: List[str], baslangic_tarihi: datetime, spor_tipi: SporTipi, 
                 mac_gunleri_offset: Optional[List[int]] = None, mac_saatleri: Optional[List[int]] = None):
        """
        Fikstür oluşturucu başlatır.
        
        Args:
            takim_listesi: Takım listesi
            baslangic_tarihi: İlk maçın tarihi (hafta başlangıç - genellikle Pazar)
            spor_tipi: Spor tipi
            mac_gunleri_offset: Maç günleri offset listesi (Cuma: -2, Cumartesi: -1, Pazar: 0) (varsayılan: [-2, -1, 0])
            mac_saatleri: Maç saatleri listesi (varsayılan: [13, 15, 17, 19, 21])
        """
        self._takim_listesi = takim_listesi.copy()
        self._baslangic_tarihi = baslangic_tarihi
        self._spor_tipi = spor_tipi
        self._mac_gunleri_offset = mac_gunleri_offset if mac_gunleri_offset is not None else [-2, -1, 0]
        self._mac_saatleri = mac_saatleri if mac_saatleri is not None else [13, 15, 17, 19, 21]
        self._haftalar = {}  # hafta_no -> [(ev_sahibi, deplasman, tarih_saat), ...]
        
        self._fikstur_olustur()
    
    # Private metot - double round-robin algoritması ile fikstür oluşturur
    def _fikstur_olustur(self):
        """Double round-robin algoritması ile fikstür oluşturur (Süper Lig mantığı)."""
        takim_sayisi = len(self._takim_listesi)
        
        if takim_sayisi < 2:
            return
        
        # Tek sayıda takım varsa, "BYE" ekle (maç yapmayan takım)
        if takim_sayisi % 2 == 1:
            takimler = self._takim_listesi + ["BYE"]
        else:
            takimler = self._takim_listesi.copy()
        
        # Her hafta kaç maç olacak (Süper Lig mantığı)
        mac_sayisi_her_hafta = len(takimler) // 2
        
        # İlk yarı hafta sayısı (her takım bir kez ev sahibi)
        ilk_yarı_hafta_sayisi = len(takimler) - 1
        hafta_sayisi = 2 * ilk_yarı_hafta_sayisi
        
        # Sezon başlangıç tarihini en yakın Pazar gününe çevir (offset hesaplaması için)
        # weekday() 0=Pazartesi, 6=Pazar döner
        # Eğer bugün Pazar ise (weekday=6), gun_farki=0
        # Eğer bugün Pazar değilse, bir sonraki Pazar'a git
        bugun_gun = self._baslangic_tarihi.weekday()  # 0=Pazartesi, 6=Pazar
        if bugun_gun == 6:  # Bugün Pazar
            hafta_baslangic_tarihi = self._baslangic_tarihi
        else:  # Bir sonraki Pazar'a git
            gun_farki = (6 - bugun_gun) % 7
            if gun_farki == 0:
                gun_farki = 7
            hafta_baslangic_tarihi = self._baslangic_tarihi + timedelta(days=gun_farki)
        
        # İlk yarı (her takım bir kez ev sahibi, bir kez deplasman)
        for hafta in range(1, ilk_yarı_hafta_sayisi + 1):
            maclar = []
            # Her hafta eşit sayıda maç oluştur (Süper Lig mantığı)
            for i in range(mac_sayisi_her_hafta):
                ev_sahibi = takimler[i]
                deplasman = takimler[len(takimler) - 1 - i]
                
                # BYE takımı maç yapmaz - bu maçı atla
                if ev_sahibi != "BYE" and deplasman != "BYE":
                    maclar.append((ev_sahibi, deplasman))
            
            # Maçları günlere ve saatlere dağıt
            maclar_tarihli = self._maclari_gunlere_dagit(maclar, hafta_baslangic_tarihi)
            self._haftalar[hafta] = maclar_tarihli
            hafta_baslangic_tarihi += timedelta(days=7)
            
            # Takımları döndür (round-robin) - ilk takım sabit, diğerleri döner
            takimler = [takimler[0]] + [takimler[-1]] + takimler[1:-1]
        
        # İkinci yarı (ev sahibi/deplasman rollerini değiştir)
        for hafta in range(ilk_yarı_hafta_sayisi + 1, hafta_sayisi + 1):
            ilk_yarı_hafta = hafta - ilk_yarı_hafta_sayisi
            maclar = []
            
            # İlk yarıdaki maçların rollerini değiştir
            for ev_sahibi, deplasman, _ in self._haftalar[ilk_yarı_hafta]:
                # Rolleri değiştir (ev sahibi <-> deplasman)
                maclar.append((deplasman, ev_sahibi))
            
            # Maçları günlere ve saatlere dağıt
            maclar_tarihli = self._maclari_gunlere_dagit(maclar, hafta_baslangic_tarihi)
            self._haftalar[hafta] = maclar_tarihli
            hafta_baslangic_tarihi += timedelta(days=7)
    
    # Private metot - maçları günlere ve saatlere dağıtır
    def _maclari_gunlere_dagit(self, maclar: List[Tuple[str, str]], hafta_baslangic: datetime) -> List[Tuple[str, str, datetime]]:
        """
        Maçları Cuma, Cumartesi, Pazar günlerine ve saatlere dağıtır.
        
        Args:
            maclar: (ev_sahibi, deplasman) tuple listesi
            hafta_baslangic: Hafta başlangıç tarihi (Pazar)
        
        Returns:
            (ev_sahibi, deplasman, tarih_saat) tuple listesi
        """
        if not maclar:
            return []
        
        maclar_tarihli = []
        mac_index = 0
        gun_index = 0
        saat_index = 0
        
        while mac_index < len(maclar):
            ev_sahibi, deplasman = maclar[mac_index]
            
            # Gün offset'i hesapla (Cuma: -2, Cumartesi: -1, Pazar: 0)
            gun_offset = self._mac_gunleri_offset[gun_index % len(self._mac_gunleri_offset)]
            mac_gunu = hafta_baslangic + timedelta(days=gun_offset)
            
            # Saat bilgisini al
            saat = self._mac_saatleri[saat_index % len(self._mac_saatleri)]
            mac_saati = mac_gunu.replace(hour=saat, minute=0, second=0, microsecond=0)
            
            maclar_tarihli.append((ev_sahibi, deplasman, mac_saati))
            
            mac_index += 1
            saat_index += 1
            
            # Eğer saatler bitti, bir sonraki güne geç
            if saat_index % len(self._mac_saatleri) == 0:
                gun_index += 1
        
        return maclar_tarihli
    
    # Belirli haftanın maçlarını LigMaci objeleri olarak döndüren metot
    def hafta_maclarini_getir(self, hafta_no: int, lig_adi: str) -> List[LigMaci]:
        """
        Belirli haftanın maçlarını LigMaci objeleri olarak döndürür.
        
        Args:
            hafta_no: Hafta numarası
            lig_adi: Lig adı
        
        Returns:
            List[LigMaci]: O haftanın maçları
        """
        if hafta_no not in self._haftalar:
            raise TurnuvaHatasi(f"Hafta {hafta_no} bulunamadı.")
        
        maclar = []
        mac_id = hafta_no * 100 + 1  # Her hafta için benzersiz ID (1001, 1002, 2001, 2002...)
        
        for ev_sahibi, deplasman, tarih in self._haftalar[hafta_no]:
            mac = LigMaci(
                mac_id=mac_id,
                ev_sahibi=ev_sahibi,
                deplasman=deplasman,
                tarih_saat=tarih,
                lig_adi=lig_adi,
                hafta_no=hafta_no,
                spor_tipi=self._spor_tipi
            )
            maclar.append(mac)
            mac_id += 1
        
        return maclar
    
    # Toplam hafta sayısını döndüren metot
    def toplam_hafta_sayisi(self) -> int:
        """Toplam hafta sayısını döndürür."""
        return len(self._haftalar)
    
    @staticmethod
    def takim_sayisi_yeterli_mi(takim_listesi: List[str]):
        """
        Fikstür oluşturmak için takım sayısının yeterli olup olmadığını kontrol eder (static method).
        
        Args:
            takim_listesi: Takım listesi
        
        Returns:
            bool: True ise yeterli (en az 2 takım), False ise yetersiz
        """
        return len(takim_listesi) >= 2
    
    @classmethod
    def fikstur_olusturucu_olustur(cls, takim_listesi: List[str], baslangic_tarihi: datetime, spor_tipi: SporTipi, 
                                   mac_gunleri_offset: Optional[List[int]] = None, mac_saatleri: Optional[List[int]] = None):
        """
        Yeni bir fikstür oluşturucu oluşturur (class method - factory pattern).
        
        Args:
            takim_listesi: Takım listesi
            baslangic_tarihi: Başlangıç tarihi
            spor_tipi: Spor tipi
            mac_gunleri_offset: Maç günleri offset listesi (varsayılan: [-2, -1, 0])
            mac_saatleri: Maç saatleri listesi (varsayılan: [13, 15, 17, 19, 21])
        
        Returns:
            FiksturOlusturucu: Yeni oluşturulmuş fikstür oluşturucu
        """
        return cls(takim_listesi, baslangic_tarihi, spor_tipi, mac_gunleri_offset, mac_saatleri)


# ============================================================================
# PUAN TABLOSU SINIFI
# ============================================================================

# Puan tablosu sınıfı - puan hesaplama, averaj/gol farkı ve sıralama işlemleri
class PuanTablosu:
    """Puan hesaplama, averaj/gol farkı ve sıralama sınıfı."""
    
    # Puan tablosu objesi oluşturur - lig yönetimi ve puan kuralları ile
    def __init__(self, lig_yonetimi: LigYonetimi, puan_kurallari: Optional[PuanKurallari] = None):
        """
        Puan tablosu oluşturur.
        
        Args:
            lig_yonetimi: LigYonetimi objesi
            puan_kurallari: PuanKurallari objesi (varsayılan: varsayılan kurallar)
        """
        self._lig_yonetimi = lig_yonetimi
        self._puan_kurallari = puan_kurallari if puan_kurallari is not None else PuanKurallari()
        self._istatistikler = {}  # takim_adi -> istatistik dict
        
        # Her takım için başlangıç istatistikleri
        for takim in lig_yonetimi.takim_listesi_getir():
            self._istatistikler[takim] = {
                "oynanan": 0,
                "galibiyet": 0,
                "beraberlik": 0,
                "maglubiyet": 0,
                "atilan": 0,
                "yenilen": 0,
                "averaj": 0,
                "puan": 0
            }
    
    # Maç sonucunu girme metodu - istatistikleri günceller
    def mac_sonucu_gir(self, lig_maci: LigMaci):
        """
        Maç sonucunu alır ve istatistikleri günceller.
        
        Args:
            lig_maci: LigMaci objesi (skor girilmiş olmalı)
        """
        if not lig_maci.skor_girildi_mi:
            raise TurnuvaHatasi("Maç sonucu girilmemiş.")
        
        ev_sahibi = lig_maci.ev_sahibi
        deplasman = lig_maci.deplasman
        skor_ev = lig_maci.skor_ev
        skor_dep = lig_maci.skor_deplasman
        spor_tipi = lig_maci.spor_tipi
        
        # Beraberlik kontrolü (voleybol/basketbol için)
        if not PuanKurallari.beraberlik_gecerli_mi(spor_tipi) and skor_ev == skor_dep:
            raise TurnuvaHatasi(f"{spor_tipi.value} için beraberlik olamaz!")
        
        # Ev sahibi istatistikleri
        if ev_sahibi in self._istatistikler:
            self._istatistikler[ev_sahibi]["oynanan"] += 1
            self._istatistikler[ev_sahibi]["atilan"] += skor_ev
            self._istatistikler[ev_sahibi]["yenilen"] += skor_dep
            
            if skor_ev > skor_dep:
                self._istatistikler[ev_sahibi]["galibiyet"] += 1
                puan = self._puan_kurallari.puan_al(spor_tipi, "galibiyet")
            elif skor_ev < skor_dep:
                self._istatistikler[ev_sahibi]["maglubiyet"] += 1
                puan = self._puan_kurallari.puan_al(spor_tipi, "maglubiyet")
            else:
                self._istatistikler[ev_sahibi]["beraberlik"] += 1
                puan = self._puan_kurallari.puan_al(spor_tipi, "beraberlik")
            
            self._istatistikler[ev_sahibi]["puan"] += puan
            self._istatistikler[ev_sahibi]["averaj"] = (
                self._istatistikler[ev_sahibi]["atilan"] - 
                self._istatistikler[ev_sahibi]["yenilen"]
            )
        
        # Deplasman istatistikleri
        if deplasman in self._istatistikler:
            self._istatistikler[deplasman]["oynanan"] += 1
            self._istatistikler[deplasman]["atilan"] += skor_dep
            self._istatistikler[deplasman]["yenilen"] += skor_ev
            
            if skor_dep > skor_ev:
                self._istatistikler[deplasman]["galibiyet"] += 1
                puan = self._puan_kurallari.puan_al(spor_tipi, "galibiyet")
            elif skor_dep < skor_ev:
                self._istatistikler[deplasman]["maglubiyet"] += 1
                puan = self._puan_kurallari.puan_al(spor_tipi, "maglubiyet")
            else:
                self._istatistikler[deplasman]["beraberlik"] += 1
                puan = self._puan_kurallari.puan_al(spor_tipi, "beraberlik")
            
            self._istatistikler[deplasman]["puan"] += puan
            self._istatistikler[deplasman]["averaj"] = (
                self._istatistikler[deplasman]["atilan"] - 
                self._istatistikler[deplasman]["yenilen"]
            )
    
    # Sıralı puan tablosunu döndüren metot - puan ve averaja göre sıralı
    def puan_tablosu_getir(self) -> List[Dict]:
        """
        Sıralı puan tablosunu döndürür.
        Sıralama: Önce puan (azalan), sonra averaj (azalan)
        
        Returns:
            List[Dict]: Sıralı puan tablosu
        """
        tablo = []
        
        for takim, istatistik in self._istatistikler.items():
            tablo.append({
                "takim": takim,
                **istatistik
            })
        
        # Sıralama: Önce puan (azalan), sonra averaj (azalan)
        tablo.sort(key=lambda x: (x["puan"], x["averaj"]), reverse=True)
        
        # Sıra numarası ekle
        for i, satir in enumerate(tablo, 1):
            satir["sira"] = i
        
        return tablo
    
    # Takım istatistiklerini döndüren metot - detaylı istatistik bilgisi
    def takim_istatistikleri_getir(self, takim_adi: str) -> Dict:
        """
        Belirli takımın detaylı istatistiklerini döndürür.
        
        Args:
            takim_adi: Takım adı
        
        Returns:
            Dict: Takım istatistikleri
        """
        if takim_adi not in self._istatistikler:
            raise TurnuvaHatasi(f"'{takim_adi}' takımı bulunamadı.")
        
        return self._istatistikler[takim_adi].copy()
    
    @staticmethod
    def puan_hesapla_galibiyet(spor_tipi: SporTipi, puan_kurallari: PuanKurallari):
        """
        Galibiyet puanını hesaplar (static method).
        
        Args:
            spor_tipi: Spor tipi
            puan_kurallari: Puan kuralları objesi
        
        Returns:
            int: Galibiyet puanı
        """
        return puan_kurallari.puan_al(spor_tipi, "galibiyet")
    
    @classmethod
    def puan_tablosu_olustur(cls, lig_yonetimi: LigYonetimi, puan_kurallari: Optional[PuanKurallari] = None):
        """
        Yeni bir puan tablosu oluşturur (class method - factory pattern).
        
        Args:
            lig_yonetimi: Lig yönetimi objesi
            puan_kurallari: Puan kuralları objesi (varsayılan: varsayılan kurallar)
        
        Returns:
            PuanTablosu: Yeni oluşturulmuş puan tablosu
        """
        return cls(lig_yonetimi, puan_kurallari)


# ============================================================================
# LİG REPOSİTORY SINIFI
# ============================================================================

# Lig repository sınıfı - lig verilerini saklama ve getirme işlemleri
class LigRepository:
    """Lig verilerini saklama ve getirme sınıfı."""
    
    # Repository objesi oluşturur - boş lig dictionary'si ile başlar
    def __init__(self):
        """Repository başlatır."""
        self._ligler = {}  # lig_adi -> LigYonetimi
    
    # Ligi kaydetme metodu - dictionary'ye ekler
    def lig_kaydet(self, lig_yonetimi: LigYonetimi):
        """
        Ligi kaydeder.
        
        Args:
            lig_yonetimi: LigYonetimi objesi
        """
        self._ligler[lig_yonetimi.lig_adi] = lig_yonetimi
    
    # Ligi getirme metodu - lig adına göre arama
    def lig_getir(self, lig_adi: str) -> Optional[LigYonetimi]:
        """
        Ligi getirir.
        
        Args:
            lig_adi: Lig adı
        
        Returns:
            LigYonetimi veya None
        """
        return self._ligler.get(lig_adi)
    
    # Tüm ligleri getiren metot - liste olarak döndürür
    def tum_ligler_getir(self) -> List[LigYonetimi]:
        """Tüm ligleri listeler."""
        return list(self._ligler.values())
    
    # Ligi silme metodu - dictionary'den çıkarır
    def lig_sil(self, lig_adi: str):
        """
        Ligi siler.
        
        Args:
            lig_adi: Silinecek lig adı
        """
        if lig_adi not in self._ligler:
            raise TurnuvaHatasi(f"'{lig_adi}' ligi bulunamadı.")
        
        del self._ligler[lig_adi]
    
    @staticmethod
    def lig_adi_gecerli_mi(lig_adi: str):
        """
        Lig adı formatını kontrol eder (static method).
        
        Args:
            lig_adi: Kontrol edilecek lig adı
        
        Returns:
            bool: True ise geçerli format, False ise geçersiz
        """
        return isinstance(lig_adi, str) and len(lig_adi) >= 3
    
    @classmethod
    def repository_olustur(cls):
        """
        Yeni bir lig repository oluşturur (class method - factory pattern).
        
        Returns:
            LigRepository: Yeni oluşturulmuş repository
        """
        return cls()


# ============================================================================
# MAÇ REPOSİTORY SINIFI
# ============================================================================

# Maç repository sınıfı - maç verilerini saklama ve getirme işlemleri
class MacRepository:
    """Maç verilerini saklama ve getirme sınıfı."""
    
    # Repository objesi oluşturur - boş maç dictionary'si ile başlar
    def __init__(self):
        """Repository başlatır."""
        self._maclar = {}  # mac_id -> MacBase
    
    # Maçı kaydetme metodu - dictionary'ye ekler
    def mac_kaydet(self, mac: MacBase):
        """
        Maçı kaydeder.
        
        Args:
            mac: MacBase veya alt sınıfı (LigMaci, HazirlikMaci, ElemeMaci)
        """
        if not isinstance(mac, MacBase):
            raise TypeError("Maç objesi MacBase veya alt sınıfı olmalıdır.")
        
        self._maclar[mac.mac_id] = mac
    
    # ID'ye göre maç getirme metodu
    def mac_getir_id_ile(self, mac_id: int) -> Optional[MacBase]:
        """
        ID'ye göre maç getirir.
        
        Args:
            mac_id: Maç ID'si
        
        Returns:
            MacBase veya None
        """
        return self._maclar.get(mac_id)
    
    # Tarihe göre maç filtreleme metodu - tarih aralığı ile
    def maclari_tarihe_gore_filtrele(self, baslangic_tarihi: Optional[datetime] = None, 
                                      bitis_tarihi: Optional[datetime] = None) -> List[MacBase]:
        """
        Tarihe göre maçları filtreler.
        
        Args:
            baslangic_tarihi: Başlangıç tarihi (None ise sınır yok)
            bitis_tarihi: Bitiş tarihi (None ise sınır yok)
        
        Returns:
            List[MacBase]: Filtrelenmiş maç listesi (tarih sırasına göre)
        """
        sonuc = []
        
        for mac in self._maclar.values():
            mac_tarihi = mac.tarih_saat
            
            # Başlangıç tarihi kontrolü
            if baslangic_tarihi is not None and mac_tarihi < baslangic_tarihi:
                continue
            
            # Bitiş tarihi kontrolü
            if bitis_tarihi is not None and mac_tarihi > bitis_tarihi:
                continue
            
            sonuc.append(mac)
        
        # Tarih sırasına göre sırala
        sonuc.sort(key=lambda m: m.tarih_saat)
        
        return sonuc
    
    # Lig/turnuva adına göre maç filtreleme metodu
    def maclari_lig_turnuva_adi_ile_filtrele(self, lig_turnuva_adi: str) -> List[MacBase]:
        """
        Lig/turnuva adına göre maçları filtreler.
        
        Args:
            lig_turnuva_adi: Lig veya turnuva adı
        
        Returns:
            List[MacBase]: Filtrelenmiş maç listesi
        """
        sonuc = []
        
        for mac in self._maclar.values():
            # LigMaci için lig_adi kontrolü
            if isinstance(mac, LigMaci):
                if mac.lig_adi == lig_turnuva_adi:
                    sonuc.append(mac)
            # ElemeMaci için tur_adi kontrolü (turnuva için)
            elif isinstance(mac, ElemeMaci):
                if mac.tur_adi == lig_turnuva_adi:
                    sonuc.append(mac)
            # HazirlikMaci için organizasyon_adi kontrolü
            elif isinstance(mac, HazirlikMaci):
                if mac.organizasyon_adi == lig_turnuva_adi:
                    sonuc.append(mac)
        
        # Tarih sırasına göre sırala
        sonuc.sort(key=lambda m: m.tarih_saat)
        
        return sonuc
    
    # Tüm maçları getiren metot - tarih sıralı
    def tum_maclari_getir(self) -> List[MacBase]:
        """
        Tüm maçları getirir.
        
        Returns:
            List[MacBase]: Tüm maçlar (tarih sırasına göre)
        """
        maclar = list(self._maclar.values())
        maclar.sort(key=lambda m: m.tarih_saat)
        return maclar
    
    # Maçı silme metodu - dictionary'den çıkarır
    def mac_sil(self, mac_id: int):
        """
        Maçı siler.
        
        Args:
            mac_id: Silinecek maç ID'si
        """
        if mac_id not in self._maclar:
            raise TurnuvaHatasi(f"ID {mac_id} ile maç bulunamadı.")
        
        del self._maclar[mac_id]
    
    def toplam_mac_sayisi(self) -> int:
        """Toplam maç sayısını döndürür."""
        return len(self._maclar)
    
    @staticmethod
    def mac_id_gecerli_mi(mac_id: int):
        """
        Maç ID formatını kontrol eder (static method).
        
        Args:
            mac_id: Kontrol edilecek maç ID'si
        
        Returns:
            bool: True ise geçerli format, False ise geçersiz
        """
        return isinstance(mac_id, int) and mac_id > 0
    
    @classmethod
    def mac_repository_olustur(cls):
        """
        Yeni bir maç repository oluşturur (class method - factory pattern).
        
        Returns:
            MacRepository: Yeni oluşturulmuş repository
        """
        return cls()
    
    @staticmethod
    def mac_id_gecerli_mi(mac_id: int):
        """
        Maç ID formatını kontrol eder (static method).
        
        Args:
            mac_id: Kontrol edilecek maç ID'si
        
        Returns:
            bool: True ise geçerli format, False ise geçersiz
        """
        return isinstance(mac_id, int) and mac_id > 0
    
    @classmethod
    def mac_repository_olustur(cls):
        """
        Yeni bir maç repository oluşturur (class method - factory pattern).
        
        Returns:
            MacRepository: Yeni oluşturulmuş repository
        """
        return cls()
