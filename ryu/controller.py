from threading import Thread
import time

from flask import jsonify, Flask
import requests

from ryu.app.simple_switch_13 import SimpleSwitch13
from ryu.app.ofctl_rest import RestStatsApi
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import ethernet, ether_types, packet


app = Flask(__name__)

@app.route('/')
def meter_stats():
    """
    This function was meant to be an aggregator for flow stats on each switch.
    Right now we are only grabbing stats from s1 because that is what the demo
    will involve.
    """
    r = requests.get('http://localhost:8080/stats/flow/1')
    r.raise_for_status()
    data = r.json()
    bytes_tx = 0
    for stat in data['1']:
        if stat['match'].get('dl_src') == '00:00:00:00:00:01':
            bytes_tx += stat['byte_count']
    # We need to accomodate the dropping of our rule with the hard timeout
    return jsonify({'bytes_tx': bytes_tx})


class QoS(SimpleSwitch13, RestStatsApi):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.throttle_info = {}
        self.flask = Thread(target=app.run, kwargs={'host': '0.0.0.0'})
        self.flask.start()

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        dpid = datapath.id
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]

        self.add_flow(datapath, 0, match, actions)

        bands = [
            parser.OFPMeterBandDrop(
                type_=ofproto.OFPMBT_DROP,
                len_=0, rate=5, burst_size=10
            )
        ]
        req = parser.OFPMeterMod(
            datapath=datapath,
            command=ofproto.OFPMC_ADD,
            flags=ofproto.OFPMF_KBPS,
            meter_id=dpid,
            bands=bands
        )

        datapath.send_msg(req)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None, timeout=0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, hard_timeout=timeout)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, hard_timeout=timeout)
        datapath.send_msg(mod)

    def add_meter_flow(self, datapath, in_port, src, dst, timeout=10):
        dpid = datapath.id
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        out_port = self.mac_to_port[dpid][dst]
        meter_key = (dpid, in_port, src, dst)

        match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)
        actions = [parser.OFPActionOutput(out_port)]
        inst = [
            parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions),
            parser.OFPInstructionMeter(1,ofproto.OFPIT_METER)
        ]
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=timeout,
            hard_timeout=0, priority=3, instructions=inst
        )

        datapath.send_msg(mod)
        self.throttle_info[meter_key]['throttle_started'] = True
        self.throttle_info[meter_key]['meter_id'] = dpid
        self.logger.info("Throttle started between %r and %r on dpid %r", src, dst, dpid)

    def should_throttle(self, datapath, in_port, src, dst, timeout=10):
        current_time = time.time()
        key = (datapath.id, in_port, src, dst)
        if key not in self.throttle_info:
            self.throttle_info[key] = {
                "detected_time": current_time,
                "meter_id": None,
                "throttle_started": False
            }
            return False
        data = self.throttle_info[key]
        if data['throttle_started']:
            self.logger.info("Forget throttling has happened between %r and %r on dpid %r", src, dst, datapath.id)
            self.throttle_info.pop(key)
            return False
        return current_time - data['detected_time'] >= timeout

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            if self.should_throttle(datapath, in_port, src, dst):
                self.add_meter_flow(datapath, in_port, src, dst)
            else:
                match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
                # verify if we have a valid buffer_id, if yes avoid to send both
                # flow_mod & packet_out
                if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                    self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                    return
                else:
                    self.add_flow(datapath, 1, match, actions, timeout=10)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

