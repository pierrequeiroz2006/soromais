import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = Path(__file__).parent
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def rodar(script):
    nome = script.replace(".py", "")
    print(f"\n  → {nome:<20} iniciando...")

    result = subprocess.run([sys.executable, BASE / script], capture_output=True, text=True, encoding='utf-8', env=ENV)

    for linha in result.stdout.strip().splitlines():
        print(f"       {linha}")

    if result.returncode != 0:
        raise RuntimeError(f"Erro em {script}:\n{result.stderr}")

    print(f"  ✓ {nome:<20} concluído")


print("\n========== PIPELINE ==========")

with ThreadPoolExecutor(max_workers=2) as executor:
    futures = {
        executor.submit(rodar, "download_pdfs.py"): "download_pdfs",
        executor.submit(rodar, "download_csv.py"): "download_csv",
    }

    for future in as_completed(futures):
        future.result()

rodar("parse_pdfs.py")
rodar("final_json.py")

print("\n========== CONCLUÍDO ==========\n")
