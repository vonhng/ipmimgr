#!/usr/bin/env python
# encoding: utf-8
"""
@version: 2.7.10
@author: vonhng
@contact: vonhng@qq.com
@file: power.py
@time: 2018/07/13 09:34
"""
from pyghmi.ipmi import command as ipmi_command
from plumbum import cli, colors


class Power(cli.Application):
    VERSION = colors.green | "1.0.0"
    COLOR_GROUPS = {"Meta-switches": colors.bold & colors.yellow, "Switches": colors.green}

    _action, _bmc, _user, _pwd = ("", "", "ADMIN", "123456")

    get_power = cli.Flag("-g", help="if given, get power status")

    @cli.switch("-s", cli.Set("on", "off", "reset", case_sensitive=True), excludes=["-g"], requires=["-i"], help="set power on|off|reset")
    def set_power(self, cmd):
        self._action = cmd

    @cli.switch("-i", str, help="IPMI IP,example: 111(only 10.10.90.111)/10.10.xxx.xxx")
    def get_ip(self, ip):
        if ip.isdigit():
            bmc = "10.10.90.{}".format(int(ip))
        else:
            bmc = ip
        self._bmc = bmc

    @cli.switch("-p", str, requires=["-u"], help="IPMI PASSWORD,default: 123456")
    def get_pwd(self, pwd):
        self._pwd = pwd

    @cli.switch("-u", str, help="IPMI USER,default: ADMIN", requires=["-i", "-p"])
    def get_user(self, user):
        self._user = user

    def main(self):
        print colors.bold | "[ IPMIINFO ] ipmiip: {}, ipmiuser: {}, ipmipwd: {}".format(self._bmc, self._user, self._pwd)
        try:
            ipmicmd = ipmi_command.Command(bmc=self._bmc, userid=self._user, password=self._pwd)
        except Exception:
            print colors.warn | "[ ERROR ] failed: not connect"
            return
        if self.get_power:
            try:
                ret = ipmicmd.get_power()
            except Exception as e:
                print colors.warn | "[ ERROR ] failed: {}".format(e)
            else:
                print colors.green | "[ OK ] power is {}".format(ret.get("powerstate", "unknow"))
        else:
            try:
                ret = ipmicmd.set_power(self._action, wait=10)
            except Exception as e:
                print colors.warn | "[ ERROR ] failed: {}".format(e)
            else:
                status = ret.get("powerstate") if ret.get("powerstate") else ret.get("pendingpowerstate")
                print colors.green | "[ OK ] power is {}".format(status, "unknow")


if __name__ == "__main__":
    Power.run()
