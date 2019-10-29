from datetime import datetime

from logs.models import Logs


def addLog(user_id=None, log_module=None, scene=None, content=None):
    addtime = datetime.now()
    log = Logs(user_id=user_id, log_module=log_module, scene=scene, content=content, addtime=addtime)
    log.save()
