from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import AntrenmanOturumuTemel
from .exceptions import (
    DuplicateOturumHatasi,
    OturumBulunamadiHatasi
)

# Antrenman oturumlarının veri erişim katmanı
class TrainingRepository:

    # Repository örneğini başlatır
    def __init__(self):
        # Veritabanı simülasyonu için dictionary kullanıyoruz (id -> nesne)
        self._storage: Dict[int, AntrenmanOturumuTemel] = {}
    
    # Yeni bir boş repository örneği oluşturur
    @classmethod
    def bos_repository_olustur(cls) -> 'TrainingRepository':
        return cls()

    # Yeni bir antrenman oturumunu sisteme kaydeder
    def kaydet(self, oturum: AntrenmanOturumuTemel) -> None:
        if oturum.oturum_id in self._storage:
            raise DuplicateOturumHatasi(f"Oturum ID {oturum.oturum_id} zaten mevcut.")
        
        self._storage[oturum.oturum_id] = oturum

    # Mevcut bir antrenman oturumunu günceller
    def guncelle(self, oturum: AntrenmanOturumuTemel) -> None:
        if oturum.oturum_id not in self._storage:
            raise OturumBulunamadiHatasi(f"Güncellenecek oturum bulunamadı: ID {oturum.oturum_id}")
        
        self._storage[oturum.oturum_id] = oturum

    # ID'si verilen oturumu sistemden siler
    def sil(self, oturum_id: int) -> None:
        if oturum_id not in self._storage:
            raise OturumBulunamadiHatasi(f"Silinecek oturum bulunamadı: ID {oturum_id}")
        
        del self._storage[oturum_id]

    # ID'si verilen oturumu bulur
    def id_ile_bul(self, oturum_id: int) -> Optional[AntrenmanOturumuTemel]:
        return self._storage.get(oturum_id)

    # Tüm antrenman oturumlarını listeler
    def tumunu_listele(self) -> List[AntrenmanOturumuTemel]:
        return list(self._storage.values())

    # Sporcu ID'sine göre antrenman oturumlarını filtreler
    def sporcuya_gore_filtrele(self, athlete_id: int) -> List[AntrenmanOturumuTemel]:
        sonuclar = []
        for oturum in self._storage.values():
            if getattr(oturum, 'athlete_id', None) == athlete_id:
                sonuclar.append(oturum)
        return sonuclar

    # Takım ID'sine göre antrenman oturumlarını filtreler
    def takima_gore_filtrele(self, team_id: int) -> List[AntrenmanOturumuTemel]:
        sonuclar = []
        for oturum in self._storage.values():
            if getattr(oturum, 'team_id', None) == team_id:
                sonuclar.append(oturum)
        return sonuclar

    # Tarih aralığına göre antrenman oturumlarını filtreler
    def tarih_araligina_gore_filtrele(self, baslangic: datetime, bitis: datetime) -> List[AntrenmanOturumuTemel]:
        sonuclar = []
        for oturum in self._storage.values():
            if oturum.tarih_saat and baslangic <= oturum.tarih_saat <= bitis:
                sonuclar.append(oturum)
        return sonuclar

    # Belirtilen tarih ve saatte çakışma olup olmadığını kontrol eder
    def detayli_cakisma_kontrol(self, tarih: datetime, sure_dk: int, haric_id: int = -1, 
                                athlete_id: int = None, saha_id: int = None) -> bool:
        # Circular import riskini önlemek için yerel import
        from .base import AntrenmanOturumuTemel
        
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
            
           # Zaman çakışıyorsa, kaynağın (Sporcu veya Saha) aynı olup olmadığına bak
            if zaman_cakisiyor:
                
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
    
    # Oturum ID'sinin geçerli formatda olup olmadığını kontrol eder
    @staticmethod
    def gecerli_oturum_id_mi(oturum_id: int) -> bool:
        return isinstance(oturum_id, int) and oturum_id > 0