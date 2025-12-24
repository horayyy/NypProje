import sys
import os
from datetime import datetime
from typing import List

# Windows konsol encoding sorunu için
# NOT: main.py zaten encoding ayarlarını yapıyor, burada tekrar yaparsak çakışma olur
# Sadece doğrudan çalıştırıldığında encoding ayarlarını yap
if sys.platform == 'win32' and __name__ == "__main__":
    try:
        import io
        # Sadece eğer henüz wrap edilmemişse wrap et
        if not isinstance(sys.stdout, io.TextIOWrapper):
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if not isinstance(sys.stderr, io.TextIOWrapper):
            if hasattr(sys.stderr, 'buffer'):
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError, OSError):
        # Zaten wrap edilmiş veya hata var, geç
        pass

# Python path'i ayarla (absolute import için)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.insert(0, project_root)

# Kendi modüllerini import ediyoruz (Absolute import kullanıyoruz)
try:
    from app.modules.module_2.repository import TrainingRepository
    from app.modules.module_2.implementations import (
        IndividualTrainingSession, 
        TeamTrainingSession, 
        RehabTrainingSession,
        TrainingManager # Servis katmanı
    )
    from app.modules.module_2.exceptions import AntrenmanHatasi, TakvimCakismasiHatasi, DuplicateOturumHatasi
except ImportError as e:
    print("KRİTİK HATA: Modüller bulunamadı!")
    print(f"Detay: {e}")
    print("Lütfen proje root dizininden çalıştırdığınızdan emin olun.")
    # Ana menüden çağrıldığında sys.exit yerine return yapalım
    if __name__ == "__main__":
        sys.exit(1)
    else:
        raise  # Ana menüden çağrıldığında exception'ı yukarı fırlat


# Program başlığını yazdırır
def baslik_yazdir():
    print("\n" + "="*50)
    print("GELİŞMİŞ ANTRENMAN YÖNETİMİ")
    print("="*50)

# Ana menü seçeneklerini yazdırır
def menu_yazdir():
    print("\n[1] Yeni Antrenman Planla (Create)")
    print("[2] Antrenmanları Listele")
    print("[3] Antrenman Tamamla")
    print("[4] Antrenman İptal Et")
    print("[5] Sporcu Geçmişi Sorgula (Filter)")
    print("[6] Tarih Aralığı Sorgula (Range)")
    print("[7] Ana Menüye Dön")
    print("[8] Çıkış")
    print("\nNot: Bilgi girişi sırasında ana menüye dönmek için 'g' tuşuna basın")
    print("-" * 50)

# Girilen değerin 'g' (geri) komutu olup olmadığını kontrol eder
def geri_don_kontrol(deger):
    if isinstance(deger, str) and deger.strip().upper() == 'G':
        print("\n>>> Ana menüye dönülüyor...")
        return True
    return False

# Kullanıcıdan input alır, eğer 'g' girilirse None döndürür
def input_veya_geri(prompt):
    deger = input(prompt)
    if geri_don_kontrol(deger):
        return None
    return deger

# Kullanıcıdan integer input alır, eğer 'g' girilirse None döndürür
def int_input_veya_geri(prompt):   
    while True:
        deger = input(prompt)
        if geri_don_kontrol(deger):
            return None
        try:
            return int(deger)
        except ValueError:
            print("Lütfen sayısal bir değer girin (Geri dönmek için 'g' tuşuna basın).")

