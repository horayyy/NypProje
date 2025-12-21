import sys
from datetime import datetime
from typing import List

# Kendi modüllerini import ediyoruz (Dosyalar aynı klasörde varsayıyoruz)
try:
    from repository import TrainingRepository
    from implementations import (
        IndividualTrainingSession, 
        TeamTrainingSession, 
        RehabTrainingSession,
        TrainingManager # Servis katmanı
    )
    from exceptions import AntrenmanHatasi, TakvimCakismasiHatasi
except ImportError as e:
    print("KRİTİK HATA: Modüller bulunamadı!")
    print(f"Detay: {e}")
    print("Lütfen 'base.py', 'implementations.py', 'repository.py', 'exceptions.py' dosyalarının 'demo.py' ile aynı klasörde olduğundan emin olun.")
    sys.exit(1)

# ==========================================
# YARDIMCI FONKSİYONLAR
# ==========================================

def baslik_yazdir():
    print("\n" + "="*50)
    print("   AKILLI KAMPÜS - GELİŞMİŞ ANTRENMAN YÖNETİMİ")
    print("="*50)

def menu_yazdir():
    print("\n[1] Yeni Antrenman Planla (Create)")
    print("[2] Antrenmanları Listele")
    print("[3] Antrenman İptal Et")
    print("[4] Sporcu Geçmişi Sorgula (Filter)")
    print("[5] Tarih Aralığı Sorgula (Range)")
    print("[6] Çıkış")
    print("-" * 50)

