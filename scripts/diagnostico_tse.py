#!/usr/bin/env python3
"""Diagnóstico: mostra como o site de resultados do TSE organiza os arquivos deste ano."""

import json
import re
import urllib.error
import urllib.request

TSE = "https://resultados.tse.jus.br"
UA = {"User-Agent": "Mozilla/5.0 (apuracao-2026 diagnostico)"}


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers or {})
    except Exception as e:
        return "ERRO %s" % e, b"", {}


st, cfg, hd = get(TSE + "/oficial/comum/config/ele-c.json")
print("== ele-c.json:", st, "| CORS:", hd.get("Access-Control-Allow-Origin"))
print(cfg[:6000].decode("utf-8", "replace"))

st, html, _ = get(TSE + "/oficial/app/index.html")
print("\n== app/index.html:", st)
scripts = re.findall(r'src="([^"]+\.js)"', html.decode("utf-8", "replace"))
print("scripts:", scripts)
padroes = set()
for s in scripts:
    st, js, _ = get(TSE + "/oficial/app/" + s.lstrip("./"))
    txt = js.decode("utf-8", "replace")
    print("--", s, st, len(txt))
    for m in re.finditer(r'.{0,140}(dados-simplificados|fotos/|-r\.json|\.jpeg|config/).{0,140}', txt):
        padroes.add(m.group(0))
print("\n== trechos com caminhos de arquivos (%d):" % len(padroes))
for p in sorted(padroes)[:60]:
    print("  ", p)

try:
    c = json.loads(cfg)
    ciclo = c.get("c")
    for pl in c.get("pl", []):
        for e in pl.get("e", []):
            cd = int(e["cd"])
            for uf, cargo in (("br", 1), ("es", 3)):
                for url in ("%s/oficial/%s/%d/dados-simplificados/%s/%s-c%04d-e%06d-r.json" % (TSE, ciclo, cd, uf, uf, cargo, cd),
                            "%s/oficial/%s/%d/dados/%s/%s-c%04d-e%06d-u.json" % (TSE, ciclo, cd, uf, uf, cargo, cd)):
                    st, body, _ = get(url)
                    print(st, url, body[:150])
except Exception as e:
    print("erro ao testar caminhos:", e)
