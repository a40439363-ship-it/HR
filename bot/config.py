from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'
load_dotenv(ENV_PATH, override=False)


@dataclass
class Config:
    bot_token: str
    admin_chat_id: int
    excel_file: str


def _clean(value: str | None, default: str = '') -> str:
    return (value or default).strip()


def _default_excel_file() -> str:
    # Railway volume bo'lsa, o'sha joydan foydalanadi.
    volume_path = _clean(os.getenv('RAILWAY_VOLUME_MOUNT_PATH'))
    if volume_path:
        return str(Path(volume_path) / 'applications.xlsx')

    data_dir = _clean(os.getenv('DATA_DIR'))
    if data_dir:
        return str(Path(data_dir) / 'applications.xlsx')

    return str(BASE_DIR / 'data' / 'applications.xlsx')


BOT_TOKEN = _clean(os.getenv('BOT_TOKEN'))
ADMIN_CHAT_ID = int(_clean(os.getenv('ADMIN_CHAT_ID') or os.getenv('ADMIN_ID'), '0') or '0')
EXCEL_FILE = _clean(os.getenv('EXCEL_FILE'), _default_excel_file())

config = Config(
    bot_token=BOT_TOKEN,
    admin_chat_id=ADMIN_CHAT_ID,
    excel_file=EXCEL_FILE,
)
