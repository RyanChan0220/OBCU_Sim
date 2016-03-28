# -*- coding: utf-8 -*-

__author__ = 'Ryan'

import ConfigParser


class OBCUSenior(object):
    def __init__(self, bytes=[]):
        self.bytes = bytes


class ZCBase(object):
    def __init__(self, train_vid=0, loop_id=0, zc_type=0, zc_count=0, data=0):
        self.train_vid = train_vid
        self.loop_id = loop_id
        self.zc_type = zc_type
        self.zc_count = zc_count
        self.data = data


class TrainBase(object):
    target_type = 0

    def __init__(self, train_vid=0, train_dir=0, marshalling=0, loop_id=0, loop_offset=0,
                 zc_id=0, atp_mode=0):
        self.train_vid = train_vid
        self.train_dir = train_dir
        self.marshalling = marshalling
        self.loop_id = loop_id
        self.loop_offset = loop_offset
        self.zc_id = zc_id
        self.atp_mode = atp_mode


class OBCU0Packet(TrainBase):
    def __init__(self, zc_count=0, obcu_count=0, train=TrainBase()):
        self.train_vid = train.train_vid
        self.train_dir = train.train_dir
        self.marshalling = train.marshalling
        self.loop_id = train.loop_id
        self.loop_offset = train.loop_offset
        self.zc_id = train.zc_id
        self.atp_mode = train.atp_mode

        self.type = 0
        self.zc_count = zc_count
        self.obcu_count = obcu_count


class OBCU1Packet(TrainBase):
    def __init__(self, zc_count=0, obcu_count=0, train=TrainBase()):
        self.train_vid = train.train_vid
        self.train_dir = train.train_dir
        self.marshalling = train.marshalling
        self.loop_id = train.loop_id
        self.loop_offset = train.loop_offset
        self.zc_id = train.zc_id
        self.atp_mode = train.atp_mode

        self.type = 1

        cf = ConfigParser.ConfigParser()
        cf.read("obcu1.conf")
        self.stop_assure = cf.getint("OBCU1", "stop_assure")
        self.reentry_light = cf.getint("OBCU1", "reentry_light")
        self.left_psd_cmd = cf.getint("OBCU1", "left_psd_cmd")
        self.right_psd_cmd = cf.getint("OBCU1", "right_psd_cmd")
        self.train_park = cf.getint("OBCU1", "train_park")
        self.zc_count = zc_count
        self.obcu_count = obcu_count
