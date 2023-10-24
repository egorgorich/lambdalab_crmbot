from modules.strings import Strings as Str

class Commands:
    """ Класс с командами """

    user = {
        "add": {
            "text":         Str.get("commands_adduser"),
            "privilege":    "user.add"
        },
        "get": {
            "text":         Str.get("commands_getuser"),
            "privilege":    "user.get"
        },
        "getall": {
            "text":         Str.get("commands_getusers"),
            "privilege":    "user.get"
        }
    }

    menu = {
        "clients": {
            #"text":         Str.get("commands_clients"),
            "privilege":    "menu.clients"
        }
    }