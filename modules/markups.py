from telebot import types

from modules.strings import Strings as Str

class Markups:
    class Start:
        def __init__(self, privileges):
            self.privileges = privileges

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = []



    #start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #buttons = []

    #if
    #start.row(types.KeyboardButton(Str.get("commands_yes")), types.KeyboardButton(Str.get("commands_no")))
    #yesnocancel.row(types.KeyboardButton(Str.get("commands_cancel")))




    yesnocancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yesnocancel.row(types.KeyboardButton(Str.get("commands_yes")), types.KeyboardButton(Str.get("commands_no")))
    yesnocancel.row(types.KeyboardButton(Str.get("commands_cancel")))