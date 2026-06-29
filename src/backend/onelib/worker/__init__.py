# register tasks
from onelib.worker.knowledge.file_worker import file_copy_celery, parse_knowledge_file_celery, \
    retry_knowledge_file_celery
from onelib.worker.knowledge.rebuild_knowledge_worker import rebuild_knowledge_celery
from onelib.worker.telemetry.mid_table import sync_mid_user_increment, sync_mid_knowledge_increment, \
    sync_mid_app_increment, sync_mid_user_interact_dtl
from onelib.worker.test.test import add
from onelib.worker.workflow.tasks import execute_workflow, continue_workflow, stop_workflow
