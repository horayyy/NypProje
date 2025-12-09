import sys
import os
from datetime import datetime

# Python'un ana klasörü görmesi için yol ayarı yapıyoruz
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(project_root)

try:
    # Yazdığımız sınıfları import ediyoruz
    from app.modules.module_3.implementations import HazirlikMaci
    print("✅ Modüller başarıyla yüklendi.\n")
except ImportError as e:
    print(f"❌ HATA: Modüller bulunamadı! {e}")
    sys.exit()

def main():
    print("--- 🏟️ MAÇ YÖNETİM SİSTEMİ DEMOSU ---\n")

    # 1. Hazırlık Maçı Oluşturma
    print("1️⃣  Yeni bir hazırlık maçı oluşturuluyor...")
    tarih = datetime(2025, 7, 15, 21, 45)
    
    # ID: 1, Beşiktaş vs Trabzonspor, Yaz Kupası
    mac1 = HazirlikMaci(1, "Beşiktaş", "Trabzonspor", tarih, "Yaz Kupası")
    
    # Detayları yazdır
    print(f"   ➥ {mac1.mac_detay_getir()}")
    print(f"   ➥ Durum: {mac1.durum}")

    # 2. Veri Güncelleme (Setter Testi)
    print("\n2️⃣  Veriler güncelleniyor (Seyirci ve Bilet)...")
    mac1.seyirci_sayisi = 25000
    mac1.bilet_fiyati = 150.0
    print(f"   ➥ Seyirci: {mac1.seyirci_sayisi}, Bilet: {mac1.bilet_fiyati} TL")

    # 3. Hasılat Hesaplama
    hasilat = mac1.hasilat_hesapla()
    print(f"   ➥ Tahmini Hasılat: {hasilat:,.2f} TL")

    # 4. Skor Girişi
    print("\n3️⃣  Maç oynanıyor ve skor giriliyor...")
    
    # DÜZELTME: 'oynaniyor' yerine 'devam_ediyor' yazıldı
    mac1.durum = "devam_ediyor" 
    
    # Maç bitti, skor 2-2
    mac1.skor_belirle(2, 2)
    
    # DÜZELTME: 'bitti' yerine 'tamamlandi' yazıldı
    mac1.durum = "tamamlandi"
    
    print(f"   ➥ Maç Sonucu: {mac1.skor}")
    print(f"   ➥ Puan Durumu: {mac1.mac_sonucu()}")

    # 5. Hata Testi (Validasyon)
    print("\n4️⃣  Hata Kontrolü Testi (Negatif Bilet Fiyatı)...")
    try:
        mac1.bilet_fiyati = -50
        print("   ❌ Hata yakalanmadı! (Bu kötü)")
    except Exception as e:
        print(f"   ✅ Beklenen Hata Yakalandı: {e}")

    print("\n-------------------------------------------")
    print("✅ DEMO BAŞARIYLA TAMAMLANDI.")

if __name__ == "__main__":
    main()