def tarih_al(mesaj="Tarih girin"):
    print(f"\n>> {mesaj}")
    while True:
        try:
            s = input("Format (YYYY-AA-GG SS:DD) Örn: 2025-12-21 14:30 : ")
            return datetime.strptime(s, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Hatalı format! Lütfen tekrar deneyin (Yıl-Ay-Gün Saat:Dakika).")

# ==========================================
# ANA PROGRAM
# ==========================================

def main():
    # 1. Repository ve Servis Katmanını Başlat
    repo = TrainingRepository()
    service = TrainingManager(repo)
    
    # Başlangıç verisi (Demo dolu görünsün diye opsiyonel ekleme)
    try:
        t1 = IndividualTrainingSession(101, 60, 1, 5, "güç", "kondisyon", datetime(2025, 5, 20, 10, 0))
        repo.kaydet(t1)
    except:
        pass # Zaten varsa geç

    baslik_yazdir()
    print("Sistem bileşenleri yüklendi... Hazır.")

    while True:
        menu_yazdir()
        secim = input("Seçiminiz: ")

        # --- 1. YENİ ANTRENMAN EKLEME ---
        if secim == '1':
            try:
                print("\n--- Yeni Antrenman Oluştur ---")
                t_id = int(input("Oturum ID: "))
                sure = int(input("Süre (Dakika): "))
                zaman = tarih_al("Antrenman Tarihi")

                print("\nTip Seçin: (B)ireysel, (T)akım, (R)ehabilitasyon")
                tip_secim = input("Seçim (B/T/R): ").upper()

                yeni_oturum = None

                if tip_secim == 'B':
                    ath_id = int(input("Sporcu ID: "))
                    ant_id = int(input("Antrenör ID: "))
                    odak = input("Odak Alanı (hız, güç, dayanıklılık): ")
                    # implementations.py içindeki gerçek sınıfı çağırıyoruz
                    yeni_oturum = IndividualTrainingSession(
                        oturum_id=t_id, sure=sure, athlete_id=ath_id, 
                        antrenor_id=ant_id, odak_alani=odak, tarih_saat=zaman
                    )

                elif tip_secim == 'T':
                    team_id = int(input("Takım ID: "))
                    saha_id = int(input("Saha ID: "))
                    kisi = int(input("Katılımcı Sayısı: "))
                    plan = input("Plan (taktik, kondisyon, teknik, maç_hazırlığı): ")
                    yeni_oturum = TeamTrainingSession(
                        oturum_id=t_id, sure=sure, team_id=team_id, 
                        saha_id=saha_id, katilimci_sayisi=kisi, 
                        antrenman_plani=plan, tarih_saat=zaman
                    )

                elif tip_secim == 'R':
                    ath_id = int(input("Sporcu ID: "))
                    fizyo_id = int(input("Fizyoterapist ID: "))
                    sakatlik = input("Sakatlık Tipi (kas, eklem, kırık): ")
                    yeni_oturum = RehabTrainingSession(
                        oturum_id=t_id, sure=sure, athlete_id=ath_id,
                        fizyoterapist_id=fizyo_id, sakatlik_tipi=sakatlik, tarih_saat=zaman
                    )
                else:
                    print("Geçersiz seçim!")
                    continue

                # Servis katmanına gönder (Çakışma kontrolü orada yapılacak)
                service.oturum_olustur(yeni_oturum)
                
                # Maliyet hesaplama özelliğini gösterelim
                print(f" >> Hesaplanan Maliyet: {yeni_oturum.oturum_maliyeti_hesapla()} TL")

            except TakvimCakismasiHatasi as e:
                print(f"\n!!! HATA: ÇAKIŞMA TESPİT EDİLDİ !!!")
                print(f"Sebep: {e}")
            except AntrenmanHatasi as e:
                print(f"\n!!! SİSTEM HATASI: {e}")
            except ValueError as e:
                print(f"\n!!! VERİ GİRİŞ HATASI: {e}")
            except Exception as e:
                print(f"\n!!! BEKLENMEYEN HATA: {e}")

        # --- 2. LİSTELEME ---
        elif secim == '2':
            print("\n--- Tüm Antrenmanlar ---")
            # Repository'den doğrudan veya servis üzerinden çekebiliriz
            liste = repo.tumunu_listele()
            if not liste:
                print("Kayıtlı antrenman yok.")
            else:
                print(f"{'ID':<5} {'TİP':<12} {'TARİH':<20} {'DURUM':<10} {'DETAY'}")
                print("-" * 65)
                for item in liste:
                    detay = item.oturum_detaylari_getir()
                    # Detayları string olarak formatla
                    tarih_str = item.tarih_saat.strftime('%Y-%m-%d %H:%M') if item.tarih_saat else "Yok"
                    
                    # Polimorfizm: Her sınıfın kendi detay alanları farklı
                    ozel_bilgi = ""
                    if "odak_alani" in detay: ozel_bilgi = f"Odak: {detay['odak_alani']}"
                    elif "katilimci_sayisi" in detay: ozel_bilgi = f"Kişi: {detay['katilimci_sayisi']}"
                    elif "sakatlik_tipi" in detay: ozel_bilgi = f"Sakatlık: {detay['sakatlik_tipi']}"

                    print(f"{item.oturum_id:<5} {item.oturum_tipi:<12} {tarih_str:<20} {item.durum:<10} {ozel_bilgi}")

        # --- 3. İPTAL ETME ---
        elif secim == '3':
            try:
                sil_id = int(input("İptal edilecek Oturum ID: "))
                service.oturum_iptal_et(sil_id)
            except AntrenmanHatasi as e:
                print(f"Hata: {e}")
            except ValueError:
                print("Lütfen sayısal ID girin.")

        # --- 4. SPORCUYA GÖRE FİLTRELEME ---
        elif secim == '4':
            try:
                sporcu_id = int(input("Aranacak Sporcu ID: "))
                rapor = service.sporcu_programi_getir(sporcu_id)
                if not rapor:
                    print(f"{sporcu_id} ID'li sporcu için kayıt bulunamadı.")
                else:
                    print(f"\n--- Sporcu ID: {sporcu_id} Geçmişi ---")
                    for r in rapor:
                        print(f"ID: {r['oturum_id']} | Tarih: {r['tarih_saat']} | Tip: {r['oturum_turu']}")
            except ValueError:
                print("ID sayı olmalıdır.")

        # --- 5. TARİH ARALIĞI SORGULAMA ---
        elif secim == '5':
            print("Başlangıç Tarihi:")
            bas = tarih_al("Başlangıç")
            print("Bitiş Tarihi:")
            bit = tarih_al("Bitiş")
            
            sonuclar = repo.tarih_araligina_gore_filtrele(bas, bit)
            if not sonuclar:
                print("Bu tarih aralığında antrenman yok.")
            else:
                print(f"\n--- {bas.date()} ile {bit.date()} Arası ---")
                for item in sonuclar:
                    print(f"ID: {item.oturum_id} - {item.tarih_saat} ({item.oturum_tipi})")

        # --- 6. ÇIKIŞ ---
        elif secim == '6':
            print("Çıkış yapılıyor...")
            break
        
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()