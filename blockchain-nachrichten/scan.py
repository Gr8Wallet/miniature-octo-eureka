#!/usr/bin/env python3
"""Durchsucht Bitcoin-Bloecke nach lesbaren Nachrichten (OP_RETURN + Coinbase).

Nutzt die oeffentliche Esplora-API (mempool.space / blockstream.info).
Beispiel:
    python3 scan.py --start 230000 --end 231000 --out funde.csv
    python3 scan.py --start 300000 --end 300500 --alle
"""
import argparse
import csv
import json
import re
import sys
import time
import urllib.request

APIS = ["https://mempool.space/api", "https://blockstream.info/api"]

# Schlagwoerter fuer "ernste" Nachrichten mit Ansprache/Kontext
STICHWORTE = [
    "help", "sorry", "forgive", "goodbye", "farewell", "rest in peace", "rip ",
    "in memory", "memorial", "died", "death", "dead", "funeral", "cancer",
    "mom", "mother", "dad", "father", "son", "daughter", "wife", "husband",
    "brother", "sister", "love you", "miss you", "if you read", "to whoever",
    "stolen", "stole", "thief", "hacker", "hacked", "scam", "police",
    "please", "dear ", "never forget", "remember", "prison", "war",
    "hilfe", "verzeih", "mama", "papa", "vermisse", "liebe dich", "tot",
]

LESBAR = re.compile(rb"[\x20-\x7e]{4,}")


def holen(pfad, als_text=False):
    letzter_fehler = None
    for api in APIS:
        for versuch in range(3):
            try:
                with urllib.request.urlopen(api + pfad, timeout=30) as r:
                    daten = r.read()
                return daten.decode() if als_text else json.loads(daten)
            except Exception as e:  # Netzfehler / Rate-Limit
                letzter_fehler = e
                time.sleep(2 ** versuch)
    raise RuntimeError(f"API nicht erreichbar ({pfad}): {letzter_fehler}")


def texte_aus_hex(hexstr, mindestlaenge):
    try:
        roh = bytes.fromhex(hexstr)
    except ValueError:
        return []
    return [m.group().decode("ascii").strip() for m in LESBAR.finditer(roh)
            if len(m.group().strip()) >= mindestlaenge]


def block_txs(blockhash):
    """Alle Transaktionen eines Blocks (Esplora liefert 25 pro Seite)."""
    start = 0
    while True:
        seite = holen(f"/block/{blockhash}/txs/{start}")
        if not seite:
            return
        yield from seite
        if len(seite) < 25:
            return
        start += 25


def scanne_block(hoehe, mindestlaenge):
    blockhash = holen(f"/block-height/{hoehe}", als_text=True).strip()
    info = holen(f"/block/{blockhash}")
    zeit = time.strftime("%Y-%m-%d %H:%M", time.gmtime(info["timestamp"]))
    for tx in block_txs(blockhash):
        for vin in tx.get("vin", []):
            if vin.get("is_coinbase"):
                for t in texte_aus_hex(vin.get("scriptsig", ""), mindestlaenge):
                    yield hoehe, zeit, tx["txid"], "coinbase", t
        for vout in tx.get("vout", []):
            if vout.get("scriptpubkey_type") == "op_return":
                for t in texte_aus_hex(vout.get("scriptpubkey", "")[2:], mindestlaenge):
                    yield hoehe, zeit, tx["txid"], "op_return", t


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--start", type=int, required=True, help="erste Blockhoehe")
    p.add_argument("--end", type=int, required=True, help="letzte Blockhoehe")
    p.add_argument("--out", default="funde.csv", help="CSV-Ausgabedatei")
    p.add_argument("--min", type=int, default=12, help="Mindestlaenge Text")
    p.add_argument("--alle", action="store_true",
                   help="alle lesbaren Texte speichern, nicht nur Stichwort-Treffer")
    p.add_argument("--stichwort", action="append", default=[],
                   help="zusaetzliches Stichwort (mehrfach moeglich)")
    a = p.parse_args()

    stichworte = [s.lower() for s in STICHWORTE + a.stichwort]
    treffer = 0
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["block", "zeit_utc", "txid", "quelle", "stichwort", "text"])
        for hoehe in range(a.start, a.end + 1):
            try:
                for blk, zeit, txid, quelle, text in scanne_block(hoehe, a.min):
                    klein = text.lower()
                    gefunden = next((s for s in stichworte if s in klein), "")
                    if gefunden or a.alle:
                        w.writerow([blk, zeit, txid, quelle, gefunden.strip(), text])
                        f.flush()
                        treffer += 1
                        print(f"[{blk}] {quelle}: {text[:100]}")
            except RuntimeError as e:
                print(f"Block {hoehe} uebersprungen: {e}", file=sys.stderr)
            time.sleep(0.2)  # API schonen
    print(f"\nFertig: {treffer} Funde in {a.out}")


if __name__ == "__main__":
    main()
