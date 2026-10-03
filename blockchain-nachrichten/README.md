# Blockchain-Nachrichten finden

`scan.py` durchsucht einen Bereich von Bitcoin-Blöcken nach lesbarem Text
(OP_RETURN-Ausgaben und Coinbase-Daten) und filtert nach Stichwörtern, die auf
ernste, persönliche Nachrichten hindeuten (Abschied, Gedenken, Diebstahl, Anrede …).

Benötigt nur Python 3, keine Zusatzpakete.

```bash
python3 scan.py --start 230000 --end 231000 --out funde.csv
python3 scan.py --start 400000 --end 400200 --stichwort "an meine"
python3 scan.py --start 250000 --end 250100 --alle   # alle Texte
```

Tipps:
- OP_RETURN-Nachrichten sind ab ca. Block 250000 (2013) häufig.
- Viele Treffer sind Spam/Protokolldaten (Omni, Counterparty) – manuell sichten.
- Funde im Block-Explorer (z. B. mempool.space/tx/<txid>) gegenprüfen.
- Ein Aufruf sollte lauten „Melde dich, wenn du das geschrieben hast" –
  keine Namen ohne Zustimmung veröffentlichen.
