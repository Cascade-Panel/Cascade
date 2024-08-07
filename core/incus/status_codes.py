from enum import Enum

class StatusCode(Enum):
    CREATED = 100
    STARTED = 101
    STOPPED = 102
    RUNNING = 103
    CANCELING = 104
    PENDING = 105
    STARTING = 106
    STOPPING = 107
    ABORTING = 108
    FREEZING = 109
    FROZEN = 110
    THAWED = 111
    ERROR = 112
    READY = 113
    SUCCESS = 200
    FAILURE = 400
    CANCELED = 401