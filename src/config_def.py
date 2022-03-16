import os

import toml
from src.utils import CFG_FIELD

# Check that the cfg file given in input is valid according to CFG_FIELD.
class Cfg:
    def __init__(self, args):
        self.path = args.cfg_path
        self.build()

    def build(self):
        assert os.path.exists(self.path), f"Path {self.path} does not exists."
        try:
            data = toml.load(self.path)
        except ValueError:
            assert False, f"{self.path} is not a toml file."

        for k, v in data.items():
            assert k in CFG_FIELD, f"Field {k} does not exists."
            for u in v:
                assert u in CFG_FIELD[k], \
                    f"Variable {u} does not exist in field {k}."
            setattr(self, k, v)

    def __repr__(self):
        return f"{self.__dict__}"
