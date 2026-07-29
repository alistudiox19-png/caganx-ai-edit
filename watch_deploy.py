#!/usr/bin/env python3
import sys
import time
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).parent.resolve()
FILES_TO_WATCH = [
    BASE_DIR / "index.html",
    BASE_DIR / "server.py",
    BASE_DIR / "vercel.json",
    BASE_DIR / "api" / "process.js",
    BASE_DIR / "api" / "preupload.js"
]

def get_mtimes():
    mtimes = {}
    for f in FILES_TO_WATCH:
        if f.exists():
            mtimes[str(f)] = f.stat().st_mtime
    return mtimes

def main():
    print("caganx AI edit - 7/24 Otomatik Git & Vercel Otomatik Dagitim Gozlemcisi Baslatildi!")
    last_mtimes = get_mtimes()

    while True:
        try:
            time.sleep(3)
            current_mtimes = get_mtimes()
            changed = False
            for k, v in current_mtimes.items():
                if k not in last_mtimes or last_mtimes[k] != v:
                    changed = True
                    break

            if changed:
                print("Dosya degisikligi tespit edildi! Otomatik Git & Vercel Push yapiliyor...")
                subprocess.run("git add .", shell=True, cwd=str(BASE_DIR))
                msg = f"Otomatik Ozellik Guncellemesi - {int(time.time())}"
                subprocess.run(f'git commit -m "{msg}"', shell=True, cwd=str(BASE_DIR))
                subprocess.run("git push origin main", shell=True, cwd=str(BASE_DIR))
                print("Vercel Otomatik Dagitim Tetiklendi!")
                last_mtimes = current_mtimes
        except Exception as e:
            print("Gozlemci hatasi:", e)

if __name__ == "__main__":
    main()
