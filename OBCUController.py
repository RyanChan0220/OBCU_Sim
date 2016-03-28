# -*- coding: utf-8 -*-

__author__ = 'Ryan'

from OBCUFrame import OBCUWindow
from OBCUModel import OBCUModel
from Timer import timer


class FrameInterface(object):
    def __init__(self, frame):
        self.frame = frame

    def add_recv(self, str_value):
        self.frame.add_recv_text(str_value)

    def add_send(self, str_value):
        self.frame.add_send_text(str_value)

    def set_cur_cycle(self, value):
        self.frame.set_cur_cycle(value)


def loop(args):
    if args[0].frame_run_mode == 0 and args[1].model_run_mode == 1:
        args[1].close()
    elif args[0].frame_run_mode == 1 and args[1].model_run_mode == 0:
        args[1].start()
    else:
        pass

if __name__ == '__main__':
    obcu_window = OBCUWindow()
    window_interface = FrameInterface(obcu_window.frame)
    obcu_sim = OBCUModel(window_interface)
    t1 = timer(loop, (obcu_window.frame, obcu_sim), interval=0.5)
    t1.start()
    obcu_window.MainLoop()
    t1.stop()




