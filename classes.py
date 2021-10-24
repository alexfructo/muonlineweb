from sql import MSSQL
from flask import flash, render_template, request
from flask_mail import Mail
import abc

class User:

    def __init__(self, username, password, email, personalid):
        self.username = username
        self.password = password
        self.email = email
        self.personalid = personalid

    @staticmethod
    def get_userid_byname(username):
        data = MSSQL.conn().execute("SELECT MEMB_GUID FROM MEMB_INFO WHERE MEMB___ID=?", username)
        data = data.fetchone()
        return data[0]

    @staticmethod
    def user_exists(username):
        query = "SELECT MEMB___ID FROM MEMB_INFO WHERE MEMB___ID=?"

        for rows in MSSQL.conn().execute(query, username):

            if rows[0] == username:
                return True
            else:
                return False

    @staticmethod
    def get_user(username):
        query = "SELECT MEMB___ID, CTL1_CODE, VIP, GOLD, CASH, VIPCREDIT FROM MEMB_INFO WHERE MEMB___ID =?"
        data = MSSQL.conn().execute(query, username)
        data = data.fetchone()
        return data

    @staticmethod
    def email_exists(email):
        query = "SELECT MAIL_ADDR FROM MEMB_INFO WHERE MAIL_ADDR=?"

        for rows in MSSQL.conn().execute(query, email):

            if rows[0] == email:
                return True
            else:
                return False

    @staticmethod
    def change_password(username, password):
        query = "UPDATE MEMB_INFO SET MEMB__PWD =? WHERE MEMB___ID =?"
        MSSQL.conn().execute(query, password, username)

    @staticmethod
    def change_personalid(username, personalid):
        query = "UPDATE MEMB_INFO SET SNO__NUMB =? WHERE MEMB___ID =?"
        MSSQL.conn().execute(query, personalid, username)

    def register(self):
        query = "INSERT INTO MEMB_INFO(MEMB___ID, MEMB_NAME, MEMB__PWD, SNO__NUMB, MAIL_ADDR, BLOC_CODE, CTL1_CODE) VALUES(?,?,?,?,?,?,?)"
        MSSQL.conn().execute(query, self.username, self.username,
                             self.password, self.personalid, self.email, '0', '0')


class Login:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def auth(self):
        query = "SELECT MEMB___ID, MEMB__PWD FROM MEMB_INFO WHERE MEMB___ID=? AND MEMB__PWD=?"

        for rows in MSSQL.conn().execute(query, self.username, self.password):

            if rows[0] == self.username:

                query = "INSERT INTO W_LOGIN(LOGIN_USERNAME, LOGIN_IP) VALUES (?,?)"
                MSSQL.conn().execute(query, self.username, request.remote_addr)
                return True
            else:
                return False

    @staticmethod
    def check_password(username, password):
        query = "SELECT MEMB___ID, MEMB__PWD FROM MEMB_INFO WHERE MEMB___ID=? AND MEMB__PWD=?"

        for rows in MSSQL.conn().execute(query, username, password):

            if rows[0] == username:
                return True
            else:
                return False

    @staticmethod
    def check_personalid(username, personalid):
        query = "SELECT MEMB___ID, SNO__NUMB FROM MEMB_INFO WHERE MEMB___ID=? AND SNO__NUMB=?"

        for rows in MSSQL.conn().execute(query, username, personalid):

            if rows[0] == username:
                return True
            else:
                return False

    @staticmethod
    def get_last_logon(username):
        query = ''' SELECT TOP 1 login_date, login_ip FROM W_LOGIN WHERE
	                (login_date < (SELECT MAX(login_date) FROM W_LOGIN)) AND login_username=?
                    ORDER BY login_date DESC
                '''
        data = MSSQL.conn().execute(query, username)
        data = data.fetchone()
        return data


