
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.modules.module_2.base import AntrenmanOturumuTemel
from app.modules.module_2.exceptions import (
    DuplicateOturumHatasi,
    OturumBulunamadiHatasi
)

class TrainingRepository:


    def __init__(self):
        # Veritabanı simülasyonu için dictionary kullanıyoruz (id -> nesne)
        self._storage: Dict[int, AntrenmanOturumuTemel] = {}

    def kaydet(self, oturum: AntrenmanOturumuTemel) -> None:

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
        """
        ID'ye göre oturum arar. Bulamazsa None döner.
        """
        return self._storage.get(oturum_id)

    def tumunu_listele(self) -> List[AntrenmanOturumuTemel]:
        """
        Sistemdeki tüm oturumları liste olarak döndürür.
        """
        return list(self._storage.values())

    def sporcuya_gore_filtrele(self, athlete_id: int) -> List[AntrenmanOturumuTemel]:
        """
        Belirli bir sporcuya ait antrenmanları listeler.
        """
        sonuclar = []
        for oturum in self._storage.values():
            # athlete_id özelliği varsa ve eşleşiyorsa
            if getattr(oturum, 'athlete_id', None) == athlete_id:
                sonuclar.append(oturum)
        return sonuclar

    def takima_gore_filtrele(self, team_id: int) -> List[AntrenmanOturumuTemel]:
        """
        Belirli bir takıma ait antrenmanları listeler.
        """
        sonuclar = []
        for oturum in self._storage.values():
            if getattr(oturum, 'team_id', None) == team_id:
                sonuclar.append(oturum)
        return sonuclar

    def tarih_araligina_gore_filtrele(self, baslangic: datetime, bitis: datetime) -> List[AntrenmanOturumuTemel]:
        """
        Belirli bir tarih aralığındaki oturumları listeler.
        """
        sonuclar = []
        for oturum in self._storage.values():
            if oturum.tarih_saat and baslangic <= oturum.tarih_saat <= bitis:
                sonuclar.append(oturum)
        return sonuclar

    def tarihe_gore_cakisma_kontrol(self, tarih: datetime, sure_dk: int, haric_id: int = -1) -> bool:

        from app.modules.module_2.base import AntrenmanOturumuTemel
        
        for oturum in self._storage.values():
            if oturum.oturum_id == haric_id:
                continue
            
            if oturum.tarih_saat:
                cakisma = AntrenmanOturumuTemel.tarih_cakismasi_kontrol(
                    oturum.tarih_saat, 
                    oturum.sure, 
                    tarih, 
                    sure_dk
                )
                if cakisma:
                    return True
        return False