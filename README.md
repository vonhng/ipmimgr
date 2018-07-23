[toc]



---

## 1. 要解决的问题

1. ipmitool的命令这么长，记不住啊

2. 使用IBM开发的pyghmi包封装，不需要使用者安装ipmitool工具

## 2. 环境要求

```

pip install pyghmi

pip install plumbum

```

## 3. 使用说明

```bash

ipmimgr 1.0.0



Usage:

    ipmimgr [SWITCHES]



Meta-switches:

    -h, --help Prints this help message and quits

    --help-all Print help messages of all subcommands and quit

    -v, --version Prints the program's version and quits



Switches:

    -g if given, get power status   # 不可与-s共用，获取节点电源状态

    -i IP:str IPMI IP,example: 111(only 10.10.90.111)/10.10.xxx.xxx   # 节点的ipmi ip，90网段直接输入最后一段即可，其他网段使用全ip

    -p PWD:str IPMI PASSWORD,default: 123456; requires -u   # ipmi pwd，默认为123456

    -s CMD:{'reset', 'on', 'off'} set power on|off|reset; requires -i; excludes -g   # 改变电源状态，重启(reset)、开启(on)、关闭(off)

    -u USER:str IPMI USER,default: ADMIN; requires -i, -p   # ipmi user，默认为ADMIN

```

## 4. Example

#### 4.1 查看节点的电源状态

>10.10.90.11的ipmi ip为10.10.90.111，账号ADMIN，密码123456

```bash

➜ ~ ipmimgr -g -i 111

[ IPMIINFO ] ipmiip: 10.10.90.111, ipmiuser: ADMIN, ipmipwd: 123456

[ ERROR ] failed: not connect

```

```bash

➜ ~ ipmimgr -g -i 10.10.90.111

[ IPMIINFO ] ipmiip: 10.10.90.111, ipmiuser: ADMIN, ipmipwd: 123456

[ ERROR ] failed: not connect
```

```bash

➜ ~ ipmimgr -g -i 10.10.90.111 -u ADMIN -p 123456

[ IPMIINFO ] ipmiip: 10.10.90.111, ipmiuser: ADMIN, ipmipwd: 123456

[ ERROR ] failed: not connect

```

#### 4.2. 修改电源状态

>10.10.90.11的ipmi ip为10.10.90.111，账号ADMIN，密码123456

## 5. TODO

#### 5.1. 解决依赖

#### 5.2. go重建

## 6. FAQ

发现远程执行ipmi查看/设置节点电源状态时，会出现大约30s超时现象，

但是此时在同一qdata集群(同一网段？)的其他节点执行则不会有这种情况