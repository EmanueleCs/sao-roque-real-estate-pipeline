# São Roque Real Estate Pipeline

Pipeline de dados end-to-end que coleta anúncios de aluguel de imóveis em São Roque/SP (fonte: [guiasaoroque.com.br](https://www.guiasaoroque.com.br/)), armazena, transforma e disponibiliza os dados em um dashboard online.

Projeto de estudo em engenharia de dados — construído para praticar todo o ciclo: coleta, armazenamento em nuvem, modelagem, transformação e visualização.

## Arquitetura

```
guiasaoroque.com.br
        │  scraping (Selenium)
        ▼
  Scraper Python
        │  dados brutos (JSON)
        ▼
  Amazon S3 (raw zone)
        │  ETL (pandas / SQL)
        ▼
  PostgreSQL (Amazon RDS)
        │
        ▼
  Dashboard online
```

A camada raw (S3) fica separada da camada tratada (Postgres) de propósito: permite reprocessar os dados sem raspar o site novamente, e é o mesmo padrão usado em pipelines de produção (data lake → data warehouse).

A descoberta das URLs de imóveis é feita via Selenium, navegando pelas páginas de listagem em `/imoveis/`. O site disponibiliza um sitemap dedicado (`sitemap_imoveis.xml`), que seria a forma preferencial de descoberta de URLs por gerar menos carga no servidor — mas ele está indisponível no momento (retornando erro), então o scraper depende da navegação simulada até que isso seja reavaliado.

## Conformidade com robots.txt

O `robots.txt` do site-fonte foi revisado antes do desenvolvimento do scraper ([ver arquivo](https://www.guiasaoroque.com.br/robots.txt)). Pontos considerados:

- O bloco de `Disallow: /` se aplica nominalmente a bots de IA (`GPTBot`, `ClaudeBot`, `Google-Extended`, etc.) e a agregadores de treinamento de modelos — não a um scraper de uso próprio para fins analíticos.
- A diretiva `Content-Signal: ai-train=no, use=reference` reforça que o conteúdo não deve ser usado para treinar modelos de IA. Este projeto não treina modelos com os dados coletados; os dados são usados apenas para gerar estatísticas agregadas de mercado (preço médio, distribuição por bairro, etc.).
- A seção pública de imóveis (`/imoveis/`) não está nas regras de `Disallow` — apenas áreas administrativas (`/admin/`, `/imoveis/admin/`) e de promoções internas (`/guia/promocao/`) estão bloqueadas.
- O site disponibiliza um `Sitemap: sitemap_imoveis.xml`, que seria a forma preferencial de descobrir as URLs de anúncios (mais estruturada e com menor carga no servidor). No momento esse sitemap está indisponível, então a descoberta de URLs é feita via navegação simulada com Selenium, dentro da área pública `/imoveis/` (não bloqueada pelo `Disallow`).

Este projeto não redistribui o conteúdo original nem republica os anúncios — apenas extrai métricas agregadas para fins de estudo.

## Stack

| Camada | Tecnologia |
|---|---|
| Coleta | Python, Selenium |
| Armazenamento bruto | Amazon S3 |
| Banco de dados | PostgreSQL (Amazon RDS) |
| Transformação | Python (pandas), SQL |
| Orquestração | Cron / Airflow |
| Dashboard | Streamlit |
| Infraestrutura | AWS (S3, RDS, IAM) |

## Status do projeto

- [x] Scraper inicial com Selenium
- [ ] Armazenamento dos dados brutos no S3
- [ ] Modelagem e carga no PostgreSQL
- [ ] Pipeline de transformação (ETL)
- [ ] Orquestração/agendamento automático
- [ ] Dashboard publicado online

## Estrutura do repositório

```
.
├── scraper/          # Scripts de coleta (Selenium)
├── etl/              # Scripts de transformação e carga
├── sql/              # Scripts de criação de schema e queries analíticas
├── dashboard/         # Código do dashboard (Streamlit)
├── docs/             # Documentação e diagramas
└── README.md
```

## Como rodar localmente

```bash
# clonar o repositório
git clone https://github.com/<seu-usuario>/sao-roque-real-estate-pipeline.git
cd sao-roque-real-estate-pipeline

# criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate

# instalar dependências
pip install -r requirements.txt

# rodar o scraper
python scraper/main.py
```

Variáveis de ambiente necessárias (crie um arquivo `.env` na raiz):

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET_NAME=
DATABASE_URL=
```

## Dados coletados

Cada anúncio inclui: preço, bairro, área (m²), número de quartos, tipo de imóvel e data da coleta.

## Roadmap

- Expandir para outras fontes de dados da região.
- Histórico de preços por imóvel ao longo do tempo.
- Alertas automáticos de novos anúncios abaixo da média de mercado.

## Licença

MIT

## Aviso

Este projeto realiza web scraping apenas para fins educacionais, respeitando o `robots.txt` do site-fonte e sem uso comercial dos dados coletados.