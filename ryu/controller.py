from ryu.app.simple_switch_13 import SimpleSwitch13
from ryu.app.ofctl_rest import RestStatsApi


class QosController(RestStatsApi, SimpleSwitch13):
    pass
