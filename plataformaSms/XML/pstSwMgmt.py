# -*- coding: utf-8 -*-
import main
import sys
import re
import time
from pathlib import Path

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtNetwork import *
from PySide6.QtWidgets import *

from datetime import date, datetime
import os
import threading
import pickle
import serial
import struct
import threading
import binascii
import backend.db_acess as db
import modules.ui_functions
from widgets import circular_progress

##############################################################
LOST_CONNECTION_THRESH_SEC = 15
########################################################################
# PEGA INFORMAÇOES DO BANCO DE DADOS
# -----------------------------------
local_database = "platforms/resources/database/optinsms.db"
servidor_local = db.listar_all_reg_server_config(local_database)
print(servidor_local[2])
if (servidor_local[0] == 1):
    print("NOME :" + servidor_local[1])
    print("IP :" + servidor_local[2])
    print("PORTA :" + str(servidor_local[3]))
    g_current_board_addr = QHostAddress(str(servidor_local[2]))
    g_current_board_port = int(servidor_local[3])
    g_local_addr = QHostAddress(str(servidor_local[2]))

else:
    sys.exit("não existe servidor configurado sem servidor")

g_buf = ""
UeNum = 0
cara = 0
msg_cara = 0
cara_r = 0
msg_r = 0
g_host_list = {}

# remet = "ALPRESTAMO"
# campanha = (
#    "%s" % ("TENES UN PRESTAMO LISTO PARA RETIRAR! Hasta 300.000 ARS. Entra ahora en ALPRESTAMO. Hace click YA en https://bit.ly/38CcaMV"))

remet = "20050"
campanha = (
    "%s" % ("VIVO Informa, não perca a oportunidade de fazer um upgrade do seu celular !"))


Flash = "NAO"
# -------------------------------------------------------------------------------------

# 保存的当前过程中的手机上号记录，便于回溯
# Salve o registro do número no telefone no processo atual para fácil retrospectão

# MCC	MNC	ISO	CIDADE	CODE	REDE
# 724	26	br	Brazil	55		AmericaNet
# 724	12	br	Brazil	55		Claro/Albra/America Movil
# 724	38	br	Brazil	55		Claro/Albra/America Movil
# 724	05	br	Brazil	55		Claro/Albra/America Movil
# 724	01	br	Brazil	55		Vivo S.A./Telemig
# 724	34	br	Brazil	55		CTBC Celular SA (CTBC)
# 724	33	br	Brazil	55		CTBC Celular SA (CTBC)
# 724	32	br	Brazil	55		CTBC Celular SA (CTBC)
# 724	08	br	Brazil	55		TIM
# 724	39	br	Brazil	55		Nextel (Telet)
# 724	00	br	Brazil	55		Nextel (Telet)
# 724	30	br	Brazil	55		Oi (TNL PCS / Oi)
# 724	31	br	Brazil	55		Oi (TNL PCS / Oi)
# 724	16	br	Brazil	55		Brazil Telcom
# 724	24	br	Brazil	55		Amazonia Celular S/A
# 724	54	br	Brazil	55		PORTO SEGURO TELECOMUNICACOES
# 724	15	br	Brazil	55		Sercontel Cel
# 724	07	br	Brazil	55		CTBC/Triangulo
# 724	19	br	Brazil	55		Vivo S.A./Telemig
# 724	03	br	Brazil	55		TIM
# 724	02	br	Brazil	55		TIM
# 724	04	br	Brazil	55		TIM
# 724	37	br	Brazil	55		Unicel do Brasil Telecomunicacoes Ltda
# 724	23	br	Brazil	55		Vivo S.A./Telemig
# 724	11	br	Brazil	55		Vivo S.A./Telemig
# 724	10	br	Brazil	55		Vivo S.A./Telemig
# 724	06	br	Brazil	55		Vivo S.A./Telemig


# ggsm1h = """ <?xml version='1.0' encoding = 'UTF-8' standalone = 'no' ?>
#    <content>
#        <rxGain> 50</rxGain>
#        <txPwr> 40</txPwr>
#        <cell itemCnt = "2"> """
# ggsmcvivo = """
#            <item>
#                <arfcnList>
#                    <arfcn itemCnt = "1"> 607</arfcn>
#                </arfcnList>
#                <mcc> 724</mcc>
#                <mnc> 11 </mnc>
#                <lai> 4011</lai>
#                <sib3CellId> 11047</sib3CellId>
#                <bsic> 7</bsic>
#                <cro> 62</cro>
#                <rxLevAccMin> 0</rxLevAccMin>
#                <reselctHyst> 0</reselctHyst>
#                <nbFreq> 802</nbFreq>
#            </item>
#            """

# ggsmcclaro = """
#            <item>
#                <arfcnList>
#                    <arfcn itemCnt = "1"> 597</arfcn>
#                </arfcnList>
#                <mcc> 724</mcc>
#                <mnc> 5</mnc>
#                <lai> 3085</lai>
#                <sib3CellId> 585</sib3CellId>
#                <bsic> 11</bsic>
#                <cro> 62</cro>
#                <rxLevAccMin> 0</rxLevAccMin>
#                <reselctHyst> 0</reselctHyst>
#                <nbFreq> 53</nbFreq>
#            </item>
#            """

# ggsmctim = """
#           <item>
#                <arfcnList>
#                    <arfcn itemCnt = "1"> 597</arfcn>
#                </arfcnList>
#                <mcc> 724</mcc>
#                <mnc> 2</mnc>
#                <lai> 3085</lai>
#                <sib3CellId> 585</sib3CellId>
#                <bsic> 11</bsic>
#                <cro> 62</cro>
#                <rxLevAccMin> 0</rxLevAccMin>
#                <reselctHyst> 0</reselctHyst>
#                <nbFreq> 613</nbFreq>
#            </item>

#            """

# ggsmcoi = """
#           <item>
#                <arfcnList>
#                    <arfcn itemCnt = "1"> 607</arfcn>
#                </arfcnList>
#                <mcc> 724</mcc>
#                <mnc> 31</mnc>
#                <lai> 4011</lai>
#                <sib3CellId> 11047</sib3CellId>
#                <bsic> 7</bsic>
#                <cro> 62</cro>
#                <rxLevAccMin> 0</rxLevAccMin>
#                <reselctHyst> 0</reselctHyst>
#                <nbFreq> 609</nbFreq>
#            </item>
#            """

# ggsm1f = """
#        </cell>
#    </content>
#    """

# ggsmc1 = None
# ggsmc2 = None
# setacel = None  # (ggsm1h + ggsmc1 + ggsmc2 + ggsm1f)
# print (setacel)

g_ue_info_list = []
g_net_mode_list = ["NO_PHY",  "GSM-WB", "GSM",  "WCDMA",  "FDD-LTE", "TDD-LTE",
                   "FDD-LTE-EXT",  "TDD-LTE-EXT", "NMM-TDD-GSM", "NMM-FDD-WCDMA", "INTERFERING"]


g_host_addr_list = []
# QHostAddress(str("168.1.14.10")),
# g_host_port = [9001, 9001, 9001, 9001, 9001, 9001, 9001, 9001, 9001, 9001, 9001]
pqp = 0
operando = False
ult_op = "NENHUMA"
vivo_sms = 0
claro_sms = 0
tim_sms = 0
oi_sms = 0
lte_b = "0000"
g_udp_socket = None
g_all_ue_list_table = None
g_filter_list_table = None
g_host_list_box = None
g_ue_info_window = None
g_set_box = None
g_saved_ue_list_edit_table = None
g_serial_port = None
widgets = None
window_obj = None
g_msg_list_tb = None
g_msg_txt = None


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
        # option.setForegroundColor = QtCore.Qt.QColor.red


def showErro(info):
    global g_set_box
    # QMessageBox.critical.setStyleSheet("background-color: gray")
    QMessageBox.critical(g_set_box, "AVISO", str(info))

    pass


class SerialPort(QObject):
    def __init__(self, dev_name):
        self.dev_name = dev_name
        self.serial = serial.Serial(dev_name, 115200, timeout=0.1)
        if not self.serial.isOpen():
            self.serial.open()
        print("serial is open " + str(self.serial.isOpen()))

        self.timer = QtCore.QTimer()
        # QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.readData)

        self.timer.start(100)

        self.timer2 = QtCore.QTimer()
        # QtCore.QObject.connect(self.timer2,QtCore.SIGNAL("timeout()"), self.sendHeatBeat)
        self.timer2.start(5000)

        self.data_byte = bytearray()
        self.data_offset = 0
        self.fouding_hdr = True
        self.hdr_offset = 0
        self.msg_len = 0

    def readData(self):
        print("Start read serial ")
        count = self.serial.inWaiting()
        print("serial had data len " + str(count))
        if count > 0:
            rec_str = self.serial.read(count)
        else:
            return
        self.data_byte = self.data_byte + rec_str
        self.anaBuf()
        pass

    def anaBuf(self):
        global g_buf
        data_len = len(self.data_byte)
        i = self.data_offset
        if(self.fouding_hdr == True):
            if((self.hdr_offset + self.msg_len) <= data_len):
                g_buf = str(
                    self.data_byte[(self.hdr_offset + 8):(self.hdr_offset + 8 + self.msg_len)])
                processBoardMsg(True)
        else:
            while((i + 8) < data_len):
                hdrValue = struct.unpack("!I", self.data_byte[i:(i+4)])
                if(hdrValue == 0x1A2B3C4D):
                    self.founding_hdr = True
                    self.msg_len = struct.unpack(
                        "I", self.data_byte[(i + 4):(i + 8)])
                    self.hdr_offset = true
                    self.data_offset = i
                    return self.anaBuf()  # goto check if buf got a total msg data
                i = i + 1

        pass

    def sendHeatBeat(self):
        self.sendData("HeatBeat")
        pass

    def sendData(self, send_string):
        str_hdr = struct.pack("!I", 0x1A2B3C4D)
        msg_len = len(send_string)
        str_len = struct.pack("I", msg_len)
        self.serial.write(str_hdr + str_len + send_string)


class WlPort(QUdpSocket):
    def __init__(self, parent=None):
        super(WlPort, self).__init__(parent)
        self.timer = QtCore.QTimer()
        # QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.sendHeatBeat)
        self.timer.timeout.connect(self.sendHeatBeat)
        self.timer.start(5000)

    def udpReceive(self):
        global g_buf, g_current_board_addr, g_current_board_port
        # print ("Reading Udp -----\n")
        rslt = self.hasPendingDatagrams()
        # print "hasPendingData %s"%(str(rslt),)
        while self.hasPendingDatagrams():
            (g_buf, g_current_board_addr,
             g_current_board_port) = self.readDatagram(8092)
            processBoardMsg()
            # print(state_str)
            # print(g_buf)#.split().pop(4))
        # if g_buf.split().pop(4) == "MODE[GSM-WB]":
        #          load_push_button.setStyleSheet("background-color: green")
        #        elif
        #          load_push_button.setStyleSheet("background-color: red")

    def sendHeatBeat(self):
        global g_host_addr_list, g_current_board_port
        hbMsg = "HeatBeat".encode()
        for item in g_host_addr_list:
            self.writeDatagram(hbMsg, item, g_current_board_port)


def initUdpSocket(objectLc):
    global g_udp_socket, g_cfg, g_current_board_port
    local_database = "platforms/resources/database/optinsms.db"
    servidor_local = db.listar_all_reg_server_config(local_database)
    print("------>" + str(servidor_local[2]))
    if (servidor_local[0] == 1):
        print("---------------------------------------------*")
        print("NOME :" + servidor_local[1])
        print("IP :" + servidor_local[2])
        print("PORTA :" + str(servidor_local[3]))
        print("---------------------------------------------*")
    else:
        print("sem servidor")

    loadCfg()
    if(None == g_udp_socket):
        g_udp_socket = WlPort()

    print("IP BINDING : " + str(servidor_local[2]))
    rslt = g_udp_socket.bind(QHostAddress(
        str(servidor_local[2])), g_current_board_port)

    if False == rslt:
        print("Udp Binding Error")
    else:
        print("Udp Binding Success")

    g_udp_socket.readyRead.connect(g_udp_socket.udpReceive)
    if False == rslt:
        print("Udp Connet Error")
    else:
        print("Udp Connet Success")


def closeUdpSocket():
    global g_host_addr_list, g_cfg
    g_udp_socket.close()
    g_host_addr_list.clear()
    print("close port " + str(g_current_board_port))


def sendUdpData(msg, peer_addr, peer_port):
    global g_udp_socket
    g_udp_socket.writeDatagram(msg, peer_addr, peer_port)


def sendStopToAllCell():
    global g_host_list
    for item in g_host_list.values():
        item.stopCell()
        # time.sleep(1)
        # item.startCell()
        # print(item.mode)
        # print(item.temp)
        # item.reboot0()
    time.sleep(0.1)  # 等待把所有的reboot命令都发给单板
    # Aguarde que todos os comandos de reinicialização sejam enviados para a placa de revestimento


def sendStopToAllBoard():
    global g_host_list
    for item in g_host_list.values():

        item.reboot0()
    time.sleep(0.1)  # 等待把所有的reboot命令都
    # Aguarde para colocar todos os comandos de reinicialização


def start_op():
    global g_host_list
    for item in g_host_list.values():
        item.setTime()
        # print(time.time())
        time.sleep(0.2)
        item.send_sms()
        time.sleep(1.2)

        item.startCell()
        # print(item.name)
        # print(g_buf.split().pop(5))
        # item.reboot0()
    time.sleep(0.1)  # 等待把所有的reboot命令都发给单板
    # Aguarde que todos os comandos de reinicialização sejam enviados para a placa de revestimento


def troca_op():
    global g_host_list
    print("chamou")
    for item in g_host_list.values():

        item.set_bts()
        time.sleep(1.2)
        item.reboot0()

        # print(item.name)
        # print(g_buf.split().pop(5))
        # item.reboot0()
    time.sleep(0.1)  # 等待把所有的reboot命令都发给单板
    # Aguarde que todos os comandos de reinicialização sejam enviados para a placa de revestimento


def processBoardMsg(is_serial=False):
    global g_udp_socket, g_buf, g_current_board_addr, g_current_board_port
    try:
        g_buf = bytes(g_buf).decode()
    except:
        # print(g_buf)
        pass
    msg_type_id = g_buf[0:3]
    # print("receive msg msg Id :" + str(msg_type_id))
    if msg_type_id == "103":
        hdlUeInfoIndi(g_buf)
    else:
        hdlHostMsg(g_buf, g_current_board_addr, msg_type_id, is_serial)


# 处理UE消息
# Processe mensagens UE
def hdlUeInfoIndi(msg):
    global g_ue_info_list, g_all_ue_list_table, g_filter_list_table
    # print(f"Novo celular Encontrado:\n{str(msg)}")
    # print(f"Dados Recebidos: {str(msg)}")
    # print("get Ue Rpt:" + str(msg))
    ueIndi = UeIndi(msg)
    g_ue_info_list.append(ueIndi)
    g_ue_info_window.addUeIndi(ueIndi)
    # g_all_ue_list_table.appendRow(ueIndi)
    # ueIndi.in_filter == True:
    # g_filter_list_table.appendRow(ueIndi)


def hdlHostMsg(msg_str, peer_addr, msg_type_id, is_serial):
    global g_set_box, g_host_list
    if is_serial is False:
        ip_int = peer_addr.toIPv4Address()
    else:
        ip_int = peer_addr

    # 检查这个远端IP对应的主机是否已经存在
    # Verifique se o host correspondente a este IP remoto já existe

    if ip_int in g_host_list.keys():
        g_host_list[ip_int].hdlInput(msg_str, msg_type_id)
    else:
        # 新建立一个Host并添加到字典中
        # Crie um novo Host e adicione-o ao dicionário
        g_host_list[ip_int] = HostBox()
        # print("IP INIT:",ip_int)
        # 显示在左边栏中
        # Aparece no trilho esquerdo

        g_set_box.addHost(g_host_list[ip_int])
        g_host_list[ip_int].hdlInput(msg_str, msg_type_id)
        # print(g_host_list[ip_int])


def getUeInfoInCfg(imsi):
    global g_cfg
    if imsi in g_cfg["saved_ue_list"].keys():
        return g_cfg["saved_ue_list"][imsi]
    else:
        return None


def updateUeInfoInCfg(imsi, ueInfo):
    global g_cfg
    g_cfg["saved_ue_list"][imsi] = ueInfo


def addSavedUeInfo(imsi, name):
    global g_cfg
    if None != name:
        g_cfg["saved_ue_list"][imsi] = (name, "IN_FILTER")
    updateSavedUeListTb()


def delUeInfoInCfg(imsi):
    global g_cfg
    if imsi in g_cfg["saved_ue_list"].keys():
        # print("Del UE " + imsi)
        del g_cfg["saved_ue_list"][imsi]
        updateSavedUeListTb()
    else:
        return None


def dumpCfg():
    global g_cfg
    blFile = open("./lcCfg.txt", "wb")
    pickle.dump(g_cfg, blFile)
    blFile.close()


