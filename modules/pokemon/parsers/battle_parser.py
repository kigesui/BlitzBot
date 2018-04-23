
class BattleParser():
    instance = None

    class __BattleParser():
        def __init__(self):
            pass

    def __init__(self):
        if not BattleParser.instance:
            BattleParser.instance = BattleParser.__BattleParser()

    def parse(self, command):
        return BattleParser.instance.parse(command)
