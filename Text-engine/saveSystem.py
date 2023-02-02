import os
import json

class SaveSystem:
    def __init__(self, player = [], location: str = "", npc = []):
        if len(player) > 0:
            self.player = player[0]
        self.npc = npc
        self.location = location
        self.player_data = []
        self.player_data_file = 'player_save.json'
        self.npc_data_file = 'npc_save.json'
        self.npc_data = []
        self.data = None

    def save(self):
        self.player_data = [
            {
                'name': self.player.name,
                'gender': self.player.gender,
                'race': self.player.race,
                'inventory': self.player.inventory,
                'money': self.player.money,
            },
            {
                'name': self.location,
            },
        ]

        if len(self.npc) > 0:
            for i in self.npc:
                newArr = {
                    'name': i['name'],
                    'married': i['married'],
                    'relationList': i['relationList'],
                    'inventory': i['inventory'],
                }
                self.npc_data.append(newArr)
            
            if os.stat(self.npc_data_file).st_size > 0:
                loadedNpcData = []
                with open(self.npc_data_file, 'r') as f:
                    loadedNpcData.append(json.loads(f.read()))
                num = 0
                for i in range(len(loadedNpcData[0])):
                    if self.npc_data[num]['name'] == loadedNpcData[0][num]['name']:
                        self.npc_data[num]['married'] = loadedNpcData[0][num]['married']
                        self.npc_data[num]['relationList'] = loadedNpcData[0][num]['relationList']
                        self.npc_data[num]['inventory'] = loadedNpcData[0][num]['inventory']
                    else:
                        self.npc_data.append(loadedNpcData[0][num])
                    num += 1
                with open(self.npc_data_file, 'w', encoding='utf-8') as jsonFile:
                    json.dump(self.npc_data, jsonFile, ensure_ascii=True, indent=4, default = lambda x: x.__dict__)

        with open(self.player_data_file, 'w', encoding='utf-8') as jsonFile:
            json.dump(self.player_data, jsonFile, ensure_ascii=True, indent=4, default = lambda x: x.__dict__)

        return jsonFile.close()

    def load(self):
        if os.path.exists(self.player_data_file) and os.path.exists(self.npc_data_file):
            if os.stat(self.player_data_file).st_size > 0:
                objs = []
                with open(self.player_data_file, 'r') as f:
                    objs.append(json.loads(f.read()))
                if os.stat(self.npc_data_file).st_size > 0:
                    with open(self.npc_data_file, 'r') as f:
                        objs.append(json.loads(f.read()))
            else:
                warning("Файл сохранений - пустой!")
                warning("Начните новую игру, что бы эта функция сработала.")
                objs = False
            return objs
        else:
            warning("Нет сохранений!")
            warning("Начните новую игру, что бы эта функция сработала.")
            return False

    def deleteSaves(self):
        warning("Вы уверены, что хотите удолить сохранения? Это окончательно.")
        if detectChoice(input()) == 'yes':
            os.remove(self.player_data_file)
            os.remove(self.npc_data_file)
            header("Данные успешно удолены.")
            return 0
        else:
            return 0