# Kullanıcıdan tarih ve saat bilgisi alır
def tarih_al(mesaj="Tarih girin", gecmis_tarihe_izin_ver=False):
    print(f"\n┌─ {mesaj} ────────────────────────────────────────┐")
    print(f"│ Format: YYYY-MM-DD HH:MM                      │")
    print(f"│ Örnek:  2025-12-21 14:30                      │")
    print(f"│ Geri:   'g' tuşuna basın                      │")
    if not gecmis_tarihe_izin_ver:
        print(f"│ Not:    Geçmiş tarih kabul edilmez                   │")
    print(f"└────────────────────────────────────────────────┘")
    
    while True:
        try:
            s = input("👉 Tarih ve Saat: ").strip()
            
            if geri_don_kontrol(s):
                return None
            
            if not s:
                print("❌ Lütfen bir tarih giriniz!")
                continue
            
            tarih = datetime.strptime(s, "%Y-%m-%d %H:%M")
            
            # Geçmiş tarih kontrolü (eğer izin verilmiyorsa)
            if not gecmis_tarihe_izin_ver:
                simdiki_zaman = datetime.now()
                if tarih < simdiki_zaman:
                    print(f"❌ Geçmiş tarih girilemez! Girilen tarih: {tarih.strftime('%d.%m.%Y %H:%M')}")
                    print(f"   Mevcut tarih: {simdiki_zaman.strftime('%d.%m.%Y %H:%M')}")
                    continue
            
            print(f"✅ Kabul edildi: {tarih.strftime('%d.%m.%Y %H:%M')}")
            return tarih
            
        except ValueError:
            print("❌ Geçersiz format! Doğru format: YYYY-MM-DD HH:MM (örn: 2025-12-21 14:30)")

# ==========================================
# ANA PROGRAM
# ==========================================

