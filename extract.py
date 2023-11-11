import openpyxl
import ndspy
import struct
import os
import yaml
from openpyxl.styles import Alignment
grammar_tree = {}

plugin = yaml.safe_load(
    open("./tools/plugins/mmsf1-new.yml", "r", encoding="utf-8"))

class Mugshot:
    def __init__(self, hex_id: str) -> None:
        self.hex_id = hex_id
    
    def to_en_name(self):
        match self.hex_id:
            case "5A00": return "Geo"
            case "5B00": return "GeoHappy"
            case "5F00": return "Kelvin"
            case "6400": return "Hope"
            case "6900": return "AaronBoreal"
            case "6E00": return "Sonia"
            case "7300": return "Luna"
            case "7800": return "Bud"
            case "7D00": return "Zack"
            case "8200": return "BobCopper"
            case "8700": return "TomDubius"
            case "8C00": return "MitchShepar"
            case "9100": return "KenSuther"
            case "9600": return "Pat"
            case "9B00": return "LegendaryMasterShin"
            case "A000": return "ChrysGolds"
            case "A500": return "LittleBoy"
            case "AA00": return "Boy"
            case "AF00": return "LittleGirl"
            case "B400": return "Girl"
            case "B900": return "Man"
            case "BE00": return "Woman"
            case "C300": return "OldMan"
            case "C800": return "OldWoman"
            case "CD00": return "Worker"
            case "D200": return "BusinessMan"
            case "D700": return "SpaceSuitWhite"
            case "DC00": return "SpaceSuitGeo"
            case "E100": return "SpaceSuitLuna"
            case "E600": return "SpaceSuitBud"
            case "EB00": return "SpaceSuitZack"
            case "F000": return "GeoVisualizer"
            case "F100": return "GeoVisualizerHappy"
            case "F500": return "GeoNoVisualizer"
            case "F600": return "GeoNoVisualizerHappy"
            case "FA00": return "VaughnPlatz"
            case "FF00": return "VeilPlatz"
            case "0401": return "ProfSnake"
            case "0901": return "Rey"
            case "0E01": return "BrotherAaron"
            case "1301": return "BrotherLucian"
            case "1801": return "BrotherToasty"
            case "1D01": return "BrotherNero"
            case "2201": return "BrotherBea"
            case "2701": return "BrotherLisbeth"
            case "2C01": return "Aaron"
            case "3101": return "Lucian"
            case "3601": return "ClaudPincer"
            case "3B01": return "DamianWolfe"
            case "4001": return "JeanCouronneXIV"
            case "4501": return "MargraveRymer"
            case "4A01": return "Principal"
            case "4F01": return "MrFamous"
            case "5401": return "Hollow"
            case "5901": return "KingHertz"
            case "5E01": return "KingHertzGold"
            case "6301": return "SheridanShadow"
            case "6801": return "LegendaryMasterShinShadow"
            case "A901": return "MegaMan"
            case "AE01": return "OmegaXis"
            case "B301": return "TaurusFire"
            case "B801": return "CygnusWing"
            case "BD01": return "HarpNote"
            case "C201": return "LibraScales"
            case "C701": return "QueenOphiuca"
            case "CC01": return "GeminiSparkWhite"
            case "D101": return "GeminiSparkBlack"
            case "DB01": return "CancerBubble"
            case "E001": return "WolfWoods"
            case "E501": return "CrownThunder"
            case "EA01": return "PegasusMagic"
            case "EF01": return "LeoKingdom"
            case "F401": return "DragonSky"
            case "F901": return "Taurus"
            case "FE01": return "Cygnus"
            case "0302": return "Lyra"
            case "0802": return "Libra"
            case "0D02": return "Ophiuca"
            case "1202": return "Gemini"
            case "1C02": return "Cepheus"
            case "2102": return "Jammer"
            case "2602": return "MrHertz"
            case "2B02": return "CommonNavi"
            case "3002": return "SpeedNavi"
            case "3502": return "FighterNavi"
            case "3A02": return "DeliveryNavi"
            case "3F02": return "PropellerMan"
            case "4402": return "KeyMan"
            case "4902": return "PitcherMan"
            case "4E02": return "ThermoMan"
            case "5302": return "EMHuman"
            case "5802": return "QuizSheet"
            case "5D02": return "InfoNavi"
            case "6202": return "ShovelMan"
            case "6702": return "TraderMan"
            case "6C02": return "MegaManEXE"
            case "7102": return "PegasusMagicShadow"
            case "7602": return "LeoKingdomShadow"
            case "7B02": return "DragonSkyShadow"
            case "8002": return "MrHertzGold"
            case "8502": return "IcePegasusMegaMan"
            case "8A02": return "FireLeoMegaMan"
            case "8F02": return "GreenDragonMegaMan"

class CommandDesc:
    def __init__(self, command):
        self.base = command['base'].replace(" ", "").lower()
        self.name = command['name']
        self.desc = command['desc']
        print(self.base, self.name, self.desc)
        grammar_tree[self.base] = self
        for alias in command['extensions']:
            grammar_tree[alias['base'].replace(" ", "").lower()] = self

    def read_command(self, buf: bytes, cursor: int):
        size = len(self.base) >> 1
        return (cursor + size, Command(self, buf[:size]))
    
    def generate_ps(self, cmd):
        return ""

for command in plugin:
    CommandDesc(command)
    
