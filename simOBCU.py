# -*- coding: utf-8 -*-
__author__ = 'Ryan'

import socket, traceback
from Timer import timer
import logging
import logging.config
import ConfigParser
from OBCUFrame import OBCUWindow

logging.config.fileConfig('logging.conf')
print_log = logging.getLogger('root')
file_log = logging.getLogger('fileLogger')

global sysCycle
canHead = '7d7200010003010000003040001a'
OBCU_ML_EFF = '88'
OBCU_CRC_EFF = '84'
RECV_EXTEND = '030c'

can_src_id = '03'

SEND1_DATA = '48'
SEND1_CRC = '50'
SEND2_DATA = '58'
SEND2_CRC = '60'
SEND3_DATA = '68'
SEND3_CRC = '70'

send_status = 0
zc_unrecv_cnt = 0


class Packet:
    def __init__(self):
        self.trainVID = ''
        self.loopID = ''
        self.type = ''
        self.data = []


class Train:
    def __init__(self):
        self.train_vid = ''
        self.loop_id = 0
        self.loop_offset = 0
        self.cycle = 0


def cov_zctype2str(zctype):
    if zctype == 0x00:
        return 'ZC0'
    else:
        if zctype == 0x20:
            return 'ZC1'
        else:
            if zctype == 0x40:
                return 'ZC2'
            else:
                if zctype == 0x60:
                    return 'ZC3'
                else:
                    if zctype == 0x80:
                        return 'ZC4'
                    else:
                        return 'Unknown'


def num_to_str(num):
    hex_num = hex(num)
    if len(hex_num) < 4:
        tmp = hex_num.replace('0x', '0')
    else:
        tmp = hex_num.replace('0x', '')
    return tmp


def creat_obcu0(vid, loop, location, ZCTC, OBCUTC):
    msg = []
    msg.append(canHead)
    msg.append(OBCU_ML_EFF)
    msg.append(RECV_EXTEND)
    msg.append(can_src_id)
    msg.append(SEND1_DATA)
    msg.append(vid)
    msg.append('0B')
    msg.append(num_to_str(loop))
    lowByteLoc = location & 0x0003
    lowByteLoc = (lowByteLoc << 6) & 0x00C0
    highByteLoc = (location >> 2) & 0x00FF

    msg.append(num_to_str(highByteLoc))
    msg.append(num_to_str(lowByteLoc))
    msg.append('00')
    msg.append(ZCTC)
    msg.append(num_to_str(OBCUTC))

    msg.append(OBCU_CRC_EFF)
    msg.append(RECV_EXTEND)
    msg.append(can_src_id)
    msg.append(SEND1_CRC)
    msg.append('00000000')
    msg.append('00000000')
    return msg


def creat_obcu1(vid, loop, location, ZCTC, OBCUTC):
    msg = []
    msg.append(canHead)
    msg.append(OBCU_ML_EFF)
    msg.append(RECV_EXTEND)
    msg.append(can_src_id)
    msg.append(SEND1_DATA)
    msg.append(vid)
    msg.append('4B')
    msg.append(num_to_str(loop))
    lowByteLoc = location & 0x0003
    lowByteLoc = (lowByteLoc << 6) & 0x00C0 | 0x001E
    highByteLoc = (location >> 2) & 0x00FF

    msg.append(num_to_str(highByteLoc))
    msg.append(num_to_str(lowByteLoc))
    msg.append('A0')
    msg.append(ZCTC)
    msg.append(num_to_str(OBCUTC))

    msg.append(OBCU_CRC_EFF)
    msg.append(RECV_EXTEND)
    msg.append(can_src_id)
    msg.append(SEND1_CRC)
    msg.append('00000000')
    msg.append('00000000')
    return msg

