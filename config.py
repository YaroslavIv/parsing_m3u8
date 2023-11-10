import os
import json
from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    cap:    List[str]
    name:   str

def read_config(path: str) -> Config:
    if not os.path.isfile(path):
        raise ValueError(f"not find config: {path}")
 
    with open(path, 'r') as f:
        config = json.load(f)
    
    return Config(config['correct'], config['name'])