class News:

    @staticmethod
    def get_news():
        data = MSSQL.conn().execute(
            "SELECT TOP 5 NEWS_ID, NEWS_DATE, NEWS_TITLE, NEWS_DESC FROM W_NEWS ORDER BY NEWS_DATE DESC;")
        data = data.fetchall()
        return data

    @staticmethod
    def get_new_byid(id):
        data = MSSQL.conn().execute(
            "SELECT NEWS_ID, NEWS_DATE, NEWS_TITLE, NEWS_DESC, NEWS_MESSAGE FROM W_NEWS WHERE NEWS_ID=?", id)
        data = data.fetchone()
        return data

    @staticmethod
    def get_all_news():
        data = MSSQL.conn().execute('''
            SELECT 
                WN.NEWS_ID,
                WN.NEWS_TITLE,
                WN.NEWS_DATE,
                MI.MEMB___ID 
            FROM 
                W_NEWS AS WN
            LEFT JOIN MEMB_INFO  AS MI
            ON
                MI.memb_guid = WN.news_author
            ORDER BY 
                NEWS_DATE
            DESC'''
        )
        data = data.fetchall()
        return data

    @staticmethod
    def delete_news_byid(id):
         MSSQL.conn().execute("DELETE FROM W_NEWS WHERE NEWS_ID=?", id)

    @staticmethod
    def update_news_byid(username, id, title, description, message):
        userid = User.get_userid_byname(username)
        MSSQL.conn().execute("UPDATE W_NEWS SET NEWS_AUTHOR=?, NEWS_TITLE=?, NEWS_DESC=?, NEWS_MESSAGE=? WHERE NEWS_ID =?", userid, title, description, message, id)

    @staticmethod
    def create_news(title, description, message, username):
        userid = User.get_userid_byname(username)
        
        MSSQL.conn().execute("INSERT INTO W_NEWS (NEWS_AUTHOR, NEWS_TITLE, NEWS_DESC, NEWS_MESSAGE) VALUES (?, ?, ?, ?)", userid, title, description, message)


class Character:

    @staticmethod
    def get_account_characters(account):
        query = '''
                SELECT
                    C.NAME , 
                    C.CLASS, 
                    C.RESETS, 
                    C.MASTERRESETS, 
                    C.CLEVEL, STRENGTH, 
                    C.DEXTERITY, 
                    C.VITALITY, 
                    C.ENERGY,
                    C.ACCOUNTID,
                    S.CONNECTSTAT,
                    AC.GAMEIDC,
                CASE WHEN
                    S.CONNECTSTAT > 0 AND AC.GAMEIDC = C.NAME
                THEN
                    1
                ELSE
                    0
                END
                AS STATUS
                FROM 
                    CHARACTER AS C
                LEFT JOIN
                    MEMB_STAT AS S ON C.ACCOUNTID = S.MEMB___ID
                LEFT JOIN
                    ACCOUNTCHARACTER AS AC ON C.ACCOUNTID = AC.ID
                WHERE 
                    ACCOUNTID = ?'''
        data = MSSQL.conn().execute(query, account)
        data = data.fetchall()
        return data

    @staticmethod
    def char_exists(charname):
        query = "SELECT UPPER(NAME) as NAME FROM CHARACTER WHERE NAME=?"

        for rows in MSSQL.conn().execute(query, charname.upper()):

            if rows[0] == charname.upper():
                return True
            else:
                return False

    @staticmethod
    def validate_charname(account, charname):
        query = "SELECT ACCOUNTID, NAME FROM CHARACTER WHERE ACCOUNTID=? AND NAME=?"

        for rows in MSSQL.conn().execute(query, account, charname):

            if rows[0] == account and rows[1] == charname:
                return True
            else:
                return False

    @staticmethod
    def update_charname(account, charname, newname):
        pass

    @staticmethod
    def char_online(charname):
        query = '''
                SELECT
                    MEMB_STAT.ConnectStat,
                    AccountCharacter.GameIDC,
                    Character.Name,
                    MEMB_INFO.memb___id,
                CASE WHEN
                    MEMB_STAT.ConnectStat > 0 and AccountCharacter.GameIDC = Character.Name
                THEN
                    1
                ELSE
                    0
                END
                AS
                    Connected
                FROM
                    Character
                LEFT JOIN
                    AccountCharacter ON Character.AccountID = AccountCharacter.Id
                LEFT JOIN
                    MEMB_STAT ON Character.AccountID = MEMB_STAT.memb___id
                LEFT JOIN
                    MEMB_INFO ON Character.AccountID = MEMB_INFO.memb___id
                WHERE
                    Character.Name =?'''
        
        for rows in MSSQL.conn().execute(query, charname):

            if rows[4] == 1:
                return True
            else:
                return False
