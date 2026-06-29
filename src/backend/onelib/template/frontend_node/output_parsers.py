from typing import Optional

from onelib.template.field.base import TemplateField
from onelib.template.frontend_node.base import FrontendNode


class OutputParserFrontendNode(FrontendNode):
    @staticmethod
    def format_field(field: TemplateField, name: Optional[str] = None) -> None:
        FrontendNode.format_field(field, name)
        field.show = True


# class RouterOutputParserFrontendNode(FrontendNode):
#     @staticmethod
#     def format_field(field: TemplateField, name: Optional[str] = None) -> None:
#         FrontendNode.format_field(field, name)
#         field.show = True