def loadCfg():
    # ------------------------------------------
    # CARREGA AS CONFIGURAÇÕES INICIAIS
    # -------------------------------------------
    global g_cfg
    g_host_addr_list.clear()
    # dumpCfg()
    # blFile = open("./smspy/lcCfg.txt", "rb")
    # g_cfg = pickle.load(blFile,encoding='iso-8859-1')
    # g_cfg = pickle.load(blFile)

    # ------------------------------------------
    # CARREGA MODULOS DO BD
    # -------------------------------------------

    local_database = "platforms/resources/database/optinsms.db"
    modulos = db.listar_all_modulos_cadastrados(local_database)
    for row_number, row_data in enumerate(modulos):
        ip_addr = QHostAddress(row_data[2])
        g_host_addr_list.append(ip_addr)
        if row_number == 0:
            bs_ip_start = ip_addr.toString()

        # print("add bs ip " + ip_addr.toString())
        # print(len(modulos))

    # print(bs_ip_start)
    g_cfg = {"bs_cnt": len(modulos), "bs_ip_start": bs_ip_start, "saved_ue_list": {
        '724102007000794': ('Opt-Vivo', 'IN_FILTER')}, "host_cfgs": {}}


def getTxtInStrTuple(strTuple, key):
    reg_car = r'%s\[(?P<key_word>.*?)\]' % (key,)
    # reg_car = reg_card.decode()#r'%s\[(?P<key_word>.*?)\]'%(key,)
    # print(reg_car)
    group = re.search(reg_car, strTuple)
    if None == group:
        return " "
    else:
        # print(str(group.group("key_word")))
        return str(group.group("key_word"))


def getTxtInStrTuple2(strTuple, key):
    reg_car = r'%s(?P<key_word>.*?)\s' % (key,)
    # reg_car = reg_card.decode()#r'%s\[(?P<key_word>.*?)\]'%(key,)
    # print(reg_car)
    group = re.search(reg_car, strTuple)
    if None == group:
        return " "
    else:
        # print(str(group.group("key_word")))
        return str(group.group("key_word"))


def updateSavedUeListTb():
    global g_saved_ue_list_edit_table, g_cfg
    if None != g_saved_ue_list_edit_table:
        # g_saved_ue_list_edit_table.loadFromCfg() #g_cfg["saved_ue_list"])
        pass


def showAddUeDialog(imsi=None):
    global myDialog
    myDialog = AddUeDialog(imsi)
    myDialog.show()
# 单板状态配置管理器


def dumpUeInfoList(file_name):
    global g_ue_info_list
    fd = open(file_name, "w")
    fd.write(
        ("BOARD  TIME             REG_TYPE    IMSI   RSRP  UL-CQI UL_RSSI UL-TA\n"))
    for item in g_ue_info_list:
        fd.write(item.text())
    fd.close()


def loadUeInfoList(file_name):
    global g_ue_info_list
    del(g_ue_info_list[0:])
    fd = open(file_name, "r")
    line_number = 0
    try:
        for line in fd:
            if line_number > 0:
                ueIndi = UeIndi(line, True)
                g_ue_info_list.append(ueIndi)
                g_ue_info_window.addUeIndi(ueIndi)
            line_number += 1

    finally:
        fd.close()


def addUeInFilter():
    global g_ue_info_list
    global g_cfg
    unfoundUeList = []
    foundUeIndiList = []
    lastUeIndi = None
    # unfoundUeList.clear()
    for item in g_cfg["saved_ue_list"].keys():
        if g_cfg["saved_ue_list"][item][1] == "IN_FILTER":
            unfoundUeList.append(item)

    for ueIndi in g_ue_info_list:
        lastUeIndi = ueIndi
        if ueIndi.imsi in g_cfg["saved_ue_list"].keys():
            try:
                unfoundUeList.remove(ueIndi.imsi)
                # foundUeIndiList.append(ueIndi)

            finally:
                pass

    if len(unfoundUeList) < 2:
        return
    if None == lastUeIndi:
        lastUeIndi = UeIndi(
            "ps_wl01 20161119-14:16:49 TA_REQ 460021010698289 -140  -10  -25 1", True)

    itemLen = len(unfoundUeList)
    for item in unfoundUeList:
        ueIndi = UeIndi(lastUeIndi, False, True, item)
        lastUeIndi = ueIndi
        g_ue_info_list.append(ueIndi)
        g_ue_info_window.addUeIndi(ueIndi)
        itemLen = itemLen - 1
        if itemLen < 2:
            return


def getXmlFileStr(input_str):
    ret1 = input_str.find('<?xml')
    ret2 = input_str.find('</content>')
    ret2 += len('</content>')
    if ret1 >= 0:
        if ret2 > ret1:
            rtv = input_str[ret1:ret2]
            return rtv
    return None

# def carrega_msg(msg_str):
#        ret1 = input_str.find('<?xml')
#        ret2 = input_str.find('</content>')
#        ret2 += len('</content>')
#        if ret1 >= 0:
#                if ret2 > ret1:
#                        rtv = input_str[ret1:ret2]
#                        return rtv
#        return None


class HostBox(QWidget):
    def __init__(self, parent=None):
        global g_current_board_addr, g_current_board_port
        super(HostBox, self).__init__(parent)
        self.peer_addr = g_current_board_addr
        self.peer_port = g_current_board_port
        self.peer_connect = False
        self.last_hb_time = 0  # Last Heartbeat time
        # "NO-PHY","GSM", "GSM-EXT","WCDMA", "FDD-LTE", "TDD-LTE", "FDD-LTE-EXT"
        self.net_mode = "UNKNOWN"
        # "EODEB_START", "ENODEB_CLOSE","IDLE", "SNIFFER", "RE_BOOTING"
        self.weilan_state = "SNIFFER"
        self.version = ""
        self.nmm_cfg = ""
        self.weilan_cfg = ""
        self.cell_para = ""
        self.current_xml = "XML_NONE"  # XML_CELL_PARA, XML_WEILAN_CFG, XML_NMM_CFG
        self.status = ""
        self.temp = "50"
        self.gps = "FALSE"
        self.timer = QtCore.QTimer()
        self.current_sys_sec = self.currentSyssec()

        # QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.onTimer)
        self.timer.timeout.connect(self.onTimer)
        # self.setStyleSheet("background-color: gray; color: black; font-weight: bold")
        # QWidget.__init__(self)
        # 读取配置 (leia a configuração)
        top_layout = QVBoxLayout(self)
        self.staus_bar = QStatusBar()
        top_layout.addWidget(self.staus_bar)
        self.staus_bar.showMessage(self.tr("Version-unkown "))

        self.net_mode_boxnet_mode_box = QComboBox()
        self.net_mode_boxnet_mode_box.insertItem(0, self.tr(" SetNetMode"))
        netModeIdx = 1
        for item in g_net_mode_list:  # "NO_PHY",  "GSM-WB", "GSM",  "WCDMA",  "FDD-LTE", "TDD-LTE", "FDD-LTE-EXT",  "TDD-LTE-EXT", "NMM-TDD-GSM", "NMM-FDD-WCDMA", "INTERFERING"
            self.net_mode_boxnet_mode_box.insertItem(netModeIdx, self.tr(item))
            netModeIdx = netModeIdx + 1

        button_set_time = QPushButton(self.tr("SyncTime"))
        button_get_version = QPushButton(self.tr("GetVersion"))
        button_start = QPushButton(self.tr("StartCell"))
        button_stop = QPushButton(self.tr("StopCell"))
        button_sniffer = QPushButton(self.tr("StartSniffer"))
        button_reboot0 = QPushButton(self.tr("RebootToIdle"))
        button_reboot1 = QPushButton(self.tr("RebootAllCell"))
        button_reboot2 = QPushButton(self.tr("RebootAndStartSniffer"))
        ctrl_button_layout = QGridLayout()
        ctrl_button_layout.addWidget(button_set_time, 0, 0)
        ctrl_button_layout.addWidget(button_get_version, 0, 1)
        ctrl_button_layout.addWidget(self.net_mode_boxnet_mode_box, 0, 2)
        ctrl_button_layout.addWidget(button_reboot0, 1, 0)
        ctrl_button_layout.addWidget(button_reboot1, 1, 1)
        ctrl_button_layout.addWidget(button_reboot2, 1, 2)
        ctrl_button_layout.addWidget(button_start, 2, 0)
        ctrl_button_layout.addWidget(button_stop, 2, 1)
        ctrl_button_layout.addWidget(button_sniffer, 2, 2)
        top_layout.addLayout(ctrl_button_layout)
        button_send = QPushButton(self.tr("Send Cmd"))
        button_send.setFixedWidth(150)
        self.cmd_line = QLineEdit()
        self.cmd_line.setMinimumWidth(240)
        cmd_layout = QHBoxLayout()
        cmd_layout.addWidget(button_send)
        cmd_layout.addWidget(self.cmd_line)
        top_layout.addLayout(cmd_layout)
        self.history_box = QTextEdit(self)  # 交互窗口 (Janela interativa)
        self.history_box.setStyleSheet(
            "QTextEdit { background-color: gray; font-weight: bold; color: white; border-radius: 9px}")
        self.history_box.verticalScrollBar()
        self.history_box.setWordWrapMode(QTextOption.NoWrap)
        self.history_box.setMaximumHeight(150)
        top_layout.addWidget(self.history_box)

        cell_para_box = QComboBox()
        cell_para_box.insertItem(0, self.tr("WireLess Cfgs"))
        cell_para_box.insertItem(1, self.tr("GET_CELL_PARA"))
        cell_para_box.insertItem(2, self.tr("SET_CELL_PARA"))
        cell_para_box.insertItem(3, self.tr("GET_NMM_PARA"))
        cell_para_box.insertItem(4, self.tr("SET_NMM_PARA"))
        weilan_cfg_box = QComboBox()
        weilan_cfg_box.insertItem(0, self.tr("App Cfgs"))
        weilan_cfg_box.insertItem(1, self.tr("GET_WORK_CFG"))
        weilan_cfg_box.insertItem(2, self.tr("SET_WORK_CFG"))
        weilan_cfg_box.insertItem(3, self.tr("GET_APP_CFG"))
        weilan_cfg_box.insertItem(4, self.tr("SET_APP_CFG"))
        weilan_cfg_box.insertItem(5, self.tr("GET_APP_CFG_EXT"))
        weilan_cfg_box.insertItem(6, self.tr("SET_APP_CFG_EXT"))

        board_cfg_box = QComboBox()
        board_cfg_box.insertItem(0, self.tr("GET_SYNC_CALI_FILE"))
        board_cfg_box.insertItem(1, self.tr("GET_PW_PWR_CALI_FILE"))

        xml_cfg_layout = QHBoxLayout()
        # xml_cfg_layout.setStyleSheet("background-color: gray; color: black; font-weight: bold")
        xml_cfg_layout.addWidget(cell_para_box)
        xml_cfg_layout.addWidget(weilan_cfg_box)
        xml_cfg_layout.addWidget(board_cfg_box)
        top_layout.addLayout(xml_cfg_layout)
        self.xml_box = QTextEdit(self)  # xml窗口
        self.xml_box.setStyleSheet(
            "QTextEdit { background-color: gray; font-weight: bold; color: white; border-radius: 9px}")
        self.xml_box.verticalScrollBar()  # 这个加纵向的滚动条
        self.xml_box.setWordWrapMode(QTextOption.NoWrap)  # 这个可以加横向的滚动条
        # self.xml_box.setAutoFillBackground(True)

        top_layout.addWidget(self.xml_box)

        # 处理函数表
        self.w = MsgEdit()
        button_set_time.clicked.connect(self.setTime)
        self.net_mode_boxnet_mode_box.activated.connect(self.actNetode)
        button_get_version.clicked.connect(self.getVersion)
        button_start.clicked.connect(self.startCell)
        button_stop.clicked.connect(self.stopCell)
        button_sniffer.clicked.connect(self.startSniffer)
        button_reboot0.clicked.connect(self.reboot0)
        button_reboot1.clicked.connect(self.reboot1)
        button_reboot2.clicked.connect(self.reboot2)
        button_send.clicked.connect(self.sendCmd)
        cell_para_box.activated.connect(self.actCellPara)
        weilan_cfg_box.activated.connect(self.actWeilanCfg)
        self.timer.start(1000)

    def onTimer(self):
        global LOST_CONNECTION_THRESH_SEC, str_connect

        self.current_sys_sec += 1

        if (self.current_sys_sec - self.last_hb_time) > LOST_CONNECTION_THRESH_SEC:  # Lose Connectiong
            if True == self.peer_connect:
                self.peer_connect = False
                self.updateStatus()

            pass
        pass

    def hdlHeatBeat(self, msg):
        # self.aftHdlMsg(msg)
        # self.last_hb_time =
        # time = getTxtInStrTuple(msg, "TIME")
        # 发送心跳响应
        # enviar resposta de batimentos cardíacos

        # self.sendHostMsg("HeatBeatAck")
        # if self.peer_connect == False: #初次连接操作。 设置事件，获取模式
        #                                #Operação de conexão inicial. definir evento, obter modo
        #        self.peer_connect = True
        #        self.sendCmmHostMsg("GetLteMode")

        local_time = self.current_sys_sec
        self.last_hb_time = local_time
        self.peer_connect = True
        self.mode = getTxtInStrTuple(msg, "MODE")
        self.his = getTxtInStrTuple2(msg, "LTE_")
        self.run = getTxtInStrTuple(msg, "STATE")
        self.temp = getTxtInStrTuple(msg, "TEMP")
        self.pps = getTxtInStrTuple(msg, "GPS")
        self.band = getTxtInStrTuple(msg, "BAND")
        self.fcn = getTxtInStrTuple(msg, "FREQ")
        self.updateStatus()
        pass

    def updateStatus(self):
        global state_str, lte_b, g_ue_info_window, str_connect
        if True == self.peer_connect:
            str_connect = "OK"
        else:
            if str_connect != "Rebooting":
                str_connect = "FAIL"

        state_str = "[%s]-[%s]-RF[%s]-[%s]C-B[%s]-F[%s]" % \
            (str_connect, self.mode, self.run, self.temp, self.band, self.fcn)
        # mode_str = "[%s]"%(self.mode)
        self.staus_bar.showMessage(self.tr(state_str))

        if str_connect == "FAIL" and self.mode == "GSM-WB":

            modulo_gsms.setText('MODULO GSM DESCONECTADO')
            modulo_icon.setStyleSheet(
                "QPushButton{border-image: url(platforms/resources/icon/off2.png)}")

            if str_connect == "FAIL" and self.mode == "GSM-WB" and self.run == "STATE_CELL_RF_OPEN":
                self.reboot1
                str_connect = "Rebooting"

        if str_connect == "OK" and self.mode == "GSM-WB":
            button_open_serial.setText("1 - EDITAR MENSAGEM ")
            button_open_serial.setDisabled(False)
            button_dump.setDisabled(False)
            modulo_gsms.setText(
                'MODULO GSM OPERACIONAL DUAL BB - TEMP %sC' % self.temp)
            modulo_icon.setStyleSheet(
                "QPushButton{border-image: url(platforms/resources/icon/on.png)}")

        if str_connect == "FAIL" and self.mode == "FDD-LTE":
            g_ue_info_window.stop()
            modulo_ltes.setText('MODULO LTE DESCONECTADO')
            modulo_icon2.setStyleSheet(
                "QPushButton{border-image: url(platforms/resources/icon/off2.png)}")
            if str_connect == "FAIL" and self.mode == "FDD-LTE" and self.run == "STATE_CELL_RF_OPEN":
                self.reboot1
                str_connect = "Rebooting"

        if str_connect == "OK" and self.mode == "FDD-LTE":
            modulo_ltes.setText(
                'MODULO 4G OPERACIONAL LTE %s - TEMP %sC' % (self.his, self.temp))
            lte_b = self.fcn
            lteband = "CANAL %s" % (lte_b)
            # g_ue_info_window = UeInfoPanel()
            g_ue_info_window.op_status.setText(self.tr(lteband))
            if self.run == "STATE_CELL_RF_OPEN":
                g_ue_info_window.start()
            if self.run == "CLOSED":
                g_ue_info_window.stop()
            modulo_icon2.setStyleSheet(
                "QPushButton{border-image: url(platforms/resources/icon/on.png)}")

    def aftHdlMsg(self, msg, isShow=True):
        try:
            buf = time.strftime("%Y/%m/%d %H:%M:%S ", time.localtime())
            buf += msg  # .decode()
            if isShow:
                self.history_box.append(buf)
        except:
            pass

    def sendHostMsg(self, msg):
        global g_serial_port
        try:
            send_buf = bytes(msg, encoding="utf-8")
            if g_serial_port is not None:
                g_serial_port.sendData(send_buf)

            else:
                sendUdpData(send_buf, self.peer_addr, self.peer_port)
        except:
            pass

    def sendCmmHostMsg(self, msg, stringin=None):

        self.sendHostMsg(msg)
        if (None is stringin):
            self.aftHdlMsg(msg)
        else:
            self.aftHdlMsg(stringin)

    def currentSyssec(self):
        return time.time()
        # date1 = datetime.datetime(1970,01,1,00,00,00)
        # utcnow()
        # date2 = datetime.datetime(localtime().tm_year,
        #                         localtime().tm_mon,
        #                        localtime().tm_mday,
        # localtime().tm_min,
        #                     localtime().tm_sec)
        # timedelta = date2 - date1
        # return timedelta.days*24*3600 + timedelta.seconds

    def setTime(self):
        send_buf = "SetTime %d" % (self.currentSyssec())
        # 读取第几个围栏
        # Leia as primeiras cercas
        self.sendCmmHostMsg(send_buf)

    def changeNetMode(self, index):
        self.sendCmmHostMsg("SwitchNetMode " + str(g_net_mode_list[index - 1]))

    def actNetode(self, index):
        if(index >= 1):
            self.changeNetMode(index)
        pass

    def getVersion(self):
        send_buf = "GetVersion"
        self.sendCmmHostMsg(send_buf)
        pass

    def send_sms(self):
        global Flash
        print('Processando SMS - enviando 1 ')
        if self.mode == "FDD-LTE":
            print('Ignorando LTE')
            pass
        if self.mode == "GSM-WB":
            print('Processando GSM - 2')
            if Flash == "ATIVADO":
                send_buf3 = (" ".join(campanha.splitlines()))  # (campanha)
                send_buf2 = (remet)
                print('SMS CLASSE 0 ...')
                self.sendCmmHostMsg("SetFlashSms 1")
                time.sleep(0.5)
                self.sendCmmHostMsg(
                    "SetSmsCfg 1 " + (send_buf2) + " " + (send_buf3))
                time.sleep(0.5)

            else:
                send_buf3 = (" ".join(campanha.splitlines()))  # (campanha)
                send_buf2 = (remet)
                print('SMS PADRAO')
                # time.sleep(0.5)
                self.sendCmmHostMsg(
                    "SetSmsCfg 1 " + (send_buf2) + " " + (send_buf3))
                time.sleep(0.5)
                # print(time.time())
                # time.sleep(3)

        pass

    def set_bts(self):
        global Flash
        print(setacel)
        print('Processando SMS SET_BTS')
        if self.mode == "FDD-LTE":
            print('Ignorando LTE')
            pass
        if self.mode == "GSM-WB":
            print('Processando GSM - 1')

            send_buf = "SetCellPara " + setacel
            self.sendHostMsg(send_buf)
            self.aftHdlMsg("SetCellPara")
            pass

    def startCell(self):
        self.sendCmmHostMsg("StartCell")

    def stopCell(self):
        self.sendCmmHostMsg("StopCell")

    def startSniffer(self):
        self.sendCmmHostMsg("StartSniffer")
        pass

    def sendCmd(self):
        # send_buf = str(self.cmd_line.text())
        string_in = self.cmd_line.text()
        # send_buf = string_in.toUtf8()
        # send_buf = string_in.encode(encoding = "UTF-8")
        self.sendCmmHostMsg(string_in, string_in)

    def sendReboot(self, idx):
        send_buf = "Reboot %d" % (idx,)
        print("REBOOT :", idx)
        self.sendCmmHostMsg(send_buf)

    def reboot0(self):
        self.sendReboot(0)
        pass

    def reboot1(self):
        global str_connect
        str_connect = "Rebooting"
        self.sendReboot(1)
        pass

    def reboot2(self):
        self.sendReboot(2)
        pass

    def actCellPara(self, index):
        if index == 1:  # 读取远端参数
            self.sendCmmHostMsg("GetCellPara")

        if index == 2:  # 把文本框里的xml文件发给板卡
            if self.current_xml != "XML_CELL_PARA":
                showErro("Current XML file in Edit no be XML_CELL_PARA")
                return
            xml_str = getXmlFileStr(str(self.xml_box.toPlainText()))
            if None == xml_str:
                print("ERRR _NO XML FILE")
                return
            send_buf = "SetCellPara " + xml_str
            self.sendHostMsg(send_buf)
            self.aftHdlMsg("SetCellPara")

        if index == 3:  # 读取远端参数
            self.sendHostMsg("GetNmmCfg")

        if index == 4:  # 把文本框里的xml文件发给板卡
            if self.current_xml != "XML_NMM_CFG":
                showErro("Current XML file in Edit no be XML_NMM_CFG")
                return
            xml_str = getXmlFileStr(str(self.xml_box.toPlainText()))
            if None == xml_str:
                print("ERRR _NO XML FILE")
                return
            send_buf = "SetNmmCfg " + xml_str
            self.sendCmmHostMsg(send_buf)
            self.aftHdlMsg("SetNmmCfg")
        pass

    def actWeilanCfg(self, index):

        if index == 1:  # 读取远端参数
            self.sendCmmHostMsg("GetBaseWorkCfg")

        if index == 2:  # 把文本框里的xml文件发给板卡
            if self.current_xml != "XML_WORK_CFG":
                showErro("Current XML file in Edit no be XML_WORK_CFG")
                return
            xml_str = getXmlFileStr(str(self.xml_box.toPlainText()))
            if None == xml_str:
                print("ERRR _NO XML FILE")
                return
            send_buf = "SetBaseWorkCfg " + xml_str
            self.sendHostMsg(send_buf)
            self.aftHdlMsg("SetWorkCfg")

        if index == 3:  # 读取远端参数
            self.sendCmmHostMsg("GetWeilanCfg")

        if index == 4:  # 把文本框里的xml文件发给板卡
            if self.current_xml != "XML_WEILAN_CFG":
                showErro("Current XML file in Edit no be XML_WEI_LAN")
                return
            xml_str = getXmlFileStr(str(self.xml_box.toPlainText()))
            if None == xml_str:
                print("ERRR _NO XML FILE")
                return
            send_buf = "SetWeilanCfg " + xml_str
            self.sendHostMsg(send_buf)
            self.aftHdlMsg("SetWeilanCfg")

        if index == 5:  # 读取远端参数
            self.sendCmmHostMsg("GetAppCfgExt")

        if index == 6:  # 把文本框里的xml文件发给板卡
            if self.current_xml != "XML_APP_CFG_EXT":
                showErro("Current XML file in Edit no be XML_APP_CFG_EXT")
                return
            xml_str = getXmlFileStr(str(self.xml_box.toPlainText()))
            if None == xml_str:
                print("ERRR _NO XML FILE")
                return
            send_buf = "SetAppCfgExt " + xml_str
            self.sendHostMsg(send_buf)
            self.aftHdlMsg("SetAppCfgExt")
        pass

        pass

    def actNmmCfg(self, index):

        if index == 2:  # 读取本地的xml文件
            self.xml_box.setText(self.tr(self.nmm_cfg))
            self.current_xml = "XML_NMM_CFG"
        pass

    def hdlInput(self, msg, msgId):
        # 响应消息
        if msgId == "109":
            self.hdlCmdAck(msg)

        elif msgId == "101":
            self.hdlHeatBeat(msg)

        elif msgId == "104":
            self.hdlGetCellParaRsp(msg)

        elif msgId == "105":
            self.hdlGetWlCfgRsp(msg)

        elif msgId == "106":
            self.hdlGetNmmCfgRsp(msg)

        elif msgId == "107":
            self.hdlSnifferRslt(msg)

        elif msgId == "108":  # Erro
            self.showErr(msg)

        elif msgId == "110":
            self.hdlVersionRsp(msg)

        elif msgId == "112":  # Erro
            self.hdlLteModeRsp(msg)

        elif msgId == "116":
            self.hdlHeatBeat(msg)

        elif msgId == "124":
            self.hdlNetModeRsp(msg)

        elif msgId == "126":
            self.hdlGetWorkCfgRsp(msg)

        elif msgId == "125":
            self.hdlGetAppCfgExtRsp(msg)
        else:
            self.aftHdlMsg(msg)

    def hdlCmdAck(self, msg):
        self.aftHdlMsg(msg)
        # print(self.aftHdlMsg(msg))
        pass

    def hdlVersionRsp(self, msg):
        self.aftHdlMsg(msg)
        self.hdlHeatBeat(msg)
        pass

    def hdlGetNmmCfgRsp(self, msg):
        self.aftHdlMsg("Nmm Cfg Read Rsp")
        xml_str = getXmlFileStr(msg)
        if None == xml_str:
            print("ERR Not found xml file in msg")
            return
        self.xml_box.setText(self.tr(xml_str))
        self.nmm_cfg = xml_str
        self.current_xml = "XML_NMM_CFG"
        pass

    def hdlGetCellParaRsp(self, msg):
        xml_str = getXmlFileStr(msg)
        if None == xml_str:
            print("ERR Not found xml file in msg")
            return
        self.xml_box.setText(self.tr(xml_str))
        self.cell_para = xml_str
        self.current_xml = "XML_CELL_PARA"
        self.aftHdlMsg("Cell Para Read Rsp")
        pass

    def hdlGetWlCfgRsp(self, msg):
        self.aftHdlMsg("WeiLan Cfg Read Rsp")
        xml_str = getXmlFileStr(msg)
        if None == xml_str:
            print("ERR Not found xml file in msg")
            return
        self.xml_box.setText(self.tr(xml_str))
        self.weilan_cfg = xml_str
        self.current_xml = "XML_WEILAN_CFG"

    def hdlGetWorkCfgRsp(self, msg):
        self.aftHdlMsg("WorkCfg Rsp")
        xml_str = getXmlFileStr(msg)
        if None == xml_str:
            print("ERR Not found xml file in msg")
            return
        self.xml_box.setText(self.tr(xml_str))
        self.nmm_cfg = xml_str
        self.current_xml = "XML_WORK_CFG"
        pass

    def hdlGetAppCfgExtRsp(self, msg):
        self.aftHdlMsg("App Cfg Exit Rsp")
        xml_str = getXmlFileStr(msg)
        if None == xml_str:
            print("ERR Not found xml file in msg")
            return
        self.xml_box.setText(self.tr(xml_str))
        self.nmm_cfg = xml_str
        self.current_xml = "XML_APP_CFG_EXT"
        pass

    def hdlSnifferRslt(self, msg):
        self.aftHdlMsg(msg)
        pass

    def showErr(self, msg):
        self.aftHdlMsg(msg)

    def hdlNetModeRsp(self, msg):
        self.aftHdlMsg(msg)
        pass

    def hdlLteModeRsp(self, msg):
        self.aftHdlMsg(msg)
        self.lte_mode = getTxtInStrTuple(msg, "MODE")
        self.updateStatus()
        if self.lte_mode == "TDD":
            self.net_mode_boxnet_mode_box.setItemText(
                0, self.tr(" Modo LTE atual--TDD"))
            self.net_mode_boxnet_mode_box.setItemText(
                1, self.tr(" Mudar para FDD"))
        elif self.lte_mode == "FDD":
            self.net_mode_boxnet_mode_box.setItemText(
                0, self.tr(" Modo LTE atual--FDD"))
            self.net_mode_boxnet_mode_box.setItemText(
                1, self.tr(" Mudar para TDD"))
        pass


