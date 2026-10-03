# „1.516 Hilferufe" – die LuBian-Nachrichten auf der Bitcoin-Blockchain

> Recherche-Dossier + Skript Teil 1 + Aufruf. Stand: Oktober 2026.
> Alle Fakten vor Veröffentlichung gegen die Quellen unten prüfen.

## Die Fakten (laut Quellen)
- **LuBian**: chinesischer Mining-Pool (Anlagen in China und Iran), zeitweise ~6 % der Bitcoin-Hashrate.
- **28. Dezember 2020**: über 90 % der Bitcoin des Pools werden abgezogen – **127.426 BTC**, damals ~3,5 Mrd. $.
- Danach schickt jemand von LuBians Adressen **1.516 Transaktionen** mit OP_RETURN-Nachrichten an die Adressen des Diebes (Kosten ca. 1,4 BTC) – sinngemäß *„bitte gebt unsere Gelder zurück"*.
- LuBian verschwindet Anfang 2021 still. Weder Pool noch Täter äußern sich öffentlich.
- **August 2025**: Arkham Intelligence deckt den Diebstahl rückwirkend auf – fast fünf Jahre später.
- **Oktober 2025**: Die US-Justiz beschlagnahmt **127.271 BTC** (~14 Mrd. $), die sie Chen Zhi und der kambodschanischen **Prince Group** (mutmaßlich „Pig-Butchering"-Betrug) zuordnet. Analysten verbinden diese Coins mit dem LuBian-Diebstahl.
- **China** (Behörde CVERC) behauptet daraufhin, die USA selbst hätten die Coins 2020 per Hack entwendet.

## Die offenen Fragen (der Kern der Story)
1. **Wer hat die 1.516 Nachrichten geschrieben?** Ein verzweifelter Techniker? Die Chefetage? Ein Skript?
2. **Wem gehörte LuBian wirklich?** Hängt der Pool mit der Prince Group zusammen – war es also Opfer oder Teil des Systems?
3. **Wer war der Dieb?** Ein Insider, Kriminelle, ein Staat?
4. **Warum hat 5 Jahre lang niemand etwas gesagt?**

## Skript – Teil 1 (ca. 60–90 Sek., Kurzvideo)
**[Hook, schwarzer Bildschirm, Text tippt sich]**
„Bitte gebt unser Geld zurück." – Diese Nachricht steht für immer in der Bitcoin-Blockchain. Nicht einmal. **1.516 Mal.**

**[Schnitt: Block-Explorer, OP_RETURN-Feld]**
Dezember 2020. Ein chinesischer Mining-Pool namens LuBian verliert über Nacht 127.000 Bitcoin. Heute wären das über zehn Milliarden Dollar. Der größte Krypto-Diebstahl aller Zeiten – und niemand hat es gemerkt.

**[Schnitt]**
Kein Pressestatement. Keine Anzeige. Nur diese Nachrichten, die jemand verzweifelt an den Dieb schickt – und dann verschwindet LuBian spurlos.

**[Schnitt: Schlagzeilen 2025]**
Fünf Jahre später taucht das Geld wieder auf: beschlagnahmt von der US-Regierung, verknüpft mit einem der größten Betrugsnetzwerke Asiens. Und China sagt: Die USA haben es selbst gestohlen.

**[Close-up, Kamera]**
Aber eine Frage stellt keiner: Wer hat diese 1.516 Nachrichten geschrieben? Wer saß 2020 an diesem Rechner?

**[Aufruf]** → siehe unten. „In Teil 2 zeige ich euch die Nachrichten selbst."

## Der Aufruf (für Video, Beschreibung, Posts)
> Hast du 2020/2021 für LuBian gearbeitet, dort gemined oder kennst jemanden, der dabei war?
> Weißt du, wer die Nachrichten an den Dieb verschickt hat?
> Schreib mir **privat** an [KONTAKT – eigenes, verschlüsseltes Postfach, z. B. Proton/Signal].
> Ich veröffentliche nichts und niemanden ohne deine Zustimmung. Quellenschutz garantiert.

Sprachen: Deutsch + Englisch + **Chinesisch** (die Zielgruppe der Zeugen sitzt dort – z. B. auf X, Reddit r/BitcoinMining, Bitcointalk, chinesischen Mining-Foren).

## Serienplan
| Teil | Inhalt |
|---|---|
| 1 | Hook: die 1.516 Nachrichten, der unbemerkte Diebstahl, Aufruf |
| 2 | Live im Block-Explorer: Nachrichten zeigen, Zeitlinie, wie Arkham es fand |
| 3 | Die Spur zur Prince Group und der Streit USA vs. China |
| 4 | Hinweise der Community / Antworten (oder: das Schweigen) |

## Selbst nachprüfen
- Arkham-Bericht (Aug. 2025) enthält die Adressen → Transaktionen in einem Explorer öffnen, OP_RETURN als Text ansehen.
- Oder mit `scan.py` den Blockbereich ab Ende Dezember 2020 (ca. Block 663.000+) scannen, Stichwort `--stichwort return`.

## Sicherheit & Recht
- Es geht um mutmaßlich organisierte Kriminalität. Keine Spekulation über konkrete Privatpersonen; Behauptungen als „laut …" kennzeichnen.
- Eigenen Kontaktkanal trennen von privaten Daten. Hinweise zu Straftaten ggf. an Behörden, nicht öffentlich posten.

## Quellen
- Cointelegraph: https://cointelegraph.com/news/3-5b-btc-heist-retroactively-uncovered-arkham
- Cybersecurity News: https://cybersecuritynews.com/bitcoin-hack-valued-3-5-billion/amp
- Bitcoin News (Seizure/Prince Group): https://bitcoinnews.com/p/us-seized-127k-btc-lubian-prince-group
- Bitcoin Magazine: https://bitcoinmagazine.com/news/u-s-seizes-14-billion-in-bitcoin-from-scam
- Cointelegraph (China-Vorwurf): https://cointelegraph.com/news/china-raises-alarm-united-states-lubian-127k-bitcoin-hack
- Decrypt: https://decrypt.co/348109/chinese-cybersecurity-watchdog-alleges-us-stole-13-2b-in-bitcoin-five-years-ago
- Alternative (aktuell, Aug. 2026): Coldcard-Hack – Opfer schreiben dem Dieb, Arkham: https://info.arkm.com/research/coldcard-why-are-users-sending-on-chain-messages-to-the-hackers-address
