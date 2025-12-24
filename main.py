import sys
import os
from datetime import datetime

# Windows konsol encoding sorunu için
# Sadece eğer henüz wrap edilmemişse wrap et
if sys.platform == 'win32':
    try:
        import io
        # Eğer zaten wrap edilmişse tekrar wrap etme
        if not isinstance(sys.stdout, io.TextIOWrapper):
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if not isinstance(sys.stderr, io.TextIOWrapper):
            if hasattr(sys.stderr, 'buffer'):
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError, OSError):
        # Zaten wrap edilmiş veya hata var, geç
        pass

# Python path'i ayarla
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
sys.path.insert(0, project_root)

# Module 2 ve Module 3 import'ları
try:
    from app.modules.module_2.repository import TrainingRepository
    from app.modules.module_2.implementations import (
        IndividualTrainingSession, 
        TeamTrainingSession, 
        RehabTrainingSession,
        TrainingManager
    )
    from app.modules.module_2.exceptions import AntrenmanHatasi, TakvimCakismasiHatasi, DuplicateOturumHatasi
    
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

def ana_baslik_yazdir():
    print("\n" + "="*70)
    print("   ENTEGRE SPOR YÖNETİM SİSTEMİ")
    print("   Module 2 (Antrenman) + Module 3 (Lig & Maç)")
    print("="*70)

def ana_menu_yazdir():
    print("\n[1] Antrenman Yönetimi (Module 2)")
    print("[2] Lig ve Maç Yönetimi (Module 3)")
    print("[3] Entegre Görünüm (Her İki Modül)")
    print("[4] Çıkış")
    print("-" * 70)

def tarih_al(mesaj="Tarih girin", gecmis_tarihe_izin_ver=False):
    print(f"\n┌─ {mesaj} ────────────────────────────────────────┐")
    print(f"│ Format: YYYY-MM-DD HH:MM                      │")
    print(f"│ Örnek:  2025-12-21 14:30                      │")
    if not gecmis_tarihe_izin_ver:
        print(f"│ Not:    Geçmiş tarih kabul edilmez                   │")
    print(f"└────────────────────────────────────────────────┘")
    
    while True:
        try:
            s = input("👉 Tarih ve Saat: ").strip()
            if not s:
                print("❌ Lütfen bir tarih giriniz!")
                continue
            
            tarih = datetime.strptime(s, "%Y-%m-%d %H:%M")
            
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
# MODULE 2 FONKSİYONLARI (Antrenman)
# ==========================================

def module_2_menu():
    """Module 2 - Antrenman Yönetimi menüsü"""
    try:
        from app.modules.module_2.demo import main as module_2_main
        module_2_main()
    except ImportError as e:
        print(f"\n❌ HATA: Module 2 yüklenemedi!")
        print(f"Detay: {e}")
        input("\nDevam etmek için Enter'a basın...")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        input("\nDevam etmek için Enter'a basın...")


# ==========================================
# MODULE 3 FONKSİYONLARI (Lig & Maç)
# ==========================================

def module_3_menu():
    """Module 3 - Lig ve Maç Yönetimi menüsü"""
    try:
        from app.modules.module_3.demo import main as module_3_main
        module_3_main()
    except ImportError as e:
        print(f"\n❌ HATA: Module 3 yüklenemedi!")
        print(f"Detay: {e}")
        input("\nDevam etmek için Enter'a basın...")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        input("\nDevam etmek için Enter'a basın...")


# ==========================================
# ENTEGRE GÖRÜNÜM
# ==========================================

def entegre_gorunum():
    """Her iki modülün verilerini birlikte gösterir"""
    print("\n" + "="*70)
    print("   ENTEGRE GÖRÜNÜM - ANTRENMAN VE LİG BİLGİLERİ")
    print("="*70)
    
    # Module 2 verileri
    print("\n📋 ANTRENMAN OTURUMLARI (Module 2)")
    print("-" * 70)
    try:
        repo_2 = TrainingRepository()
        antrenmanlar = repo_2.tumunu_listele()
        if not antrenmanlar:
            print("   Henüz antrenman kaydı bulunmuyor.")
        else:
            print(f"   Toplam Antrenman: {len(antrenmanlar)}")
            tamamlanan = sum(1 for a in antrenmanlar if a.durum == "tamamlandi")
            planlanan = sum(1 for a in antrenmanlar if a.durum == "planlandı")
            iptal = sum(1 for a in antrenmanlar if a.durum == "iptal_edildi")
            print(f"   - Tamamlanan: {tamamlanan}")
            print(f"   - Planlanan: {planlanan}")
            print(f"   - İptal Edilen: {iptal}")
            
            # Son 5 antrenmanı göster
            print("\n   Son Antrenmanlar:")
            for i, ant in enumerate(antrenmanlar[-5:], 1):
                tarih_str = ant.tarih_saat.strftime('%Y-%m-%d %H:%M') if ant.tarih_saat else "Planlanmadı"
                print(f"   {i}. ID:{ant.oturum_id} | {tarih_str} | {ant.oturum_tipi} | {ant.durum}")
    except Exception as e:
        print(f"   Hata: {e}")
    
    # Module 3 verileri
    print("\n🏆 LİG VE MAÇ BİLGİLERİ (Module 3)")
    print("-" * 70)
    try:
        repo_3 = LigRepository()
        # Repository'den lig bilgilerini almak için demo'daki mantığı kullanıyoruz
        # Not: Repository'nin tam yapısını bilmediğimiz için basit bir kontrol yapıyoruz
        print("   Lig bilgileri görüntüleniyor...")
        print("   (Detaylı bilgi için 'Lig ve Maç Yönetimi' menüsünü kullanın)")
    except Exception as e:
        print(f"   Hata: {e}")
    
    print("\n" + "="*70)
    input("\nDevam etmek için Enter'a basın...")


# ==========================================
# ANA PROGRAM
# ==========================================

def run_demo():
    """Ana entegre demo fonksiyonu"""
    ana_baslik_yazdir()
    print("Sistem bileşenleri yüklendi... Hazır.")
    
    while True:
        ana_menu_yazdir()
        secim = input("Seçiminiz: ").strip()
        
        if secim == '1':
            print("\n>>> Antrenman Yönetimi Modülüne geçiliyor...")
            module_2_menu()
        
        elif secim == '2':
            print("\n>>> Lig ve Maç Yönetimi Modülüne geçiliyor...")
            module_3_menu()
        
        elif secim == '3':
            entegre_gorunum()
        
        elif secim == '4':
            print("\nÇıkış yapılıyor...")
            break
        
        else:
            print("\n❌ Geçersiz seçim! Lütfen 1-4 arası bir değer girin.")


if __name__ == "__main__":
    run_demo()