class AddUeDialog(QDialog):
    def __init__(self, imsi=None, parent=None):
        super(AddUeDialog, self).__init__(parent)
        self.setWindowTitle(self.tr("Add-Update Ue"))
        imsi_lable = QLabel(self.tr("imsi:"))
        self.imsi_edit = QLineEdit()
        name_lable = QLabel(self.tr("Name:"))
        if None != imsi:
            self.imsi_edit.setText(self.tr(imsi))
        self.name_edit = QLineEdit()
        button_ok = QPushButton(self.tr("Apply"))
        button_cancel = QPushButton(self.tr("Cancel"))
        main_layout = QGridLayout(self)
        main_layout.addWidget(imsi_lable, 0, 0)
        main_layout.addWidget(self.imsi_edit, 0, 1)
        main_layout.addWidget(name_lable, 1, 0)
        main_layout.addWidget(self.name_edit, 1, 1)
        main_layout.addWidget(button_ok, 2, 0)
        main_layout.addWidget(button_cancel, 2, 1)
        self.connect(button_ok, SIGNAL("clicked()"), self.addUe)
        self.connect(button_cancel, SIGNAL("clicked()"), self.close)

    def addUe(self):
        global g_ue_info_window
        imsi = str(self.imsi_edit.text())
        name = str(self.name_edit.text())
        addSavedUeInfo(imsi, name)
        g_ue_info_window.resetFilter()
        self.close()


