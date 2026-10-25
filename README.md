# Apuração 2026: app de celular em tempo real

Tudo numa tela só do celular, atualizando sozinho a cada 10 segundos:

- **Presidente, Brasil:** foto, porcentagem e votos de cada candidato (Lula em **vermelho**,
  Flávio em **azul**), % de seções apuradas e a **diferença de votos** entre os dois.
- **Governador do Espírito Santo:** foto, porcentagem e votos dos candidatos. Se o ES não tiver
  2º turno para governador, mostra o resultado do 1º turno com quem foi **eleito**. Também com a
  **diferença de votos**.
- **Presidente por estado:** os 27 estados + exterior em quadradinhos, cada um com % apurado e a
  barra vermelho/azul com a porcentagem de cada candidato e a **diferença de votos** (ES em destaque). Ordena por A–Z,
  % apurado ou nº de eleitores, e filtrar só os estados onde **Lula** ou **Flávio** está à frente.

Todos os números (votos, %, diferença) vêm exatamente dos arquivos oficiais do TSE. As fotos carregam
separado e nunca atrasam a atualização dos números.

**Fotos:** a automação *Copiar fotos do TSE* (aba **Actions** do GitHub) copia as fotos oficiais dos
candidatos do TSE para a pasta `fotos/` a cada push e a cada 20 min nos dias 25 e 26/10. Para rodar na
hora: Actions → Copiar fotos do TSE → **Run workflow**. O app usa essa cópia; se faltar, busca direto no
TSE e, para Lula e Flávio, na Wikipédia. Fotos que falharem são tentadas de novo a cada minuto.

Os dados são os mesmos arquivos que o site oficial usa (`resultados.tse.jus.br`): Presidente 2º turno = eleição
**6258**, Governador 2º turno = eleição **6260** (1º turno: 6257 e 6259). Formato 2026:
`/oficial/ele2026/<eleição>/dados/<uf>/<uf>-c<cargo>-e<eleição>-u.json` e fotos em
`/oficial/ele2026/<eleição>/fotos/<uf>/<sqcand>.jpeg`. O TSE libera a leitura direta (CORS) para `veyronerp.github.io`.

## Instalar no celular (sem senha, sem loja)

### 1. Abrir o app

👉 **https://raw.githack.com/veyronerp/2026/main/index.html**

Funciona na hora, sem configurar nada: o githack mostra os arquivos deste repositório público como site.
Cada correção enviada para o `main` aparece em poucos minutos.

**Opcional, endereço mais curto:** **https://veyronerp.github.io/2026/** depois de ativar o GitHub Pages
(uma vez só, pelo navegador do celular, não pelo app do GitHub):

1. Digite **github.com/veyronerp/2026/settings/pages** no Chrome/Safari.
   (Se a página vier cortada, menu do navegador → "Versão para computador".)
2. *Source*: **Deploy from a branch** → Branch: **main**, pasta **/ (root)** → **Save**.
3. Espere 1–2 minutos e abra o link acima.

### 2. Colocar na tela inicial

- **Android (Chrome):** abra o link → menu ⋮ → **Instalar app** (ou "Adicionar à tela inicial").
- **iPhone (Safari):** abra o link → botão Compartilhar → **Adicionar à Tela de Início**.

Pronto: vira um ícone "Apuração" que abre em tela cheia. Toque em **Manter tela ligada** para o
celular não apagar enquanto você acompanha.

## Como os dados chegam

O app busca os arquivos direto do TSE. Se o navegador bloquear (regra de segurança CORS), ele tenta
automaticamente proxies públicos gratuitos (allorigins, corsproxy, codetabs), que só repassam os arquivos
públicos do TSE. No rodapé do app aparece qual fonte está em uso.

## Outra eleição

No app, abra **Configurar eleição** e cole o link do site do TSE (ou digite o código da eleição).

## No computador (opcional)

Com Python 3: `python3 monitor.py` abre o painel em http://localhost:8000 usando um proxy local
(não depende dos proxies públicos). `python3 monitor.py --terminal` mostra o resultado no terminal.
No Windows, dois cliques em `iniciar-windows.bat`.

## Observações

- 10 s é o mesmo intervalo mínimo do botão "atualizar" do site do TSE. Não diminua: o TSE bloqueia
  temporariamente quem faz requisições demais.
- O resultado oficial é sempre o publicado pelo TSE.
