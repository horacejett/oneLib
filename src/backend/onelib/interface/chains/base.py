from typing import Any, ClassVar, Dict, List, Optional, Type

from onelib.custom.customs import get_custom_nodes
from onelib.interface.base import LangChainTypeCreator
from onelib.interface.importing.utils import import_class
from onelib.common.services.config_service import settings
from onelib.template.frontend_node.chains import ChainFrontendNode
from loguru import logger
from onelib.utils.util import build_template_from_class, build_template_from_method
from onelib_langchain import chains as onelib_chains
from onelib_langchain import sql as onelib_sql
from onelib_langchain.rag.onelib_rag_chain import oneLibRetrievalQA
from langchain import chains
from langchain_experimental import sql

# Assuming necessary imports for Field, Template, and FrontendNode classes


class ChainCreator(LangChainTypeCreator):
    type_name: str = 'chains'

    @property
    def frontend_node_class(self) -> Type[ChainFrontendNode]:
        return ChainFrontendNode

    # We need to find a better solution for this
    from_method_nodes: ClassVar[Dict] = {
        'APIChain': 'from_llm_and_api_docs',
        'ConversationalRetrievalChain': 'from_llm',
        'LLMCheckerChain': 'from_llm',
        'SQLDatabaseChain': 'from_llm',
        'LLMRouterChain': 'from_llm',
        'oneLibRetrievalQA': 'from_llm',
        'QAGenerationChain': 'from_llm',
        'QAGenerationChainV2': 'from_llm',
    }

    @property
    def type_to_loader_dict(self) -> Dict:
        if self.type_dict is None:
            # langchain
            self.type_dict: dict[str, Any] = {
                chain_name: import_class(f'langchain.chains.{chain_name}')
                for chain_name in chains.__all__
            }
            # onelib-langchain
            onelib = {
                chain_name: import_class(f'onelib_langchain.chains.{chain_name}')
                for chain_name in onelib_chains.__all__
            }
            # If configured incustom_chains, it will not start frommethodHow to initialize, resulting in an error
            self.type_dict['oneLibRetrievalQA'] = oneLibRetrievalQA
            self.type_dict.update(onelib)

            # sql community
            community = {
                chain_name: import_class(f'langchain_experimental.sql.{chain_name}')
                for chain_name in sql.__all__
            }
            self.type_dict.update(community)

            # sql community
            onelib_sql_add = {
                chain_name: import_class(f'onelib_langchain.sql.{chain_name}')
                for chain_name in onelib_sql.__all__
            }
            self.type_dict.update(onelib_sql_add)

            from onelib.interface.chains.custom import CUSTOM_CHAINS

            self.type_dict.update(CUSTOM_CHAINS)
            # Filter according to settings.chains
            self.type_dict = {
                name: chain
                for name, chain in self.type_dict.items()
                if name in settings.chains or settings.dev
            }
        return self.type_dict

    def get_signature(self, name: str) -> Optional[Dict]:
        try:
            if name in get_custom_nodes(self.type_name).keys():
                return get_custom_nodes(self.type_name)[name]
            elif name in self.from_method_nodes.keys():
                return build_template_from_method(
                    name,
                    type_to_cls_dict=self.type_to_loader_dict,
                    method_name=self.from_method_nodes[name],
                    add_function=True,
                )
            return build_template_from_class(name, self.type_to_loader_dict, add_function=True)
        except ValueError as exc:
            raise ValueError(f'Chain {name} not found: {exc}') from exc
        except AttributeError as exc:
            logger.error(f'Chain {name} not loaded: {exc}')
            return None

    def to_list(self) -> List[str]:
        names = []
        for _, chain in self.type_to_loader_dict.items():
            chain_name = (chain.function_name()
                          if hasattr(chain, 'function_name') else chain.__name__)
            names.append(chain_name)
        return names


chain_creator = ChainCreator()
