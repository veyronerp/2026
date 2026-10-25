#!/usr/bin/env python3
"""Copia as fotos dos candidatos do TSE para a pasta fotos/ (usada pelo app).

Busca os candidatos a Presidente (Brasil) e a Governador do ES nos arquivos de resultados
e baixa a foto de cada um. Tenta primeiro a pasta de fotos do sistema de resultados e,
se não achar, a foto do perfil no DivulgaCandContas. Fotos já baixadas não são baixadas de novo.
Nunca falha o job: só informa o que conseguiu.
"""

import json
import os
import sys
import urllib.request

TSE = "https://resultados.tse.jus.br"
DIVULGA = "https://divulgacandcontas.tse.jus.br/divulga/rest"
ELEICAO = int(os.environ.get("ELEICAO", "6258"))
ANO = 2026
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fotos")
UA = {"User-Agent": "Mozilla/5.0 (apuracao-2026 fotos)"}


def baixar(url, timeout=20):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def json_de(url):
    return json.loads(baixar(url))


def eh_imagem(b):
    return len(b) > 1500 and (b[:3] == b"\xff\xd8\xff" or b[:8] == b"\x89PNG\r\n\x1a\n")


def resultado(ciclo, ele, uf, cargo):
    return json_de("%s/oficial/%s/%d/dados-simplificados/%s/%s-c%04d-e%06d-r.json" % (TSE, ciclo, ele, uf, uf, cargo, ele))


def main():
    os.makedirs(PASTA, exist_ok=True)
    try:
        cfg = json_de(TSE + "/oficial/comum/config/ele-c.json")
    except Exception as e:
        print("Não consegui ler a configuração do TSE:", e)
        cfg = {}
    ciclo = cfg.get("c") or "ele%d" % ANO
    eleicoes = [ELEICAO] + sorted({int(e["cd"]) for pl in cfg.get("pl", []) for e in pl.get("e", [])
                                   if str(e.get("cd", "")).isdigit()} - {ELEICAO}, reverse=True) + [ELEICAO - 1]

    # id da eleição no DivulgaCandContas (perfil dos candidatos), se disponível
    divulga_ids = []
    try:
        for e in json_de(DIVULGA + "/v1/eleicao/ordinarias"):
            if int(e.get("ano", 0)) == ANO:
                divulga_ids.append(e["id"])
    except Exception as e:
        print("DivulgaCandContas indisponível:", e)

    alvos = []  # (sqcand, nome, eleicao, uf)
    for uf, cargo, rotulo in (("br", 1, "Presidente"), ("es", 3, "Governador ES")):
        for ele in eleicoes:
            try:
                d = resultado(ciclo, ele, uf, cargo)
            except Exception:
                continue
            if d.get("cand"):
                print("%s: eleição %d, %d candidatos" % (rotulo, ele, len(d["cand"])))
                alvos += [(c["sqcand"], c.get("nm", ""), ele, uf) for c in d["cand"]]
                break
        else:
            print("%s: arquivo de resultados não encontrado" % rotulo)

    novas = 0
    for sq, nome, ele, uf in alvos:
        destino = os.path.join(PASTA, "%s.jpg" % sq)
        if os.path.exists(destino):
            continue
        urls = ["%s/oficial/%s/%d/fotos/%s/%s.%s" % (TSE, ciclo, e, uf, sq, ext)
                for e in dict.fromkeys([ele] + eleicoes) for ext in ("jpeg", "jpg")]
        urls += ["%s/arquivo/img/%s/%s/%s" % (DIVULGA, i, sq, uf.upper()) for i in divulga_ids]
        for url in urls:
            try:
                b = baixar(url)
            except Exception:
                continue
            if eh_imagem(b):
                with open(destino, "wb") as f:
                    f.write(b)
                novas += 1
                print("foto de %s (%s) <- %s" % (nome, sq, url))
                break
        else:
            print("sem foto para %s (%s)" % (nome, sq))
    print("%d foto(s) nova(s)" % novas)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Erro:", e)
    sys.exit(0)
