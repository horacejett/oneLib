from typing import Any, Dict, List, Optional, Type

from onelib.interface.base import LangChainTypeCreator
from onelib.interface.importing.utils import import_class
from onelib.interface.vector_store.constants import CUSTOM_VECTORSTORE
from onelib.common.services.config_service import settings
from onelib.template.frontend_node.vectorstores import VectorStoreFrontendNode
from loguru import logger
from onelib.utils.util import build_template_from_method
from onelib_langchain import vectorstores as contribute_vectorstores
from langchain_community import vectorstores


class VectorstoreCreator(LangChainTypeCreator):
    type_name: str = 'vectorstores'

    @property
    def frontend_node_class(self) -> Type[VectorStoreFrontendNode]:
        return VectorStoreFrontendNode

    @property
    def type_to_loader_dict(self) -> Dict:
        if self.type_dict is None:
            self.type_dict: dict[str, Any] = {
                vectorstore_name:
                import_class(f'langchain_community.vectorstores.{vectorstore_name}')
                for vectorstore_name in vectorstores.__all__
                if vectorstore_name != 'Milvus'  # use onelib_langchain
            }
            self.type_dict.update({
                vectorstore_name:
                import_class(f'onelib_langchain.vectorstores.{vectorstore_name}')
                for vectorstore_name in contribute_vectorstores.__all__
            })
            self.type_dict.update(CUSTOM_VECTORSTORE)
        return self.type_dict

    def get_signature(self, name: str) -> Optional[Dict]:
        """Get the signature of an embedding."""
        try:
            return build_template_from_method(
                name,
                type_to_cls_dict=self.type_to_loader_dict,
                method_name='from_texts',
            )
        except ValueError as exc:
            raise ValueError(f'Vector Store {name} not found') from exc
        except AttributeError as exc:
            logger.error(f'Vector Store {name} not loaded: {exc}')
            return None

    def to_list(self) -> List[str]:
        return [
            vectorstore for vectorstore in self.type_to_loader_dict.keys()
            if vectorstore in settings.vectorstores or settings.dev
        ]


vectorstore_creator = VectorstoreCreator()
