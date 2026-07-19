import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dashboard.utils.database import *
except ImportError:
    from utils.database import *

print(get_tables())

print(database_statistics())

print(latest_year())

print(health_check())
print(get_tables())