# Ana program fonksiyonu
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
            print("\n--- Yeni Antrenman Oluştur (Geri dönmek için herhangi bir aşamada 'g' tuşuna basın) ---")
            
            # Oturum ID kontrolü - Eğer ID zaten varsa tekrar istesin
            t_id = None
            while True:
                temp_id = int_input_veya_geri("Oturum ID: ")
                if temp_id is None:
                    # Kullanıcı 'g' tuşuna bastı, ana menüye dön
                    t_id = None
                    break
                mevcut_oturum = repo.id_ile_bul(temp_id)
                if not mevcut_oturum:
                    t_id = temp_id
                    break  # Geçerli ID, döngüden çık
                print(f"!!! UYARI: {temp_id} ID'li oturum zaten mevcut! Lütfen farklı bir ID girin.")
            
            if t_id is None:
                continue  # Ana menüye dön
            
            try:
                sure = int_input_veya_geri("Süre (Dakika): ")
                if sure is None:
                    continue
                
                zaman = tarih_al("Antrenman Tarihi")
                if zaman is None:
                    continue

                # Tip seçimi kontrolü - B/T/R olmalı
                tip_secim = None
                while True:
                    temp_tip = input_veya_geri("\nTip Seçin: (B)ireysel, (T)akım, (R)ehabilitasyon\nSeçim (B/T/R): ")
                    if temp_tip is None:
                        tip_secim = None
                        break
                    temp_tip = temp_tip.upper().strip()
                    if temp_tip in ['B', 'T', 'R']:
                        tip_secim = temp_tip
                        break
                    print(f"!!! HATA: Geçersiz seçim. Lütfen B, T veya R girin. Girilen değer: '{temp_tip}'")
                    print("Lütfen tekrar deneyin.")
                
                if tip_secim is None:
                    continue

                yeni_oturum = None

                if tip_secim == 'B':
                    ath_id = int_input_veya_geri("Sporcu ID: ")
                    if ath_id is None:
                        continue
                    ant_id = int_input_veya_geri("Antrenör ID: ")
                    if ant_id is None:
                        continue
                    
                    # Odak alanı kontrolü
                    odak = None
                    while True:
                        temp_odak = input_veya_geri("Odak Alanı (hız, güç, dayanıklılık, esneklik, koordinasyon): ")
                        if temp_odak is None:
                            odak = None
                            break
                        if IndividualTrainingSession.odak_alani_gecerli_mi(temp_odak):
                            odak = temp_odak
                            break
                        print(f"!!! HATA: Geçersiz odak alanı. Geçerli değerler: hız, güç, dayanıklılık, esneklik, koordinasyon")
                        print(f"Girilen değer: '{temp_odak}'. Lütfen tekrar deneyin.")
                    
                    if odak is None:
                        continue
                    # implementations.py içindeki gerçek sınıfı çağırıyoruz
                    yeni_oturum = IndividualTrainingSession(
                        oturum_id=t_id, sure=sure, athlete_id=ath_id, 
                        antrenor_id=ant_id, odak_alani=odak, tarih_saat=zaman
                    )

                elif tip_secim == 'T':
                    team_id = int_input_veya_geri("Takım ID: ")
                    if team_id is None:
                        continue
                    
                    # Saha ID kontrolü - 1-5 arası olmalı ve çakışma kontrolü
                    saha_id = None
                    while True:
                        temp_saha_id = int_input_veya_geri("Saha ID (1-5 arası): ")
                        if temp_saha_id is None:
                            # Kullanıcı 'g' tuşuna bastı, ana menüye dön
                            saha_id = None
                            break
                        
                        # 1-5 arası kontrolü
                        if not (1 <= temp_saha_id <= 5):
                            print(f"!!! HATA: Saha ID 1 ile 5 arasında olmalıdır. Girilen değer: {temp_saha_id}")
                            print("Lütfen tekrar deneyin.")
                            continue
                        
                        # Çakışma kontrolü - Tarih ve süre bilgisi mevcut olduğu için kontrol edebiliriz
                        if zaman and sure:
                            cakisma_var = repo.detayli_cakisma_kontrol(
                                tarih=zaman,
                                sure_dk=sure,
                                haric_id=t_id,  # Yeni oluşturulacak oturum ID'si
                                athlete_id=None,  # Takım antrenmanında sporcu yok
                                saha_id=temp_saha_id
                            )
                            
                            if cakisma_var:
                                tarih_str = zaman.strftime('%Y-%m-%d %H:%M')
                                print(f"!!! UYARI: {temp_saha_id} numaralı saha {tarih_str} tarihinde dolu!")
                                print(f"Lütfen başka bir saha ID giriniz.")
                                continue
                        
                        # Geçerli saha ID, döngüden çık
                        saha_id = temp_saha_id
                        break
                    
                    if saha_id is None:
                        continue  # Ana menüye dön
                    
                    # Katılımcı sayısı kontrolü - 2-30 arası olmalı
                    kisi = None
                    while True:
                        temp_kisi = int_input_veya_geri("Katılımcı Sayısı (2-30 arası): ")
                        if temp_kisi is None:
                            kisi = None
                            break
                        if 2 <= temp_kisi <= 30:
                            kisi = temp_kisi
                            break
                        print(f"!!! HATA: Katılımcı sayısı 2 ile 30 arasında olmalıdır. Girilen değer: {temp_kisi}")
                        print("Lütfen tekrar deneyin.")
                    
                    if kisi is None:
                        continue
                    
                    # Antrenman planı kontrolü
                    plan = None
                    while True:
                        temp_plan = input_veya_geri("Plan (taktik, kondisyon, teknik, maç_hazırlığı): ")
                        if temp_plan is None:
                            plan = None
                            break
                        if TeamTrainingSession.antrenman_plani_gecerli_mi(temp_plan):
                            plan = temp_plan
                            break
                        print(f"!!! HATA: Geçersiz antrenman planı. Geçerli değerler: taktik, kondisyon, teknik, maç_hazırlığı")
                        print(f"Girilen değer: '{temp_plan}'. Lütfen tekrar deneyin.")
                    
                    if plan is None:
                        continue
                    yeni_oturum = TeamTrainingSession(
                        oturum_id=t_id, sure=sure, team_id=team_id, 
                        saha_id=saha_id, katilimci_sayisi=kisi, 
                        antrenman_plani=plan, tarih_saat=zaman
                    )

                elif tip_secim == 'R':
                    ath_id = int_input_veya_geri("Sporcu ID: ")
                    if ath_id is None:
                        continue
                    fizyo_id = int_input_veya_geri("Fizyoterapist ID: ")
                    if fizyo_id is None:
                        continue
                    
                    # Sakatlık tipi kontrolü
                    sakatlik = None
                    while True:
                        temp_sakatlik = input_veya_geri("Sakatlık Tipi (kas, eklem, kırık, burkulma, yırtık, diğer): ")
                        if temp_sakatlik is None:
                            sakatlik = None
                            break
                        if RehabTrainingSession.sakatlik_tipi_gecerli_mi(temp_sakatlik):
                            sakatlik = temp_sakatlik
                            break
                        print(f"!!! HATA: Geçersiz sakatlık tipi. Geçerli değerler: kas, eklem, kırık, burkulma, yırtık, diğer")
                        print(f"Girilen değer: '{temp_sakatlik}'. Lütfen tekrar deneyin.")
                    
                    if sakatlik is None:
                        continue
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
            except DuplicateOturumHatasi as e:
                print(f"\n!!! HATA: AYNI ID MEVCUT !!!")
                print(f"Sebep: {e}")
            except AntrenmanHatasi as e:
                print(f"\n!!! SİSTEM HATASI: {e}")
            except ValueError as e:
                print(f"\n!!! VERİ GİRİŞ HATASI: {e}")
            except Exception as e:
                print(f"\n!!! BEKLENMEYEN HATA: {e}")

        # --- 2. LİSTELEME ---
        elif secim == '2':
            print("\n--- Tüm Antrenmanlar (Detaylı Liste) ---")
            # Repository'den doğrudan veya servis üzerinden çekebiliriz
            liste = repo.tumunu_listele()
            if not liste:
                print("Kayıtlı antrenman yok.")
            else:
                # Başlık satırı
                print(f"\n{'Antrenman ID':<13} {'TÜR':<14} {'TARİH':<19} {'SÜRE':<7} {'DURUM':<13} {'MALİYET':<10}")
                print("-" * 82)
                
                for item in liste:
                    detay = item.oturum_detaylari_getir()
                    tarih_str = item.tarih_saat.strftime('%Y-%m-%d %H:%M') if item.tarih_saat else "Planlanmadı"
                    maliyet = item.oturum_maliyeti_hesapla()
                    oturum_turu = detay.get('oturum_turu', 'bilinmiyor')
                    
                    # Ana satır
                    print(f"{item.oturum_id:<13} {oturum_turu.capitalize():<14} {tarih_str:<19} {item.sure:>5}dk {item.durum.capitalize():<13} {maliyet:>8.2f} TL")
                    
                    # Detay satırı (girintili)
                    detay_satiri = "      └─ "
                    
                    if oturum_turu == "bireysel":
                        detay_satiri += f"Sporcu:{detay.get('athlete_id')} | Antrenör:{detay.get('antrenor_id')} | "
                        detay_satiri += f"Tip:{item.oturum_tipi} | Odak:{detay.get('odak_alani')}"
                        if detay.get('performans_notu') is not None:
                            detay_satiri += f" | Performans:{detay.get('performans_notu')}/10"
                            
                    elif oturum_turu == "takım":
                        detay_satiri += f"Takım:{detay.get('team_id')} | Saha:{detay.get('saha_id')} | "
                        detay_satiri += f"Kişi:{detay.get('katilimci_sayisi')} | Plan:{detay.get('antrenman_plani')}"
                        
                    elif oturum_turu == "rehabilitasyon":
                        detay_satiri += f"Sporcu:{detay.get('athlete_id')} | Fizyoterapist:{detay.get('fizyoterapist_id')} | "
                        detay_satiri += f"Sakatlık:{detay.get('sakatlik_tipi')} | Program:{detay.get('rehab_programi')}"
                        if detay.get('ilerleme_notu') is not None:
                            detay_satiri += f" | İlerleme:{detay.get('ilerleme_notu')}/10"
                    
                    print(detay_satiri)
                
                print("-" * 82)
                print(f"Toplam: {len(liste)} antrenman | ", end="")
                # İptal edilen antrenmanları toplam maliyetten hariç tut
                toplam_maliyet = sum(item.oturum_maliyeti_hesapla() for item in liste if item.durum != "iptal_edildi")
                print(f"Toplam Tahmini Maliyet: {toplam_maliyet:.2f} TL")

        # --- 3. TAMAMLAMA ---
        elif secim == '3':
            tamam_id = int_input_veya_geri("Tamamlanacak Oturum ID: ")
            if tamam_id is None:
                continue
            try:
                service.oturum_tamamla(tamam_id)
            except AntrenmanHatasi as e:
                print(f"Hata: {e}")

        # --- 4. İPTAL ETME ---
        elif secim == '4':
            sil_id = int_input_veya_geri("İptal edilecek Oturum ID: ")
            if sil_id is None:
                continue
            try:
                service.oturum_iptal_et(sil_id)
            except AntrenmanHatasi as e:
                print(f"Hata: {e}")

        # --- 5. SPORCUYA GÖRE FİLTRELEME ---
        elif secim == '5':
            sporcu_id = int_input_veya_geri("Aranacak Sporcu ID: ")
            if sporcu_id is None:
                continue
            try:
                rapor = service.sporcu_programi_getir(sporcu_id)
                if not rapor:
                    print(f"{sporcu_id} ID'li sporcu için kayıt bulunamadı.")
                else:
                    print(f"\n--- Sporcu ID: {sporcu_id} Geçmişi ---")
                    for r in rapor:
                        # Tarih formatını düzenle (ISO formatından okunabilir formata)
                        tarih_str = r['tarih_saat']
                        if tarih_str:
                            try:
                                # ISO formatındaki tarihi parse et ve formatla
                                tarih_dt = datetime.fromisoformat(tarih_str.replace('Z', '+00:00'))
                                tarih_str = tarih_dt.strftime('%Y-%m-%d %H:%M')
                            except (ValueError, AttributeError):
                                # Eğer parse edilemezse olduğu gibi göster
                                pass
                        else:
                            tarih_str = "Planlanmadı"
                        print(f"ID: {r['oturum_id']} | Tarih: {tarih_str} | Tip: {r['oturum_turu']}")
            except Exception as e:
                print(f"Hata: {e}")

        # --- 6. TARİH ARALIĞI SORGULAMA ---
        elif secim == '6':
            print("Başlangıç Tarihi:")
            bas = tarih_al("Başlangıç", gecmis_tarihe_izin_ver=True)
            if bas is None:
                continue
            print("Bitiş Tarihi:")
            bit = tarih_al("Bitiş", gecmis_tarihe_izin_ver=True)
            if bit is None:
                continue
            
            sonuclar = repo.tarih_araligina_gore_filtrele(bas, bit)
            if not sonuclar:
                print("Bu tarih aralığında antrenman yok.")
            else:
                print(f"\n--- {bas.date()} ile {bit.date()} Arası ---")
                for item in sonuclar:
                    # Tarih formatını düzenle
                    tarih_str = item.tarih_saat.strftime('%Y-%m-%d %H:%M') if item.tarih_saat else "Planlanmadı"
                    print(f"ID: {item.oturum_id} - {tarih_str} ({item.oturum_tipi})")

        # --- 7. ANA MENÜYE DÖN ---
        elif secim == '7':
            print("\n>>> Ana menüye dönülüyor...")
            return  # Ana menüye dön
        
        # --- 8. ÇIKIŞ ---
        elif secim == '8':
            print("Çıkış yapılıyor...")
            sys.exit(0)
        
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()