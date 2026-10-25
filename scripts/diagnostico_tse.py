#!/usr/bin/env python3
"""Diagnóstico: mostra arquivos reais do TSE de 2026 (formato e fotos)."""

import urllib.error
import urllib.request

TSE = "https://resultados.tse.jus.br/oficial/ele2026"
UA = {"User-Agent": "Mozilla/5.0 (apuracao-2026 diagnostico)", "Origin": "https://veyronerp.github.io"}


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=10) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, b"", {}
    except Exception as e:
        return "ERRO %s" % e, b"", {}


for url, n in ((TSE + "/6258/dados/br/br-c0001-e006258-u.json", 9000),
               (TSE + "/6260/dados/es/es-c0003-e006260-u.json", 9000),
               (TSE + "/6258/dados/sp/sp-c0001-e006258-u.json", 600)):
    st, body, _ = get(url)
    print("\n== CONTEÚDO", st, url, len(body))
    print(body[:n].decode("utf-8", "replace"))

for p in ("6258/fotos/br/280002542548.jpeg", "6258/fotos/br/280002542548.jpg", "6258/fotos/br/280002551544.jpeg",
          "6257/fotos/br/280002542548.jpeg", "6258/fotos/br/br280002542548.jpeg", "6258/fotos/br/280002542548.png"):
    st, body, hd = get(TSE + "/" + p)
    print("FOTO", st, p, len(body), hd.get("Content-Type"))