class MugshotShowNPCCommand(CommandDesc):
    def __init__(self):
        super().__init__(plugin["f500"])
    def generate_ps(self, cmd):
        return "在对话框内显示头像 " + ""

class Command:
    def __init__(self, desc: CommandDesc, hex_bytes: bytes) -> None:
        self.desc = desc
        self.hex_bytes = hex_bytes

class RawByte:
    def __init__(self, hex_bytes: str) -> None:
        self.hex_bytes = hex_bytes

# grammar_tree["e600"] = Command("e600", "子脚本结束")
# grammar_tree["e700"] = Command("e700", "等待按键按下0")
# grammar_tree["e701"] = Command("e701", "等待按键按下1")
# grammar_tree["e702"] = Command("e702", "等待按键按下2")
# grammar_tree["e800"] = Command("e800", "对话框开启")
# grammar_tree["e801"] = Command("e801", "对话框关闭")
# grammar_tree["f200"] = Command("f200", "清空对话框")


def read_tbl():
    with open("./tools/plugins/rnr1-utf8.tbl", "r", encoding="utf-8") as f:
        for line in f.readlines():
            [code, character] = line.split("=", 1)
            character = character.strip()
            if character == "\\n":
                character = "\n"  # Command(code, "换行")
            grammar_tree[code.lower()] = character
            # print(code, character)


read_tbl()

# print(grammar_tree)

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet["A1"] = "脚本文件名"
sheet["B1"] = "类型"
sheet["C1"] = "内容"
sheet["D1"] = "译文"
sheet["D2"] = "指令备注"


def read_msg(file_name: str):
    buf = ""
    result = []
    with open(f"_workspace/mess_raw/{file_name}", "rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(0, os.SEEK_SET)
        start_pos = struct.unpack("<H", f.read(2))[0]
        cur_pos = start_pos
        while cur_pos < size:
            if cur_pos < start_pos:
                start_pos = cur_pos
            try:
                cur_pos = struct.unpack("<H", f.read(2))[0]
            except Exception:
                break
        print(file_name, "startpos", start_pos, start_pos >> 1)
        f.seek(start_pos, os.SEEK_SET)
        data = f.read()
        cursor = 0
        while cursor < len(data):
            h = hex(data[cursor])[2:]
            h = "0" * (2 - len(h)) + h
            buf += h
            selection = []
            first_selection = []

            if buf in grammar_tree:
                if len(result) > 0 and isinstance(result[-1], str) and isinstance(grammar_tree[buf], str):
                    result[-1] += grammar_tree[buf]
                elif isinstance(grammar_tree[buf], CommandDesc):
                    (cursor, cmd) = grammar_tree[buf].read_command(
                        bytes.fromhex(buf), cursor)
                    result.append(cmd)
                else:
                    result.append(grammar_tree[buf])
                buf = ""
            else:
                while len(first_selection) + len(selection) > 0:
                    first_selection = []
                    selection = []
                    for key in grammar_tree:
                        pos = buf.find(key)
                        if pos == 0:
                            first_selection.append((key, pos))
                        elif pos != -1 and pos % 2 == 0:
                            selection.append((key, pos))
                    
                    if len(first_selection) > 0:
                        first_selection.sort(key=lambda x: x[1])
                        buf = buf[len(first_selection[0][0]):]
                        if len(result) > 0 and isinstance(result[-1], str) and isinstance(first_selection[0][0], str):
                            result[-1] += grammar_tree[first_selection[0][0]]
                        elif isinstance(first_selection[0][0], CommandDesc):
                            (cursor, cmd) = first_selection[0][0].read_command(
                                bytes.fromhex(buf), cursor)
                            result.append(cmd)
                        else:
                            result.append(grammar_tree[first_selection[0][0]])
                    elif len(selection) > 0:
                        selection.sort(key=lambda x: x[1])
                        pos = selection[0][1]
                        unknown_code = buf[pos:]
                        buf = buf[pos + len(selection[0][0]):]
                        if pos > 0:
                            result.append(RawByte(unknown_code))
                        # result.append("\n[UNKNOWN_CODE: $" + unknown_code + "]\n")
                        result.append(grammar_tree[selection[0][0]])
                        if len(result) > 0 and isinstance(result[-1], str) and isinstance(selection[0][0], str):
                            result[-1] += grammar_tree[selection[0][0]]
                        elif isinstance(selection[0][0], CommandDesc):
                            (cursor, cmd) = selection[0][0].read_command(
                                bytes.fromhex(buf), cursor)
                            cursor -= 1
                            result.append(cmd)
                        else:
                            result.append(grammar_tree[selection[0][0]])
            cursor += 1
        counter = 1
        for line in result:
            counter += 1
            if isinstance(line, str):
                sheet.append([file_name, "文字", line, ""])
            elif isinstance(line, Command):
                sheet.append([file_name, "指令", line.desc.name +
                             " $" + line.hex_bytes.hex(), ""])
            elif isinstance(line, RawByte):
                sheet.append([file_name, "原始数据", line.hex_bytes, ""])


mess_raw = os.listdir("_workspace/mess_raw")
mess_raw.sort()
for file in mess_raw:
    read_msg(file)
    # try:
    #     read_msg(file)
    # except Exception as e:
    #     print(e.with_traceback(None))
    #     pass

print("Applying alignment")
for row in sheet.iter_rows():
    for cell in row:
        cell.alignment = Alignment(wrap_text=True)

print("Saving")
workbook.save("result.xlsx")

# print(result)
# print("".join(result))
