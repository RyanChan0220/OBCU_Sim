# -*- coding: utf-8 -*-
__author__ = 'Ryan'


# ##########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import ConfigParser
import os

# ##########################################################################
## Class OBCUFrame
###########################################################################

class OBCUFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"OBCU Sim  V0.5.5", pos=wx.DefaultPosition,
                          size=wx.Size(1000, 700),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        fgSizer3 = wx.FlexGridSizer(3, 1, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer3.SetMinSize(wx.Size(1000, 600))
        fgSizer4 = wx.FlexGridSizer(3, 8, 0, 0)
        fgSizer4.SetFlexibleDirection(wx.BOTH)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer4.SetMinSize(wx.Size(1000, 100))
        fgSizer14 = wx.FlexGridSizer(3, 6, 0, 0)
        fgSizer14.SetFlexibleDirection(wx.BOTH)
        fgSizer14.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer14.SetMinSize(wx.Size(500, 100))
        self.m_staticText511 = wx.StaticText(self, wx.ID_ANY, u"列车ID", wx.Point(-1, -1), wx.Size(-1, -1), 0)
        self.m_staticText511.Wrap(-1)
        fgSizer14.Add(self.m_staticText511, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_train_ID = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        fgSizer14.Add(self.m_text_train_ID, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_staticText5111 = wx.StaticText(self, wx.ID_ANY, u"所在ZC区域", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_staticText5111.Wrap(-1)
        fgSizer14.Add(self.m_staticText5111, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_zc_id = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        fgSizer14.Add(self.m_text_zc_id, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_staticText5115 = wx.StaticText(self, wx.ID_ANY, u"列车方向", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_staticText5115.Wrap(-1)
        fgSizer14.Add(self.m_staticText5115, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_train_dir = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        fgSizer14.Add(self.m_text_train_dir, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText51112 = wx.StaticText(self, wx.ID_ANY, u"列车编组", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_staticText51112.Wrap(-1)
        fgSizer14.Add(self.m_staticText51112, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_combo_train_sharllChoices = [u"2", u"4", u"6", u"8"]
        self.m_combo_train_sharll = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1),
                                                m_combo_train_sharllChoices, 0)
        self.m_combo_train_sharll.SetSelection(3)
        fgSizer14.Add(self.m_combo_train_sharll, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText5116 = wx.StaticText(self, wx.ID_ANY, u"所在环线ID", wx.Point(-1, -1), wx.Size(70, -1), 0)
        self.m_staticText5116.Wrap(-1)
        fgSizer14.Add(self.m_staticText5116, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_train_loop = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        fgSizer14.Add(self.m_text_train_loop, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText5117 = wx.StaticText(self, wx.ID_ANY, u"列车位置偏移", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_staticText5117.Wrap(-1)
        fgSizer14.Add(self.m_staticText5117, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_train_offset = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        fgSizer14.Add(self.m_text_train_offset, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText83 = wx.StaticText(self, wx.ID_ANY, u"初始车载模式", wx.DefaultPosition, wx.Size(-1, -1), 0)
        self.m_staticText83.Wrap(-1)
        fgSizer14.Add(self.m_staticText83, 0, wx.ALL, 5)

        m_combo_atpmodeChoices = [u"RM_UNPOS", u"RM", u"SM", u"AM", u"AR"]
        self.m_combo_atpmode = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(100, -1),
                                           m_combo_atpmodeChoices, 0)
        self.m_combo_atpmode.SetSelection(0)
        fgSizer14.Add(self.m_combo_atpmode, 0, wx.ALL, 5)

        self.m_button_refresh = wx.Button(self, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer14.Add(self.m_button_refresh, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        fgSizer4.Add(fgSizer14, 1, wx.EXPAND, 5)

        fgSizer15 = wx.FlexGridSizer(3, 4, 0, 0)
        fgSizer15.SetFlexibleDirection(wx.BOTH)
        fgSizer15.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer15.SetMinSize(wx.Size(500, 100))
        self.m_staticText5112 = wx.StaticText(self, wx.ID_ANY, u"DST  IP", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_staticText5112.Wrap(-1)
        fgSizer15.Add(self.m_staticText5112, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_twc_ip = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(120, 20), 0)
        fgSizer15.Add(self.m_text_twc_ip, 0, wx.ALL, 5)

        self.m_staticText5113 = wx.StaticText(self, wx.ID_ANY, u"OBCU  IP", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_staticText5113.Wrap(-1)
        fgSizer15.Add(self.m_staticText5113, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_obcu_ip = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(120, 20), 0)
        fgSizer15.Add(self.m_text_obcu_ip, 0, wx.ALL, 5)

        self.m_staticText51113 = wx.StaticText(self, wx.ID_ANY, u"DST  PORT", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_staticText51113.Wrap(-1)
        fgSizer15.Add(self.m_staticText51113, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_twc_port = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, 20), 0)
        fgSizer15.Add(self.m_text_twc_port, 0, wx.ALL, 5)

        self.m_staticText51114 = wx.StaticText(self, wx.ID_ANY, u"OBCU  PORT", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_staticText51114.Wrap(-1)
        fgSizer15.Add(self.m_staticText51114, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_obcu_port = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, 20), 0)
        fgSizer15.Add(self.m_text_obcu_port, 0, wx.ALL, 5)

        self.m_staticText16 = wx.StaticText(self, wx.ID_ANY, u"目标设备类型", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText16.Wrap(-1)
        fgSizer15.Add(self.m_staticText16, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_comboBox_dstTypeChoices = [u"TWC设备", u"ZC直连"]
        self.m_comboBox_dstType = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                              m_comboBox_dstTypeChoices, 0)
        self.m_comboBox_dstType.SetSelection(1)
        fgSizer15.Add(self.m_comboBox_dstType, 0, wx.ALL, 5)

        fgSizer4.Add(fgSizer15, 1, wx.EXPAND, 5)

        fgSizer3.Add(fgSizer4, 1, wx.EXPAND, 5)

        fgSizer5 = wx.FlexGridSizer(2, 5, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer5.SetMinSize(wx.Size(1000, 100))
        fgSizer12 = wx.FlexGridSizer(2, 4, 0, 0)
        fgSizer12.SetFlexibleDirection(wx.BOTH)
        fgSizer12.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer12.SetMinSize(wx.Size(500, 100))
        self.m_checkBox_obcu0 = wx.CheckBox(self, wx.ID_ANY, u"回复OBCU0", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer12.Add(self.m_checkBox_obcu0, 0,
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_checkBox_obcu1 = wx.CheckBox(self, wx.ID_ANY, u"回复OBCU1", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer12.Add(self.m_checkBox_obcu1, 0,
                      wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button_obcu1 = wx.Button(self, wx.ID_ANY, u"OBCU1 配置", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer12.Add(self.m_button_obcu1, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button_refresh_tc = wx.Button(self, wx.ID_ANY, u"刷新报文周期", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer12.Add(self.m_button_refresh_tc, 0, wx.ALL, 5)

        self.m_staticText77 = wx.StaticText(self, wx.ID_ANY, u"报文周期初始值", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText77.Wrap(-1)
        fgSizer12.Add(self.m_staticText77, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_text_init_cycle = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1), wx.Size(50, -1), 0)
        fgSizer12.Add(self.m_text_init_cycle, 0,
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_checkBox_inc = wx.CheckBox(self, wx.ID_ANY, u"是否自动递增", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer12.Add(self.m_checkBox_inc, 0,
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_checkBox_crc = wx.CheckBox(self, wx.ID_ANY, u"计算CRC", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer12.Add(self.m_checkBox_crc, 0,
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        fgSizer5.Add(fgSizer12, 1, wx.EXPAND, 5)

        fgSizer13 = wx.FlexGridSizer(2, 4, 0, 0)
        fgSizer13.SetFlexibleDirection(wx.BOTH)
        fgSizer13.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer13.SetMinSize(wx.Size(500, 100))
        self.m_checkBox_senior = wx.CheckBox(self, wx.ID_ANY, u"使用高级模式", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer13.Add(self.m_checkBox_senior, 0,
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_button_senior = wx.Button(self, wx.ID_ANY, u"高级模式", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button_senior.Enable(False)

        fgSizer13.Add(self.m_button_senior, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText_curcycle = wx.StaticText(self, wx.ID_ANY, u"                   当前周期：", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.m_staticText_curcycle.Wrap(-1)
        self.m_staticText_curcycle.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))

        fgSizer13.Add(self.m_staticText_curcycle, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl_cur_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                               wx.TE_RIGHT)
        fgSizer13.Add(self.m_textCtrl_cur_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox_autoRun = wx.CheckBox(self, wx.ID_ANY, u"自动跑车", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer13.Add(self.m_checkBox_autoRun, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button_start = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.Size(60, -1), 0)
        fgSizer13.Add(self.m_button_start, 0,
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_checkBox_show = wx.CheckBox(self, wx.ID_ANY, u"显示数据", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_checkBox_show.SetValue(True)
        fgSizer13.Add(self.m_checkBox_show, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.m_button_clear = wx.Button(self, wx.ID_ANY, u"清空显示", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer13.Add(self.m_button_clear, 0, wx.ALL, 5)

        fgSizer5.Add(fgSizer13, 1, wx.EXPAND, 5)

        fgSizer3.Add(fgSizer5, 1, wx.EXPAND, 5)

        fgSizer6 = wx.FlexGridSizer(4, 1, 0, 0)
        fgSizer6.SetFlexibleDirection(wx.BOTH)
        fgSizer6.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer6.SetMinSize(wx.Size(1000, 400))
        self.m_staticText78 = wx.StaticText(self, wx.ID_ANY, u"接收的数据", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText78.Wrap(-1)
        fgSizer6.Add(self.m_staticText78, 0, 0, 5)

        m_listBox_recvChoices = []
        self.m_listBox_recv = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(1000, 200), m_listBox_recvChoices,
                                         wx.LB_HSCROLL)
        fgSizer6.Add(self.m_listBox_recv, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText79 = wx.StaticText(self, wx.ID_ANY, u"发送的数据", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText79.Wrap(-1)
        fgSizer6.Add(self.m_staticText79, 0, 0, 5)

        m_listBox_sendChoices = []
        self.m_listBox_send = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(1000, 200), m_listBox_sendChoices,
                                         wx.LB_HSCROLL)
        fgSizer6.Add(self.m_listBox_send, 0, wx.ALL | wx.EXPAND, 5)

        fgSizer3.Add(fgSizer6, 1, wx.EXPAND, 5)

        self.SetSizer(fgSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button_refresh.Bind(wx.EVT_BUTTON, self.refresh)
        self.m_button_obcu1.Bind(wx.EVT_BUTTON, self.obcu1_conf)
        self.m_button_refresh_tc.Bind(wx.EVT_BUTTON, self.refresh_tc)
        self.m_checkBox_senior.Bind(wx.EVT_CHECKBOX, self.open_senior)
        self.m_button_senior.Bind(wx.EVT_BUTTON, self.senior)
        self.m_button_start.Bind(wx.EVT_BUTTON, self.start)
        self.m_button_clear.Bind(wx.EVT_BUTTON, self.clear_listbox)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def obcu1_conf(self, event):
        os.startfile("obcu1.conf")
        event.Skip()

    def clear_listbox(self, event):
        self.m_listBox_recv.Clear()
        self.m_listBox_send.Clear()
        event.Skip()

    obcu_senior_mode = False
    def open_senior(self, event):
        self.obcu_senior_mode = not self.obcu_senior_mode

        self.m_button_senior.Enable(self.obcu_senior_mode)

        self.m_text_train_ID.Enable(not self.obcu_senior_mode)
        self.m_text_zc_id.Enable(not self.obcu_senior_mode)
        self.m_text_train_dir.Enable(not self.obcu_senior_mode)
        self.m_combo_train_sharll.Enable(not self.obcu_senior_mode)
        self.m_text_train_loop.Enable(not self.obcu_senior_mode)
        self.m_text_train_offset.Enable(not self.obcu_senior_mode)
        self.m_combo_atpmode.Enable(not self.obcu_senior_mode)
        self.m_button_obcu1.Enable(not self.obcu_senior_mode)
        event.Skip()

    frame_run_mode = 0
    start_btn_count = 0

    def start(self, event):
        self.start_btn_count += 1
        if self.start_btn_count % 2 == 1:
            self.enable_all(False)
            self.m_button_start.SetLabel(u"Stop")
            self.frame_run_mode = 1
        else:
            self.enable_all(True)
            if self.frame_run_mode != 0:
                self.m_button_start.SetLabel(u"Start")
                self.frame_run_mode = 0
            else:
                pass
        self.write_all()
        event.Skip()

    def refresh(self, event):
        cf = ConfigParser.ConfigParser()
        cf.read("data.conf")
        cf.set("system", "refresh", 1)
        cf.set("train", "train_id", self.get_train_id())
        cf.set("train", "zc_id", self.get_zc_id())
        cf.set("train", "train_dir", self.get_train_dir())
        cf.set("train", "train_marshalling", self.get_train_marshalling())
        cf.set("train", "train_loop", self.get_loop_id())
        cf.set("train", "train_offset", self.get_loop_offset())
        cf.set("train", "atp_mode", self.get_atp_mode())
        if self.m_checkBox_inc.IsChecked():
            cf.set("check", "increment", 1)
        else:
            cf.set("check", "increment", 0)
        with open("data.conf", "w") as fp_data:
            cf.write(fp_data)
        event.Skip()

    def refresh_tc(self, event):
        cf = ConfigParser.ConfigParser()
        cf.read("data.conf")
        cf.set("system", "refresh_tc", 1)
        cf.set("train", "train_init_count", self.get_init_count())
        with open("data.conf", "w") as fp_data:
            cf.write(fp_data)
        event.Skip()

    def write_all(self):
        cf = ConfigParser.ConfigParser()
        cf.read("data.conf")
        cf.set("udp", "dst_ip", self.get_dst_ip())
        cf.set("udp", "dst_port", self.get_dst_port())
        cf.set("udp", "obcu_ip", self.get_obcu_ip())
        cf.set("udp", "obcu_port", self.get_obcu_port())
        cf.set("udp", "dst_type", self.get_dst_type())

        cf.set("train", "train_id", self.get_train_id())
        cf.set("train", "zc_id", self.get_zc_id())
        cf.set("train", "train_dir", self.get_train_dir())
        cf.set("train", "train_marshalling", self.get_train_marshalling())
        cf.set("train", "train_loop", self.get_loop_id())
        cf.set("train", "train_offset", self.get_loop_offset())
        cf.set("train", "train_init_count", self.get_init_count())
        cf.set("train", "atp_mode", self.get_atp_mode())

        if self.m_checkBox_obcu0.IsChecked():
            cf.set("check", "obcu0", 1)
        else:
            cf.set("check", "obcu0", 0)
        if self.m_checkBox_obcu1.IsChecked():
            cf.set("check", "obcu1", 1)
        else:
            cf.set("check", "obcu1", 0)
        if self.m_checkBox_senior.IsChecked():
            cf.set("check", "senior", 1)
        else:
            cf.set("check", "senior", 0)
        if self.m_checkBox_inc.IsChecked():
            cf.set("check", "increment", 1)
        else:
            cf.set("check", "increment", 0)
        if self.m_checkBox_crc.IsChecked():
            cf.set("check", "crc", 1)
        else:
            cf.set("check", "crc", 0)
        if self.m_checkBox_autoRun.IsChecked():
            cf.set("check", "auto_run", 1)
        else:
            cf.set("check", "auto_run", 0)

        with open("data.conf", "w") as fp_data:
            cf.write(fp_data)

    def enable_all(self, value):
        # self.m_text_train_ID.Enable(value)
        # self.m_text_zc_id.Enable(value)
        # self.m_text_train_dir.Enable(value)
        # self.m_combo_train_sharll.Enable(value)
        # self.m_text_train_loop.Enable(value)
        # self.m_text_train_offset.Enable(value)
        # self.m_combo_atpmode.Enable(value)
        self.m_checkBox_obcu0.Enable(value)
        self.m_checkBox_obcu1.Enable(value)
        self.m_text_twc_ip.Enable(value)
        self.m_text_twc_port.Enable(value)
        self.m_text_obcu_ip.Enable(value)
        self.m_text_obcu_port.Enable(value)
        # self.m_text_init_cycle.Enable(value)
        # self.m_checkBox_inc.Enable(value)
        self.m_checkBox_crc.Enable(value)
        self.m_checkBox_senior.Enable(value)
        self.m_button_senior.Enable(value)
        self.m_button_obcu1.Enable(value)
        self.m_comboBox_dstType.Enable(value)
        self.m_checkBox_autoRun.Enable(value)

    def senior(self, event):
        os.startfile("senior.conf")
        event.Skip()

    def set_cur_cycle(self, value):
        str_value = "%d" % value
        self.m_textCtrl_cur_text.SetValue(str_value)

    def add_send_text(self, str_msg):
        if self.m_checkBox_show.IsChecked():
            self.m_listBox_send.Insert(str_msg + "\n", 0)
        else:
            pass

    def add_recv_text(self, str_msg):
        if self.m_checkBox_show.IsChecked():
            self.m_listBox_recv.Insert(str_msg + "\n", 0)
        else:
            pass

    def set_obcu_ip(self, value):
        self.m_text_obcu_ip.write(value)

    def get_obcu_ip(self):
        return self.m_text_obcu_ip.GetValue()

    def set_obcu_port(self, value):
        str_value = "%d" % value
        self.m_text_obcu_port.write(str_value)

    def get_obcu_port(self):
        return self.m_text_obcu_port.GetValue()

    def set_dst_ip(self, value):
        self.m_text_twc_ip.write(value)

    def get_dst_ip(self):
        return self.m_text_twc_ip.GetValue()

    def set_dst_port(self, value):
        str_value = "%d" % value
        self.m_text_twc_port.write(str_value)

    def get_dst_port(self):
        return self.m_text_twc_port.GetValue()

    def set_dst_type(self, value):
        self.m_comboBox_dstType.SetSelection(value)

    def get_dst_type(self):
        return self.m_comboBox_dstType.GetCurrentSelection()

    def set_train_id(self, value):
        str_value = "%d" % value
        self.m_text_train_ID.write(str_value)

    def get_train_id(self):
        return self.m_text_train_ID.GetValue()

    def set_zc_id(self, value):
        str_value = "%d" % value
        self.m_text_zc_id.write(str_value)

    def get_zc_id(self):
        return self.m_text_zc_id.GetValue()

    def set_train_dir(self, value):
        str_value = "%d" % value
        self.m_text_train_dir.write(str_value)

    def get_train_dir(self):
        return self.m_text_train_dir.GetValue()

    def set_train_marshalling(self, value):
        self.m_combo_train_sharll.SetSelection(value)

    def get_train_marshalling(self):
        return self.m_combo_train_sharll.GetCurrentSelection()

    def set_loop_id(self, value):
        str_value = "%d" % value
        self.m_text_train_loop.write(str_value)

    def get_loop_id(self):
        return self.m_text_train_loop.GetValue()

    def set_loop_offset(self, value):
        str_value = "%d" % value
        self.m_text_train_offset.write(str_value)

    def get_loop_offset(self):
        return self.m_text_train_offset.GetValue()

    def set_atp_mode(self, value):
        self.m_combo_atpmode.SetSelection(value)

    def get_atp_mode(self):
        return self.m_combo_atpmode.GetCurrentSelection()

    def set_init_count(self, value):
        str_value = "%d" % value
        self.m_text_init_cycle.write(str_value)

    def get_init_count(self):
        return self.m_text_init_cycle.GetValue()

    def set_check_obcu0(self, value):
        self.m_checkBox_obcu0.SetValue(value)

    def set_check_obcu1(self, value):
        self.m_checkBox_obcu1.SetValue(value)

    def set_check_inc(self, value):
        self.m_checkBox_inc.SetValue(value)

    def set_check_crc(self, value):
        self.m_checkBox_crc.SetValue(value)

    def set_check_senior(self, value):
        self.m_checkBox_senior.SetValue(value)

    def set_check_auto_run(self, value):
        self.m_checkBox_autoRun.SetValue(value)

class OBCUWindow(wx.App):
    def OnInit(self):
        print "OBCU Windows Start!"
        self.frame = OBCUFrame(None)
        self.frame.Show(True)
        try:
            cf = ConfigParser.ConfigParser()
            cf.read("data.conf")
            #net configer
            obcu_ip = cf.get("udp", "obcu_ip")
            obcu_port = cf.getint("udp", "obcu_port")
            dst_ip = cf.get("udp", "dst_ip")
            dst_port = cf.getint("udp", "dst_port")
            dst_type = cf.getint("udp", "dst_type")
            self.frame.set_obcu_ip(obcu_ip)
            self.frame.set_obcu_port(obcu_port)
            self.frame.set_dst_ip(dst_ip)
            self.frame.set_dst_port(dst_port)
            self.frame.set_dst_type(dst_type)
            #train configer
            train_id = cf.getint("train", "train_id")
            zc_id = cf.getint("train", "zc_id")
            train_dir = cf.getint("train", "train_dir")
            train_marshalling = cf.getint("train", "train_marshalling")
            train_loop = cf.getint("train", "train_loop")
            train_offset = cf.getint("train", "train_offset")
            train_init_count = cf.getint("train", "train_init_count")
            atp_mode = cf.getint("train", "atp_mode")
            self.frame.set_train_id(train_id)
            self.frame.set_zc_id(zc_id)
            self.frame.set_train_dir(train_dir)
            self.frame.set_train_marshalling(train_marshalling)
            self.frame.set_loop_id(train_loop)
            self.frame.set_loop_offset(train_offset)
            self.frame.set_init_count(train_init_count)
            self.frame.set_atp_mode(atp_mode)
            #check configer
            check_obcu0 = cf.getint("check", "obcu0")
            check_obcu1 = cf.getint("check", "obcu1")
            check_senior = cf.getint("check", "senior")
            check_increment = cf.getint("check", "increment")
            check_crc = cf.getint("check", "crc")
            check_auto_run = cf.getint("check", "auto_run")
            if check_obcu0 == 1:
                self.frame.set_check_obcu0(True)
            else:
                self.frame.set_check_obcu0(False)
            if check_obcu1 == 1:
                self.frame.set_check_obcu1(True)
            else:
                self.frame.set_check_obcu1(False)
            if check_senior == 1:
                self.frame.set_check_senior(True)
            else:
                self.frame.set_check_senior(False)
            if check_increment == 1:
                self.frame.set_check_inc(True)
            else:
                self.frame.set_check_inc(False)
            if check_crc == 1:
                self.frame.set_check_crc(True)
            else:
                self.frame.set_check_crc(False)
            if check_auto_run == 1:
                self.frame.set_check_auto_run(True)
            else:
                self.frame.set_check_auto_run(False)
        except IOError, e:
            pass
        return True

    def OnExit(self):
        print "OBCU Windows Exit!"



