# Apuração 2026: app de celular em tempo real

Tudo numa tela só do celular, atualizando sozinho a cada 10 segundos:

- **Presidente, Brasil:** foto, porcentagem e votos de cada candidato (Lula em **vermelho**,
  Flávio em **azul**), % de seções apuradas, quem está à frente e por quantos votos.
- **Governador do Espírito Santo:** foto, porcentagem e votos dos candidatos. Se o ES não tiver
  2º turno para governador, mostra o resultado do 1º turno com quem foi **eleito**.
- **Presidente por estado:** os 27 estados + exterior em quadradinhos, cada um com % apurado e a
  barra vermelho/azul com a porcentagem de cada candidato (ES em destaque). Ordena por A–Z,
  % apurado ou nº de eleitores.

Fotos: primeiro a foto oficial do TSE; se ela não carregar, a foto da Wikipédia (Lula e Flávio).

Os dados são os mesmos arquivos que o site oficial usa (`resultados.tse.jus.br`), eleição **6258**.

## Instalar no celular (sem senha, sem loja)

### 1. Publicar o app (uma vez só, pelo navegador do celular em github.com)

1. Abra **github.com/veyronerp/apuracao-2026 → Settings**.
   (No celular, se não aparecer "Settings", use o menu do navegador → "Versão para computador".)
2. **General → Danger Zone → Change visibility → Make public.** O GitHub Pages grátis só funciona
   em repositório público. O repositório não tem nenhum dado pessoal nem senha.
3. **Pages** (menu da esquerda) → *Source*: **Deploy from a branch** → Branch:
   **ccr-b6bec831-6or9ox**, pasta **/ (root)** → **Save**.
4. Espere 1–2 minutos. O app fica em: **https://veyronerp.github.io/apuracao-2026/**

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
