import sqlite3 as sl
from datetime import datetime

from modules.print import Print as Con
from modules.strings import Strings as Str
from modules.default import Default as Def

class Database:
    name = "database.db"
    pref = "db"

    @classmethod
    def load(cls):
        """ Инициализация базы. Создание таблиц и заполнение необходимых для работы данных """

        Con.print(cls.pref, Str.get("database_load"))

        # Создаем стандартные таблицы
        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            cur.executescript(""" CREATE TABLE IF NOT EXISTS settings(
                name TEXT PRIMARY KEY,
                value TEXT
            ); 
            CREATE TABLE IF NOT EXISTS users(
                tid INTEGER PRIMARY KEY,
                state TEXT,
                action TEXT,
                temp TEXT,
                date INTEGER,
                firstname TEXT,
                lastname TEXT,
                phone INTEGER,
                rank TEXT,
                active INTEGER,
                description TEXT
            );
            CREATE TABLE IF NOT EXISTS ranks(
                name TEXT PRIMARY KEY,
                displayname TEXT,
                privileges TEXT,
                description TEXT
            ); """)

        # Заполняем стандартные настройки
        for key in Def.settings:
            dvalue = Def.settings[key]
            bvalue = cls.settingGetAll().get(key)
            if bvalue is None:
                if dvalue == "*":
                    cls.settingInput(key)
                    continue
                cls.settingSet(key, dvalue)

        # Создаем стандартные ранги
        if not cls.rankGetAll():
            Con.print(cls.pref, Str.get("setup_ranks"))
            for key in Def.ranks:
                v = Def.ranks[key]
                cls.rankCreate(key, v["displayname"], v["privileges"], v["description"])

        # Создаем первого супервизора
        if not cls.userGetAll():
            Con.print(cls.pref, Str.get("setup_supervisor"))
            v = {"tid": 0, "firstname": "", "lastname": "", "phone": 0, "description": ""}
            for key in v:
                v[key] = Con.input(cls.pref, Str.get(f"setup_{key}"))
            cls.userCreate(v["tid"], v["firstname"], v["lastname"], v["phone"], "supervisor", v["description"], 1)

        __settings = cls.settingGetAll()
        __ranks = cls.rankGetAll()
        __users = cls.userGetAll()
        Con.print(cls.pref ,Str.get("database_loaded", nranks=len(__ranks), nusers=len(__users)))

    @classmethod
    def settingInput(cls, name):
        """ Создание настройки или замена значения настройки с клавиатуры в базе
        - name  - str - Имя настройки в базе """
        cls.settingSet(name, Con.input(cls.pref, Str.get("setup_input", name=name)))

    @classmethod
    def settingSet(cls, name, value):
        """ Создание настройки или замена значения настройки в базе
        - name  - str - Имя настройки в базе
        - value - str - Значение настройки """

        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" INSERT OR REPLACE INTO settings(name, value) VALUES (?, ?) """, (name, value))
                Con.print(cls.pref, Str.get("setting_set", name=name, value=value))
                return True
            except Exception as error:
                Con.printex(cls.pref, Str.get("setting_seterror", name=name), error)
        return False

    @classmethod
    def settingGet(cls, name):
        """ Получение значениея по имени настройки
        - name - str - Имя настройки в базе """

        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" SELECT * FROM settings WHERE name = ? """, [name])
                result = cur.fetchone()
                if result is None: return None
                return result[1]
            except Exception as error:
                Con.printex(cls.pref, Str.get("setting_geterror", name=name), error)
        return None

    @classmethod
    def settingGetAll(cls):
        """ Получение всех настроек """

        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" SELECT * FROM settings """)
                fetch = cur.fetchall()
                result = {}

                if fetch is None: return None
                for key in fetch:
                    result[key[0]] = key[1]

                return result
            except Exception as error:
                Con.printex(cls.pref, Str.get("setting_getallerror"), error)
        return None

    @classmethod
    def rankCreate(cls, name, dname, privileges, desc):
        """ Создание ранга и запись в базу
        - name          - str - Уникальное имя ранга
        - dname         - str - Имя для отображения
        - privileges    - str - Наименования привелегий через запятую, без пробелов
        - desc          - str - Описание ранга """

        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                privileges = ",".join(privileges)
                cur.execute(""" INSERT INTO ranks(name, displayname, privileges, description) 
                    VALUES (?, ?, ?, ?) """, (name, dname, privileges, desc))
                Con.print(cls.pref, Str.get("rank_create", name=name, dname=dname))
                return True
            except sl.IntegrityError:
                Con.printex(cls.pref, Str.get("rank_createerror", name=name, dname=dname), Str.get("rank_createexist"))
            except Exception as error:
                Con.printex(cls.pref, Str.get("rank_createerror", name=name, dname=dname), error)
        return False

    @classmethod
    def rankGetAll(cls):
        """ Получение картежей всех рангов """

        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" SELECT * FROM ranks """)
                fetch = cur.fetchall()
                if fetch is None: return None
                result = list()

                for key in fetch:
                    rank = {
                        "name": key[0],
                        "displayname": key[1],
                        "privileges": key[2],
                        "description": key[3]
                    }
                    result.append(rank)

                return result
            except Exception as error:
                Con.printex(cls.pref, Str.get("rank_getallerror"), error)
        return None

    @classmethod
    def rankGet(cls, name):
        """ Получение картежа ранга
         - name - str - Имя ранга """

        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" SELECT * FROM ranks WHERE name=? """, (name, ))
                fetch = cur.fetchone()
                if fetch is None: return None
                result = dict()
                result["name"] = fetch[0]
                result["displayname"] = fetch[1]
                result["privileges"] = fetch[2]
                result["description"] = fetch[3]

                return result
            except Exception as error:
                Con.printex(cls.pref, Str.get("rank_geterror", name=name), error)
        return None

    @classmethod
    def userCreate(cls, tid, fname, lname, phone, rank, desc, active):
        """ Создание пользователя и запись в базу
        - tid      - int - Telegram ID пользователя
        - fname    - str - Имя пользователя
        - lname    - str - Фамилия пользователя
        - phone    - int - Номер телефона пользователя, начиная с 900
        - rank     - str - Имя ранга
        - active   - int - Активен ли пользователь, 0 если неактивен
        - desc     - str - Описание пользователя """

        if cls.rankGet(rank) is None and rank != "":
            Con.printex(cls.pref, Str.get("user_createerror", fname=fname, lname=lname, tid=tid), Str.get("user_createrank", rank=rank))
            return False

        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            date = cls.timeStamp()
            try:
                cur.execute(""" INSERT INTO users(tid, state, action, temp, date, firstname, lastname, phone, rank, active, description) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """, (tid, "", "", "", date, fname, lname, phone, rank, int(active), desc))
                Con.print(cls.pref, Str.get("user_create", fname=fname, lname=lname, tid=tid))
                return True
            except sl.IntegrityError:
                Con.printex(cls.pref, Str.get("user_createerror", fname=fname, lname=lname, tid=tid), Str.get("user_createexist"))
            except Exception as error:
                Con.printex(cls.pref, Str.get("user_createerror", fname=fname, lname=lname, tid=tid), error)
        return False

    @classmethod
    def userGetAll(cls):
        """ Получение картежей всех пользователей в базе """

        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" SELECT * FROM users """)
                fetch = cur.fetchall()
                if fetch is None: return None
                result = list()

                for key in fetch:
                    user = {
                        "tid": key[0],
                        "state": key[1],
                        "action": key[2],
                        "temp": key[3],
                        "date": key[4],
                        "firstname": key[5],
                        "lastname": key[6],
                        "phone": key[7],
                        "rank": key[8],
                        "active": key[9],
                        "description": key[10]
                    }
                    result.append(user)

                return result
            except Exception as error:
                Con.printex(cls.pref, Str.get("user_getallerror"), error)
        return None

    @classmethod
    def userGet(cls, tid):
        """ Получение картежа пользователя
         - tid - int - Telegram ID пользователя """

        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" SELECT * FROM users WHERE tid=? """, (tid,))
                fetch = cur.fetchone()
                if fetch is None: return None
                result = dict()
                result["tid"] = fetch[0]
                result["state"] = fetch[1]
                result["action"] = fetch[2]
                result["temp"] = fetch[3]
                result["date"] = fetch[4]
                result["firstname"] = fetch[5]
                result["lastname"] = fetch[6]
                result["phone"] = fetch[7]
                result["rank"] = fetch[8]
                result["active"] = fetch[9]
                result["description"] = fetch[10]

                return result
            except Exception as error:
                Con.printex(cls.pref, Str.get("user_geterror", tid=tid), error)
        return None

    @classmethod
    def userGetPrivileges(cls, tid):
        rank = cls.rankGet(cls.userGet(tid).get("rank"))

        return rank.get("privileges").split(",")

    @classmethod
    def userHasPrivilege(cls, tid, privilege):
        """ Проверка есть ли у пользователя привелегия
        - tid       - int - Telegram ID пользователя
        - privilege - str - Имя привелегии """

        privileges = cls.userGetPrivileges(tid)

        if "*" in privileges: return True
        return privilege in privileges

    @classmethod
    def userSetState(cls, tid, state):
        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" UPDATE users SET state=? WHERE tid=? """, (state, tid))
                return True
            except Exception as error:
                return False

    @classmethod
    def userSetAction(cls, tid, act):
        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" UPDATE users SET action=? WHERE tid=? """, (act, tid))
                return True
            except Exception as error:
                return False

    @classmethod
    def userSetTemp(cls, tid, data):
        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" UPDATE users SET temp=? WHERE tid=? """, (data, tid))
                return True
            except Exception as error:
                return False

    @classmethod
    def parseTemp(cls, temp):
        temp = temp.split(",")
        result = {}
        for key in temp:
            spl = key.split(":")
            result[spl[0]] = spl[1]
        return result

    @classmethod
    def parsePhone(cls, phone):
        phone = str(phone)
        return f"+7 ({phone[:3]}) {phone[3:6]}-{phone[6:8]}-{phone[8:]}"

    @classmethod
    def timeStamp(cls):
        return datetime.timestamp(datetime.now())

    @classmethod
    def timeStampParse(cls, stamp):
        return datetime.fromtimestamp(stamp)

    @classmethod
    def userClearCursor(cls, tid):
        with sl.connect(cls.name) as sql:
            cur = sql.cursor()
            try:
                cur.execute(""" UPDATE users SET state=? WHERE tid=? """, ("", tid))
                cur.execute(""" UPDATE users SET action=? WHERE tid=? """, ("", tid))
                cur.execute(""" UPDATE users SET temp=? WHERE tid=? """, ("", tid))
                return True
            except Exception as error:
                return False