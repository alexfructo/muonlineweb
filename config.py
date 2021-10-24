################################################################################################################################
#   Continente MU Web Page
#
#   @author     Alex <alexfructo@gmail.com>
#   @version    1.0.0
#   @date       18/04/2019   
################################################################################################################################


################################################################################################################################
#   SQL SERVER CONNECTION SETTINGS
################################################################################################################################

SQL_DRIVER  = "{ODBC Driver 17 for SQL Server}"    # SQL SERVER ODBC DRIVER NAME
SQL_HOST    = "localhost"       # SQL SERVER HOST OR IP
SQL_USER    = "alex"            # SQL SERVER USERNAME
SQL_PASS    = "admin"           # SQL SERVER PASSWORD
SQL_BASE    = "MUOnline"        # SQL SERVER DATABASE
SQL_PORT    = 1433              # SQL SERVER TCP PORT

################################################################################################################################
#   EMAIL SMTP SETTINGS
################################################################################################################################

SMTP_HOST   = 'smtp.gmail.com'
SMTP_PORT   = 465
SMTP_SSL    = True
SMTP_USER   = ''
SMTP_PASS   = ''

################################################################################################################################
#   MU ONLINE SERVER SETTINGS
################################################################################################################################

SERVER_NAME     = "Continente MU"   # SERVER GAME NAME
SERVER_CSPORT   = "44405"           # SERVER GAME CONNECT PORT
SERVER_MAX_PLAY = 100               # SERVER MAX PLAYERS ON
CHAR_CNAME_COST = 50                # CASH COST TO CHARACTER CHANGE NAME

################################################################################################################################
#   APP SETTINGS
################################################################################################################################

WEB_SECRET_KEY      = ""    # APP SECRET KEY
WEB_PUBLIC_KEY      = "6LcGX-4UAAAAAFjOUz3mkqm7X_lHME6itambsphh"    # APP PUBLIC KEY
WEB_HOST            = "localhost"                                   # WEB SERVER HOST OR IP
WEB_PORT            = 80                                            # WEB SERVER TCP PORT
WEB_DEBUG           = True                                          # APP DEBUG MODE
WEB_TIMEZONE        = 'America/Sao_Paulo'                           # APP SERVER TIMEZONE
WEB_LOCALE          = ['pt_BR', 'pt']                               # APP INTERNALIZATION (i18n)

