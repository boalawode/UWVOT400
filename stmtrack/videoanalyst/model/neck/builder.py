# -*- coding: utf-8 -*
from typing import Dict, List

from loguru import logger
from yacs.config import CfgNode

from stmtrack.videoanalyst.model.module_base import ModuleBase
from stmtrack.videoanalyst.model.neck.neck_base import TASK_NECKS
from stmtrack.videoanalyst.utils import merge_cfg_into_hps


def build(task: str, cfg: CfgNode):
    r"""
    Builder function.

    Arguments
    ---------
    task: str
        builder task name (track|vos)
    cfg: CfgNode
        buidler configuration

    Returns
    -------
    torch.nn.Module
        module built by builder
    """
    if task in TASK_NECKS:
        neck_modules = TASK_NECKS[task]
    else:
        logger.error("no task model for task {}".format(task))
        exit(-1)

    name = cfg.name
    neck_module = neck_modules[name]()
    hps = neck_module.get_hps()
    hps = merge_cfg_into_hps(cfg[name], hps)
    neck_module.set_hps(hps)
    neck_module.update_params()

    return neck_module


def get_config(task_list: List) -> Dict[str, CfgNode]:
    r"""
    Get available component list config

    Returns
    -------
    Dict[str, CfgNode]
        config with list of available components
    """
    cfg_dict = {task: CfgNode() for task in task_list}
    for cfg_name, module in TASK_NECKS.items():
        cfg = cfg_dict[cfg_name]
        cfg["name"] = "unknown"
        for name in module:
            cfg[name] = CfgNode()
            task_model = module[name]
            hps = task_model.default_hyper_params
            for hp_name in hps:
                cfg[name][hp_name] = hps[hp_name]
    return cfg_dict
