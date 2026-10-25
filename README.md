# Apuração 2026 — monitor em tempo real

Painel que mostra a apuração oficial do TSE e **se atualiza sozinho a cada 10 segundos**.
Usa os mesmos arquivos de dados do site oficial
(`resultados.tse.jus.br`), então os números são os mesmos de lá.

Por padrão abre a eleição **6258 / Brasil / Presidente**, a do link:
https://resultados.tse.jus.br/oficial/app/index.html#/eleicao/6258/uf/br/cargo/1/vis/nominal/resultados

## Como usar (o jeito mais fácil)

Precisa do Python 3 instalado (https://www.python.org/downloads/; no Windows marque
"Add Python to PATH" na instalação). Nada mais precisa ser instalado.

1. Baixe o projeto: botão verde **Code → Download ZIP** no GitHub e descompacte.
2. **Windows:** dê dois cliques em `iniciar-windows.bat`.
   **Mac/Linux:** abra o terminal na pasta e rode `python3 monitor.py`.
3. O navegador abre em **http://localhost:8000** com o painel. Deixe a janela preta aberta.

### Só no terminal (sem navegador)

```
python3 monitor.py --terminal
```

## O que o painel mostra

- % de seções totalizadas e o horário da última totalização do TSE
- Cada candidato: % dos votos válidos, total de votos, foto, e quantos votos ganhou na última atualização
- Vantagem do 1º sobre o 2º (em votos e pontos percentuais)
- Eleitorado, comparecimento, abstenção, brancos e nulos
- Histórico das atualizações durante a sessão
- O título da aba mostra quem lidera e o % apurado (dá para acompanhar com a aba em segundo plano)

## Outra eleição, estado ou cargo

No painel, abra **"Configurar eleição / estado / cargo"** e cole o link do site do TSE
(ou preencha os campos). Pelo terminal:

```
python3 monitor.py --eleicao 6258 --uf sp --cargo 3    # Governador de SP
```

Cargos: 1 = Presidente, 3 = Governador, 5 = Senador.

## Por que precisa do `monitor.py`?

O navegador normalmente bloqueia uma página de outro site de ler os dados do TSE (regra de
segurança chamada CORS). O `monitor.py` roda um servidorzinho só no seu computador
(`127.0.0.1`) que busca os arquivos no TSE e entrega ao painel. Ele só repassa endereços
`resultados.tse.jus.br/oficial/...`. Se você abrir o `index.html` direto e o TSE permitir o
acesso, também funciona sem o `monitor.py`.

## Observações

- O intervalo é de 10 s, o mesmo mínimo do botão "atualizar" do site do TSE. Não diminua:
  o TSE bloqueia temporariamente IPs que fazem requisições demais.
- O resultado oficial é sempre o publicado pelo TSE.
