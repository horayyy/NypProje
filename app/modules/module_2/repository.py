from typing import List, Optional, Dict, Any
from datetime import datetime

# base modülünden temel sınıfı alıyoruz
# DİKKAT: Circular import hatası almamak için gerekirse metod içinde import edilir,
# ancak type hinting için burada durabilir.
from base import AntrenmanOturumuTemel
from exceptions import (
    DuplicateOturumHatasi,
    OturumBulunamadiHatasi
)

class TrainingRepository:
    """
    Antrenman oturumlarının veri erişim katmanı.
    Veritabanı yerine in-memory dictionary kullanır.
    """

    def __init__(self):
        # Veritabanı simülasyonu için dictionary kullanıyoruz (id -> nesne)
        self._storage: Dict[int, AntrenmanOturumuTemel] = {}

    def kaydet(self, oturum: AntrenmanOturumuTemel) -> None:
        """
        Yeni bir antrenman oturumunu sisteme kaydeder.
        """
        if oturum.oturum_id in self._storage:
            raise DuplicateOturumHatasi(f"Oturum ID {oturum.oturum_id} zaten mevcut.")
        
        self._storage[oturum.oturum_id] = oturum

    def guncelle(self, oturum: AntrenmanOturumuTemel) -> None:
        """
        Mevcut bir antrenman oturumunu günceller.
        """
        if oturum.oturum_id not in self._storage:
            raise OturumBulunamadiHatasi(f"Güncellenecek oturum bulunamadı: ID {oturum.oturum_id}")
        
        self._storage[oturum.oturum_id] = oturum

    def sil(self, oturum_id: int) -> None:
        """
        ID'si verilen oturumu sistemden siler.
        """
        if oturum_id not in self._storage:
            raise OturumBulunamadiHatasi(f"Silinecek oturum bulunamadı: ID {oturum_id}")
        
        del self._storage[oturum_id]

    def id_ile_bul(self, oturum_id: int) -> Optional[AntrenmanOturumuTemel]:
        return self._storage.get(oturum_id)

    def tumunu_listele(self) -> List[AntrenmanOturumuTemel]:
        return list(self._storage.values())

    def sporcuya_gore_filtrele(self, athlete_id: int) -> List[AntrenmanOturumuTemel]:
        sonuclar = []
        for oturum in self._storage.values():
            if getattr(oturum, 'athlete_id', None) == athlete_id:
                sonuclar.append(oturum)
        return sonuclar

    def takima_gore_filtrele(self, team_id: int) -> List[AntrenmanOturumuTemel]:
        sonuclar = []
        for oturum in self._storage.values():
            if getattr(oturum, 'team_id', None) == team_id:
                sonuclar.append(oturum)
        return sonuclar

    def tarih_araligina_gore_filtrele(self, baslangic: datetime, bitis: datetime) -> List[AntrenmanOturumuTemel]:
        sonuclar = []
        for oturum in self._storage.values():
            if oturum.tarih_saat and baslangic <= oturum.tarih_saat <= bitis:
                sonuclar.append(oturum)
        return sonuclar

    def detayli_cakisma_kontrol(self, tarih: datetime, sure_dk: int, haric_id: int = -1, 
                                athlete_id: int = None, saha_id: int = None) -> bool:
        """
        Belirtilen tarih ve saatte çakışma olup olmadığını kontrol eder.
        """
        # Circular import riskini önlemek için yerel import
        from base import AntrenmanOturumuTemel
        
        for oturum in self._storage.values():
            # 1. Kendisiyle kıyaslamayı atla
            if oturum.oturum_id == haric_id:
                continue
            
            # 2. Tarihi ayarlanmamış (None olan) oturumları atla
            if not oturum.tarih_saat:
                continue
            
            # 3. Zaman Çakışması Kontrolü
            zaman_cakisiyor = AntrenmanOturumuTemel.tarih_cakismasi_kontrol(
                oturum.tarih_saat, 
                oturum.sure, 
                tarih, 
                sure_dk
            )
            
            if zaman_cakisiyor:
                # Zaman çakışıyorsa, kaynağın (Sporcu veya Saha) aynı olup olmadığına bak
                
                # A) Sporcu Çakışması: Eğer athlete_id verildiyse kontrol et
                mevcut_sporcu_id = getattr(oturum, 'athlete_id', None)
                if athlete_id is not None and mevcut_sporcu_id is not None:
                    if mevcut_sporcu_id == athlete_id:
                        return True
                
                # B) Saha Çakışması: Eğer saha_id verildiyse kontrol et
                mevcut_saha_id = getattr(oturum, 'saha_id', None)
                if saha_id is not None and mevcut_saha_id is not None:
                    if mevcut_saha_id == saha_id:
                        return True

        return False