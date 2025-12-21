from datetime import datetime, timedelta
import sys
import os

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

try:
    from app.modules.module_3.implementations import HazirlikMaci, LigMaci, ElemeMaci, MacServisi, PuanTablosu, Fikstur
    from app.modules.module_3.base import MacBase, TurnuvaHatasi
    from app.modules.module_3.repository import MacRepository
    print("✅ Modüller başarıyla yüklendi.")
except ImportError as e:
    print(f"❌ Modül yükleme hatası: {e}")
    sys.exit()

print("\n--- 🏟️ MAÇ YÖNETİM SİSTEMİ TESTİ BAŞLIYOR ---\n")

try:
    # 1. Nesne Oluşturma Testi
    print("1️⃣  Hazırlık Maçı Oluşturuluyor...")
    tarih = datetime(2025, 6, 15, 20, 0)
    # ID: 101, GS vs FB, Tarih, Org: Yaz Kupası
    mac = HazirlikMaci(101, "Galatasaray", "Fenerbahçe", tarih, "Yaz Kupası")
    print(f"   ➥ Başarılı! Maç: {mac.mac_detay_getir()}")

    # 2. Kapsülleme ve Validasyon Testi (Setter)
    print("\n2️⃣  Veri Güncelleme ve Kontrol Testi...")
    
    # Seyirci sayısını güncelle
    mac.seyirci_sayisi = 50000
    print(f"   ➥ Seyirci sayısı 50,000 yapıldı.")

    # Bilet fiyatını güncelle
    mac.bilet_fiyati = 200.0
    print(f"   ➥ Bilet fiyatı 200.0 TL yapıldı.")

    # Hatalı veri testi (Negatif fiyat)
    print("   ➥ Hatalı giriş testi (Negatif Bilet Fiyatı)...")
    try:
        mac.bilet_fiyati = -50
    except Exception as e:
        print(f"      ✅ Beklenen hata yakalandı: {e}")

    # 3. İş Mantığı Testi (Hasılat ve Skor)
    print("\n3️⃣  Hasılat ve Skor Testi...")
    hasilat = mac.hasilat_hesapla()
    print(f"   ➥ Tahmini Hasılat: {hasilat:,.2f} TL")
    
    mac.skor_belirle(2, 1)
    print(f"   ➥ Skor Girildi: {mac.skor}")
    print(f"   ➥ Puan Durumu Çıktısı: {mac.puan_hesapla()}")

    # 4. Statik ve Sınıf Metotları Testi
    print("\n4️⃣  Sayaç (Class Method) Kontrolü...")
    # Base sınıftaki sayaç
    toplam = MacBase.toplam_sayi_getir()
    # Alt sınıftaki sayaç
    hazirlik_toplam = HazirlikMaci.toplam_hazirlik_getir()
    
    print(f"   ➥ Sistemdeki Toplam Maç: {toplam}")
    print(f"   ➥ Toplam Hazırlık Maçı: {hazirlik_toplam}")
    
    if toplam > 0 and hazirlik_toplam > 0:
        print("   ✅ Sayaçlar doğru çalışıyor.")
    else:
        print("   ❌ Sayaç hatası!")

    print("\n5️⃣  Lig Maçı Testi...")
    lig_mac = LigMaci(201, "Galatasaray", "Beşiktaş", datetime.now(), "Süper Lig", 1)
    lig_mac.skor_belirle(3, 1)
    lig_mac.durum = "finished"
    puan_sonuc = lig_mac.puan_hesapla()
    print(f"   ➥ Puan Sonucu: {puan_sonuc}")
    gol_farki = lig_mac.gol_farki_hesapla()
    print(f"   ➥ Gol Farkı: {gol_farki}")

    print("\n6️⃣  Eleme Maçı Testi...")
    eleme_mac = ElemeMaci(301, "Manchester City", "Real Madrid", datetime.now(), "Final")
    eleme_mac.skor_belirle(1, 1)
    eleme_mac.penalti_skoru_belirle(3, 4)
    eleme_mac.durum = "finished"
    eleme_sonuc = eleme_mac.mac_sonucu()
    print(f"   ➥ Eleme Sonucu: {eleme_sonuc}")

    print("\n7️⃣  Repository Testi...")
    repo = MacRepository()
    repo.kaydet(mac)
    repo.kaydet(lig_mac)
    repo.kaydet(eleme_mac)
    bulunan = repo.id_ile_bul(101)
    print(f"   ➥ ID ile bulunan maç: {bulunan.mac_detay_getir()}")
    lig_maclar = repo.lige_gore_filtrele("Süper Lig")
    print(f"   ➥ Süper Lig maçları: {len(lig_maclar)} adet")
    tamamlanan = repo.duruma_gore_filtrele("finished")
    print(f"   ➥ Tamamlanan maçlar: {len(tamamlanan)} adet")

    print("\n8️⃣  Service Testi...")
    servis = MacServisi(repo)
    yeni_mac = servis.mac_olustur('friendly', 401, "Trabzonspor", "Başakşehir", datetime.now(), organizasyon_adi="Kış Kupası")
    repo.kaydet(yeni_mac)
    print(f"   ➥ Service ile oluşturulan maç: {yeni_mac.mac_detay_getir()}")
    
    servis.sonuc_gir(201, 2, 0)
    puan_tablosu = servis.puan_tablosu_getir("Süper Lig")
    print(f"   ➥ Puan tablosu: {len(puan_tablosu)} takım")

    print("\n9️⃣  Entity Testi...")
    puan_tablo = PuanTablosu("Galatasaray")
    puan_tablo.mac_ekle(3, 1, 3)
    puan_tablo.mac_ekle(2, 0, 3)
    tablo_bilgi = puan_tablo.tablo_bilgisi_getir()
    print(f"   ➥ Puan Tablosu: {tablo_bilgi['takim']} - {tablo_bilgi['puan']} puan")
    
    fikstur = Fikstur("Test Lig", datetime.now())
    fikstur.mac_ekle(mac)
    fikstur.mac_ekle(lig_mac)
    fikstur_bilgi = fikstur.fikstur_bilgisi_getir()
    print(f"   ➥ Fikstür: {fikstur_bilgi['organizasyon']} - {fikstur_bilgi['toplam_mac']} maç")

    print("\n🔟 Polymorphism Testi...")
    farkli_maclar = [mac, lig_mac, eleme_mac]
    print("   ➥ Farklı maç tipleri:")
    for m in farkli_maclar:
        print(f"      {m.mac_detay_getir()}")
        print(f"      Sonuç: {m.mac_sonucu()}")

    print("\n1️⃣1️⃣  Farklı Spor Dalları Testi...")
    basketbol_mac = servis.mac_olustur('league', 501, "Fenerbahçe", "Anadolu Efes", datetime.now(), sport_type='basketbol', lig_adi="Basketbol Ligi", hafta_no=1)
    voleybol_mac = servis.mac_olustur('friendly', 502, "Eczacıbaşı", "Vakıfbank", datetime.now(), sport_type='voleybol', organizasyon_adi="Voleybol Turnuvası")
    repo.kaydet(basketbol_mac)
    repo.kaydet(voleybol_mac)
    
    print(f"   ➥ Basketbol maçı: {basketbol_mac.sport_type}")
    print(f"   ➥ Voleybol maçı: {voleybol_mac.sport_type}")
    
    spor_bilgi = mac.spor_dali_ozel_bilgi()
    print(f"   ➥ Futbol özellikleri: {spor_bilgi}")
    
    futbol_maclar = repo.spor_dalina_gore_filtrele("futbol")
    print(f"   ➥ Futbol maçları: {len(futbol_maclar)} adet")
    
    spor_istatistik = servis.spor_dali_istatistik("futbol")
    print(f"   ➥ Futbol istatistik: {spor_istatistik}")

    print("\n✅ TEST BAŞARIYLA TAMAMLANDI!")

except Exception as e:
    print(f"\n❌ BEKLENMEYEN HATA: {e}")
    import traceback
    traceback.print_exc()