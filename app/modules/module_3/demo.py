import sys
import os
from datetime import datetime

# Windows konsol encoding sorunu için
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(project_root)

try:
    from app.modules.module_3.implementations import ElemeMaci
    from app.modules.module_3.repository import LigYonetimi, PuanTablosu, LigRepository
    from app.modules.module_3.base import SporTipi, TurnuvaHatasi
except ImportError as e:
    print("KRİTİK HATA: Modüller bulunamadı!")
    print(f"Detay: {e}")
    print("Lütfen proje root dizininden çalıştırdığınızdan emin olun.")
    sys.exit(1)

# ==========================================
# YARDIMCI FONKSİYONLAR
# ==========================================

def baslik_yazdir():
    print("\n" + "="*60)
    print("   MODÜL 3 - LİG VE MAÇ YÖNETİM SİSTEMİ")
    print("="*60)

def menu_yazdir():
    print("\n[1] Lig Oluştur")
    print("[2] Fikstür Oluştur")
    print("[3] Maç Sonuçları Gir")
    print("[4] Puan Tablosu Görüntüle")
    print("[5] Takım İstatistikleri")
    print("[6] Takım Maç Geçmişi")
    print("[7] Lig Bilgileri")
    print("[8] Çıkış")
    print("-" * 60)

def tarih_al(mesaj="Tarih girin"):
    print(f"\n>> {mesaj}")
    while True:
        try:
            s = input("Format (YYYY-AA-GG) Örn: 2024-09-01 : ")
            return datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            print("Hatalı format! Lütfen tekrar deneyin (Yıl-Ay-Gün).")

def spor_dali_sec():
    print("\nSpor Dalı Seçin:")
    print("[1] Futbol")
    print("[2] Voleybol")
    print("[3] Basketbol")
    while True:
        secim = input("Seçiminiz (1/2/3): ")
        if secim == '1':
            return SporTipi.FUTBOL
        elif secim == '2':
            return SporTipi.VOLEYBOL
        elif secim == '3':
            return SporTipi.BASKETBOL
        else:
            print("Geçersiz seçim! Lütfen 1, 2 veya 3 girin.")

# ==========================================
# ANA PROGRAM
# ==========================================

