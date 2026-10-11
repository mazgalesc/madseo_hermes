#!/usr/bin/env python3
"""Genera un'immagine per il sito con gemini-3-pro-image (Agent Platform, modalita' express).

Uso:
  ~/seo-content/.venv/bin/python genera-immagine.py --tipo copertina --prompt "..." --out ~/seo-content/content/foo.png
  ~/seo-content/.venv/bin/python genera-immagine.py --tipo infografica --prompt-file /tmp/prompt.txt --out ...

Tipi: "copertina" (16:9, 4K, ridotta a 1408x768) e "infografica" (3:2, 2K, ridotta a 1264x848).

Accanto al file grande (PNG, l'originale) salva sempre:
  - `<nome>-web.webp` — la versione da **caricare su WordPress** (WebP: -95/96% di peso);
  - `<nome>-anteprima.jpg` — un'anteprima leggera per guardarla.
Se `cwebp` non c'e' (`brew install webp`), il file per il web resta PNG e lo script lo segnala:
non caricare un PNG da centinaia di KB quando il WebP ne pesa venti.
"""
import argparse
import pathlib
import struct
import subprocess
import sys
import time

PRESET = {
    "copertina": {"aspect": "16:9", "size": "4K", "web": (1408, 768)},
    "infografica": {"aspect": "3:2", "size": "2K", "web": (1264, 848)},
    "logo": {"aspect": "1:1", "size": "4K", "web": (1024, 1024)},
}


def chiave_google() -> str:
    env = pathlib.Path.home() / ".hermes" / ".env"
    for riga in env.read_text().splitlines():
        if riga.startswith("GOOGLE_API_KEY="):
            return riga.split("=", 1)[1].strip()
    raise SystemExit("GOOGLE_API_KEY non trovata in ~/.hermes/.env")


def main() -> int:
    ap = argparse.ArgumentParser(description="Genera un'immagine per il sito")
    ap.add_argument("--tipo", choices=sorted(PRESET), default="copertina")
    ap.add_argument("--prompt", help="testo del prompt")
    ap.add_argument("--prompt-file", help="file che contiene il prompt")
    ap.add_argument("--out", required=True, help="percorso del PNG da salvare")
    ap.add_argument("--modello", default="gemini-3-pro-image")
    args = ap.parse_args()

    if args.prompt_file:
        prompt = pathlib.Path(args.prompt_file).read_text().strip()
    elif args.prompt:
        prompt = args.prompt.strip()
    else:
        raise SystemExit("serve --prompt o --prompt-file")

    preset = PRESET[args.tipo]
    from google import genai
    from google.genai import types

    client = genai.Client(vertexai=True, api_key=chiave_google())
    uscita = pathlib.Path(args.out).expanduser()
    uscita.parent.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    risposta = client.models.generate_content(
        model=args.modello,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio=preset["aspect"], image_size=preset["size"]),
        ),
    )
    dt = time.time() - t0

    salvata = False
    for parte in risposta.candidates[0].content.parts:
        if getattr(parte, "inline_data", None) and parte.inline_data.data:
            dati = parte.inline_data.data
            uscita.write_bytes(dati)
            larghezza, altezza = struct.unpack(">II", dati[16:24])
            print(f"originale: {larghezza}x{altezza} px | {len(dati)/1_000_000:.1f} MB | {dt:.0f}s")
            salvata = True
        elif getattr(parte, "text", None):
            print("testo dal modello:", parte.text[:200].strip())

    if not salvata:
        print("NESSUN DATO IMMAGINE nella risposta", file=sys.stderr)
        return 1

    # versione per il web (WebP) e anteprima (macOS: sips per ridimensionare, cwebp per il formato)
    #
    # Perche' WebP e non PNG: misurato sul campo il 21/09/2026, una copertina passa da
    # 595 KB a 22 KB (-96%) e la 768x515 servita ai telefoni da 346 KB a 16 KB (-95%).
    # Il PNG resta come originale, ma quello che si carica su WordPress e' il WebP.
    # Le infografiche hanno molto testo: qualita' piu' alta, altrimenti le lettere si impastano.
    larghezza_web, altezza_web = preset["web"]
    qualita = 88 if args.tipo == "infografica" else 82
    ridotta = uscita.with_name(uscita.stem + "-web.png")
    web = uscita.with_name(uscita.stem + "-web.webp")
    anteprima = uscita.with_name(uscita.stem + "-anteprima.jpg")
    subprocess.run(["sips", "-z", str(altezza_web), str(larghezza_web), str(uscita), "--out", str(ridotta)],
                   capture_output=True, check=False)
    if not ridotta.exists():          # alcuni macOS non accettano -z su quel PNG: prova il ridimensionamento a larghezza
        subprocess.run(["sips", "--resampleWidth", str(larghezza_web), str(uscita), "--out", str(ridotta)],
                       capture_output=True, check=False)
    fatto_webp = False
    if ridotta.exists():
        esito = subprocess.run(["cwebp", "-q", str(qualita), "-quiet", str(ridotta), "-o", str(web)],
                               capture_output=True, check=False)
        fatto_webp = web.exists() and web.stat().st_size > 0
        if not fatto_webp:
            print("ATTENZIONE: cwebp non ha prodotto il WebP; resta il PNG per il web "
                  f"({esito.returncode}). Installalo con: brew install webp", file=sys.stderr)
        ridotta.unlink(missing_ok=True)   # il PNG ridotto non serve piu': resta l'originale grande
    else:
        print("ATTENZIONE: sips non ha ridimensionato: carica il PNG originale", file=sys.stderr)
    subprocess.run(["sips", "-Z", "1400", "-s", "format", "jpeg", "-s", "formatOptions", "82",
                    str(uscita), "--out", str(anteprima)], capture_output=True, check=False)
    for f in (web, anteprima):
        if f.exists():
            print(f"{f.name}: {f.stat().st_size/1000:.0f} KB  ({larghezza_web}x{altezza_web})")
    if not fatto_webp:
        print("ATTENZIONE: il file per il web e' PNG, non WebP: pesera' circa 15 volte tanto.", file=sys.stderr)
    print(f"salvata in {uscita}")
    if args.tipo == "infografica":
        print("ATTENZIONE: guarda l'immagine e verifica che testo e disposizione siano corretti "
              "prima di usarla (il modello puo' sbagliare la griglia).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
