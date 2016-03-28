# -*- coding: utf-8 -*-

__author__ = 'Ryan'

import logging
import logging.config
from Type import *
import socket, select
import ConfigParser
from Timer import timer
from ctypes import *
import time


class OBCUModel(object):
    CAN_HEAD = '7d7200010003010000003040001a'
    OBCU_ML_EFF = '88'
    OBCU_CRC_EFF = '84'
    CAN_RECV_EXTEND = ['0303', '030C', '030F', '0330', '0333', '033C', '033F', '03C0', '03C3', '03CC',
                       '03CF', '03F0', '03F3', '03FC', '03FF', '0C03', '0C0C', '0C0F', '0C30', '0C33',
                       '0C3C', '0C3F', '0CC0', '0CC3']
    CAN_SRC_ID = '03'
    SEND1_DATA = '48'
    SEND1_CRC = '50'
    SEND2_DATA = '58'
    SEND2_CRC = '60'
    SEND3_DATA = '68'
    SEND3_CRC = '70'
    HEAD_FRAME = 54
    FRAME_LEN = 26
    OBCU_HEAD = len(CAN_HEAD) + 10
    ZC0_TYPE = 0x00
    ZC1_TYPE = 0x20
    ZC2_TYPE = 0x40
    ZC3_TYPE = 0x60
    ZC4_TYPE = 0x80
    RM_UNPOS = 0
    RM = 1
    SM = 2
    AM = 3
    AR = 4

    model_run_mode = 0
    dst_type = 0
    logging.config.fileConfig('logging.conf')
    file_log = logging.getLogger('fileLogger')
    socket_dst = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    crc_dll = cdll.LoadLibrary("crc.dll")

    obcu0_senior = OBCUSenior()
    obcu1_senior = OBCUSenior()

    last_loop_id = 0
    train_id = 0
    zc_id = 0
    train_dir = 0
    train_mar = 0
    train_loop = 0
    train_offset = 0
    top_atp_mode = RM_UNPOS
    atp_mode = RM_UNPOS

    list_msg = list()

    def __init__(self, i_frame):
        self.i_frame = i_frame
        self.obcu_count = 0
        self.system_count = 0
        self.obcu_inc_flag = False
        self.check_obcu0 = 0
        self.check_obcu1 = 0
        self.check_inc = 0
        self.check_senior = 0
        self.check_crc = 0
        self.check_auto_run = 0
        self.zc1_count = 0
        self.last_system_count = self.system_count

    def start(self):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read("data.conf")
            obcu_ip = cf.get("udp", "obcu_ip")
            obcu_port = cf.getint("udp", "obcu_port")
            self.file_log.info("Creating socket...")
            self.socket_dst = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket_dst.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.dst_ip = cf.get("udp", "dst_ip")
            self.dst_port = cf.getint("udp", "dst_port")
            self.dst_type = cf.getint("udp", "dst_type")
            if self.dst_type == 0:
                self.HEAD_FRAME = 24
                self.OBCU_HEAD = 24 + 10
                self.FRAME_LEN = 50
            self.socket_dst.bind((obcu_ip, obcu_port))
            # self.socket_dst.setblocking(False)
            self.file_log.info("Socket bind success...")
            self.obcu_count = cf.getint("train", "train_init_count")
            self.check_obcu0 = cf.getint("check", "obcu0")
            self.check_obcu1 = cf.getint("check", "obcu1")
            self.check_senior = cf.getint("check", "senior")
            self.check_crc = cf.getint("check", "crc")
            self.check_auto_run = cf.getint("check", "auto_run")
            self.check_inc = cf.getint("check", "increment")
            if self.check_inc == 1:
                self.obcu_inc_flag = True
            else:
                self.obcu_inc_flag = False
            system_cycle = cf.getfloat("system", "cycle")
            recv_cycle = cf.getfloat("system", "recv_cycle")

            self.train_id = cf.getint("train", "train_id")
            self.zc_id = cf.getint("train", "zc_id")
            self.train_dir = cf.getint("train", "train_dir")
            self.train_mar = cf.getint("train", "train_marshalling")
            self.train_loop = cf.getint("train", "train_loop")
            self.train_offset = cf.getint("train", "train_offset")
            self.top_atp_mode = cf.getint("train", "atp_mode")

            cf.read("senior.conf")
            bytes = []
            bytes.append(int(cf.get("OBCU0", "byte1"), 16))
            bytes.append(int(cf.get("OBCU0", "byte2"), 16))
            bytes.append(int(cf.get("OBCU0", "byte3"), 16))
            bytes.append(int(cf.get("OBCU0", "byte4"), 16))
            bytes.append(int(cf.get("OBCU0", "byte5"), 16))
            bytes.append(int(cf.get("OBCU0", "byte6"), 16))
            bytes.append(int(cf.get("OBCU0", "byte7"), 16))
            bytes.append(int(cf.get("OBCU0", "byte8"), 16))
            self.obcu0_senior = OBCUSenior(bytes)

            bytes = []
            bytes.append(int(cf.get("OBCU1", "byte1"), 16))
            bytes.append(int(cf.get("OBCU1", "byte2"), 16))
            bytes.append(int(cf.get("OBCU1", "byte3"), 16))
            bytes.append(int(cf.get("OBCU1", "byte4"), 16))
            bytes.append(int(cf.get("OBCU1", "byte5"), 16))
            bytes.append(int(cf.get("OBCU1", "byte6"), 16))
            bytes.append(int(cf.get("OBCU1", "byte7"), 16))
            bytes.append(int(cf.get("OBCU1", "byte8"), 16))
            self.obcu1_senior = OBCUSenior(bytes)

            self.list_msg = list()
            self.t1 = timer(self.__recv, args=0, interval=recv_cycle)
            self.t1.start()
            self.t2 = timer(self.__count, args=0, interval=system_cycle)
            self.t2.start()
            self.model_run_mode = 1
            self.zc1_count = 0
            self.last_system_count = self.system_count
            self.file_log.info("model start!")
        except socket.error, e:
            self.close()
            self.file_log.info(e)

    def close(self):
        self.t1.stop()
        self.t2.stop()
        time.sleep(1)
        # self.socket_dst.shutdown(socket.SHUT_RDWR)
        self.socket_dst.close()
        self.model_run_mode = 0
        self.file_log.info("model closed!")

    def __count(self):
        self.system_count += 1
        self.zc1_count += 1
        self.i_frame.set_cur_cycle(self.system_count)
        if self.obcu_inc_flag:
            self.obcu_count += 1

    def __recv(self):
        train = self.__create_train()
        # str_obcu = "ID: %d, loop: %d, offset: %d, atp: %d, count: %d\n" % (train.train_vid, train.loop_id,
        # train.loop_offset, train.atp_mode,
        # self.obcu_count)
        # self.i_frame.add_send_text(str_obcu)
        try:
            # infds, outfds, errfds = select.select([self.socket_dst, ], [], [], 5)
            # if len(infds) != 0:
            recv_msg, recv_addr = self.socket_dst.recvfrom(8192)
            # if len(recv_msg) > 0:
            #     print "recv"
            # else:
            #     print "unrecv"
            if recv_addr[0] != self.dst_ip and recv_addr[1] != self.dst_port:
                return
            hex_msg = recv_msg.encode('hex')
            len_msg = len(hex_msg)

            frame_num = 0
            if self.dst_type == 1:
                self.list_msg.append(hex_msg[0:self.HEAD_FRAME])
                frame_num = (len_msg - self.HEAD_FRAME) / self.FRAME_LEN
            else:
                frame_num = len_msg / self.FRAME_LEN
            for i in range(frame_num):
                if self.dst_type == 1:
                    self.list_msg.append(
                        hex_msg[(self.HEAD_FRAME + i * self.FRAME_LEN):(self.HEAD_FRAME + (i + 1) * self.FRAME_LEN)])
                else:
                    self.list_msg.append(hex_msg[self.HEAD_FRAME + i * self.FRAME_LEN:(i + 1) * self.FRAME_LEN])
            len_list = len(self.list_msg)
            list_pack = list()
            if self.dst_type == 1:
                start_pos = 1
            else:
                start_pos = 0
            if self.dst_type == 1 or self.list_msg[0][4:6] == '06' or self.list_msg[0][4:6] == '07' or self.list_msg[0][4:6] == '08' \
                    or self.list_msg[0][4:6] == '09' or self.list_msg[0][4:6] == '0a':
                if len_list >= 2:
                    if self.dst_type == 1 or self.list_msg[1][4:6] == '16' or self.list_msg[1][4:6] == '17' or self.list_msg[1][4:6] == '18' \
                            or self.list_msg[1][4:6] == '19' or self.list_msg[1][4:6] == '1a':
                        for i in range(start_pos, len_list, 2):
                            train_vid = int(self.list_msg[i][10:12], 16)
                            zc_type = int(self.list_msg[i][12:14], 16) & 0xE0
                            data = self.list_msg[i][10:26] + self.list_msg[i + 1][10:26]
                            zc_count = int(self.list_msg[i + 1][10:12], 16)
                            if train.train_vid == train_vid or train_vid == 0xFF:
                                if zc_type == self.ZC0_TYPE or zc_type == self.ZC1_TYPE \
                                        or zc_type == self.ZC2_TYPE or zc_type == self.ZC3_TYPE:
                                    loop_id = int(self.list_msg[i][14:16], 16) & 0x3F
                                    pack = ZCBase(train_vid, loop_id, zc_type, zc_count, data)
                                    if self.check_auto_run == 1 and self.dst_type == 0:
                                        train.loop_id = loop_id
                                        list_pack.append(pack)
                                    else:
                                        if self.dst_type == 0:
                                            list_pack.append(pack)
                                        elif self.dst_type == 1 and loop_id == train.loop_id:
                                            list_pack.append(pack)
                                        else:
                                            pass
                                else:
                                    pass
                            else:
                                pass
                                # self.file_log.info("Recv %s msg: %s", self.__zctype2str(zc_type), data)
                        for pack in list_pack:
                            # str_log = "Train %d Recv %s (ZC: %d -- OBCU: %d), data: %s" % (train.train_vid,
                            #                                                                self.__zctype2str(pack.zc_type),
                            #                                                                pack.zc_count,
                            #                                                                self.obcu_count,
                            #                                                                pack.data[10:26] + pack.data[36:48])
                            if self.last_loop_id == train.loop_id:
                                pass
                            else:
                                if self.last_loop_id == 0:
                                    pass
                                else:
                                    self.train_offset = 1
                                    train.loop_offset = 1
                            self.last_loop_id = train.loop_id
                            if pack.zc_type == self.ZC1_TYPE:
                                self.__parse_zc1(pack)
                                obcu0 = OBCU0Packet(pack.zc_count, self.obcu_count, train)
                                obcu1 = OBCU1Packet(pack.zc_count, self.obcu_count, train)
                                self.zc1_count = 0
                                if train.atp_mode == self.RM_UNPOS:
                                    # obcu0.loop_id = 1
                                    obcu0.loop_offset = 0
                                    # self.send_obcu0(obcu0)
                                else:
                                    if self.SM <= self.top_atp_mode:
                                        self.atp_mode = self.SM
                                    else:
                                        self.atp_mode = self.RM
                                self.send_obcu1(obcu1)
                                break
                            elif pack.zc_type == self.ZC2_TYPE:
                                str_log = "%d RECV %s[Tzc=%d]: loop id=%d\ndata=%s" % (
                                    self.obcu_count & 0xFF, self.__zctype2str(pack.zc_type),
                                    pack.zc_count, pack.loop_id,
                                    pack.data)
                                self.file_log.info(str_log)
                                self.i_frame.add_recv(str_log)
                                break
                            elif pack.zc_type == self.ZC3_TYPE:
                                str_log = "%d RECV %s[Tzc=%d]: loop id=%d\ndata=%s" % (
                                    self.obcu_count & 0xFF, self.__zctype2str(pack.zc_type),
                                    pack.zc_count, pack.loop_id,
                                    pack.data)
                                self.file_log.info(str_log)
                                self.i_frame.add_recv(str_log)
                                break
                            elif pack.zc_type == self.ZC4_TYPE:
                                str_log = "%d RECV %s[Tzc=%d]: loop id=%d\ndata=%s" % (
                                    self.obcu_count & 0xFF, self.__zctype2str(pack.zc_type),
                                    pack.zc_count, pack.loop_id,
                                    pack.data)
                                self.file_log.info(str_log)
                                self.i_frame.add_recv(str_log)
                                break
                            elif pack.zc_type == self.ZC0_TYPE:
                                if (self.atp_mode == self.RM_UNPOS or self.atp_mode == self.RM) and self.zc1_count > 5:
                                    str_log = "%d RECV %s[Tzc=%d]: loop id=%d\ndata=%s" % (
                                        self.obcu_count & 0xFF, self.__zctype2str(pack.zc_type),
                                        pack.zc_count, pack.loop_id,
                                        pack.data)
                                    self.file_log.info(str_log)
                                    self.i_frame.add_recv(str_log)
                                    obcu0 = OBCU0Packet(pack.zc_count, self.obcu_count, train)
                                    if train.atp_mode == self.RM_UNPOS:
                                        # obcu0.loop_id = 1
                                        obcu0.loop_offset = 0
                                    if self.system_count == self.last_system_count:
                                        pass
                                    else:
                                        self.last_system_count = self.system_count
                                        self.send_obcu0(obcu0)
                                else:
                                    pass
                                break
                            else:
                                self.file_log.info("Recv %d!", pack.zc_type)
                        if self.zc1_count >= 5:
                            self.atp_mode = self.RM
                        self.list_msg = list()
                    else:
                        self.list_msg = list()
                else:
                    pass
            else:
                self.list_msg = list()
        except (KeyboardInterrupt, SystemExit):
            self.file_log.info("Recv error!")
            self.close()

    def __parse_zc1(self, zc1=ZCBase()):
        emc_btn = (int(zc1.data[4:6], 16) & 0xC0) >> 6
        key_sw = (int(zc1.data[6:8], 16) & 0xF8) >> 3
        tar_zc = int(zc1.data[6:8], 16) & 0x07
        psd_st = (int(zc1.data[8:10], 16) & 0x80) >> 7
        tsr_st = (int(zc1.data[8:10], 16) & 0x40) >> 6
        tar_loop = int(zc1.data[8:10], 16) & 0x3F
        tar_offset1 = int(zc1.data[10:12], 16)
        tar_offset2 = int(zc1.data[12:14], 16) & 0xC0
        tar_offset = (tar_offset1 << 2) + (tar_offset2 >> 6)
        sig_sta = (int(zc1.data[12:14], 16) & 0x20) >> 5
        stop_req = (int(zc1.data[12:14], 16) & 0x10) >> 4
        keep_seg = (int(zc1.data[12:14], 16) & 0x08) >> 3
        reen_btn = (int(zc1.data[12:14], 16) & 0x06) >> 1
        spe_cmd = (int(zc1.data[14:16], 16) & 0xF0) >> 4

        str_log = "%d RECV %s[Tzc=%d]: loop=%d,eBtn=%d,kSW=%d,tZC=%d,tloop=%d,tOff=%d,\n" \
                  "sig=%d,sReq=%d,kSeg=%d,PSD=%d,TSR=%d,reBtn=%d,sCmd=%d\ndata=%s" \
                  % (self.obcu_count & 0xFF, self.__zctype2str(zc1.zc_type), zc1.zc_count, zc1.loop_id, emc_btn, key_sw, tar_zc,
                     tar_loop, tar_offset, sig_sta, stop_req, keep_seg, psd_st, tsr_st, reen_btn, spe_cmd, zc1.data)
        self.file_log.info(str_log)
        self.i_frame.add_recv(str_log)

    def __create_train(self):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read("data.conf")
            if cf.getint("system", "refresh") == 1:
                self.train_id = cf.getint("train", "train_id")
                self.zc_id = cf.getint("train", "zc_id")
                self.train_dir = cf.getint("train", "train_dir")
                self.train_mar = cf.getint("train", "train_marshalling")
                self.train_loop = cf.getint("train", "train_loop")
                self.train_offset = cf.getint("train", "train_offset")
                self.top_atp_mode = cf.getint("train", "atp_mode")
                self.check_inc = cf.getint("check", "increment")
                if self.check_inc == 1:
                    self.obcu_inc_flag = True
                else:
                    self.obcu_inc_flag = False
                cf.set("system", "refresh", 0)
                with open("data.conf", "w") as fp_data:
                    cf.write(fp_data)
            elif cf.getint("system", "refresh_tc") == 1:
                self.obcu_count = cf.getint("train", "train_init_count")
                cf.set("system", "refresh_tc", 0)
                with open("data.conf", "w") as fp_data:
                    cf.write(fp_data)
            else:
                pass

            train = TrainBase(self.train_id, self.train_dir, self.train_mar, self.train_loop, self.train_offset,
                              self.zc_id, self.top_atp_mode)
            return train
        except IOError, e:
            self.file_log(e)
            self.close()

    def send(self, msg, msg_type, mode):
        try:
            hex_msg = list()
            str_log = "%d AtpMode:%d SEND %s: " % (self.obcu_count & 0xFF, mode, msg_type)
            for i in range(0, len(msg), 2):
                hex_msg.append(chr(int(msg[i:i + 2], 16)))
                if (i >= self.OBCU_HEAD) and (i < self.OBCU_HEAD + 16) or (i >= (self.OBCU_HEAD + self.FRAME_LEN)):
                    str_log += msg[i:i + 2]
                    str_log += " "
            send_msg = ''.join(hex_msg)
            self.socket_dst.sendto(send_msg, (self.dst_ip, self.dst_port))
            self.file_log.info(str_log)
            self.i_frame.add_send(str_log)
        except socket, e:
            self.file_log.error(e)

    def send_obcu0(self, obcu0=OBCU0Packet()):
        msg = list()
        str_msg = ''
        crc_msg = ''
        if self.dst_type == 1:
            msg.append(self.CAN_HEAD)
            msg.append(self.OBCU_ML_EFF)
            msg.append(self.CAN_RECV_EXTEND[obcu0.loop_id - 1])
            msg.append(self.CAN_SRC_ID)
            msg.append(self.SEND1_DATA)
        else:
            msg.append('80')
            msg.append(self.__num2str(obcu0.train_vid))
            msg.append('82')
            msg.append(self.__num2str(obcu0.zc_id))
            msg.append(self.__num2str(self.system_count & 0xFF))
            msg.append('01')
            msg.append('0019')
            msg.append('20')
            msg.append('40')
            msg.append('000d')
            msg.append('74')
            msg.append('81')
            msg.append('0d')
            msg.append(self.__num2str(self.system_count & 0xFF))
            msg.append('08')
        if self.check_senior == 0:
            msg.append(self.__num2str(obcu0.train_vid))
            byte2 = 0xFF & ((obcu0.type << 6) & 0xC0) | ((obcu0.target_type << 4) & 0x10) \
                    | ((obcu0.train_dir << 3) & 0x08) | (obcu0.zc_id & 0x07)
            msg.append(self.__num2str(byte2))
            byte3 = 0xFF & ((obcu0.marshalling << 6) & 0xC0) | (obcu0.loop_id & 0x3F)
            msg.append(self.__num2str(byte3))
            byte4 = 0xFF & (obcu0.loop_offset >> 2)
            msg.append(self.__num2str(byte4))
            byte5 = 0xFF & ((obcu0.loop_offset & 0x03) << 6) & 0xC0
            msg.append(self.__num2str(byte5))
            msg.append('00')
            msg.append(self.__num2str(obcu0.zc_count & 0xFF))
            msg.append(self.__num2str(obcu0.obcu_count & 0xFF))
        else:
            for i in range(0, 7, 1):
                msg.append(self.__num2str(self.obcu0_senior.bytes[i]))

        if self.dst_type == 0:
            crc_msg = ''.join(msg[15:])
        else:
            crc_msg = ''.join(msg[5:])
        crc = 0
        if self.check_crc == 1:
            crc = self.__cal_crc(crc_msg)

        if self.check_obcu0 == 1 and self.dst_type == 0:
            str_msg = ''.join(msg)
            self.send(str_msg, "OBCU0", obcu0.atp_mode)
            self.file_log.info("SEND: " + str_msg)
            msg = list()
        else:
            pass
        if self.dst_type == 1:
            msg.append(self.OBCU_CRC_EFF)
            msg.append(self.CAN_RECV_EXTEND[obcu0.loop_id - 1])
            msg.append(self.CAN_SRC_ID)
            msg.append(self.SEND1_CRC)
        else:
            msg.append('80')
            msg.append(self.__num2str(obcu0.train_vid))
            msg.append('82')
            msg.append(self.__num2str(obcu0.zc_id))
            msg.append(self.__num2str(self.system_count & 0xFF))
            msg.append('01')
            msg.append('0019')
            msg.append('20')
            msg.append('40')
            msg.append('000d')
            msg.append('74')
            msg.append('81')
            msg.append('13')
            msg.append(self.__num2str(self.system_count & 0xFF))
            msg.append('04')
        msg.append(self.__num2str((crc >> 24) & 0xFF))
        msg.append(self.__num2str((crc >> 16) & 0xFF))
        msg.append(self.__num2str((crc >> 8) & 0xFF))
        msg.append(self.__num2str(crc & 0xFF))
        msg.append('00000000')
        str_msg = ''.join(msg)
        if self.check_obcu0 == 1:
            self.send(str_msg, "OBCU0", obcu0.atp_mode)
            self.file_log.info("SEND: " + str_msg)
        else:
            pass


    def send_obcu1(self, obcu1=OBCU1Packet()):
        msg = list()
        str_msg = ''
        crc_msg = ''
        if self.dst_type == 1:
            msg.append(self.CAN_HEAD)
            msg.append(self.OBCU_ML_EFF)
            msg.append(self.CAN_RECV_EXTEND[obcu1.loop_id - 1])
            msg.append(self.CAN_SRC_ID)
            msg.append(self.SEND1_DATA)
        else:
            msg.append('80')
            msg.append(self.__num2str(obcu1.train_vid))
            msg.append('82')
            msg.append(self.__num2str(obcu1.zc_id))
            msg.append(self.__num2str(self.system_count & 0xFF))
            msg.append('01')
            msg.append('0019')
            msg.append('20')
            msg.append('40')
            msg.append('000d')
            msg.append('74')
            msg.append('81')
            msg.append('0e')
            msg.append(self.__num2str(self.system_count & 0xFF))
            msg.append('08')
        if self.check_senior == 0:
            msg.append(self.__num2str(obcu1.train_vid))
            byte2 = 0xFF & ((obcu1.type << 6) & 0xC0) | ((obcu1.target_type << 4) & 0x10) \
                    | ((obcu1.train_dir << 3) & 0x08) | (obcu1.zc_id & 0x07)
            msg.append(self.__num2str(byte2))
            byte3 = 0xFF & ((obcu1.marshalling << 6) & 0xC0) | (obcu1.loop_id & 0x3F)
            msg.append(self.__num2str(byte3))
            byte4 = 0xFF & (obcu1.loop_offset >> 2)
            msg.append(self.__num2str(byte4))
            byte5 = 0xFF & ((obcu1.loop_offset & 0x03) << 6) | ((obcu1.stop_assure << 5) & 0x20) \
                    | ((obcu1.reentry_light << 3) & 0x18) | (obcu1.atp_mode & 0x07)
            msg.append(self.__num2str(byte5))
            byte6 = 0xFF & ((obcu1.left_psd_cmd << 6) & 0xC0) | ((obcu1.right_psd_cmd << 4) & 0x30) \
                    | ((obcu1.train_park << 3) & 0x08)
            msg.append(self.__num2str(byte6))
            msg.append(self.__num2str(obcu1.zc_count & 0xFF))
            msg.append(self.__num2str(obcu1.obcu_count & 0xFF))
        else:
            for i in range(0, 7, 1):
                msg.append(self.__num2str(self.obcu1_senior.bytes[i]))

        if self.dst_type == 0:
            crc_msg = ''.join(msg[15:])
        else:
            crc_msg = ''.join(msg[5:])
        crc = 0
        if self.check_crc == 1:
            crc = self.__cal_crc(crc_msg)

        if self.check_obcu1 == 1 and self.dst_type == 0:
            str_msg = ''.join(msg)
            self.send(str_msg, "OBCU1", obcu1.atp_mode)
            self.file_log.info("SEND: " + str_msg)
            msg = list()
        else:
            pass
        if self.dst_type == 1:
            msg.append(self.OBCU_CRC_EFF)
            msg.append(self.CAN_RECV_EXTEND[obcu1.loop_id - 1])
            msg.append(self.CAN_SRC_ID)
            msg.append(self.SEND1_CRC)
        else:
            msg.append('80')
            msg.append(self.__num2str(obcu1.train_vid))
            msg.append('82')
            msg.append(self.__num2str(obcu1.zc_id))
            msg.append(self.__num2str(self.system_count & 0xFF))
            msg.append('01')
            msg.append('0019')
            msg.append('20')
            msg.append('40')
            msg.append('000d')
            msg.append('74')
            msg.append('81')
            msg.append('14')
            msg.append(self.__num2str(self.system_count & 0xFF))
            msg.append('04')
        msg.append(self.__num2str((crc >> 24) & 0xFF))
        msg.append(self.__num2str((crc >> 16) & 0xFF))
        msg.append(self.__num2str((crc >> 8) & 0xFF))
        msg.append(self.__num2str(crc & 0xFF))
        msg.append('00000000')
        str_msg = ''.join(msg)
        if self.check_obcu1 == 1:
            self.send(str_msg, "OBCU1", obcu1.atp_mode)
            self.file_log.info("SEND: " + str_msg)
        else:
            pass

    def __cal_crc(self, str_data):
        list_data = list()
        for i in range(0, len(str_data), 2):
            list_data.append(chr(int(str_data[i:i + 2], 16)))
        str_data = ''.join(list_data)
        str_buf = create_string_buffer(str_data)
        crc_c = self.crc_dll.fnCalcCrc32(byref(str_buf), 8)
        return crc_c

    def __zctype2str(self, zctype):
        if zctype == self.ZC0_TYPE:
            return 'ZC0'
        else:
            if zctype == self.ZC1_TYPE:
                return 'ZC1'
            else:
                if zctype == self.ZC2_TYPE:
                    return 'ZC2'
                else:
                    if zctype == self.ZC3_TYPE:
                        return 'ZC3'
                    else:
                        if zctype == self.ZC4_TYPE:
                            return 'ZC4'
                        else:
                            return 'Unknown'

    def __num2str(self, num):
        hex_num = hex(num)
        if len(hex_num) < 4:
            tmp = hex_num.replace('0x', '0')
        else:
            tmp = hex_num.replace('0x', '')
        return tmp