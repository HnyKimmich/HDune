# json_loader 占位
import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
