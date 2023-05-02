[![Not Maintained](https://img.shields.io/badge/Maintenance%20Level-Not%20Maintained-yellow.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)<br>
[![CodeFactor](https://www.codefactor.io/repository/github/hermengardo/mtp_facebook_group_scraper/badge)](https://www.codefactor.io/repository/github/hermengardo/mtp_facebook_group_scraper)

# Introdução
- Raspador para publicações em grupos do facebook.
- Desenvolvido para a matéria de Métodos e Técnicas de Pesquisa II (USP/2022).

# Instalação

1. Clone o repositório
```sh
git clone https://github.com/hermengardo/MTP_facebook_group_scraper.git
```

2. Instale os requerimentos
```sh
pip install -r requirements.txt
```

3. Edite e execute o arquivo *main.py*

- **Nota**: é necessário possuir o Mozilla Firefox instalado em seu computador.

# Exemplo de uso

```python
from scraper import Scraper


def main():
    Scraper(email="seu_email",
            password="sua_senha",
            group_id="nome_do_grupo", # Encontrado em: facebook.com/groups/nome_do_grupo
            pages=1)


if __name__ == "__main__":
    main()
```

# Descrição
| param         | type       | description |
| ------------- | ------------- | ----------- |
| email | str | facebook email |
| password | str | facebook password |
| group_id | int | nome ou id do grupo |
| pages| int | o número máximo de páginas para raspar ||

- Qualquer falha de coleta será salva em "log.txt"
- Não é necessário instalar o Geckodriver ou qualquer outro webdriver.