# 用于管理手机查找表的插件。
# 手机可以支持几个状态，可以选择是否过滤，也可以删除，添加。
class SavedUeListBox(QWidget):
    def __init__(self, parent=None):
        global g_cfg
        super(SavedUeListBox, self).__init__(parent)
        lab_blk_ue_list = QLabel(self.tr("监控手机列表"))
        # self.setFixedHeight(205)
        self.itemCnt = 20
        self.saved_ue_list_tb = QTableWidget(self.itemCnt, 3)
        self.saved_ue_list_tb.setColumnWidth(0, 60)
        self.saved_ue_list_tb.setColumnWidth(1, 90)
        self.saved_ue_list_tb.setColumnWidth(2, 170)
        self.saved_ue_list_tb.setMinimumWidth(330)
        # self.saved_ue_list_tb.setSelectionMode(QAbstractItemView.NoSelection)
        self._current_idx = 0
        self._current_selected_row = 0
        self.loadFromCfg(g_cfg["saved_ue_list"])
        v_layout = QHBoxLayout()
        main_layout = QVBoxLayout(self)
        button_add = QPushButton(self.tr("Add New Imsi"))
        button_all_select = QPushButton(self.tr("Filter All"))

        v_layout.addWidget(button_add)
        v_layout.addWidget(button_all_select)
        main_layout.addLayout(v_layout)
        main_layout.addWidget(self.saved_ue_list_tb)
        # self.connect(button_add, SIGNAL("clicked()"), self.newUe)
        button_add.clicked.connect(self.newUe)
        # self.connect(button_all_select, SIGNAL("clicked()"), self.allFilter)
        button_all_select.clicked.connect(self.allFilter)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested[QtCore.QPoint].connect(
            self.onRightPopMenu)
        self.loadFromCfg(g_cfg["saved_ue_list"])

    def appendUe(self, imsi, nameAoption):
        if self._current_idx >= self.itemCnt:
            self.itemCnt += 5
            self.saved_ue_list_tb.setRowCount(self.itemCnt)
        self.saved_ue_list_tb.setItem(
            self._current_idx, 0, QTableWidgetItem(self.tr(nameAoption[1])))
        self.saved_ue_list_tb.setItem(
            self._current_idx, 1, QTableWidgetItem(self.tr(nameAoption[0])))
        self.saved_ue_list_tb.setItem(
            self._current_idx, 2, QTableWidgetItem(self.tr(imsi)))
        self._current_idx += 1

    def loadFromCfg(self, saved_ue_dict):
        self.saved_ue_list_tb.clear()
        self.saved_ue_list_tb.setHorizontalHeaderLabels(
            ['OPTION', 'name', 'IMSI'])
        #
        self._current_idx = 0
        for key in saved_ue_dict.keys():
            # print ("Add %s Ue In Table Curret Idx %d", (key,self._current_idx))
            self.appendUe(key, saved_ue_dict[key])

    def newUe(self):
        showAddUeDialog()

    def allFilter(self):
        pass

    def tbCellClicked(self, row, column):
        self._current_selected_row = row
        # print "TABLE CLICK ROW %d"%(row,)

    def itemClicked(self, item):
        self._current_selected_row = 0
        print("TABLE CLICK ROW %d" % (self.currentRow(),))
        pass

    def setInFilter(self):
        # print "Update TABLE CLICK ROW %d"%(self.saved_ue_list_tb.currentRow(),)
        imsi = self.currentImsi()
        if None == imsi:
            return

        ue = getUeInfoInCfg(imsi)
        if None == ue:
            # updateSavedUeListTb()
            return
        if ue[1] == "IN_FILTER":
            return
        else:
            ueTmp = (ue[0], "IN_FILTER")
            updateUeInfoInCfg(imsi, ueTmp)
            updateSavedUeListTb()

    def setOutFilter(self):
        imsi = self.currentImsi()
        if None == imsi:
            return

        ue = getUeInfoInCfg(imsi)
        if None == ue:
            # updateSavedUeListTb()
            return
        if ue[1] == "NOT_IN_FILTER":
            return
        else:
            ueTmp = (ue[0], "NOT_IN_FILTER")
            updateUeInfoInCfg(imsi, ueTmp)
            updateSavedUeListTb()

    def changeUeName(self):
        # print "Update TABLE CLICK ROW %d"%(self.saved_ue_list_tb.currentRow(),)
        imsi = self.currentImsi()
        if None == imsi:
            return
        ue = getUeInfoInCfg(imsi)
        if None == ue:
            # updateSavedUeListTb()
            return
        (name, ok) = QInputDialog.getText(self, self.tr("Name"),
                                          self.tr("Input New Name:"), QLineEdit.Normal, ue[0])

        if ok and (not name.isEmpty()):
            ueTmp = (name, ue[1])
            updateUeInfoInCfg(imsi, ueTmp)
            # ue[0] = str(name)
            updateSavedUeListTb()
        pass

    def delUe(self):
        # print "Update TABLE CLICK ROW %d"%(self.saved_ue_list_tb.currentRow(),)
        imsi = self.currentImsi()
        if None == imsi:
            return

        ue = getUeInfoInCfg(imsi)
        if None == ue:
            # updateSavedUeListTb()
            return

        button = QMessageBox.question(self, "CONFIRME", self.tr("Excluir?"),
                                      QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if button == QMessageBox.Ok:
            delUeInfoInCfg(imsi)
        pass

    def currentImsi(self):
        row = self.saved_ue_list_tb.currentRow()
        item = self.saved_ue_list_tb.item(row, 1)
        if None == item:
            return None
        else:
            return str(item.text())

    def onRightPopMenu(self, point):
        rightPopMenu = QtGui.QMenu(self)
        action = QtGui.QAction(self.tr("IN_FILTER"), self,
                               priority=QtGui.QAction.LowPriority, triggered=self.setInFilter)

        rightPopMenu.addAction(action)
        action = QtGui.QAction(self.tr("NOT_IN_FILTER"), self,
                               priority=QtGui.QAction.LowPriority, triggered=self.setOutFilter)

        rightPopMenu.addAction(action)
        action = QtGui.QAction(self.tr("Change"), self,
                               priority=QtGui.QAction.LowPriority, triggered=self.changeUeName)
        rightPopMenu.addAction(action)
        action = QtGui.QAction(self.tr("Delete"), self,
                               priority=QtGui.QAction.LowPriority, triggered=self.delUe)
        rightPopMenu.addAction(action)
        rightPopMenu.exec_(self.mapToGlobal(point))


# 获取本地配置的界面。包括，本地ip，本地端口，高亮名单等配置。这些配置可以放在Init文件里。并且提供一个
# Obtém a interface para a configuração local. Incluindo, IP local, porta local, lista de
# destaque e outras configurações. Essas configurações podem ser colocadas em um arquivo Init.
# E fornecer um   TELA PRINCIPAL
class LocalSetBox(QWidget):
    def __init__(self, parent=None):
        global g_cfg, g_saved_ue_list_edit_table, modulo_icon, modulo_icon2, msg_list_tb, modulo_ltes, modulo_gsms, g_ue_info_window, button_open_serial, button_dump, operando
        self.cellCfg = ""
        self.appCfg = ""
        self.w = MsgEdit()
        QWidget.__init__(self)

        # Painel de conf original
        lab_Local_addr = QLabel(self.tr("Bs Start Ip"))
        self.edit_bs_ip_start = QLineEdit()
        lab_Local_port = QLabel(self.tr("Search Bs Cnt"))
        self.edit_bs_ip_cnt = QLineEdit()
        v_layout = QGridLayout()  # QHBoxLayout()
        # v_layout.addWidget(lab_Local_addr)
        # v_layout.addWidget(self.edit_bs_ip_start)
        # v_layout.addWidget(lab_Local_port)
        # v_layout.addWidget(self.edit_bs_ip_cnt)

        g_saved_ue_list_edit_table = MsgListBox()  # SavedUeListBox()
        modulo_icon = QPushButton()
        modulo_icon.setStyleSheet(
            "QPushButton{border-image: url(platforms/resources/icon/off.png)}")
        #           "QPushButton:hover{border-image: url(icon/on.png)}"
        #           "QPushButton:pressed{border-image: url(img/off2.png)}")
        #           "QPushButton:pressed{border-image: url(img/off2.png)}")

        modulo_gsms = QLabel("STATUS DO MODULO GSM")
        modulo_gsms.setToolTip('Verde=Operando, Vermelho=Falha')
        modulo_gsms.setFont(QFont('Arial', 12))
        modulo_gsms.setAutoFillBackground(True)

        # modulo_gsms.setStyleSheet("QLabel { background-color: Gray; font-weight: bold; color: yellow; border-radius: 19px; qproperty-alignment: AlignCenter; }")
        modulo_ltes = QLabel("STATUS DO MODULO 4G LTE")
        modulo_icon.setMaximumWidth(40)
        modulo_icon.setMinimumHeight(40)
        modulo_icon.setToolTip('Verde=Operando, Vermelho=Falha')
        modulo_ltes.setFont(QFont('Arial', 12))
        modulo_ltes.setAutoFillBackground(True)

        # modulo_ltes.setStyleSheet("' { background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #505354, stop: 1 #88898a); font-weight: bold; color: yellow; border-radius: 19px; qproperty-alignment: AlignCenter; }")

        modulo_icon2 = QPushButton()
        modulo_icon2.setStyleSheet(
            "QPushButton{border-image: url(platforms/resources/icon/off.png)}")
        #           "QPushButton:hover{border-image: url(icon/on.png)}"
        #           "QPushButton:pressed{border-image: url(img/off2.png)}")
        modulo_icon2.setToolTip('Verde=Operando, Vermelho=Falha')
        modulo_icon2.setMaximumWidth(40)
        modulo_icon2.setMinimumHeight(40)

        v_layout.addWidget(modulo_icon, 0, 2)
        v_layout.addWidget(modulo_gsms, 0, 1)

        v_layout.addWidget(modulo_icon2, 2, 2)
        v_layout.addWidget(modulo_ltes, 2, 1)

        button_rload = QPushButton(self.tr("Reload Cfg"))
        button_dump = QPushButton("3 - INICIAR OPERAÇÃO")
        button_dump.setStyleSheet("QPushButton:hover{background-color: green}"
                                  "QPushButton:pressed{background-color: lightgreen; color: green}")
        self.button_state_chg = QPushButton(self.tr("2 - CONECTAR PUSH   "))
        self.button_state_chg.setStyleSheet("QPushButton:hover{background-color: green}"
                                            "QPushButton:pressed{background-color: lightgreen; color: green}")
        button_open_serial = QPushButton("1 - EDITAR MENSAGEM ")
        button_open_serial.setStyleSheet("QPushButton:hover{background-color: green}"
                                         "QPushButton:pressed{background-color: lightgreen; color: green}")
        button_open_serial.setMinimumWidth(150)
        # op_label = button_dump
        self.active_state = False
        # self.operando = False
        layout = QGridLayout(self)  # QVBoxLayout(self)
        layout.addLayout(v_layout, 0, 1)
        # layout.addWidget(g_saved_ue_list_edit_table, 4, 1)
        # layout.addWidget(button_set_msg, 1, 1)
        # layout.addWidget(button_add_fake, 3, 1)
        # layout.addWidget(button_add_fake2, 4, 1)
        layout.addWidget(button_dump, 3, 1)
        layout.addWidget(self.button_state_chg, 2, 1)
        layout.addWidget(button_open_serial, 1, 1)
        # fakebox = g_set_box
        # 添加黑名单，从blklist
        # Adicione uma lista negra da lista blklist
        self.setLayout(layout)
        self.reload()
        button_rload.clicked.connect(self.reload)
        button_dump.clicked.connect(self.dump)
        self.button_state_chg.clicked.connect(self.chgState)

        button_open_serial.clicked.connect(self.change_the_tab_to_btn_new)

    def change_the_tab_to_btn_new(self):
        global widgets, window_obj
        btn = widgets.btn_new
        btnName = btn.objectName()
        if operando == True:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('ATENÇÃO')
            msgBox.setWindowIcon(QtGui.QIcon(
                'platforms/resources/icon/stat.png'))
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setStyleSheet(
                "Background-color: rgb(44, 49, 60); font-weight: bold; color: lightgray")
            msgBox.setText('Dispositivo em operação')
            msgBox.setInformativeText(
                'Para trocar a mensagem é preciso reiniciar, confirma?')
            msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            msgBox.setEscapeButton(QMessageBox.Cancel)
            # msgBox.setDefaultButton(QMessageBox.Ok)
            retval = msgBox.exec_()
            if retval == QMessageBox.Ok:
                self.dump()
                sendStopToAllBoard()
                # self.chgState()
                closeUdpSocket()
                button_open_serial.setText('AGUARDANDO DISPOSITIVO')
                time.sleep(3)
                initUdpSocket(self)
                # button_open_serial.setReadOnly(True)
                button_open_serial.setEnabled(False)
                button_dump.setEnabled(False)
                print('foi')
            # else:
            #    widgets.stackedWidget.setCurrentWidget(widgets.smspy_editar_page)  # SET PAGE
            #    modules.ui_functions.UIFunctions.resetStyle(window_obj, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            #    btn.setStyleSheet(modules.ui_functions.UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        else:
            widgets.stackedWidget.setCurrentWidget(
                widgets.smspy_editar_page)  # SET PAGE
            modules.ui_functions.UIFunctions.resetStyle(
                window_obj, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(modules.ui_functions.UIFunctions.selectMenu(
                btn.styleSheet()))  # SELECT MENU

        # print(f'Button "button_open_serial" pressed!')

    def change_the_tab_to_btn_home(self):
        global widgets, window_obj
        btn = widgets.btn_widgets
        btnName = btn.objectName()

        widgets.stackedWidget.setCurrentWidget(widgets.smspy_page)  # SET PAGE
        modules.ui_functions.UIFunctions.resetStyle(
            window_obj, btnName)  # RESET ANOTHERS BUTTONS SELECTED
        btn.setStyleSheet(modules.ui_functions.UIFunctions.selectMenu(
            btn.styleSheet()))  # SELECT MENU

        # print(f'Button "button_open_serial" pressed!')

    def chgState(self):
        if self.active_state == False:
            initUdpSocket(self)
            self.button_state_chg.setText(self.tr("2 - DESCONEC.  PUSH  "))
            self.active_state = True

        elif self.active_state == True:
            # sendStopToAllBoard()
            closeUdpSocket()
            self.button_state_chg.setText(self.tr("2 - CONECTAR PUSH   "))
            self.active_state = False

    def chgSerial(self):
        global g_serial_port
        if self.active_state == False:
            g_serial_port = SerialPort(g_cfg["bs_ip_start"])
            button_open_serial.setText(self.tr("CloseSerial"))
            self.active_state = True

    def reload(self):
        global g_cfg, g_saved_ue_list_edit_table
        loadCfg()
        # self.edit_bs_ip_cnt.setText(str(g_cfg["bs_cnt"]))
        # self.edit_bs_ip_start.setText(str(g_cfg["bs_ip_start"]))

        # g_saved_ue_list_edit_table.loadFromCfg()#g_cfg["saved_ue_list"])

    def hdlBlkUeTuple(self, rowNb):
        if None != self.saved_ue_list_tb.item(rowNb, 1):
            textImsi = self.saved_ue_list_tb.item(rowNb, 1).text()
        else:
            textImsi = None

        if None != textImsi:
            textName = self.saved_ue_list_tb.item(rowNb, 0).text()
            if None == textName:
                texName = "NO_NAME"
            g_cfg["saved_ue_list"].append((str(textImsi), (textName)))

    def stopallCell(self):
        global g_cfg
        sendStopToAllCell()
        # self.reload()

    def dump(self):
        global g_cfg, operando

        if self.active_state == False:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('ATENÇÃO')
            msgBox.setWindowIcon(QtGui.QIcon(
                'platforms/resources/icon/stat.png'))
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setStyleSheet(
                "Background-color: rgb(44, 49, 60); font-weight: bold; color: lightgray")
            msgBox.setText('Dispositivo não conectado')
            msgBox.setInformativeText(
                'Ligue o equipamento e após alguns instantes clique em conectar!')
            msgBox.setStandardButtons(QMessageBox.Ok)  # | QMessageBox.Ok)
            msgBox.setEscapeButton(QMessageBox.Ok)
            # msgBox.setDefaultButton(QMessageBox.Ok)
            retval = msgBox.exec_()
        else:
            # continue

            if operando == False:
                button_dump.setText("3 - PARAR OPERAÇÃO")
                start_op()
                g_ue_info_window.start()
                operando = True
                # text_port = str(self.edit_bs_ip_cnt.text())
                # g_cfg["bs_cnt"] = int(text_port)
                # text_port = str(self.edit_bs_ip_start.text())
                # g_cfg["bs_ip_start"] = str(text_port)

            elif operando == True:
                sendStopToAllCell()
                # g_ue_info_window.stop()

                button_dump.setText("3 - INICIAR OPERAÇÃO")
                operando = False

      # def fade(self):


class StatusBox(QToolBox):
    def __init__(self, parent=None):
        # global teste
        super(StatusBox, self).__init__(parent)
        self.setMinimumWidth(360)
        # self.setMaximumWidth(500)
        self.localStatusBox = localStatusBox()
        self.addItem(self.StatusBox, self.tr("Status"))

    def addHost(self, host_box):
        # host_box.peer_addr.toString())
        self.addItem(host_box, self.tr("Remote Board:")+g_buf.split().pop(4))
        # if g_buf.split().pop(4) == "MODE[GSM-WB]":
        #    load_push_button.setStyleSheet("background-color: red")#('QPushButton {background-color: #A3C1DA; border:  none}')
        #    #print (testa.self.imsi_cnt)
        # else:
        #    print (g_buf.split().pop(4))


class SetBox(QToolBox):
    def __init__(self, parent=None):
        # global teste
        super(SetBox, self).__init__(parent)
        self.setMinimumWidth(400)

        self.localBox = LocalSetBox()

        self.addItem(self.localBox, self.tr("DASHBOARD"))

    def addHost(self, host_box):

        nome_modulo = ''
        codigo_indice = g_buf.split().pop(2)
        if codigo_indice.isnumeric():
            nome_modulo = g_buf.split().pop(3)
            frequencia = g_buf.split().pop(5)
        else:
            nome_modulo = g_buf.split().pop(2)
            frequencia = g_buf.split().pop(4)

        print("NOME :" + nome_modulo)

        self.addItem(host_box, self.tr("Remote Board :") +
                     host_box.peer_addr.toString() + " - " + nome_modulo + " " + frequencia)   # g_buf.split().pop(4))#
        # if g_buf.split().pop(4) == "MODE[GSM-WB]":
        #    # ('QPushButton {background-color: #A3C1DA; border:  none}')
        #    load_push_button.setStyleSheet("background-color: red")
        #    #print (testa.self.imsi_cnt)
        # else:

       # print("[" + g_buf.split().pop(0) + "] " + g_buf.split().pop(1) + " " +
       #       g_buf.split().pop(2) + " " + g_buf.split().pop(3) + " " +
       #       g_buf.split().pop(4) + " " + g_buf.split().pop(5) + " " +
       #       g_buf.split().pop(6) + " " + g_buf.split().pop(7))


class UeIndi(object):

    def __init__(self, ueInfo, fromeFile=False, fromUe=False, imsi=None):
        global again4
        if True == fromUe:
            ueindi = ueInfo
            # entregue = 0
            soma = 1
            self.board_name = ueindi.board_name
            self.time = ueindi.time
            self.reg_type = ueindi.reg_type
            self.imsi = imsi
            self.imei = tmsi
            self.cqi = str(int(ueindi.cqi)/2 + 7)
            self.rssi = str(int(ueindi.rssi)/2 + 5)
            self.ul_ta = str(1)
            self.rscp = ueindi.rscp
            return

        if False == fromeFile:
            global pqp, ult_op, claro_sms, vivo_sms, tim_sms, oi_sms
            _time = getTxtInStrTuple(ueInfo, "time")
            self.time = time.strftime(
                "%Y%m%d-%H:%M:%S", time.localtime(int(_time)))
            self.imsi = getTxtInStrTuple(ueInfo, "imsi")
            self.imei = getTxtInStrTuple(ueInfo, "imei")
            if re.match('^000000000000000', self.imei):
                self.imei = "NÃO DISP"
            self.rscp = getTxtInStrTuple(ueInfo, "rsrp")
            # print("RSCP :" + self.rscp)
            self.cqi = getTxtInStrTuple(ueInfo, "ulCqi")
            # print("RSCP :" + self.cqi)
            if re.match('^72410', self.imsi):
                self.cqi = "VIVO"
            if re.match('^72406', self.imsi):
                self.cqi = "VIVO"
            if re.match('^72411', self.imsi):
                self.cqi = "VIVO"
            if re.match('^72423', self.imsi):
                self.cqi = "VIVO"
            if re.match('^72405', self.imsi):
                self.cqi = "CLARO"
            if re.match('^72403', self.imsi):
                self.cqi = "TIM"
            if re.match('^72402', self.imsi):
                self.cqi = "TIM"
            if re.match('^72404', self.imsi):
                self.cqi = "TIM"
            if re.match('^72441', self.imsi):
                self.cqi = "S-MVNO"
            if re.match('^72431', self.imsi):
                self.cqi = "OI"
            if re.match('^72416', self.imsi):
                self.cqi = "OI"
            if re.match('^72439', self.imsi):
                self.cqi = "NEXTEL"
            if re.match('^72400', self.imsi):
                self.cqi = "NEXTEL"
            if re.match('^72454', self.imsi):
                self.cqi = "TIM"
            if re.match('^72417', self.imsi):
                self.cqi = "CORREIOS"

            if re.match('^722310', self.imsi):
                self.cqi = "CLARO"
            if re.match('^7227', self.imsi):
                self.cqi = "MOVISTAR"
            if re.match('^7220', self.imsi):
                self.cqi = "MOVISTAR"
            if re.match('^72234', self.imsi):
                self.cqi = "PERSONAL"

            if re.match(' ', self.cqi):
                self.cqi = "NAO CAD"
            self.rssi = getTxtInStrTuple(ueInfo, "ulSig")
            # log JRP
            # print(self.rssi)
            self.ul_ta = getTxtInStrTuple(ueInfo, "ulTa")
            if self.ul_ta == "":
                self.ul_ta = "1"
            self.reg_type = getTxtInStrTuple(ueInfo, "taType")
            if self.reg_type == "ATTACH":
                self.reg_type = "CONECT"
            if self.reg_type == "REDIRECTION":
                self.reg_type = "RD GSM"
            if self.reg_type == "MEAS_RPT":
                self.reg_type = "CONT"
            if self.reg_type == "LAURAU":
                self.reg_type = "COM"
            if self.reg_type == "LAUSMS":
                self.reg_type = "OK"
                pqp += 1
                ult_op = self.cqi
                if self.cqi == "VIVO":
                    vivo_sms += 1
                if self.cqi == "CLARO":
                    claro_sms += 1
                if self.cqi == "TIM":
                    tim_sms += 1
                if self.cqi == "OI":
                    oi_sms += 1
                print(pqp, self.cqi)
            if self.reg_type == "TA_REQ":
                self.reg_type = "INIC"

            list_ue_info = ueInfo.split()
            if True is list_ue_info[2].isdigit():
                self.board_name = list_ue_info[3]
            else:
                self.board_name = list_ue_info[2]

        else:
            list_ue_info = ueInfo.split()
            self.board_name = list_ue_info[0]
            self.time = list_ue_info[1]
            self.reg_type = list_ue_info[2]
            self.imsi = list_ue_info[3]
            self.imei = list_ue_info[4]
            self.cqi = list_ue_info[5]
            self.rssi = list_ue_info[6]
            self.ul_ta = list_ue_info[7]


class UeIndiTable(QTableWidget):

    def __init__(self, parent=None):
        super(UeIndiTable, self).__init__(parent)
        delegate = AlignDelegate(self)
        self.setItemDelegate(delegate)
        self.row_cnt = 2
        self.current_row = 0
        self.setColumnCount(6)
        self.setRowCount(self.row_cnt)
        self.setMinimumWidth(250)
        self.setColumnWidth(0, 130)
        self.setColumnWidth(1, 125)
        self.setColumnWidth(2, 105)
        self.setColumnWidth(3, 85)
        self.setColumnWidth(4, 90)
        self.setColumnWidth(5, 150)
        # self.setColumnWidth(6, 80)
        # self.setColumnWidth(7, 40)
        # self.setColumnWidth(8, 40)
        self.setMaximumHeight(350)  # RowHeight(0, 12)
        self.verticalHeader().setDefaultSectionSize(9)
        self.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
        # "QTableWidget QTableCornerButton::section {background-color: black}")
        self.verticalHeader().setStyleSheet(
            "QHeaderView::section {border:none; border-radius: 1px; border-right:1px solid gray;}")
        self.setStyleSheet(
            "QTableWidget { background-color: gray; font-weight: bold; color: black; border-radius: 8px}" "QTableWidget QTableCornerButton::section {background-color: transparent}")
        # self.setStyleSheet("background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #88898a, stop: 1 #033d99);color: black; font-weight: bold")
        # self.setForeground(QBrush(QColor(70, 255, 50)))
        # self.verticalHeader().setTextAlignment(Qt::AlignCenter)
        self.ue_list = []
        self.initPage()
        self.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested[QtCore.QPoint].connect(
            self.onRightPopMenu)

    def setRowCnt(self, row_cnt):
        self.row_cnt = row_cnt
        self.setRowCount(row_cnt)

    def initPage(self):
        self.clear()
        del (self.ue_list[0:])
        self.current_row = 0

        self.setHorizontalHeaderLabels(
            ['HORA', 'IMSI', "OPER.", 'ORIGEM', 'EVENTO', 'IMEI'])

    def setRow(self, ue_indi, rowIdx):
        # timeStr=time.strftime("%Y%m%d-%H:%M:%S", time.localtime(int(ue_indi.time)))
        # print ("setRow")
        global pqp
        local_database = "platforms/resources/database/optinsms.db"
        dados_consultar = {"operadora": ue_indi.cqi,
                           "evento": ue_indi.reg_type,
                           "imsi": ue_indi.imsi}
        # qtd_achou = db.procura_celular_cadastrado(local_database, dados_consultar)
        # if qtd_achou:
        # print("Achou " + ue_indi.imsi)

        if None != ue_indi.name:
            self.setItem(rowIdx, 2, QTableWidgetItem(
                self.tr(ue_indi.name)))  # OPERADORA
        self.setItem(rowIdx, 3, QTableWidgetItem(
            self.tr(ue_indi.board_name)))   # ORIGEM
        self.setItem(rowIdx, 0, QTableWidgetItem(
            self.tr(ue_indi.time)))         # HORA DE RECEBIMENTO
        self.setItem(rowIdx, 1, QTableWidgetItem(
            self.tr(ue_indi.imsi)))         # IMSI DO CELULAR
        self.setItem(rowIdx, 4, QTableWidgetItem(
            self.tr(ue_indi.reg_type)))     # EVENTO
        self.setItem(rowIdx, 5, QTableWidgetItem(
            self.tr(ue_indi.imei)))         # IMEI
        self.setItem(rowIdx, 2, QTableWidgetItem(
            self.tr(ue_indi.cqi)))          # NOME DA OPERADORA

        # print(f"Novo Registro: ")
        # print(f"==============")
        # print(f"Registro N: {rowIdx}")

        horaCompleta = str(ue_indi.time)
        hora = horaCompleta[(len(horaCompleta) - 8):len(horaCompleta)]

        data_hoje = date.today()
        data_hoje.strftime("%dd/%mm/%YYYY")

        # Colocar a Função de Gravar na Base de Dados logo abaixo:
        # Chamar a Função: insert_dados_celulares_encontrados
        # hora = ue_indi.time[(len(ue_indi.time) - 8):len(ue_indi.time)]
        dados_salvar = {"data_received": data_hoje,
                        "hora_received": hora,
                        "operadora": ue_indi.cqi,
                        "evento": ue_indi.reg_type,
                        "emei": ue_indi.imei,
                        "imsi": ue_indi.imsi,
                        "modulo": ue_indi.board_name,
                        "msg_enviada": pqp,
                        "id_campanha": 1}  # Indicar se a mensagem foi enviada ou não

        db.insert_dados_celulares_encontrados(local_database, dados_salvar)

    def appendRow(self, ue_indi):
        if self.row_cnt == self.current_row:
            self.row_cnt += 5
            self.setRowCount(self.row_cnt)
            self.scrollToBottom()
        self.setRow(ue_indi, self.current_row)
        self.current_row += 1

    def showUeList(self, ueList):
        show_cnt = 0
        self.initPage()
        for item in ueList:
            self.appendRow(item)

    def currentImsi(self):
        row = self.currentRow()
        item = self.item(row, 2)
        if None == item:
            return None
        else:
            return str(item.text())

    def addUe(self):
        # imsi = self.currentImsi()
        # showAddUeDialog(imsi)
        print(self.currentRow())
        pass

    def onRightPopMenu(self, point):
        pass
        rightPopMenu = QMenu(self)
        action = QAction(self.tr("Add To Black List"), self,
                         priority=QAction.LowPriority, triggered=self.addUe)
        rightPopMenu.addAction(action)
        rightPopMenu.exec_(self.mapToGlobal(point))


class UeInfoPanel(QWidget):
    def __init__(self, parent=None):
        global g_ue_info_list, g_all_ue_list_table, g_filter_list_table, load_push_button, remet, campanha, rembut, op_status, fb_painel
        QWidget.__init__(self)
        # 上栏显示属性
        # Exibir propriedades na coluna superior
        testa = 3
        self.imsi_per_page = 0  # 0: show all UE
        self.current_page = 0
        self.imsi_cnt = 0
        self.page_cnt = 0
        self.show_last_page = True

        # 下栏显示属性
        # A coluna inferior mostra as propriedades

        self.filter_option = "IN_FILTER"  # "ALL_SAVED_UE" "IMSI_SEARCH"
        # self.imsi_match_str = None
        g_all_ue_list_table = UeIndiTable()
        g_filter_list_table = UeIndiTable()
        # g_all_ue_list_table.size(200) # Geometry(10, 10, 10_1, 10_2)
        g_all_ue_list_table.setMinimumWidth(300)
        g_all_ue_list_table.setRowCnt(self.imsi_per_page)
        g_filter_list_table.setRowCnt(30)

        # load_push_button = QPushButton(self.tr("GSM"))
        self.save_push_button = QPushButton(self.tr("Exportar"))
        # reset_push_button = QPushButton(self.tr("Reset Recoder"))
        self.page_cfg_box = QComboBox()
        self.page_cfg_box.insertItem(0, self.tr("20/Page"))
        self.page_cfg_box.insertItem(1, self.tr("40/page"))
        self.page_cfg_box.insertItem(2, self.tr("80/Page"))
        self.page_cfg_box.insertItem(3, self.tr("160/Page"))
        self.page_cfg_box.insertItem(4, self.tr("320/Page"))
        self.page_cfg_box.insertItem(5, self.tr("Show All"))
        next_push_button = QPushButton(self.tr("Prev"))
        prev_push_button = QPushButton(self.tr("Next"))
        switch_to_push_button = QPushButton(self.tr("Go To"))
        self.switch_page_line = QLineEdit()
        self.switch_page_line.setFixedWidth(100)
        lab_page_name = QLabel(self.tr("页    "))
        first_push_button = QPushButton(self.tr("Fist Page"))
        last_push_button = QPushButton(self.tr("Last Page"))
        button_layout = QHBoxLayout()
        # button_layout.addWidget(load_push_button)
        # main_layout.addWidget(save_push_button)
        # button_layout.addWidget(reset_push_button)
        # button_layout.addWidget(self.page_cfg_box)
        # button_layout.addWidget(next_push_button)
        # button_layout.addWidget(prev_push_button)
        button_layout.addWidget(switch_to_push_button)
        button_layout.addWidget(self.switch_page_line)
        button_layout.addWidget(lab_page_name)
        button_layout.addWidget(first_push_button)
        button_layout.addWidget(last_push_button)

        lab_filter_name = QLabel(self.tr("          Filter Condition"))
        self.filter_option_box = QComboBox()
        self.filter_option_box.insertItem(0, self.tr("Black List Only"))
        self.filter_option_box.insertItem(1, self.tr("All in Filter"))
        self.filter_option_box.insertItem(2, self.tr("Filt by IMSI"))
        self.search_str_line = QLineEdit()
        self.search_str_line.setFixedWidth(250)

        search_layout = QHBoxLayout()
        # search_layout.setMargin(15)
        # search_layout.setSpacing(10)
        search_layout.addWidget(lab_filter_name)
        search_layout.addWidget(self.filter_option_box)
        search_layout.addWidget(self.search_str_line)
        # search_layout.setSizeConstraint(QLayout.SetFixedSize)
        # 设置字体显示色彩相关函数
        # Definir a função de correlação de cores de exibição de fonte
        pe = QPalette()
        # 字体变红 fonte fica vermelha
        pe.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.red)
        # self.lab_ue_cnt_info = QLabel(self.tr("  Aguardando dados..."))

        # MOSTRAR OPERADORAS
        self.op1_name = QLabel(self.tr("SMS - 0"))
        self.op2_name = QLabel(self.tr("SMS - 0"))
        self.op3_name = QLabel(self.tr("SMS - 0"))
        self.op4_name = QLabel(self.tr("SMS - 0"))

        self.op_status = QLabel(self.tr("PARADO"))
        # self.op_status2 = QLabel(self.tr("PARADO"))
        self.op_status3 = QLabel(self.tr("PARADO"))
        self.op_status4 = QLabel(self.tr("PARADO"))

        self.imsi_con = QLabel(self.tr("PARADO"))
        self.sms_t = QLabel(self.tr("NENHUM"))
        self.movie_screen = QLabel()
        # expand and center the label
        # self.movie_screen.setSizePolicy(QSizePolicy.Expanding,
        #    QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        # self.movie_screen.setMaximunHeight(100)
        self.movie_screen.setFixedSize(75, 75)

        # self.btn_start = QPushButton("Start Animation")
        # self.btn_start.clicked.connect(self.start)

        # self.btn_stop = QPushButton("Stop Animation")
        # self.btn_stop.clicked.connect(self.stop)

        # positin the widgets
        # main_layout = QVBoxLayout()
        # main_layout.addWidget(self.movie_screen)
        # main_layout.addWidget(self.btn_start)
        # main_layout.addWidget(self.btn_stop)
        # self.setLayout(main_layout)

        # use an animated gif file you have in the working folder
        # or give the full file path
        ag_file = "platforms/resources/icon/scanner.gif"
        self.movie = QMovie(ag_file, QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        # optionally display first frame
        self.movie.start()
        self.movie.stop()

        # MOSTRAR OPERADORAS
        self.ico_op1 = QPushButton()
        self.ico_op1.setFixedSize(90, 26)
        self.ico_op1.setStyleSheet(
            "QPushButton{border-image: url(platforms/resources/icon/vivo.png)}")

        self.ico_op2 = QPushButton()
        self.ico_op2.setFixedSize(72, 26)
        self.ico_op2.setStyleSheet(
            "QPushButton{border-image: url(platforms/resources/icon/claro.png)}")

        self.ico_op3 = QPushButton()
        self.ico_op3.setFixedSize(57, 20)
        self.ico_op3.setStyleSheet(
            "QPushButton{border-image: url(platforms/resources/icon/tim.png)}")

        self.ico_op4 = QPushButton()
        self.ico_op4.setFixedSize(32, 32)
        self.ico_op4.setStyleSheet(
            "QPushButton{border-image: url(platforms/resources/icon/oi.png)}")

        self.sms_icon = QPushButton()
        self.sms_icon.setFixedSize(27, 18)
        self.sms_icon.setStyleSheet(
            "QPushButton{border-image: url(platforms/resources/icon/env.png)}")

        self.imsi_icon = QPushButton()
        self.imsi_icon.setFixedSize(80, 59)
        self.imsi_icon.setStyleSheet(
            "QPushButton{border-image: url(platforms/resources/icon/imsi.png)}")

        # self.lab_ue_cnt_info.setFont(QFont('Arial', 12))
        # self.lab_ue_cnt_info.setMaximumHeight(30)
        # self.lab_ue_cnt_info.setAutoFillBackground(True)
        # self.lab_ue_cnt_info.setStyleSheet(
        #    "QLabel { background-color: black; font-weight: bold; color: gray; border-radius: 9px; qproperty-alignment: AlignCenter; }")

        # MOSTRAR OPERADORAS
        self.op1_name.setStyleSheet(
            "QLabel { background-color: transparent; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")
        self.op2_name.setStyleSheet(
            "QLabel { background-color: transparent; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")
        self.op3_name.setStyleSheet(
            "QLabel { background-color: transparent; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")
        self.op4_name.setStyleSheet(
            "QLabel { background-color: transparent; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")

        self.sms_t.setStyleSheet(
            "QLabel { background-color: transparent; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")
        self.op_status.setStyleSheet(
            "QLabel { background-color: transparent; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")
        # self.op_status2.setStyleSheet(
        #    "QLabel { background-color: white; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")

        self.op_status3.setStyleSheet(
            "QLabel { background-color: transparent; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")
        self.op_status4.setStyleSheet(
            "QLabel { background-color: transparent; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")
        self.imsi_con.setStyleSheet(
            "QLabel { background-color: transparent; font-weight: bold; color: gray; qproperty-alignment: AlignCenter; }")

        self.msg_feedback = QLabel(
            self.tr("    REMETENTE: %s \n   MENSAGEM:    \n    %s " % (remet, campanha)))
        fb_painel = self.msg_feedback
        self.msg_feedback.setMinimumHeight(180)
        self.msg_feedback.setMaximumHeight(380)
        # self.msg_feedback.setMaximumWidth(500)
        self.msg_feedback.setAutoFillBackground(True)
        self.msg_feedback.setWordWrap(True)
        self.msg_feedback.setStyleSheet(
            "QLabel { background-color: gray; font-family: Arial; font-weight: bold; font-size: 14px ; color: black; border-radius: 9px; qproperty-alignment: AlignCenter; }")

        info_layout = QGridLayout()
        # info_layout.ro
        info_layout.setColumnStretch(0, 0)
        info_layout.setColumnStretch(1, 0)
        info_layout.setColumnStretch(2, 0)
        info_layout.setColumnStretch(3, 0)
        info_layout.setColumnStretch(4, 0)
        info_layout.setColumnStretch(5, 0)
        info_layout.setColumnStretch(6, 0)
        info_layout.setRowStretch(0, 1)
        info_layout.setRowStretch(1, 1)
        # info_layout.setRowStretch( 2, 0 )

        # info_layout.addWidget(msg_feedback, 0, 1)
        # info_layout.addWidget(lab_ue_cnt_info, 0, 2)

        lab_blk_ue = QLabel(self.tr("Filt UE"))
        main_layout = QVBoxLayout(self)

        # main_layout.addLayout(button_layout, 0)
        main_layout.addWidget(self.msg_feedback)
        # main_layout.addWidget(self.lab_ue_cnt_info)
        main_layout.addLayout(info_layout)
        # MOSTRAR OPERADORAS
        # info_layout.addWidget(self.lab_ue_cnt_info, 2, 0)
        info_layout.addWidget(self.op1_name, 1, 0, Qt.AlignCenter)
        info_layout.addWidget(self.op2_name, 1, 1, Qt.AlignCenter)
        info_layout.addWidget(self.op3_name, 1, 2, Qt.AlignCenter)
        info_layout.addWidget(self.op4_name, 1, 3, Qt.AlignCenter)
        info_layout.addWidget(self.sms_t, 1, 4, Qt.AlignCenter)
        info_layout.addWidget(self.op_status, 1, 5, Qt.AlignCenter)
        # info_layout.addWidget(self.op_status2, 2, 5, Qt.AlignHCenter)
        info_layout.addWidget(self.imsi_con, 1, 6, Qt.AlignCenter)

        # MOSTRAR OPERADORAS
        info_layout.addWidget(self.ico_op1, 0, 0, 2, 1, Qt.AlignHCenter)
        info_layout.addWidget(self.ico_op2, 0, 1, 2, 1, Qt.AlignHCenter)
        info_layout.addWidget(self.ico_op3, 0, 2, 2, 1, Qt.AlignHCenter)
        info_layout.addWidget(self.ico_op4, 0, 3, 2, 1, Qt.AlignHCenter)

        info_layout.addWidget(self.sms_icon, 0, 4, 2, 1, Qt.AlignHCenter)
        info_layout.addWidget(self.movie_screen, 0, 5, 2, 1, Qt.AlignHCenter)
        info_layout.addWidget(self.imsi_icon, 0, 6, 2, 1, Qt.AlignHCenter)

        main_layout.addWidget(g_all_ue_list_table)
        # main_layout.addLayout(search_layout)
        # main_layout.addWidget(g_filter_list_table)
        # self.ico_op1.clicked.connect(self.start)
        # self.ico_op2.clicked.connect(self.stop)
        # main_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.save_push_button.clicked.connect(self.gerarRelatorios)
        # load_push_button.clicked.connect(self.loadUeList)
        # reset_push_button.clicked.connect(self.resetUeList)
        # self.page_cfg_box.activated.connect(self.pageCfg)
        # next_push_button.clicked.connect(self.nextPage)
        # prev_push_button.clicked.connect(self.prevPage)
        # switch_to_push_button.clicked.connect(self.switchToPage)
        # first_push_button.clicked.connect(self.goFirstPage)
        # last_push_button.clicked.connect(self.goLastPage)
        # self.filter_option_box.activated.connect(self.filterCfg)

        self.search_str_line.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.search_str_line.customContextMenuRequested[QtCore.QPoint].connect(
            addUeInFilter)
        self.update_label()

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.update_label)
        # self.timer.start(10000)

    def update_label(self):
        global campanha, remet
        # current_time = str(datetime.datetime.now().time())
        dentro = campanha
        dentro2 = remet
        # print(campanha)
        self.msg_feedback.setText(
            "    REMETENTE: \n    %s \n\n    MENSAGEM: \n    %s " % (dentro2, dentro))

    def start(self):
        """sart animnation"""
        self.movie.start()

    def stop(self):
        # """stop the animation"""
        self.movie.stop()

    # def msg_feedback(self):
    #         global remet
    #         msgbuf = remet
    #         self.msg_feedback.setText(self.tr(msgbuf))

    def consulta_dados_de_telefones_gravados(self):
        # print('rsdados')
        # local_database = str(Path(__file__).parent / "database" / "/platforms/resources/database/optinsms.db")
        local_database = "platforms/resources/database/optinsms.db"
        rsdados = db.listar_all_dados_Celulares_Retornados(local_database)
        # ---------------------------------------------------------------
        # Create List of Dictionary
        # print(rsdados)
        listadados = []
        # listadados.items()
        for row_number, row_data in enumerate(rsdados):
            listadados.append(
                {"id": row_data[0], "data_received": row_data[1],
                 "hora_received": row_data[2], "operadora": row_data[3],
                 "evento": row_data[4], "emei": row_data[5],
                 "imsi": row_data[6], "modulo": row_data[7],
                 "msg_enviada": row_data[8]})
        # return
        # valor = list(listadados.items())
        # for keys,values in str(listadados.items()):
        #    print(keys)
        #    print(values)
        # print(listadados)
        return listadados
        # print(listadados)
        # print(str(listadados))
        # a_dictionary = listadados
        # dictionary_items = listadados[1].items()
        # for item in dictionary_items:

        # listadados = {"titulo": "Relatorio de Telefones Encontrados",
        #              "tituloItem1": "Hora",
        #              "tituloItem2": "imsi",
        #              "tituloItem3": "imei",
        #              "tituloItem4": "Operadora",
        #              "tituloItem5": "Origem",
        #              "tituloItem6": "Evento"}
        # print('listadados')

    def gerarRelatorios(self):
        # print("Gerar Relatorios")
        listaDadosCorpoRel = self.consulta_dados_de_telefones_gravados()

        print("Dados processados:\n", listaDadosCorpoRel)
        dadosParam = {}
        dadosParam = {"titulo": "Relatorio de Telefones Encontrados",
                      "tituloItem1": "Hora",
                      "tituloItem2": "imsi",
                      "tituloItem3": "imei",
                      "tituloItem4": "Operadora",
                      "tituloItem5": "Origem",
                      "tituloItem6": "Evento"}
        nomeArquivo = "listaTelefonesColetados.pdf"
        # print(dadosParam)
        # geraRel.gerarPDF(nomeArquivo, dadosParam, listaDadosCorpoRel)

    def saveUeList(self):
        timeStr = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        s, fileType = QFileDialog.getSaveFileName(
            self, "Save IMSI log", "./"+timeStr, "Log File(*.log)")
        # fd = open(str(s), "w")
        # pickle.dump(ue_info_list, fd)
        # blFile.close()
        dumpUeInfoList(s)

    def loadUeList(self):
        s = QFileDialog.getOpenFileName(
            self, "Open IMSI log", "./", "Log File(*.log)")
        loadUeInfoList(s)
        self.resetFilter()
        self.reloadUpperUeList()

    def resetUeList(self):
        global g_ue_info_list
        button = QMessageBox.question(self, "Confirme", self.tr("Salvar os logs?"),
                                      QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if button == QMessageBox.Ok:
            self.saveUeList()
        del(g_ue_info_list[0:])
        g_all_ue_list_table.initPage()
        g_filter_list_table.initPage()
        self.imsi_cnt = 0
        self.page_cnt = 0
        self.current_page = 0

    def update_ue_cnt_info(self):
        # self.current_page = 0
        # self.imsi_cnt = 0
        # self.page_cnt = 0
        global pqp, ult_op, claro_sms, vivo_sms, tim_sms, oi_sms
        info = "   %d IMSI em contato     |     Mensagens entregues %d     | Vivo %d | Claro %d | Ultima operadora %s" % (
            self.imsi_cnt, pqp, vivo_sms, claro_sms, ult_op)
        info2 = "CONTATO - %d" % (self.imsi_cnt)
        clarosms = "SMS - %d" % (claro_sms)
        vivosms = "SMS - %d" % (vivo_sms)
        oisms = "SMS - %d" % (oi_sms)
        timsms = "SMS - %d" % (tim_sms)
        smstotal = "TOTAL - %d" % (pqp)
        # lteband = "CANAL %s"%(lte_b)
        # self.ui.lcd.display(self.imsi_cnt)
        # info = "%d Conexões recebidas,   %d Páginas,         Página atual --%d "%(self.imsi_cnt, self.page_cnt, self.current_page)
        # self.lab_ue_cnt_info.setText(self.tr(info))

        # MOSTRAR AS OPERADORAS
        self.op1_name.setText(self.tr(vivosms))
        self.op2_name.setText(self.tr(clarosms))
        self.op3_name.setText(self.tr(timsms))
        self.op4_name.setText(self.tr(oisms))

        # self.op_status.setText(self.tr(lteband))
        # self.lcdview.display(self.imsi_cnt)

        self.sms_t.setText(self.tr(smstotal))
        self.imsi_con.setText(self.tr(info2))

    def addUeIndiUpper(self, ueIndi):
        # 上栏信息统计
        # Estatísticas na coluna superior
        self.imsi_cnt += 1
        g_all_ue_list_table.appendRow(ueIndi)
        pass

        if self.imsi_per_page > 0:
            page_cnt = (self.imsi_cnt + self.imsi_per_page - 1) / \
                self.imsi_per_page
        else:
            page_cnt = 1
            self.current_page = 1

        # print "page Cnt %d, self.page_cnt %d"%(page_cnt, self.page_cnt)
        # if self.show_last_page: #显示最后1页的时候
        #        if self.imsi_per_page > 0:
        #                if page_cnt > self.page_cnt:
        #                        g_all_ue_list_table.initPage()
        #                        self.current_page = page_cnt
        #        g_all_ue_list_table.appendRow(ueIndi)
        # else:
        #        if self.current_page == page_cnt:
        #                g_all_ue_list_table.appendRow(ueIndi)
        # self.page_cnt = page_cnt
            self.update_ue_cnt_info()

    def addUeIndiFilter(self, ueIndi, re_compire=True):
        # self.filter_option = "IN_FILTER" #"ALL_SAVED_UE" "IMSI_SEARCH" "NO_ACTIVE"
        # self.imsi_match_str = None
        # 上栏信息统计
        # 根据过滤条件进行
        if re_compire:
            saved_ue_cfg = getUeInfoInCfg(ueIndi.imsi)
            ueIndi.name = ""
            ueIndi.in_filter = False
            if None != saved_ue_cfg:
                ueIndi.name = saved_ue_cfg[0]
                if saved_ue_cfg[1] == "IN_FILTER":
                    ueIndi.in_filter = True

        if self.filter_option == "IMSI_SEARCH":
            imsi_search = str(self.search_str_line.text())
            # print("IMSI SEARCH :math %s, UE IMSI%s"%(imsi_search, ueIndi.imsi))
            if len(imsi_search) > 0:
                if ueIndi.imsi.find(imsi_search) >= 0:
                    # print("-----------founded-------")
                    g_filter_list_table.appendRow(ueIndi)
        elif self.filter_option == "IN_FILTER":
            if ueIndi.in_filter:
                g_filter_list_table.appendRow(ueIndi)
        elif self.filter_option == "ALL_SAVED_UE":
            if ueIndi.name != "":
                g_filter_list_table.appendRow(ueIndi)

    def addUeIndi(self, ueIndi):
        self.addUeIndiFilter(ueIndi)
        self.addUeIndiUpper(ueIndi)

    def goToPage(self, page_number, reload=False):
        global g_ue_info_list
        _reload = reload  # 外部设置或者本地运算确认是否需要重新加载所有的列表

        if self.imsi_per_page <= 0:  # SHOW ALL UE
            self.page_cnt = 1
            self.current_page = 1
            if _reload:
                g_all_ue_list_table.showUeList(g_ue_info_list)
                self.update_ue_cnt_info()
                return

        if self.current_page != page_number:
            _reload = True
        if False == _reload:
            return

        start_ue_idx = (page_number - 1) * self.imsi_per_page
        if(page_number >= self.page_cnt):  # last page
            page_number = self.page_cnt
            self.current_page = self.page_cnt
            start_ue_idx = (page_number - 1) * self.imsi_per_page
            end_ue_idx = len(g_ue_info_list)
            self.show_last_page = True
        else:
            end_ue_idx = page_number * self.imsi_per_page
            self.current_page = page_number
            self.show_last_page = False

        g_all_ue_list_table.showUeList(g_ue_info_list[start_ue_idx:end_ue_idx])
        self.update_ue_cnt_info()
        # g_all_ue_list_table.initPage()
        # for item in g_ue_info_list[start_ue_idx:end_ue_idx]:
        #        self.addUeIndiUpper(item)

    def goLastPage(self):
        self.goToPage(self.page_cnt)

    def goFirstPage(self):
        self.goToPage(1)

    def nextPage(self):
        if self.current_page > 1:
            self.goToPage(self.current_page - 1)

    def prevPage(self):
        self.goToPage(self.current_page + 1)

    def switchToPage(self):
        page_str = str(self.switch_page_line.text())
        page_number = int(page_str)
        if page_number != self.current_page:
            self.goToPage(page_number)

    def reloadUpperUeList(self):
        global g_ue_info_list
        self.imsi_cnt = len(g_ue_info_list)
        self.page_cnt = 1
        if self.imsi_per_page > 0:
            self.page_cnt = (
                self.imsi_cnt + self.imsi_per_page - 1) / self.imsi_per_page

        self.goToPage(self.page_cnt, True)

    def resetFilter(self):
        global g_ue_info_list
        g_filter_list_table.initPage()
        for item in g_ue_info_list:
            self.addUeIndiFilter(item, True)

    # self.filter_option = "IN_FILTER" #"ALL_SAVED_UE" "IMSI_SEARCH" "NO_ACTIVE"
    def filterCfg(self, index):
        _option = "IN_FILTER"
        if index == 0:
            _option = "IN_FILTER"
        elif index == 1:
            _option = "ALL_SAVED_UE"
        elif index == 2:
            _option = "IMSI_SEARCH"
        else:
            _option = "IMSI_SEARCH"

        if _option != self.filter_option:
            self.filter_option = _option
            self.resetFilter()
        elif _option == "IMSI_SEARCH":
            self.resetFilter()

    def pageCfg(self, index):
        _imsi_per_page = -1
        if index < 5:
            _imsi_per_page = 20 * (1 << index)
        if self.imsi_per_page != _imsi_per_page:
            self.imsi_per_page = _imsi_per_page
            if self.imsi_per_page > 0:
                g_all_ue_list_table.setRowCnt(self.imsi_per_page)
        else:
            return

        self.reloadUpperUeList()


class Panel(QWidget):
    def __init__(self, parent=None):
        global g_ue_info_window, g_set_box  # g_status_box
        QWidget.__init__(self)
        g_ue_info_window = UeInfoPanel()
        g_ue_info_window.setMinimumWidth(800)
        g_ue_info_window.setMaximumHeight(700)
        g_set_box = SetBox()
        g_set_box.setMaximumWidth(400)
        # g_status_box = StatusBox()
        main_layout = QHBoxLayout(self)
        # main_layout.addWidget(g_status_box)
        main_layout.addWidget(g_set_box)
        main_layout.addWidget(g_ue_info_window)


class MsgListBox(QTableWidget):
    def __init__(self, parent=None):
        global c_cfg, g_msg_txt, MsgEdit
        super(MsgListBox, self).__init__(parent)
        lab_blk_ue_list = QLabel(self.tr("监控手机列表"))
        # self.setFixedHeight(205)
        self.itemCnt = 10
        # self.msg_list_tb = QTableWidget(self)
        self.setColumnCount(4)
        # tabela = msg_list_tb(self)
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 1000)
        # self.msg_list_tb.setColumnWidth(3,100)
        self.setMinimumWidth(500)
        # self.msg_list_tb.setSelectionMode(QAbstractItemView.NoSelection)
        self._current_idx = 0
        self._current_selected_row = 0
        self.loadFromCfg()  # c_cfg["msg_db_list"])
        # v_layout=QHBoxLayout()
        # main_layout=QVBoxLayout(self)
        # button_add=QPushButton(self.tr("Atualizar"))
        # button_all_select=QPushButton(self.tr("Filter All"))
        # g_msg_txt = MsgEdit()
        # v_layout.addWidget(button_add)
        # v_layout.addWidget(button_all_select)
        # main_layout.addLayout(v_layout)
        # main_layout.addWidget(self)
        # self.connect(button_add, SIGNAL("clicked()"), self.newUe)
        # button_add.clicked.connect(self.loadFromCfg)
        # self.connect(button_all_select, SIGNAL("clicked()"), self.allFilter)
        # button_all_select.clicked.connect(self.allFilter)
        self.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested[QtCore.QPoint].connect(
            self.onRightPopMenu)
        self.loadFromCfg()  # c_cfg["msg_db_list"])

    def appendUe(self, MENSAGEM, nameAoption):  # nameAoption):
        if self._current_idx >= self.itemCnt:
            self.itemCnt += 5
            self.msg_list_tb.setRowCount(self.itemCnt)
        self.msg_list_tb.setItem(self._current_idx, 2,
                                 QTableWidgetItem(self.tr(nameAoption[1])))
        self.msg_list_tb.setItem(self._current_idx, 1,
                                 QTableWidgetItem(self.tr(nameAoption[0])))
        self.msg_list_tb.setItem(self._current_idx, 0,
                                 QTableWidgetItem(self.tr(MENSAGEM)))
        self._current_idx += 1

    def loadFromCfg(self):  # , msg_list_tb_dict):
        self.clear()
        self.setHorizontalHeaderLabels(['QUANDO', 'REMETENTE', 'MENSAGEM'])
        #
        self._current_idx = 0
        local_database = "platforms/resources/database/optinsms.db"
        rows = db.listar_campanhas(local_database)
        for row in rows:
            _current_idx = rows.index(row)
            self.insertRow(_current_idx)
            # add more if there is more columns in the database.
            self.setItem(_current_idx, 0, QTableWidgetItem(row[1]))
            self.setItem(_current_idx, 1, QTableWidgetItem(row[3]))
            self.setItem(_current_idx, 2, QTableWidgetItem(row[2]))
            # self.msg_list_tb.setItem(inx, 3, QTableWidgetItem(row[4]))
        # for row in msg_list_tb_dict.keys():
        #        #print ("Add %s Ue In Table Curret Idx %d", (key,self._current_idx))
        #        self.appendUe(key, msg_list_tb_dict[key])

    def newUe(self):
        showAddUeDialog()

    def allFilter(self):
        showErro("teste")
        pass

    def allFilter1(self):
        global campanha
        pass
        # self.tbCellClicked(self, row, column)
        # g_msg_txt = MsgEdit()
        # t1 = self.currentColumn()
        # t2 = self.currentRow()
        # campanha = (self.item(t2,t1).text())
        # print(campanha)
        # g_msg_txt.msg_txt.setVisible(True)
        # g_msg_txt.msg_txt.setFocus()
        # g_msg_txt.msg_txt.setPlainText('teste')

        # g_msg_txt.msg_txt.update()
        # g_msg_txt.processo()
        # QtWidgets.QPlainTextEdit.update(self)
        # pass

    def tbCellClicked(self, row, column):
        self._current_selected_row = row
        print("TABLE CLICK ROW %d" % (row,))

    def itemClicked(self, item):
        self._current_selected_row = 0
        print("TABLE CLICK ROW %d" % (self.currentRow,))
        # pass

    def onRightPopMenu(self, point):
        rightPopMenu = QMenu(self)
        action = QAction(self.tr("IN_FILTER"), self,
                         priority=QAction.LowPriority, triggered=self.allFilter)

        rightPopMenu.addAction(action)
        action = QAction(self.tr("NOT_IN_FILTER"), self,
                         priority=QAction.LowPriority, triggered=self.allFilter1)

        # rightPopMenu.addAction(action)
        # action = QtGui.QAction(self.tr("Change"), self,
        #                 priority=QtGui.QAction.LowPriority, triggered=self.changeUeName)

        # rightPopMenu.addAction(action)
        # action = QtGui.QAction(self.tr("Delete"), self,
        #                 priority=QtGui.QAction.LowPriority, triggered=self.delUe)
        rightPopMenu.addAction(action)
        # (self.mapToGlobal(point))
        rightPopMenu.exec_(self.mapToGlobal(point))

    # def currentCOD(self):
    #        row = self.msg_list_tb.currentRow()
    #        item = self.msg_list_tb.item(row, 1)
    #        if None == item:
    #                return None
    #        else:
    #                return str(item.text())


class MsgEdit(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        global g_msg_list_tb, remet, campanha
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle(self.tr("Definir campanha"))
        self.setWindowIcon(QtGui.QIcon('platforms/resources/icon/stat.png'))
        # self.setStyleSheet("background-color: lightgray")#("background: light#QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #000);green")
        self.label = QLabel("Digite sua mensagem e selecione o tipo de SMS:")
        layout.addWidget(self.label)
        top_layout = QGridLayout()
        # top_layout.setColumnStretch(0, 10)
        self.sender = QLabel(self.tr("Remetente:"))
        self.sender.setStyleSheet("font-weight: bold")
        self.msglabel = QLabel(self.tr("Mensagem:"))
        self.char_count = QLabel(self.tr(
            "Contadores - Remetente: usados 0 restantes 11 |  Mensagem: usados 0 restantes 1000"))
        self.msglabel.setStyleSheet("font-weight: bold")
        self.sender.setMaximumWidth(80)
        self.sender_line = QLineEdit()
        self.sender_line.setStyleSheet(
            "background-color: gray; color: black; font-weight: bold")
        self.sender_line.setMaxLength(11)
        self.sender_line.setMaximumWidth(110)
        self.sender_line.textChanged.connect(self.conta_sender)
        top_layout.addWidget(self.sender, 0, 0, Qt.AlignLeft)
        top_layout.addWidget(self.char_count, 0, 1, Qt.AlignLeft)
        # top_layout.setColumnStretch(0, 10)
        top_layout.addWidget(self.sender_line, 1, 0, Qt.AlignLeft)
        top_layout.addWidget(self.msglabel, 2, 0, Qt.AlignLeft)
        g_msg_list_tb = MsgListBox()

        msg_list = QHBoxLayout()
        layout.addLayout(top_layout)
        self.msg_txt = QPlainTextEdit(self)
        self.msg_txt.setUpdatesEnabled(True)
        self.msg_txt.setStyleSheet(
            "background-color: gray; color: black; font-weight: bold")
        self.msg_txt.textChanged.connect(self.conta_msg)
        layout.addWidget(self.msg_txt)
        msg_cmd_layout = QGridLayout()
        self.sms_cfg_box = QComboBox()
        self.sms_cfg_box.insertItem(0, self.tr("Tipo de SMS"))
        self.sms_cfg_box.insertItem(1, self.tr("SMS Padrão"))
        self.sms_cfg_box.insertItem(2, self.tr("Flash SMS"))
        self.sms_save_button = QPushButton(self.tr("Salvar e voltar"))
        self.sms_save_button.setStyleSheet("QPushButton:hover{background-color: green}"
                                           "QPushButton:pressed{background-color: lightgreen}")
        back_button = QPushButton(self.tr(""))
        back_button.setStyleSheet("border: none")
        back_button2 = QPushButton(self.tr(""))
        # ("QPushButton{border: none}"
        back_button2.setStyleSheet("border: none")
        # "QPushButton:hover{background-color: green}"
        # "QPushButton:pressed{background-color: lightgreen}")#("background-color: green")("border: none")
        # back_button.setStyleSheet("background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #040);green")
        # back_button.setStyleSheet("hover: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #090);green")
        msg_cmd_layout.addWidget(self.sms_cfg_box, 0, 0)
        msg_cmd_layout.addWidget(self.sms_save_button, 0, 1)
        msg_cmd_layout.addWidget(back_button, 0, 2)
        msg_cmd_layout.addWidget(back_button2, 0, 3)
        layout.addLayout(msg_cmd_layout)
        layout.addLayout(msg_list)
        # msg_list.addWidget(g_msg_list_tb)
        self.setLayout(layout)
        # cara = 0
        self.sms_save_button.clicked.connect(self.rembut)  # (dumpMsg)
        self.sms_cfg_box.activated.connect(self.TipoSms)
        self.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested[QtCore.QPoint].connect(
            self.onRightPopMenu)

    def conta_sender(self):
        global cara, msg_cara
        cara = (len(self.sender_line.text()))
        self.mostra_carac()
        # print(len(self.sender_line.text()))

    def processo(self):
        print(campanha)
        # self.msg_txt.setFocus()
        # QCoreApplication.processEvents()
        # self.msg_txt.set

        # self.msg_txt.setPlainText(campanha)
        # QApplication.QWidgets.processEvents()
        # self.msg_txt.paintEvent()       #self.msg_txt.setStyleSheet("background-color: red; color: blue; font-weight: bold")
        # self.layout.repaint()
        print(self.msg_txt.toPlainText())
        msg_txt.update()
        # QtWidgets.QPlainTextEdit.update(self)
        # QCoreApplication.processEvents()
        # update()
        repaint()
        QtWidgets.QApplication.processEvents()
        QCoreApplication.processEvents()
        # self.processEvents()

    def conta_msg(self):
        global cara, msg_cara
        msg_cara = (len(self.msg_txt.toPlainText()))
        if msg_cara > 1000:
            self.sms_save_button.setEnabled(False)
            msgBox = QMessageBox()
            msgBox.setWindowTitle('ATENÇÃO')
            msgBox.setWindowIcon(QtGui.QIcon(
                'platforms/resources/icon/stat.png'))
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setStyleSheet(
                "Background-color: rgb(44, 49, 60); font-weight: bold; color: lightgray")
            msgBox.setText('Mensagem excedeu 1000 caracteres')
            msgBox.setInformativeText(
                'Corrija a mensagem para ativar o botão salvar!')
            msgBox.setStandardButtons(QMessageBox.Ok)  # | QMessageBox.Ok)
            msgBox.setEscapeButton(QMessageBox.Ok)
        # msgBox.setDefaultButton(QMessageBox.Ok)
            retval = msgBox.exec_()
            # showErro("Excedeu limite. Campanha não pode ser salva!")
        else:
            self.sms_save_button.setDisabled(False)
        self.mostra_carac()
        # print(len(self.msg_txt.toPlainText()))

    def TipoSms(self, index):
        global Flash
        if index == 1:  # 读取远端参数
            showErro("teste")
        if index == 2:  # 读取远端参数
            Flash = "ATIVADO"

    def mostra_carac(self):
        # self.current_page = 0
        # self.imsi_cnt = 0
        # self.page_cnt = 0
        global cara, msg_cara, cara_r, msg_r

        if cara == 0:
            cara_r = 11
            print(cara_r)
        else:
            cara_r = 11-(cara)

        if msg_cara == 0:
            msg_r = 1000
            print(cara)
            print(cara_r)
        else:
            msg_r = 1000-(msg_cara)
        info = "Contadores - Remetente: usados %d restantes %d |  Mensagem: usados %d restantes %d" % (
            cara, cara_r, msg_cara, msg_r)
        # self.ui.lcd.display(self.imsi_cnt)
        # info = "%d Conexões recebidas,   %d Páginas,         Página atual --%d "%(self.imsi_cnt, self.page_cnt, self.current_page)
        self.char_count.setText(self.tr(info))
        # self.lcdview.display(self.imsi_cnt)

    def change_the_tab_to_btn_widgets(self):
        global widgets, window_obj
        btn = widgets.btn_widgets
        btnName = btn.objectName()

        widgets.stackedWidget.setCurrentWidget(widgets.smspy_page)  # SET PAGE
        modules.ui_functions.UIFunctions.resetStyle(
            window_obj, btnName)  # RESET ANOTHERS BUTTONS SELECTED
        btn.setStyleSheet(modules.ui_functions.UIFunctions.selectMenu(
            btn.styleSheet()))  # SELECT MENU

    def rembut(self):
        global remet, campanha, UeInfoPanel, state_str, HostBox, fb_painel
        data_hoje = date.today()

        if operando == True:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('ATENÇÃO')
            msgBox.setWindowIcon(QtGui.QIcon(
                'platforms/resources/icon/stat.png'))
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setStyleSheet(
                "Background-color: rgb(44, 49, 60); font-weight: bold; color: lightgray")
            msgBox.setText('Dispositivo em operação')
            msgBox.setInformativeText(
                'Para trocar a mensagem é preciso reiniciar, confirma?')
            msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            msgBox.setEscapeButton(QMessageBox.Cancel)
            # msgBox.setDefaultButton(QMessageBox.Ok)
            retval = msgBox.exec_()
            if retval == QMessageBox.Ok:
                # self.dump()
                sendStopToAllBoard()
                # self.chgState()
                closeUdpSocket()
                button_open_serial.setText('AGUARDANDO DISPOSITIVO')
                time.sleep(3)
                initUdpSocket(self)
                # button_open_serial.setReadOnly(True)
                button_open_serial.setEnabled(False)
                button_dump.setEnabled(False)
                button_dump.setText("3 - INICIAR OPERAÇÃO")

            if retval == QMessageBox.Cancel:
                return

        campanha = self.msg_txt.toPlainText()
        remet = self.sender_line.text()

        dados_salvar = {"data_received": data_hoje,
                        "mensagem": campanha,
                        "evento": remet}  # Indicar se a mensagem foi enviada ou não

        # local_database = str(Path(__file__).parent / "database" / "/platforms/resources/database//platforms/resources/database/optinsms.db")
        local_database = "platforms/resources/database/optinsms.db"
        # print(f"Local do Database:\n", local_database)
        # print(f"Dados a Salvar:\n", dados_salvar)
        if remet == "":
            msgBox = QMessageBox()
            msgBox.setWindowTitle('ATENÇÃO')
            msgBox.setWindowIcon(QtGui.QIcon(
                'platforms/resources/icon/stat.png'))
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setStyleSheet(
                "Background-color: rgb(44, 49, 60); font-weight: bold; color: lightgray")
            msgBox.setText('============== Mensagem incompleta ==============')
            msgBox.setInformativeText('O remetente é obrigatório!')
            msgBox.setStandardButtons(QMessageBox.Ok)  # | QMessageBox.Ok)
            msgBox.setEscapeButton(QMessageBox.Ok)
            # msgBox.setDefaultButton(QMessageBox.Ok)
            retval = msgBox.exec_()
            return
        if campanha == "":
            msgBox = QMessageBox()
            # msgBox.setFixedWidht(300)
            msgBox.setWindowTitle('ATENÇÃO')
            msgBox.setWindowIcon(QtGui.QIcon(
                'platforms/resources/icon/stat.png'))
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setStyleSheet(
                "Background-color: rgb(44, 49, 60); font-weight: bold; color: lightgray")
            msgBox.setText('============== Mensagem incompleta ==============')
            msgBox.setInformativeText(
                'Não é possível enviar mensagem em branco!')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setEscapeButton(QMessageBox.Ok)
            retval = msgBox.exec_()
            return

        db.insert_campanhas(local_database, dados_salvar)
        g_msg_list_tb.loadFromCfg()
        self.change_the_tab_to_btn_widgets()
        send_buf3 = (" ".join(campanha.splitlines()))  # (campanha)
        send_buf2 = (remet)
        print('SMS CLASSE 0 ...')
        # self.sendCmmHostMsg("SetFlashSms 1")
        # time.sleep(0.5)
        print("SetSmsCfg 1 " + (send_buf2) + " " + (send_buf3))
        time.sleep(0.5)
        print(" ".join(campanha.splitlines()))
        fb_painel.setText(
            "    REMETENTE: \n    %s \n\n    MENSAGEM: \n    %s " % (send_buf2, campanha))

    def dumpMsg(self):
        global c_cfg
        clFile = open("./msgdb.txt", "wb")
        pickle.dump(c_cfg, clFile)
        clFile.close()

    def allFilter(self):
        showErro("teste")
        pass

    def allFilter1(self):
        broca = self.msg_list_tb.itemClicked
        # self.msg_list_tb._current_selected_row = row
        # broca = (self.msg_list_tb.currentRow)
        print(broca)

    def onRightPopMenu(self, point):
        rightPopMenu = QMenu(self)
        action = QAction(self.tr("IN_FILTER"), self,
                         priority=QAction.LowPriority, triggered=self.allFilter)

        rightPopMenu.addAction(action)
        action = QAction(self.tr("NOT_IN_FILTER"), self,
                         priority=QAction.LowPriority, triggered=self.allFilter1)

        # rightPopMenu.addAction(action)
        # action = QtGui.QAction(self.tr("Change"), self,
        #                 priority=QtGui.QAction.LowPriority, triggered=self.changeUeName)

        # rightPopMenu.addAction(action)
        # action = QtGui.QAction(self.tr("Delete"), self,
        #                 priority=QtGui.QAction.LowPriority, triggered=self.delUe)
        rightPopMenu.addAction(action)
        # (self.mapToGlobal(point))
        rightPopMenu.exec_(self.mapToGlobal(point))


class MsgEdit2(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        global g_msg_list_tb, remet, campanha
        super().__init__()
        layout = QHBoxLayout()
        # self.setWindowTitle(self.tr("Definir campanha"))
        # self.setWindowIcon(QtGui.QIcon('platforms/resources/icon/stat.png'))
        # self.setStyleSheet("background-color: lightgray")#("background: light#QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #000);green")

        top_layout = QGridLayout()
        botton_layout = QHBoxLayout()
        # top_layout.setColumnStretch(0, 200)
        top_layout.setRowStretch(0, 2)
        top_layout.setRowStretch(1, 2)
        top_layout.setRowStretch(2, 2)
        top_layout.setRowStretch(3, 1)
        top_layout.setRowStretch(4, 2)
        self.op_title = QLabel(self.tr(
            "Selecione e clique na operadora 1, em seguida selecione e clique na operadora 2"))
        self.op_title.setFont(QFont('Arial', 18))
        self.op1_ico = QLabel()
        self.op2_ico = QLabel()
        self.op3_ico = QLabel()
        # self.op1_ico.setStyleSheet("QLabel { background-color: black; border-image: url(platforms/resources/icon/vivo.png) -10 -10 -10 -10 cover strech;  background-repeat: no-repeat; background-position: center; font-weight: bold; color: gray; border-radius: 9px; qproperty-alignment: AlignCenter; }")
        # self.op1_ico.setStyleSheet("QPushButton{border-image: url(platforms/resources/icon/vivo.png)}")
        self.op1_ico.setFixedSize(326, 76)
        self.op2_ico.setFixedSize(200, 76)
        self.op3_ico.setFixedSize(200, 54)
        # self.op3_ico.setFixedSize(94,94)
        self.op1_ico.setStyleSheet(
            "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/vivo.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
        self.op2_ico.setStyleSheet(
            "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/claro.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
        self.op3_ico.setStyleSheet(
            "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/tim.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
        self.op_title.setStyleSheet(
            "QLabel { background-color: rgb(40,44,52) ; font-weight: bold;  }")
        # self.op3_ico.setStyleSheet("QPushButton{border-image: url(platforms/resources/icon/claro.png);}")
        # self.op3_ico.setStyleSheet("QLabel { background-color: black; border-image: url(platforms/resources/icon/oi.png) 0 0 0 0 strech strech;  background-repeat: no-repeat; background-position: center; font-weight: bold; color: gray; border-radius: 9px; qproperty-alignment: AlignCenter; }")
        # self.op3_ico.setStyleSheet("QLabel { background-color: black; background-image: url(platforms/resources/icon/claro.png);  background-repeat: no-repeat; background-position: center; font-weight: bold; color: gray; border-radius: 9px; qproperty-alignment: AlignCenter; }")
        # self.op3_ico.setStyleSheet("background-image: url(platforms/resources/icon/claro.png)")
        # self.op3_ico.setStyleSheet("border: none")
        self.op1 = QComboBox()
        self.op1.setStyleSheet(
            "QComboBox QAbstractItemView::item {min-height: 65px; }")

        # self.op1.insertItem(0,self.tr("VIVO"))
        # self.op1.insertItem(1,self.tr("CLARO"))
        # self.op1.insertItem(2,self.tr("TIM"))
        # self.op1.insertItem(3,self.tr(" OI "))
        self.op1.setIconSize(QSize(150, 50))
        self.op1.addItem(QIcon("platforms/resources/icon/vivo.png"), '')
        self.op1.addItem(QIcon("platforms/resources/icon/claro.png"), '')
        self.op1.addItem(QIcon("platforms/resources/icon/tim.png"), '')
        self.op1.addItem(QIcon("platforms/resources/icon/oi.png"), '')
        self.op1.view().setRowHidden(1, True)
        self.op2 = QComboBox()
        self.op2.setStyleSheet(
            "QComboBox QAbstractItemView::item {min-height: 65px; }")
        self.op2.addItem(QIcon("platforms/resources/icon/vivo.png"), '')
        self.op2.addItem(QIcon("platforms/resources/icon/claro.png"), '')
        self.op2.addItem(QIcon("platforms/resources/icon/tim.png"), '')
        self.op2.addItem(QIcon("platforms/resources/icon/oi.png"), '')
        self.op2.setIconSize(QSize(150, 50))
        # self.op2.insertItem(0,self.tr("VIVO"))
        # self.op2.insertItem(1,self.tr("CLARO"))
        # self.op2.insertItem(2,self.tr("TIM"))
        # self.op2.insertItem(3,self.tr("OI"))
        self.op2.setCurrentIndex(1)
        self.op2.setEnabled(False)
        self.reload = QPushButton(self.tr("ESCOLHER  NOVAMENTE"))
        self.reload.setFixedSize(326, 76)

        self.reload.setStyleSheet("QPushButton{border-radius: 20px; font-weight: bold; }"
                                  "QPushButton:hover{background-color: green}"
                                  "QPushButton:pressed{background-color: lightgreen; color: green}")

        self.aplica = QPushButton(self.tr("CONFIRMAR ALTERAÇÃO"))
        self.aplica.setFixedSize(326, 76)
        self.aplica.setStyleSheet("QPushButton{border-radius: 20px; font-weight: bold;}"
                                  "QPushButton:hover{background-color: green}"
                                  "QPushButton:pressed{background-color: lightgreen; color: green}")
        # self.reload.setMinimumWidth(90)

        # top_layout.addWidget(self.sender, 0, 0, Qt.AlignLeft)
        # top_layout.addWidget(self.char_count, 0, 1, Qt.AlignLeft)
        # top_layout.addWidget(self.op1_ico, 0, 0, Qt.AlignCenter)
        top_layout.addWidget(self.op_title, 0, 0, Qt.AlignCenter)
        top_layout.addWidget(self.op1, 2, 0, Qt.AlignCenter)
        top_layout.addWidget(self.op1_ico, 1, 0, Qt.AlignCenter)
        # top_layout.addWidget(self.op3_ico, 2, 1, Qt.AlignCenter)
        top_layout.addWidget(self.op2_ico, 1, 2, Qt.AlignCenter)
        top_layout.addWidget(self.op2, 2, 2, Qt.AlignCenter)
        top_layout.addWidget(self.reload, 4, 0, Qt.AlignCenter)
        top_layout.addWidget(self.aplica, 4, 2, Qt.AlignCenter)
        # top_layout.addWidget(self.char_count, 0, 1, Qt.AlignLeft)
        # top_layout.setColumnStretch(0, 10)
        # top_layout.setColumnStretch(1, 1)
        # top_layout.setColumnStretch(2, 10)

        # g_msg_list_tb = MsgListBox()

        # msg_list = QHBoxLayout()

        # botton_layout.addWidget(self.op1_ico)#, Qt.AlignCenter)
        # botton_layout.addWidget(self.op3_ico, Qt.AlignHCenter)
        # botton_layout.addWidget(self.reload)#, Qt.AlignCenter)

        layout.addLayout(top_layout)

        layout.addLayout(botton_layout)

        # layout.addWidget(self.op1)
        # msg_cmd_layout = QGridLayout()

        back_button = QPushButton(self.tr(""))
        back_button.setStyleSheet("border: none")
        back_button2 = QPushButton(self.tr(""))
        # ("QPushButton{border: none}"
        back_button2.setStyleSheet("border: none")
        # "QPushButton:hover{background-color: green}"
        # "QPushButton:pressed{background-color: lightgreen}")#("background-color: green")("border: none")
        # back_button.setStyleSheet("background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #040);green")
        # back_button.setStyleSheet("hover: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #090);green")
        # msg_cmd_layout.addWidget(self.sms_cfg_box, 0, 0)
        # msg_cmd_layout.addWidget(self.sms_save_button, 0, 1)
        # msg_cmd_layout.addWidget(back_button, 0, 2)
        # msg_cmd_layout.addWidget(back_button2, 0, 3)
        # layout.addLayout(msg_cmd_layout)
        # layout.addLayout(msg_list)
        # msg_list.addWidget(g_msg_list_tb)
        self.setLayout(layout)
        # cara = 0
        # COMENTADO PARA NÃO ATERAR AS ONFIGURAÇOES PADRÃO
        # self.aplica.clicked.connect(self.aplica_gsm)  # (dumpMsg)
        self.reload.clicked.connect(self.reload_op)  # (dumpMsg)
        # self.sms_cfg_box.activated.connect(self.TipoSms)
        self.op1.activated.connect(self.op1names)
        self.op2.activated.connect(self.op2names)
        # self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        # self.customContextMenuRequested[QtCore.QPoint].connect(self.onRightPopMenu)

    def aplica_gsm(self):
        global setacel
        setacel = (ggsm1h + ggsmc1 + ggsmc2 + ggsm1f)
        msgBox = QMessageBox()
        msgBox.setWindowTitle('CONFIRMA?')
        msgBox.setWindowIcon(QtGui.QIcon('platforms/resources/icon/stat.png'))
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setStyleSheet(
            "Background-color: rgb(44, 49, 60); font-weight: bold; color: lightgray")
        msgBox.setText('TROCAR OPERADORAS')
        msgBox.setInformativeText(
            'Para trocar a operadora irá reiniciar, confirma?')
        msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Cancel)
        # msgBox.setDefaultButton(QMessageBox.Ok)
        retval = msgBox.exec_()
        if retval == QMessageBox.Ok:

            print(setacel)
            troca_op()

    def reload_op(self):

        self.op1.setEnabled(True)
        self.op1.setCurrentIndex(0)
        self.op2.setCurrentIndex(1)

        # self.op1_ico.setStyleSheet("QPushButton{border-image: url(platforms/resources/icon/vivo.png)}")
        self.op1_ico.setStyleSheet(
            "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/vivo.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
        self.op1_ico.setFixedSize(326, 76)
        self.op2_ico.setFixedSize(200, 76)
        # self.op2_ico.setStyleSheet("QPushButton{border-image: url(platforms/resources/icon/claro.png)}")
        self.op2_ico.setStyleSheet(
            "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/claro.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
        self.op1.view().setRowHidden(0, False)
        self.op1.view().setRowHidden(1, True)
        self.op1.view().setRowHidden(2, False)
        self.op1.view().setRowHidden(3, False)
        self.op2.view().setRowHidden(0, False)
        self.op2.view().setRowHidden(1, False)
        self.op2.view().setRowHidden(2, False)
        self.op2.view().setRowHidden(3, False)
        self.op2.setEnabled(False)

    def op1names(self, index):
        global ggsmc1, ggsmc2, ggsmcvivo, ggsmcclaro, ggsmctim, ggsmcoi

        if index == 0:  # 读取远端参数 ler parâmetros remotos
            self.op2.view().setRowHidden(0, True)
            ggsmc1 = (ggsmcvivo)
            self.op1.setEnabled(False)
            self.op2.setEnabled(True)
        if index == 1:  # 读取远端参数 ler parâmetros remotos
            self.op2.view().setRowHidden(1, True)
            ggsmc1 = (ggsmcclaro)
            self.op1_ico.setFixedSize(200, 76)
            self.op1_ico.setStyleSheet(
                "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/claro.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")

            self.op1.setEnabled(False)
            self.op2.setEnabled(True)
        if index == 2:  # 读取远端参数 ler parâmetros remotos
            self.op2.view().setRowHidden(2, True)
            ggsmc1 = ggsmctim
            self.op1_ico.setFixedSize(200, 54)
            self.op1_ico.setStyleSheet(
                "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/tim.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
            # print(ggsmc1)
            # setacel = (ggsm1h + ggsmc1)
            # print(setacel)
            # self.op1_ico.setStyleSheet("QPushButton{border-image: url(platforms/resources/icon/tim.png)}")
            self.op1.setEnabled(False)
            self.op2.setEnabled(True)
        if index == 3:  # 读取远端参数 ler parâmetros remotos
            self.op2.view().setRowHidden(3, True)
            ggsmc1 = (ggsmcoi)
            self.op1_ico.setFixedSize(94, 94)
            self.op1_ico.setStyleSheet(
                "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/oi.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")

            self.op1.setEnabled(False)
            self.op2.setEnabled(True)

    def op2names(self, index):
        global ggsmc1, ggsmc2, ggsmcvivo, ggsmcclaro, ggsmctim, ggsmcoi
        if index == 0:  # 读取远端参数
            # ler parâmetros remotos
            self.op2_ico.setFixedSize(300, 76)
            ggsmc2 = (ggsmcvivo)
            self.op2_ico.setStyleSheet(
                "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/vivo.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
            # self.op2_ico.setStyleSheet("QPushButton{border-image: url(platforms/resources/icon/vivo.png)}")
            self.op2.setEnabled(False)
        if index == 1:  # 读取远端参数 ler parâmetros remotos
            ggsmc2 = (ggsmcclaro)
            self.op2_ico.setFixedSize(200, 76)
            self.op2_ico.setStyleSheet(
                "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/claro.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
            # self.op2_ico.setStyleSheet("QPushButton{border-image: url(platforms/resources/icon/claro.png)}")
            self.op2.setEnabled(False)
        if index == 2:  # 读取远端参数 ler parâmetros remotos
            ggsmc2 = (ggsmctim)
            self.op2_ico.setFixedSize(200, 54)
            self.op2_ico.setStyleSheet(
                "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/tim.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
            # self.op2_ico.setStyleSheet("QPushButton{border-image: url(platforms/resources/icon/tim.png)}")
            self.op2.setEnabled(False)
        if index == 3:  # 读取远端参数 ler parâmetros remotos
            ggsmc2 = (ggsmcoi)
            self.op2_ico.setFixedSize(94, 94)
            self.op2_ico.setStyleSheet(
                "QLabel { background-color: rgb(40,44,52) ; border-image: url(platforms/resources/icon/oi.png) 0 0 0 0 cover strech; border-radius: 9px; qproperty-alignment: AlignCenter; }")
            # self.op3_ico.setFixedSize(100,64)
            # self.op2_ico.setStyleSheet("QPushButton{border-image: url(platforms/resources/icon/oi.png)}")
            self.op2.setEnabled(False)

    def change_the_tab_to_btn_widgets(self):
        global widgets, window_obj
        btn = widgets.btn_widgets
        btnName = btn.objectName()

        widgets.stackedWidget.setCurrentWidget(widgets.smspy_page)  # SET PAGE
        modules.ui_functions.UIFunctions.resetStyle(
            window_obj, btnName)  # RESET ANOTHERS BUTTONS SELECTED
        btn.setStyleSheet(modules.ui_functions.UIFunctions.selectMenu(
            btn.styleSheet()))  # SELECT MENU

    def rembut(self):
        global remet, campanha, UeInfoPanel, state_str, HostBox
        data_hoje = date.today()

        dados_salvar = {"data_received": data_hoje,
                        "mensagem": campanha,
                        "evento": remet}  # Indicar se a mensagem foi enviada ou não

        # local_database = str(Path(__file__).parent / "database" / "/platforms/resources/database//platforms/resources/database/optinsms.db")
        local_database = "platforms/resources/database/optinsms.db"
        # print(f"Local do Database:\n", local_database)
        # print(f"Dados a Salvar:\n", dados_salvar)

        db.insert_campanhas(local_database, dados_salvar)
        g_msg_list_tb.loadFromCfg()
        self.change_the_tab_to_btn_widgets()
        send_buf3 = (" ".join(campanha.splitlines()))  # (campanha)
        send_buf2 = (remet)
        print('SMS CLASSE 0 ...')
        # self.sendCmmHostMsg("SetFlashSms 1")
        # time.sleep(0.5)
        print("SetSmsCfg 1 " + (send_buf2) + " " + (send_buf3))
        time.sleep(0.5)
        print(" ".join(campanha.splitlines()))

    def dumpMsg(self):
        global c_cfg
        clFile = open("./msgdb.txt", "wb")
        pickle.dump(c_cfg, clFile)
        clFile.close()

    def allFilter(self):
        showErro("teste")
        pass

    def allFilter1(self):
        broca = self.msg_list_tb.itemClicked
        # self.msg_list_tb._current_selected_row = row
        # broca = (self.msg_list_tb.currentRow)
        print(broca)

    def onRightPopMenu(self, point):
        rightPopMenu = QMenu(self)
        action = QAction(self.tr("IN_FILTER"), self,
                         priority=QAction.LowPriority, triggered=self.allFilter)

        rightPopMenu.addAction(action)
        action = QAction(self.tr("NOT_IN_FILTER"), self,
                         priority=QAction.LowPriority, triggered=self.allFilter1)

        # rightPopMenu.addAction(action)
        # action = QtGui.QAction(self.tr("Change"), self,
        #                 priority=QtGui.QAction.LowPriority, triggered=self.changeUeName)

        # rightPopMenu.addAction(action)
        # action = QtGui.QAction(self.tr("Delete"), self,
        #                 priority=QtGui.QAction.LowPriority, triggered=self.delUe)
        rightPopMenu.addAction(action)
        # (self.mapToGlobal(point))
        rightPopMenu.exec_(self.mapToGlobal(point))


class SMSPYWindow(QWidget):
    def __init__(self, _self, _widgets):  # 构造函数
        global widgets, window_obj
        window_obj = _self
        widgets = _widgets

        super(SMSPYWindow, self).__init__()
        # self.setWindowTitle(self.tr("LTE SMS PUSH Control")) #构造函数
        # self.resize(1000,650)
        # self.setWindowIcon(QtGui.QIcon('icon/stat.png'))
        self.w = MsgEdit()
        # self.setStyleSheet("background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #000);green")  ##c1f);green")
        # self.setStyleSheet("QLabel { background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #000);green")
        self.button = QPushButton("Push for Window")
        self.etiq = QLabel('teste')
        # self.etiq.setStyleSheet("background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #040);green")
        # self.button.clicked.connect(self.toggle_window)
        self.panel = Panel(self)
        layout = QHBoxLayout()
        layout.addWidget(self.panel)
        self.setLayout(layout)

        # self.setCentralWidget(panel)

        def toggle_window(self, checked):
            if self.w.isVisible():
                self.w.hide()
            else:
                self.w.show()

            # self.setStyleSheet("background-color: lightcyan")
            # main = SetBox()
            # main = UeIndiTable()
            # main = UeInfoPanel()
            # panel = Panel()
            self.panel = Panel(self)
            # self.setCentralWidget(panel)  #使用的是子类继承父类的方法

            self.createActions()
            self.createMenus()
            # self.createToolBars()
            message = "LTE SMS Manager"
            self.statusBar().showMessage(message)

        # -----------------------------------------------------------------
        # 添加菜单函数及提示框函数
        # Adicionar função de menu e função de caixa de prompt

        def createToolBars(self):
            # self.fileToolBar = self.addToolBar("File")
            # self.fileToolBar.addAction(self.exitAct)
            self.editToolBar = self.addToolBar("Help")
            self.editToolBar.addAction(self.aboutAct)

        def createActions(self):
            self.exitAct = QAction(QIcon('icon/exit.png'), "E&xit", self, shortcut="Ctrl+Q",
                                   statusTip="Exit the application", triggered=self.close)
            self.aboutAct = QAction(QIcon('icon/query.png'), "&About", self,
                                    statusTip="Show the application's About box",
                                    triggered=self.about)

        def createMenus(self):
            self.fileMenu = self.menuBar().addMenu("&File")
            self.fileMenu.addSeparator()
            self.fileMenu.addAction(self.exitAct)

            self.helpMenu = self.menuBar().addMenu("&Help")
            self.fileMenu.addSeparator()
            self.helpMenu.addAction(self.aboutAct)

        def about(self):
            # self.infoLabel.setText("Invoked <b>Help|About</b>")

            QMessageBox.about(self, "Sobre...",
                                    "Sms LTE-SB Dual-GSM")
            # "The <b>UeMonitor</b> is copyright belongs to PanstonTech. ")

        # -----------------------------------------------------------------
        # 重写关闭窗口事件
        # Substituir evento de fechamento de janela

        def closeEvent(self, event):
            os._exit(0)
