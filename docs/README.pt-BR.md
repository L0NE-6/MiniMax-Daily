# 🧠 MiniMax Daily

**Check-in diário do MiniMax Code · renovação de OAuth · execução em arquivo único**

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Português (BR)**

> **Manutenção original por L0NE-6** · Versão: **v1.0.0** (2026-11-23)

## Limites de uso

O repositório oficial e os assets de Release são gratuitos. Não revenda, não coloque atrás de pagamento, não republique como edição interna ou exclusiva, não remova avisos de copyright e não use a identidade do autor ou os QR codes de doação para sugerir autorização oficial. Consulte [NOTICE.md](../NOTICE.md).

## O que faz

O projeto lê o arquivo de credencial Shared MCode OAuth do MiniMax Code, renova o access token quando ele está perto de expirar, consulta o estado do check-in do dia e envia o claim somente quando o servidor informa que a recompensa está disponível. O caminho legado com JWT no leveldb continua disponível para clientes antigos.

O fluxo principal usa apenas a biblioteca padrão do Python e requer Python 3.8 ou superior.

## Início rápido

1. Entre no cliente desktop do MiniMax Code.
2. Localize o arquivo OAuth, normalmente em `~/.minimax/auth/prod/cn/mcode-public/auth.json`.
3. Execute:

```bash
python minimax_daily.py status
python minimax_daily.py auto
```

Uma credencial renovada é gravada atomicamente no mesmo arquivo. A conta de execução precisa de permissão de leitura e escrita.

## Qinglong

1. Envie `minimax_daily.py`.
2. Coloque `auth.json` em um diretório privado e persistente.
3. Defina `MINIMAX_OAUTH_AUTH_FILE` para esse arquivo.
4. Crie a tarefa com `task minimax_daily.py auto`.
5. Uma execução diária, como `17 7 * * *`, é suficiente.

## GitHub Actions

O workflow está em [`.github/workflows/minimax.yml`](../.github/workflows/minimax.yml).

- Push para `main`: executa testes, compilação e Ruff.
- `workflow_dispatch`: grava o secret `MINIMAX_AUTH_JSON` em `$RUNNER_TEMP/auth.json` e executa `python minimax_daily.py auto`.

| Secret | Obrigatório | Valor |
| :--- | :---: | :--- |
| `MINIMAX_AUTH_JSON` | Sim para execução manual | JSON completo do `auth.json` do MiniMax |

Repositórios públicos não persistem tokens rotacionados. O workflow não faz commit, upload ou armazenamento do `auth.json`; o arquivo existe apenas no diretório temporário do Runner atual. Se o Refresh Token for rotacionado, o novo valor será perdido ao final do job, e o Secret poderá precisar de atualização antes da próxima execução.

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
| :--- | :---: | :--- |
| `MINIMAX_OAUTH_AUTH_FILE` | Condicional | Caminho do `auth.json` OAuth atual. |
| `MINIMAX_LS_LEVELDB` | Opcional | Diretório leveldb legado alternativo. |
| `MINIMAX_DESKTOP_VERSION` | Opcional | Versão desktop nos headers; padrão `3.1.6`. |

## CLI

| Comando | Comportamento |
| :--- | :--- |
| `python minimax_daily.py auto` | Consulta e faz check-in quando disponível. |
| `python minimax_daily.py status` | Apenas consulta o estado. |
| `python minimax_daily.py login` | Inicia o Device Flow e aguarda confirmação no navegador. |

## Critérios de sucesso

| Resultado | Significado | Código de saída |
| :--- | :--- | :---: |
| `CLAIMED` | `claim_result=1`, recompensa recebida. | 0 |
| `ALREADY` | Já recebido hoje, inclusive `claim_result=2` idempotente. | 0 |
| `PENDING` | Disponível, mas o modo status não enviou claim. | 0 |
| `INACTIVE` | Nenhum item ativo ou recebível hoje. | 0 |
| `NO_SESSION` | Sessão inválida. | 1 |
| `NETWORK` | Falha de rede. | 1 |
| `NO_AUTH` | Nenhuma credencial encontrada. | 2 |
| `ERROR` | Erro de API, JSON, parâmetro ou execução. | 1 ou 2 |

HTTP 200 sozinho não é sucesso. O estado do servidor, a resposta do claim, os pontos e a sequência de dias são a evidência de aceite.

## Privacidade e aviso

O repositório não contém conta, telefone, token, JWT ou dados de dispositivo. O script não imprime valores de credenciais. Não publique `auth.json`, cookies ou tráfego autenticado completo em uma issue.

Este projeto independente não é afiliado nem endossado pela MiniMax. A API pode mudar. Respeite os termos de serviço e use por sua conta e risco.

## Apoio

<p align="center">
  <img src="../assets/donate-wechat.png" width="220" alt="QR de doação WeChat" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../assets/donate-alipay.jpg" width="220" alt="QR de doação Alipay" />
</p>

Os QR codes servem apenas para gorjetas voluntárias ao autor. Cobranças de terceiros por download, implantação, edição privada ou acesso a grupo de membros não são autorizadas.

## Star History

<a href="https://star-history.com/#L0NE-6/MiniMax-Daily&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
    <img alt="MiniMax Daily Star History" src="https://api.star-history.com/svg?repos=L0NE-6/MiniMax-Daily&type=Date" />
  </picture>
</a>
