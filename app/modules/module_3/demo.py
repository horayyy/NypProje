import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(project_root)

try:
    from app.modules.module_3.implementations import ElemeMaci
except ImportError:
    sys.exit()

def main():
    final = ElemeMaci(2025, "Manchester City", "Real Madrid", datetime.now(), "Final")
    
    final.durum = "finished"
    final.skor_belirle(1, 1)
    
    print(final.mac_sonucu())

    final.penalti_skoru_belirle(3, 4)
    
    print(final.mac_sonucu())

if __name__ == "__main__":
    main()