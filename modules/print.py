class Print:
    @classmethod
    def printex(cls, pref, text, error):
        error = str(error)[0].upper() + str(error)[1:]
        print(f"#{pref[:2].upper()}# — {text}", f"\n     ~ {error}")

    @classmethod
    def print(cls, pref, text):
        print(f"#{pref[:2].upper()}# — {text}")

    @classmethod
    def input(cls, pref, text):
        return input(f"#{pref[:2].upper()}# = {text}")