import sys
import os
from datetime import datetime, timedelta

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(project_root)

try:
    from app.modules.module_3.implementations import HazirlikMaci, LigMaci, ElemeMaci, MacServisi, PuanTablosu, Fikstur
    from app.modules.module_3.repository import MacRepository
except ImportError as e:
    print(f"Import hatası: {e}")
    sys.exit()

def main():
    print("=== MAÇ & TURNUVA YÖNETİM SİSTEMİ DEMO ===\n")
    
    repository = MacRepository()
    servis = MacServisi(repository)
    
    print("1. Polymorphism Örneği - Farklı Maç Tipleri ve Spor Dalları\n")
    maclar = []
    mac1 = servis.mac_olustur('friendly', 1, "Galatasaray", "Fenerbahçe", datetime.now(), sport_type='futbol', organizasyon_adi="Yaz Kupası")
    mac2 = servis.mac_olustur('league', 2, "Beşiktaş", "Trabzonspor", datetime.now() + timedelta(days=1), sport_type='basketbol', lig_adi="Basketbol Süper Ligi", hafta_no=1)
    mac3 = servis.mac_olustur('tournament', 3, "Manchester City", "Real Madrid", datetime.now() + timedelta(days=2), sport_type='futbol', tur_adi="Final")
    mac4 = servis.mac_olustur('league', 4, "Eczacıbaşı", "Vakıfbank", datetime.now() + timedelta(days=3), sport_type='voleybol', lig_adi="Voleybol Ligi", hafta_no=1)
    maclar.extend([mac1, mac2, mac3, mac4])
    
    for mac in maclar:
        repository.kaydet(mac)
        print(f"  {mac.mac_detay_getir()}")
        print(f"  Spor Dalı: {mac.sport_type}")
        if isinstance(mac, HazirlikMaci):
            spor_bilgi = mac.spor_dali_ozel_bilgi()
            print(f"  Spor Özellikleri: {spor_bilgi}")
        print(f"  Sonuç: {mac.mac_sonucu()}\n")
    
    print("2. Service Kullanımı - Fikstür Oluşturma\n")
    takimlar = ["Galatasaray", "Fenerbahçe", "Beşiktaş", "Trabzonspor"]
    fikstur = servis.fikstur_olustur(takimlar, datetime.now(), "Süper Lig")
    print(f"  Organizasyon: {fikstur.organizasyon_adi}")
    print(f"  Toplam Maç: {fikstur.mac_sayisi_getir()}")
    for mac in fikstur.maclar[:3]:
        print(f"  - {mac.ev_sahibi} vs {mac.deplasman}")
    
    print("\n3. Sonuç Girişi ve Puan Tablosu\n")
    mac2.skor_belirle(2, 1)
    mac2.durum = "finished"
    servis.puan_tablosu_guncelle("Basketbol Süper Ligi", mac2)
    
    mac5 = servis.mac_olustur('league', 5, "Galatasaray", "Beşiktaş", datetime.now() + timedelta(days=3), sport_type='futbol', lig_adi="Süper Lig", hafta_no=1)
    repository.kaydet(mac5)
    mac5.skor_belirle(1, 0)
    mac5.durum = "finished"
    servis.puan_tablosu_guncelle("Süper Lig", mac5)
    
    puan_tablosu = servis.puan_tablosu_getir("Süper Lig")
    print("  Puan Tablosu:")
    for i, takim in enumerate(puan_tablosu, 1):
        print(f"  {i}. {takim['takim']}: {takim['puan']} puan ({takim['galibiyet']}-{takim['beraberlik']}-{takim['maglubiyet']})")
    
    print("\n4. Repository Kullanımı - Filtreleme\n")
    lig_maclar = repository.lige_gore_filtrele("Süper Lig")
    print(f"  Süper Lig maçları: {len(lig_maclar)} adet")
    
    futbol_maclar = repository.spor_dalina_gore_filtrele("futbol")
    print(f"  Futbol maçları: {len(futbol_maclar)} adet")
    
    basketbol_maclar = repository.spor_dalina_gore_filtrele("basketbol")
    print(f"  Basketbol maçları: {len(basketbol_maclar)} adet")
    
    tamamlanan = repository.duruma_gore_filtrele("finished")
    print(f"  Tamamlanan maçlar: {len(tamamlanan)} adet")
    
    print("\n5. Takım Geçmişi\n")
    gs_gecmis = servis.takim_gecmisi_listele("Galatasaray")
    print(f"  Takım: {gs_gecmis['takim']}")
    print(f"  Toplam Maç: {gs_gecmis['toplam_mac']}")
    print(f"  Gol Farkı: {gs_gecmis['gol_farki']}")
    
    print("\n6. Spor Dalı İstatistikleri\n")
    futbol_istatistik = servis.spor_dali_istatistik("futbol")
    print(f"  {futbol_istatistik['spor_dali']}: {futbol_istatistik['toplam_mac']} maç")
    
    basketbol_istatistik = servis.spor_dali_istatistik("basketbol")
    print(f"  {basketbol_istatistik['spor_dali']}: {basketbol_istatistik['toplam_mac']} maç")
    
    print("\n=== DEMO TAMAMLANDI ===")

if __name__ == "__main__":
    main()