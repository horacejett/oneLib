from onelib import CustomComponent
from onelib.field_typing import Data


class Component(CustomComponent):
    documentation: str = 'http://docs.onelib.org/components/custom'

    def build_config(self):
        return {'param': {'display_name': 'Parameter'}}

    def build(self, param: Data) -> Data:
        return param
