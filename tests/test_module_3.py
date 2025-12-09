from datetime import datetime
import sys
import os

# Python'un modülleri bulabilmesi için yol ayarı
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    # Yazdığımız sınıfları import ediyoruz
    from app.modules.module_3.implementations import HazirlikMaci
    from app.modules.module_3.base import MacBase, TurnuvaHatasi
    print("✅ Modüller başarıyla yüklendi.")
except ImportError as e:
    print(f"❌ Modül yükleme hatası: {e}")
    print("Lütfen dosyayı 'app' klasörünün olduğu ana dizinde çalıştırdığından emin ol.")
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

    print("\n✅ TEST BAŞARIYLA TAMAMLANDI! Kodlarınız canavar gibi çalışıyor.")

except Exception as e:
    print(f"\n❌ BEKLENMEYEN HATA: {e}")