

# Base class
from .base import AntrenmanOturumuTemel

# Ana sınıflar (Subclass'lar)
from .implementations import (
    IndividualTrainingSession,
    TeamTrainingSession,
    RehabTrainingSession,
    TrainingManager,
    TrainingPlan,
    TrainingSchedule,
    TrainingStatistics
)

# Repository
from .repository import TrainingRepository

# Önemli Exception'lar
from .exceptions import (
    AntrenmanHatasi,
    OturumBulunamadiHatasi,
    TakvimCakismasiHatasi,
    DuplicateOturumHatasi,
    GecersizOturumIdHatasi,
    GecersizSporcuIdHatasi,
    GecersizTakimIdHatasi,
    GecersizOturumTipiHatasi,
    GecersizOturumDurumuHatasi,
    GecersizTarihSaatHatasi,
    GecersizSureHatasi,
    GecersizSahaIdHatasi,
    SahaDoluHatasi
)

# Modül versiyonu
__version__ = "1.0.0"

# Dışarıdan import edilebilecek sınıfların listesi (__all__)
__all__ = [
    # Base
    "AntrenmanOturumuTemel",
    
    # Subclass'lar
    "IndividualTrainingSession",
    "TeamTrainingSession",
    "RehabTrainingSession",
    
    # Service & Repository
    "TrainingManager",
    "TrainingRepository",
    
    # Entity sınıfları
    "TrainingPlan",
    "TrainingSchedule",
    "TrainingStatistics",
    
    # Exception'lar
    "AntrenmanHatasi",
    "OturumBulunamadiHatasi",
    "TakvimCakismasiHatasi",
    "DuplicateOturumHatasi",
    "GecersizOturumIdHatasi",
    "GecersizSporcuIdHatasi",
    "GecersizTakimIdHatasi",
    "GecersizOturumTipiHatasi",
    "GecersizOturumDurumuHatasi",
    "GecersizTarihSaatHatasi",
    "GecersizSureHatasi",
    "GecersizSahaIdHatasi",
    "SahaDoluHatasi",
]

