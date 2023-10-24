class Strings:
    """ Класс локализации """

    lang = "RU"

    strings = {
        "RU": {
            "start_connect":                    "Соединение с Telegram ботом '%name%' (%username%) установлено!",
            "start_connecterror":               "Ошибка соединения с Telegram ботом.",
            "start_connecterrorex":             "Неполадки с интернет соединением или Telegram API Token указан неверно.",

            "database_load":                    "Начата загрузка базы данных...",
            "database_loaded":                  "База данных загружена. Ранги: %nranks%, Пользователи: %nusers%.",

            "default_ranks_user_dname":         "Пользователь",
            "default_ranks_user_desc":          "Стандартный пользователь, работник.",
            "default_ranks_admin_dname":        "Администратор",
            "default_ranks_admin_desc":         "Администратор CRM.",
            "default_ranks_supervisor_dname":   "Руководитель",
            "default_ranks_supervisor_desc":    "Руководитель CRM.",

            "setting_set":                  "Настройка '%name%' изменена на '%value%'.",
            "setting_seterror":             "Ошибка изменения настройки '%name%'.",
            "setting_geterror":             "Ошибка чтения настройки '%name%'.",
            "setting_getallerror":          "Ошибка чтения настроек.",

            "setup_ranks":                  "Создание стандартных рангов:",
            "setup_supervisor":             "Создание первого супервизора:",
            "setup_input":                  "Настройка '%name%' отсутствует, введите: ",
            "setup_tid":                    "Telegram ID аккаунта: ",
            "setup_firstname":              "Имя: ",
            "setup_lastname":               "Фамилия: ",
            "setup_phone":                  "Номер телефона (слитно, без пробелов, начиная с 900): ",
            "setup_description":            "Описание: ",

            "rank_create":                  "Ранг '%dname% (%name%)' создан.",
            "rank_createerror":             "Ошибка создания ранга '%dname% (%name%)'.",
            "rank_createexist":             "Ранг уже существует.",
            "rank_createdefaultexist":      "Стандартный ранг уже существует.",
            "rank_geterror":                "Ошибка получения данных о ранге '%name%'.",
            "rank_getallerror":             "Ошибка получения данных о рангах.",

            "user_create":                  "Пользователь '%fname% %lname%' (%tid%) создан.",
            "user_createerror":             "Ошибка создания пользователя '%fname% %lname%' (%tid%).",
            "user_createexist":             "Пользователь уже существует.",
            "user_createrank":              "Ранг '%rank% не существует.",
            "user_geterror":                "Ошибка получения данных о пользователе (%tid%).",
            "user_getallerror":             "Ошибка получения данных о пользователях.",

            "message_yourid":               "Твой *Telegram ID: `%tid%`*\\.",
            "message_start":                "👤 *%fname% %lname%*\n"\
                                            "├ *Твой ID:* `%tid%`\n"\
                                            "├ *Номер:* `%phone%`\n"\
                                            "├ *Ранг:* `%rank%`\n"\
                                            "└ *Зарегистрирован:* `%date%`",

            "commands_adduser":             "Новый пользователь",
            "commands_adduser_tid":         "Введите *Telegram ID* пользователя:",
            "commands_adduser_tidexists":   "Такой *Telegram ID* уже используется",
            "commands_adduser_name":        "Введите *имя* и *фамилию* пользователя \\(через пробел\\):",
            "commands_adduser_phone":       "Введите *номер телефона* пользователя \\(начиная с 900, без пробелов\\):",
            "commands_adduser_rank":        "Укажите *ранг* пользователя:",
            "commands_adduser_rankinvalid": "Такой *ранг* не существует",
            "commands_adduser_desc":        "Введите *описание* пользователя:",
            "commands_adduser_active":      "Будет создан пользователь *%fname%* *%lname%*, сделать его *активным*?",
            "commands_getuser":             "О пользователе",
            "commands_getusers":            "Все пользователи",

            "commands_yes":                 "Да",
            "commands_no":                  "Нет",
            "commands_cancel":              "Отмена",
        }
    }

    @classmethod
    def get(cls, key, **kwargs):
        """ Обработка строк локализации """

        result = cls.strings[cls.lang][key]
        if kwargs is not None:
            for k in kwargs:
                if type(kwargs[k]) is not str: kwargs[k] = str(kwargs[k])
                result = result.replace(f"%{k}%", kwargs[k])
        return result