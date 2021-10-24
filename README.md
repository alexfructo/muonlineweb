# Continente MU Web Page

Página web simples para servidores de MU Online.

Desenvolvido com Python/Flask.

## Funcionalidades
  
* Cadastro de jogadores.
* Painel de gerenciamento para jogadores.
* Cadastro e gerenciamento de notícias para o administrador do servidor.

## Instalação

Utilize o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar as dependências do projeto.

```bash
pip install -r requirements.txt
```

## Configuração

As configurações básicas estão no arquivo "config.py" conexão com MSSQL, SMTP e GameServer.
```python
SQL_DRIVER  = "{ODBC Driver 17 for SQL Server}" # SQL SERVER ODBC DRIVER NAME
SQL_HOST    = "localhost"                          
SQL_USER    = ""                                    
SQL_PASS    = ""                                    
SQL_BASE    = ""                                    
SQL_PORT    = 1433                                 

SMTP_HOST   = 'smtp.gmail.com'
SMTP_PORT   = 465
SMTP_SSL    = True
SMTP_USER   = ''
SMTP_PASS   = ''

SERVER_NAME     = "Continente MU"   # SERVER GAME NAME
SERVER_CSPORT   = "44405"           # SERVER GAME CONNECT PORT
SERVER_MAX_PLAY = 100               # SERVER MAX PLAYERS ON
CHAR_CNAME_COST = 50                # CASH COST TO CHARACTER CHANGE NAME
```

## Pré visualização
