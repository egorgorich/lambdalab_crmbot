from modules.strings import Strings as Str

class Default:
    settings = {
        "token": "*",
    }

    ranks = {
        "user": {
            "displayname":  Str.get("default_ranks_user_dname"),
            "privileges":   (),
            "description":  Str.get("default_ranks_user_desc")
        },
        "admin": {
            "displayname":  Str.get("default_ranks_admin_dname"),
            "privileges":   (),
            "description":  Str.get("default_ranks_admin_desc")
        },
        "supervisor": {
            "displayname":  Str.get("default_ranks_supervisor_dname"),
            "privileges":   ("*"),
            "description":  Str.get("default_ranks_supervisor_desc")
        }
    }