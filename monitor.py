#!/usr/bin/env python3
"""Monitor da apuração 2026 (dados oficiais do TSE), atualizando a cada 10 segundos.

Uso:
    python3 monitor.py              # abre o painel no navegador (http://localhost:8000)
    python3 monitor.py --terminal   # mostra os resultados direto no terminal

Opções: --eleicao 6258 --uf br --cargo 1 --porta 8000 --ciclo ele2026
Só usa a biblioteca padrão do Python (3.8+), nada para instalar.
"""

import argparse
import http.server
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser

TSE = "https://resultados.tse.jus.br"
INTERVALO = 10
PASTA = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (monitor-apuracao-2026)"
ARQUIVOS = {"/index.html", "/manifest.webmanifest", "/sw.js",
            "/icons/icon-180.png", "/icons/icon-192.png", "/icons/icon-512.png"}


def baixar(caminho):
    req = urllib.request.Request(TSE + caminho, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(), r.headers.get("Content-Type", "application/octet-stream")


def descobrir_ciclo(padrao="ele2026"):
    try:
        dados, _ = baixar("/oficial/comum/config/ele-c.json")
        return json.loads(dados).get("c") or padrao
    except Exception:
        return padrao


def caminho_resultado(ciclo, eleicao, uf, cargo):
    return "/oficial/%s/%s/dados-simplificados/%s/%s-c%04d-e%06d-r.json" % (
        ciclo, eleicao, uf, uf, int(cargo), int(eleicao))


# ---------------------------------------------------------------- painel web

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=PASTA, **kw)

    def do_GET(self):
        if self.path.startswith("/tse/"):
            return self.proxy(self.path[len("/tse"):])
        if self.path in ("/", ""):
            self.path = "/index.html"
        rota = self.path.split("?")[0]
        if rota not in ARQUIVOS and not re.match(r"^/fotos/\d+\.jpg$", rota):
            return self.send_error(404)
        return super().do_GET()

    def proxy(self, caminho):
        # só repassa arquivos do sistema de resultados do TSE
        if not caminho.startswith("/oficial/") or ".." in caminho:
            return self.send_error(403)
        try:
            corpo, tipo = baixar(caminho)
            self.send_response(200)
            self.send_header("Content-Type", tipo)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
        except urllib.error.HTTPError as e:
            self.send_error(e.code, "TSE respondeu %s" % e.code)
        except Exception as e:
            self.send_error(502, "Falha ao acessar o TSE: %s" % e)

    def log_message(self, fmt, *args):
        pass


def painel(args):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", args.porta), Handler)
    url = "http://localhost:%d/?ele=%s" % (args.porta, args.eleicao)
    if args.ciclo:
        url += "&ciclo=" + args.ciclo
    print("Painel da apuração rodando em: " + url)
    print("Deixe esta janela aberta. Para encerrar, aperte Ctrl+C.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")


# ------------------------------------------------------------ modo terminal

def num(x):
    return int("".join(ch for ch in str(x or "") if ch.isdigit()) or 0)


def pct(x):
    try:
        return float(str(x or "0").replace(".", "").replace(",", "."))
    except ValueError:
        return 0.0


def br(n):
    return "{:,}".format(n).replace(",", ".")


def brp(p):
    return ("%.2f" % p).replace(".", ",") + "%"


def terminal(args):
    ciclo = args.ciclo or descobrir_ciclo()
    caminho = caminho_resultado(ciclo, args.eleicao, args.uf, args.cargo)
    anterior, deltas, ult_hora = {}, {}, None
    if os.name == "nt":
        os.system("")  # habilita cores ANSI no Windows
    while True:
        inicio = time.time()
        try:
            d = json.loads(baixar(caminho)[0])
            hora = (d.get("dg", ""), d.get("hg", ""), d.get("st"))
            cands = sorted(d.get("cand", []), key=lambda c: -num(c.get("vap")))
            if hora != ult_hora:
                if ult_hora is not None:
                    deltas = {c["sqcand"]: num(c.get("vap")) - anterior.get(c["sqcand"], 0) for c in cands}
                anterior = {c["sqcand"]: num(c.get("vap")) for c in cands}
                ult_hora = hora
            linhas = [
                "\033[2J\033[H\033[1mAPURAÇÃO 2026 — %s %s turno — TSE\033[0m" % (
                    "BRASIL" if args.uf == "br" else args.uf.upper(), (d.get("t", "") + "º") if d.get("t") else ""),
                "Seções totalizadas: \033[1m%s\033[0m (%s de %s)   Totalização TSE: %s %s" % (
                    brp(pct(d.get("pst"))), br(num(d.get("st"))), br(num(d.get("s"))), d.get("dg", ""), d.get("hg", "")),
                "",
            ]
            for c in cands:
                p = pct(c.get("pvap"))
                barra = "█" * int(round(p / 2.5))
                extra = "  +%s" % br(deltas[c["sqcand"]]) if deltas.get(c["sqcand"]) else ""
                st = ("  [%s]" % c["st"]) if c.get("st") else ""
                linhas.append("%-24s %7s  %13s votos  %s%s%s" % (
                    (c.get("nm") or "")[:24], brp(p), br(num(c.get("vap"))), barra, extra, st))
            if len(cands) >= 2:
                linhas.append("")
                linhas.append("Vantagem: %s votos" % br(num(cands[0].get("vap")) - num(cands[1].get("vap"))))
            linhas.append("")
            linhas.append("Brancos %s · Nulos %s · Abstenção %s · Comparecimento %s" % (
                brp(pct(d.get("pvb"))), brp(pct(d.get("ptvn") or d.get("pvn"))),
                brp(pct(d.get("pa"))), brp(pct(d.get("pc")))))
            linhas.append("Consultado às %s · atualiza a cada %ds · Ctrl+C para sair" % (time.strftime("%H:%M:%S"), INTERVALO))
            print("\n".join(linhas), flush=True)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print("[%s] erro ao consultar %s%s: %s" % (time.strftime("%H:%M:%S"), TSE, caminho, e), flush=True)
        time.sleep(max(1, INTERVALO - (time.time() - inicio)))


def main():
    ap = argparse.ArgumentParser(description="Monitor da apuração 2026 (TSE)")
    ap.add_argument("--terminal", action="store_true", help="mostrar no terminal em vez do navegador")
    ap.add_argument("--eleicao", default="6258", help="código da eleição no site do TSE (padrão 6258)")
    ap.add_argument("--uf", default="br", help="br = Brasil, ou sigla do estado (sp, rj, ...)")
    ap.add_argument("--cargo", default="1", help="1 = Presidente, 3 = Governador")
    ap.add_argument("--ciclo", default="", help="pasta do ciclo no TSE (padrão: automático)")
    ap.add_argument("--porta", type=int, default=8000)
    args = ap.parse_args()
    args.uf = args.uf.lower()
    try:
        terminal(args) if args.terminal else painel(args)
    except KeyboardInterrupt:
        print("\nEncerrado.")
        sys.exit(0)


if __name__ == "__main__":
    main()