def recv_zc_msg(args):
    try:
        message, address = args[0].recvfrom(8192)
        # print "Recv data from ", address

        hexMessage = message.encode('hex')
        lenMessage = len(hexMessage)
        # print "Length is %d" % lenMessage
        listMessage = []
        listMessage.append(hexMessage[0:53])
        frameNum = (lenMessage - 54) / 26
        for i in range(frameNum):
            listMessage.append(hexMessage[(54 + i * 26): (54 + ((i + 1) * 26))])
        listLen = len(listMessage)
        # print "Recv CAN Frame Num: %d" % listLen
        listPacket = []
        for i in range(1, listLen, 2):
            pack = Packet()
            pack.trainVID = int(listMessage[i][10:12], 16)
            pack.loopID = int(listMessage[i][14:16], 16) & 0x3F
            pack.type = int(listMessage[i][12:14], 16) & 0xE0
            pack.data = listMessage[i] + listMessage[i + 1]
            listPacket.append(pack)
        # print "Recved Packet Num: %d" % (len(listPacket))

        # creat a train
        global sysCycle
        train_1 = Train()
        train_1.cycle = sysCycle & 0x00FF
        # if sysCycle % 250 == 0:
        # train_1.cycle = sysCycle - 10
        # print "Send OBCU cycle is %d" % train_1.cycle
        train_1.loop_id = 4
        train_1.loop_offset = 30
        train_1.train_vid = '11'

        global send_status
        global zc_unrecv_cnt
        zc_unrecv_cnt += 1
        strOBCU = ''
        str_send_type = ''
        for packet in listPacket:
            if packet.loopID == train_1.loop_id:
                pack_type = cov_zctype2str(packet.type)
                if (pack_type == 'ZC0') and (send_status == 0):
                    zcTC = packet.data[38:40]
                    obcu0 = creat_obcu0(train_1.train_vid, train_1.loop_id, train_1.loop_offset, str(zcTC),
                                        train_1.cycle)
                    strOBCU = ''.join(obcu0)
                    file_log.info("Train %s Recv %s (ZC: %s) %s : %s", train_1.train_vid, pack_type,
                                  str(zcTC), packet.data[10:26], packet.data[36:52])
                    str_send_type = 'OBCU0'
                    send_status = 1
                else:
                    if pack_type == 'ZC1':
                        zc_unrecv_cnt = 0
                        zcTC = packet.data[38:40]
                        obcu1 = creat_obcu1(train_1.train_vid, train_1.loop_id, train_1.loop_offset, str(zcTC),
                                            train_1.cycle)
                        strOBCU = ''.join(obcu1)
                        file_log.info("Train %s Recv %s (ZC: %s) %s : %s", train_1.train_vid, pack_type,
                                  str(zcTC), packet.data[10:26], packet.data[36:52])
                        str_send_type = 'OBCU1'
                        break
        if zc_unrecv_cnt > 6:
            send_status = 0
        if len(strOBCU) > 0:
            file_log.info("Send TO ZC (ACK: %s, %s: %s): %s : %s", str(zcTC), str_send_type, train_1.cycle,
                          strOBCU[38:54], strOBCU[64:72])
            hexOBCU = []
            for cntI in range(0, len(strOBCU), 2):
                hexOBCU.append(chr(int(strOBCU[cntI:cntI + 2], 16)))
            sendData = ''.join(hexOBCU)
            # s_recv_zc.sendto(sendData, args[1])
    except (KeyboardInterrupt, SystemExit):
        s_recv_zc.shutdown()
        s_recv_zc.close()
        raise
    except:
        traceback.print_exc()


def cycle():
    global sysCycle
    sysCycle += 1
    file_log.info("####################\t%d\t#######################", sysCycle)


if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    cf.read("system.conf")
    system_cycle = cf.getfloat("system", "cycle")
    ip = cf.get("udp", "zc_local_ip")
    port_zc = cf.getint("udp", "zc_local_recv_port")
    port_obcu = cf.getint("udp", "zc_dst_send_port")
    s_recv_zc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_recv_zc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print_log.info("Creating socket...")
    s_recv_zc.bind((ip, port_obcu))
    print_log.info("Socket bind success..")
    global sysCycle
    sysCycle = 0
    t1 = timer(recv_zc_msg, (s_recv_zc, (ip, port_zc)), 1, system_cycle)
    t1.start()
    t3 = timer(cycle, 0, 3, system_cycle)
    t3.start()

    while True:
        pass