def main():
    repository = LigRepository()
    mevcut_lig = None
    puan_tablosu = None
    
    baslik_yazdir()
    print("Sistem hazır.")

    while True:
        menu_yazdir()
        secim = input("Seçiminiz: ")

        # --- 1. LİG OLUŞTUR ---
        if secim == '1':
            try:
                print("\n--- Yeni Lig Oluştur ---")
                lig_adi = input("Lig adı: ")
                if len(lig_adi) < 3:
                    print("Lig adı en az 3 karakter olmalıdır.")
                    continue
                
                spor_tipi = spor_dali_sec()
                sezon_baslangic = tarih_al("Sezon başlangıç tarihi")
                
                mevcut_lig = LigYonetimi(lig_adi, spor_tipi, sezon_baslangic)
                
                print(f"\nKaç takım eklemek istiyorsunuz? (En az 2)")
                takim_sayisi = int(input("Takım sayısı: "))
                
                if takim_sayisi < 2:
                    print("En az 2 takım gereklidir.")
                    continue
                
                print(f"\nTakım adlarını girin:")
                for i in range(takim_sayisi):
                    while True:
                        takim_adi = input(f"Takım {i+1}: ").strip()
                        if not takim_adi:
                            print("Hata: Takım adı boş olamaz.")
                            continue
                        try:
                            mevcut_lig.takim_ekle(takim_adi)
                            break
                        except TurnuvaHatasi as e:
                            print(f"Hata: {e}")
                
                repository.lig_kaydet(mevcut_lig)
                puan_tablosu = PuanTablosu(mevcut_lig)
                
                print(f"\n✓ Lig başarıyla oluşturuldu!")
                print(f"  Lig: {mevcut_lig.lig_adi}")
                print(f"  Spor: {spor_tipi.value}")
                print(f"  Takımlar: {mevcut_lig.takim_listesi_getir()}")
                
            except ValueError as e:
                print(f"Hata: Geçersiz değer - {e}")
            except TurnuvaHatasi as e:
                print(f"Hata: {e}")
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")

        # --- 2. FİKSTÜR OLUŞTUR ---
        elif secim == '2':
            if not mevcut_lig:
                print("\nÖnce bir lig oluşturmalısınız!")
                continue
            
            try:
                print("\n--- Fikstür Oluştur ---")
                fikstur = mevcut_lig.fikstur_olustur()
                toplam_hafta = fikstur.toplam_hafta_sayisi()
                print(f"✓ Fikstür başarıyla oluşturuldu!")
                print(f"  Toplam hafta sayısı: {toplam_hafta}")
                
                print("\n" + "="*60)
                print("TÜM HAFTALAR FİKSTÜRÜ")
                print("="*60)
                
                for hafta_no in range(1, toplam_hafta + 1):
                    maclar = mevcut_lig.haftalik_maclar_getir(hafta_no)
                    print(f"\n📅 {hafta_no}. HAFTA ({len(maclar)} maç)")
                    print("-" * 60)
                    for i, mac in enumerate(maclar, 1):
                        if mac.tarih_saat:
                            # Gün adını al (Türkçe) - weekday() kullanarak daha güvenilir
                            # weekday() 0=Pazartesi, 1=Salı, 2=Çarşamba, 3=Perşembe, 4=Cuma, 5=Cumartesi, 6=Pazar
                            gun_numarasi = mac.tarih_saat.weekday()
                            gun_adi_tr = {0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe", 
                                         4: "Cuma", 5: "Cumartesi", 6: "Pazar"}.get(gun_numarasi, "Bilinmiyor")
                            tarih_saat_str = mac.tarih_saat.strftime("%Y-%m-%d %H:%M")
                            durum_bilgisi = ""
                            if mac.skor_girildi_mi:
                                durum_bilgisi = f" [Skor: {mac.skor}]"
                            print(f"  {i}. {mac.ev_sahibi} vs {mac.deplasman} ({gun_adi_tr}, {tarih_saat_str}){durum_bilgisi}")
                        else:
                            print(f"  {i}. {mac.ev_sahibi} vs {mac.deplasman} (Tarih belirtilmemiş)")
                    
            except TurnuvaHatasi as e:
                print(f"Hata: {e}")
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")

        # --- 3. MAÇ SONUÇLARI GİR ---
        elif secim == '3':
            if not mevcut_lig:
                print("\nÖnce bir lig oluşturmalısınız!")
                continue
            
            if not puan_tablosu:
                puan_tablosu = PuanTablosu(mevcut_lig)
            
            try:
                print("\n--- Maç Sonuçları Gir ---")
                
                # Fikstür yoksa oluştur
                try:
                    fikstur = mevcut_lig.fikstur_olustur()
                except:
                    pass
                
                hafta_no = int(input("Hafta numarası: "))
                maclar = mevcut_lig.haftalik_maclar_getir(hafta_no)
                
                print(f"\n{hafta_no}. Hafta Maçları:")
                tamamlanan_maclar = []
                bekleyen_maclar = []
                
                for mac in maclar:
                    if mac.skor_girildi_mi:
                        tamamlanan_maclar.append(mac)
                    else:
                        bekleyen_maclar.append(mac)
                
                if tamamlanan_maclar:
                    print("\n✓ Tamamlanan Maçlar:")
                    for i, mac in enumerate(tamamlanan_maclar, 1):
                        print(f"  {i}. {mac.ev_sahibi} vs {mac.deplasman} - Skor: {mac.skor} (✓)")
                
                if bekleyen_maclar:
                    print("\n⏳ Bekleyen Maçlar:")
                    for i, mac in enumerate(bekleyen_maclar, 1):
                        print(f"  {i}. {mac.ev_sahibi} vs {mac.deplasman}")
                
                if not bekleyen_maclar:
                    print("\n✓ Bu haftanın tüm maçları zaten tamamlanmış!")
                    continue
                
                print("\nMaç sonuçlarını girin:")
                for mac in bekleyen_maclar:
                    print(f"\n{mac.ev_sahibi} vs {mac.deplasman}")
                    
                    # Spor tipine göre açıklama
                    if mevcut_lig.spor_tipi == SporTipi.FUTBOL:
                        print("  (Gol sayısı girin)")
                    elif mevcut_lig.spor_tipi == SporTipi.VOLEYBOL:
                        print("  (Set sayısı girin - 3 set alan kazanır, max 5 set)")
                    elif mevcut_lig.spor_tipi == SporTipi.BASKETBOL:
                        print("  (Her çeyreğin skorunu girin - 4 çeyrek)")
                    
                    while True:
                        try:
                            skor_ev = 0
                            skor_dep = 0
                            
                            # Basketbol için çeyrek skorları
                            if mevcut_lig.spor_tipi == SporTipi.BASKETBOL:
                                print("  Çeyrek skorları:")
                                ceyrek_skorlari_ev = []
                                ceyrek_skorlari_dep = []
                                
                                for ceyrek in range(1, 5):
                                    skor_ev_ceyrek = int(input(f"    {ceyrek}. Çeyrek - {mac.ev_sahibi} skoru: "))
                                    skor_dep_ceyrek = int(input(f"    {ceyrek}. Çeyrek - {mac.deplasman} skoru: "))
                                    
                                    if skor_ev_ceyrek < 0 or skor_dep_ceyrek < 0:
                                        print("  Hata: Skorlar negatif olamaz.")
                                        raise ValueError
                                    
                                    ceyrek_skorlari_ev.append(skor_ev_ceyrek)
                                    ceyrek_skorlari_dep.append(skor_dep_ceyrek)
                                    skor_ev += skor_ev_ceyrek
                                    skor_dep += skor_dep_ceyrek
                                
                                # Çeyrek skorlarını göster
                                ceyrek_str = " - ".join([f"{c1}-{c2}" for c1, c2 in zip(ceyrek_skorlari_ev, ceyrek_skorlari_dep)])
                                print(f"  Çeyrek skorları: {ceyrek_str}")
                                print(f"  Toplam: {mac.ev_sahibi} {skor_ev} - {skor_dep} {mac.deplasman}")
                            else:
                                # Futbol ve Voleybol için normal skor girişi
                                skor_ev = int(input(f"  {mac.ev_sahibi} skoru: "))
                                skor_dep = int(input(f"  {mac.deplasman} skoru: "))
                            
                            # Voleybol için set kontrolü (3 set alan kazanır, max 5 set)
                            if mevcut_lig.spor_tipi == SporTipi.VOLEYBOL:
                                if skor_ev < 0 or skor_ev > 5 or skor_dep < 0 or skor_dep > 5:
                                    print("  Hata: Set sayısı 0-5 arası olmalıdır.")
                                    continue
                                # Kazanan 3 set almalı, kaybeden 0-2 set arası olmalı
                                if skor_ev == 3:
                                    if skor_dep < 0 or skor_dep > 2:
                                        print("  Hata: Kazanan 3 set alır, kaybeden 0-2 set arası olmalıdır.")
                                        continue
                                elif skor_dep == 3:
                                    if skor_ev < 0 or skor_ev > 2:
                                        print("  Hata: Kazanan 3 set alır, kaybeden 0-2 set arası olmalıdır.")
                                        continue
                                else:
                                    print("  Hata: Kazanan takım 3 set almalıdır.")
                                    continue
                            
                            mac.skor_belirle(skor_ev, skor_dep)
                            mac.durum = "tamamlandi"
                            puan_tablosu.mac_sonucu_gir(mac)
                            
                            # Skor formatını spor tipine göre göster
                            if mevcut_lig.spor_tipi == SporTipi.VOLEYBOL:
                                print(f"  ✓ Sonuç kaydedildi: {skor_ev}-{skor_dep} (set)")
                            elif mevcut_lig.spor_tipi == SporTipi.BASKETBOL:
                                print(f"  ✓ Sonuç kaydedildi: {skor_ev} - {skor_dep} (toplam)")
                            else:
                                print(f"  ✓ Sonuç kaydedildi: {skor_ev} - {skor_dep}")
                            break
                        except TurnuvaHatasi as e:
                            print(f"  Hata: {e}")
                        except ValueError:
                            print("  Lütfen sayısal değer girin.")
                
            except TurnuvaHatasi as e:
                print(f"Hata: {e}")
            except ValueError:
                print("Hata: Geçersiz hafta numarası.")
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")

        # --- 4. PUAN TABLOSU GÖRÜNTÜLE ---
        elif secim == '4':
            if not mevcut_lig:
                print("\nÖnce bir lig oluşturmalısınız!")
                continue
            
            if not puan_tablosu:
                puan_tablosu = PuanTablosu(mevcut_lig)
            
            try:
                print("\n--- Puan Tablosu ---")
                tablo = puan_tablosu.puan_tablosu_getir()
                
                # Spor tipine göre tablo formatı
                if mevcut_lig.spor_tipi == SporTipi.FUTBOL:
                    print("-" * 70)
                    print(f"{'Sıra':<6} {'Takım':<20} {'O':<4} {'G':<4} {'B':<4} {'M':<4} {'A':<6} {'Y':<6} {'Av':<6} {'Puan':<6}")
                    print("-" * 70)
                    for satir in tablo:
                        print(f"{satir['sira']:<6} {satir['takim']:<20} {satir['oynanan']:<4} {satir['galibiyet']:<4} "
                              f"{satir['beraberlik']:<4} {satir['maglubiyet']:<4} {satir['atilan']:<6} "
                              f"{satir['yenilen']:<6} {satir['averaj']:<6} {satir['puan']:<6}")
                else:
                    print("-" * 70)
                    print(f"{'Sıra':<6} {'Takım':<20} {'O':<4} {'G':<4} {'M':<4} {'A':<6} {'Y':<6} {'Av':<6} {'Puan':<6}")
                    print("-" * 70)
                    for satir in tablo:
                        print(f"{satir['sira']:<6} {satir['takim']:<20} {satir['oynanan']:<4} {satir['galibiyet']:<4} "
                              f"{satir['maglubiyet']:<4} {satir['atilan']:<6} "
                              f"{satir['yenilen']:<6} {satir['averaj']:<6} {satir['puan']:<6}")
                
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")

        # --- 5. TAKIM İSTATİSTİKLERİ ---
        elif secim == '5':
            if not mevcut_lig:
                print("\nÖnce bir lig oluşturmalısınız!")
                continue
            
            if not puan_tablosu:
                puan_tablosu = PuanTablosu(mevcut_lig)
            
            try:
                print("\n--- Takım İstatistikleri ---")
                
                # Takım listesini göster
                takimlar = mevcut_lig.takim_listesi_getir()
                print("Mevcut takımlar:")
                for i, takim in enumerate(takimlar, 1):
                    print(f"  {i}. {takim}")
                
                takim_adi = input("\nTakım adı: ").strip()
                
                # Takım adını kontrol et (büyük/küçük harf duyarsız)
                takim_bulundu = None
                for takim in takimlar:
                    if takim.lower() == takim_adi.lower():
                        takim_bulundu = takim
                        break
                
                if not takim_bulundu:
                    print(f"Hata: '{takim_adi}' takımı bulunamadı.")
                    print("Lütfen listedeki takımlardan birini seçin.")
                    continue
                
                istatistik = puan_tablosu.takim_istatistikleri_getir(takim_bulundu)
                
                print(f"\n{takim_bulundu} İstatistikleri:")
                print(f"  Oynanan: {istatistik['oynanan']}")
                print(f"  Galibiyet: {istatistik['galibiyet']}")
                if mevcut_lig.spor_tipi == SporTipi.FUTBOL:
                    print(f"  Beraberlik: {istatistik['beraberlik']}")
                print(f"  Mağlubiyet: {istatistik['maglubiyet']}")
                print(f"  Atılan: {istatistik['atilan']}")
                print(f"  Yenilen: {istatistik['yenilen']}")
                print(f"  Averaj: {istatistik['averaj']}")
                print(f"  Puan: {istatistik['puan']}")
                
            except TurnuvaHatasi as e:
                print(f"Hata: {e}")
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")
                import traceback
                traceback.print_exc()

        # --- 6. TAKIM MAÇ GEÇMİŞİ ---
        elif secim == '6':
            if not mevcut_lig:
                print("\nÖnce bir lig oluşturmalısınız!")
                continue
            
            if not mevcut_lig._fikstur:
                print("\nÖnce fikstür oluşturmalısınız!")
                continue
            
            try:
                print("\n--- Takım Maç Geçmişi ---")
                
                # Takım listesini göster
                takimlar = mevcut_lig.takim_listesi_getir()
                print("Mevcut takımlar:")
                for i, takim in enumerate(takimlar, 1):
                    print(f"  {i}. {takim}")
                
                takim_adi = input("\nTakım adı: ").strip()
                
                # Takım adını kontrol et (büyük/küçük harf duyarsız)
                takim_bulundu = None
                for takim in takimlar:
                    if takim.lower() == takim_adi.lower():
                        takim_bulundu = takim
                        break
                
                if not takim_bulundu:
                    print(f"Hata: '{takim_adi}' takımı bulunamadı.")
                    print("Lütfen listedeki takımlardan birini seçin.")
                    continue
                
                mac_gecmisi = mevcut_lig.takim_mac_gecmisi_getir(takim_bulundu)
                
                if not mac_gecmisi:
                    print(f"\n{takim_bulundu} için henüz maç bulunmuyor.")
                    continue
                
                print(f"\n{takim_bulundu} Maç Geçmişi ({len(mac_gecmisi)} maç):")
                print("="*80)
                print(f"{'Hafta':<8} {'Tarih':<12} {'Rakip':<25} {'Skor':<15} {'Durum':<10}")
                print("-"*80)
                
                for mac in mac_gecmisi:
                    # Rakip takımı belirle
                    if mac.ev_sahibi == takim_bulundu:
                        rakip = mac.deplasman
                        ev_sahibi_mi = True
                    else:
                        rakip = mac.ev_sahibi
                        ev_sahibi_mi = False
                    
                    # Skor bilgisi
                    if mac.skor_girildi_mi:
                        if ev_sahibi_mi:
                            skor_str = f"{mac.skor_ev} - {mac.skor_deplasman}"
                        else:
                            skor_str = f"{mac.skor_deplasman} - {mac.skor_ev}"
                    else:
                        skor_str = "Henüz oynanmadı"
                    
                    # Durum
                    durum_str = mac.durum.replace("_", " ").title()
                    
                    # Tarih formatı
                    tarih_str = mac.tarih_saat.strftime("%Y-%m-%d")
                    
                    print(f"{mac.hafta_no:<8} {tarih_str:<12} {rakip:<25} {skor_str:<15} {durum_str:<10}")
                
                print("="*80)
                
            except TurnuvaHatasi as e:
                print(f"Hata: {e}")
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")
                import traceback
                traceback.print_exc()

        # --- 7. LİG BİLGİLERİ ---
        elif secim == '7':
            if not mevcut_lig:
                print("\nÖnce bir lig oluşturmalısınız!")
                continue
            
            try:
                print("\n--- Lig Bilgileri ---")
                bilgi = mevcut_lig.lig_bilgisi_getir()
                print(f"Lig Adı: {bilgi['lig_adi']}")
                print(f"Spor Tipi: {bilgi['spor_tipi']}")
                print(f"Sezon Başlangıç: {bilgi['sezon_baslangic']}")
                print(f"Takım Sayısı: {bilgi['takim_sayisi']}")
                print(f"Takımlar: {', '.join(bilgi['takimlar'])}")
                
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")

        # --- 8. ÇIKIŞ ---
        elif secim == '8':
            print("\nÇıkış yapılıyor...")
            break
        
        else:
            print("\nGeçersiz seçim!")

if __name__ == "__main__":
    main()
