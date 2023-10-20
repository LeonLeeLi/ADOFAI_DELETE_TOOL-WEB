import json
import os
import re

class OneLineEncoder(json.JSONEncoder):
    def encode(self, o):
        return json.dumps(o, separators=(",", ":"))


class Encoder:
    def __init__(self, filepath, event_type, newfilename, indent=None):
        self.filepath = filepath
        self.event_type = event_type
        self.indent = indent
        self.newfilename = newfilename

    def encode_and_dump(self):
        with open(self.filepath, "r", encoding="utf-8-sig") as f:
            data = json.load(f)

        # 处理actions单行格式化
        actions = [action for action in data["actions"]]
        data["actions"] = actions

        # 编码并输出
        with open(self.filepath, "w", encoding="utf-8-sig") as f:
            json.dump(data, f, cls=OneLineEncoder, indent=2)

        with open(self.filepath, "r", encoding="utf-8-sig") as f:
            content = f.read()

        with open(self.filepath, "w", encoding="utf-8-sig") as f:
            f.write(content)

    # 修复JSON文件中的语法错误,并格式化代码
    def fix_json(self):
        # 读取文件内容
        with open(self.filepath, "r", encoding="utf-8-sig") as f:
            content = f.read()

        # 使用正则表达式删除所有末尾逗号
        content = re.sub(r",(\s+})", r"}", content)
        content = re.sub(r",,", r",", content)
        content = json.loads(content)

        # 保存格式化后的文件内容
        with open(self.filepath, "w", encoding="utf-8-sig") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)

    # 删除指定事件类型
    def remove_event(self):

        with open(self.filepath, "r", encoding="utf-8-sig") as f:
            data = json.load(f)

        actions = []
        for action in data["actions"]:
            if action["eventType"] not in self.event_type:
                actions.append(action)

        data["actions"] = actions

        new_filepath = f"modify/{self.newfilename}"
        with open(new_filepath, "w", encoding="utf-8-sig") as f:
            json.dump(data, f)
