#!/usr/bin/env python3
"""Diagnóstico: mostra como o site de resultados do TSE organiza os arquivos deste ano."""

import json
import re
import urllib.error
import urllib.request

TSE = "https://resultados.tse.jus.br"
UA = {"User-Agent": "Mozilla/5.0 (apuracao-2026 diagnostico)", "Origin": "https://veyronerp.github.io"}


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=10) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, b"", dict(e.headers or {})
    except Exception as e:
        return "ERRO %s" % e, b"", {}


st, cfg, hd = get(TSE + "/oficial/comum/config/ele-c.json")
print("== ele-c.json:", st)
print("== cabeçalhos:", {k: v for k, v in hd.items() if k.lower().startswith(("access-control", "cache", "content-type", "age", "x-"))})
c = json.loads(cfg)
for pl in c.get("pl", []):
    if pl.get("c") == "ele2026":
        print("pleito", pl.get("cd"), pl.get("dt"), [(e["cd"], e.get("cdt2"), e["nm"]) for e in pl.get("e", [])])

st, html, _ = get(TSE + "/oficial/app/index.html")
main = re.findall(r'src="(main[^"]+\.js)"', html.decode("utf-8", "replace"))
if main:
    st, js, _ = get(TSE + "/oficial/app/" + main[0])
    txt = js.decode("utf-8", "replace")
    print("\n== main.js", st, len(txt))
    vistos = set()
    for m in re.finditer(r'.{0,120}(\.json|\.jpeg|\.jpg|-c0|"-e"|-u\b|-r\b|-v\b).{0,120}', txt):
        s = m.group(0)
        k = s[100:160]
        if k in vistos:
            continue
        vistos.add(k)
        print("  >>", s)
        if len(vistos) > 70:
            break

print("\n== testes de caminhos")
achados = []
for ele, uf, cargo in ((6258, "br", 1), (6257, "br", 1), (6260, "es", 3), (6259, "es", 3), (6258, "es", 1)):
    base = "%s/oficial/ele2026/%d" % (TSE, ele)
    e6 = "e%06d" % ele
    for p in ("dados/{uf}/{uf}-c{c:04d}-{e}-u.json", "dados/{uf}/{uf}-c{c:04d}-{e}-v.json", "dados/{uf}/{uf}-c{c:04d}-{e}-r.json",
              "dados/{uf}/{uf}-{e}-ab.json", "dados/{uf}/{uf}-c{c:04d}-{e}-e.json", "dados/{uf}/{uf}-{e}-e.json",
              "dados-simplificados/{uf}/{uf}-c{c:04d}-{e}-r.json", "config/{uf}-{e}-cm.json", "config/mun-{e}-cm.json",
              "config/{uf}/{uf}-{e}-cm.json"):
        url = base + "/" + p.format(uf=uf, c=cargo, e=e6)
        st, body, hd = get(url)
        print(st, url, "CORS=", hd.get("Access-Control-Allow-Origin"))
        if st == 200:
            achados.append((url, body))
for url, body in achados:
    print("\n== CONTEÚDO", url, len(body))
    print(body[:2500].decode("utf-8", "replace"))
