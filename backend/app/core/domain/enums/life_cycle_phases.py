from typing import List
from lcax import LifeCycleStage
from enum import Enum


class LifeCyclePhases(str, Enum):
    """mapping of single life cycle stages to broader life cycle phases"""
    PRODUCTION : List[LifeCycleStage] = [LifeCycleStage.a1a3]
    CONSTRUCTION : List[LifeCycleStage] = [LifeCycleStage.a4, LifeCycleStage.a5]
    OPERATION : List[LifeCycleStage] = [LifeCycleStage.b1, LifeCycleStage.b2, LifeCycleStage.b3, LifeCycleStage.b4, LifeCycleStage.b5]
    OPERATIONAL_ENERGY : List[LifeCycleStage] = [LifeCycleStage.b6]
    OPERATIONAL_WATER : List[LifeCycleStage] = [LifeCycleStage.b7]
    OPERATIONAL_TRANSPORT : List[LifeCycleStage] = [LifeCycleStage.b8]
    DISASSEMBLY : List[LifeCycleStage] = [LifeCycleStage.c1, LifeCycleStage.c2]
    DISPOSAL : List[LifeCycleStage] = [LifeCycleStage.c3, LifeCycleStage.c4]
    REUSE : List[LifeCycleStage] = [LifeCycleStage.d]