#!/usr/bin/env python3
"""Espansione keyless delle keyword con l'autocomplete di Google e Bing (nessuna chiave).

Uso:
  python3 suggest.py wordpress "hosting wordpress" --hl it --gl it
  python3 suggest.py --seeds-file ~/seo-content/shared/semi.txt --out ~/seo-content/audits/suggest.json

Attenzione: i suggerimenti danno la FORMA della domanda, non il volume.
Zero suggerimenti per un seme va controprovato con due semi di controllo.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def google(seed: str, hl: str, gl: str) -> list[str]:
    # client=chrome e non firefox: verificato il 14/10/2026 su quattro semi, chrome rende
    # 15 suggerimenti e firefox 10. Il conteggio dei suggerimenti È un segnale del metodo
    # («molti suggerimenti = domanda vera»), quindi si usa la resa più ricca. La forma
    # della risposta è identica: [0] = query, [1] = elenco dei suggerimenti.
    url = ("https://suggestqueries.google.com/complete/search?client=chrome"
           f"&hl={hl}&gl={gl}&q={urllib.parse.quote(seed)}")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return json.loads(r.read().decode("utf-8", "replace"))[1]


def bing(seed: str) -> list[str]:
    url = "https://api.bing.com/osjson.aspx?query=" + urllib.parse.quote(seed)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return json.loads(r.read().decode("utf-8", "replace"))[1]


def main() -> None:
    ap = argparse.ArgumentParser(description="Autocomplete keyless (Google + Bing)")
    ap.add_argument("seeds", nargs="*", help="semi da espandere")
    ap.add_argument("--seeds-file", default=None, help="file con un seme per riga")
    ap.add_argument("--hl", default="it")
    ap.add_argument("--gl", default="it")
    ap.add_argument("--engine", default="both", choices=["google", "bing", "both"])
    ap.add_argument("--out", default=None, help="file .json di destinazione")
    args = ap.parse_args()

    seeds = list(args.seeds)
    if args.seeds_file:
        seeds += [l.strip() for l in open(os.path.expanduser(args.seeds_file)) if l.strip() and not l.startswith("#")]
    if not seeds:
        sys.exit("Nessun seme: passali come argomenti o con --seeds-file")

    per_seed: dict[str, dict[str, list[str]]] = {}
    tutti: list[str] = []
    for seed in seeds:
        res: dict[str, list[str]] = {}
        if args.engine in ("google", "both"):
            try:
                res["google"] = google(seed, args.hl, args.gl)
            except Exception as exc:  # noqa: BLE001
                res["google"] = []
                print(f"  ! google '{seed}': {type(exc).__name__}: {exc}", file=sys.stderr)
        if args.engine in ("bing", "both"):
            try:
                res["bing"] = bing(seed)
            except Exception as exc:  # noqa: BLE001
                res["bing"] = []
                print(f"  ! bing '{seed}': {type(exc).__name__}: {exc}", file=sys.stderr)
        per_seed[seed] = res
        tutti += res.get("google", []) + res.get("bing", [])
        n_google = len(res.get("google", []))
        n_bing = len(res.get("bing", []))
        etichetta = "=== 0: controprova necessaria" if (n_google == 0 and args.engine != "bing") else ""
        print(f"[{seed}] google={n_google} bing={n_bing} {etichetta}")
        for s in res.get("google", [])[:6]:
            print(f"    - {s}")

    unici = sorted({s.strip() for s in tutti if s.strip()}, key=lambda x: x.lower())
    print(f"\n# TOTALE suggerimenti={len(tutti)} unici={len(unici)} su {len(seeds)} semi")
    for s in unici[:40]:
        print(f"  * {s}")

    if args.out:
        path = os.path.abspath(os.path.expanduser(args.out))
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        json.dump({"hl": args.hl, "gl": args.gl, "engine": args.engine, "per_seed": per_seed,
                   "unici": unici}, open(path, "w"), ensure_ascii=False, indent=1)
        print(f"# scritto: {path}")


if __name__ == "__main__":
    main()
