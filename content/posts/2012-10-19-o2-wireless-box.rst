..
   Copyright (c) 2012 Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

Lobotomising an O2 Wireless Box IV
==================================

:date: 2012-10-19
:tags: old
:summary: This is a resurrection of a post from my old personal website. The
          info here is long out of date, but I don't like information to die.

Introduction
------------

.. figure:: /images/1280px-O2_Wireless_Box_IV.jpg
   :width: 100%
   :alt: Photo of an O2 Wireless Box IV.

   Photo of an O2 Wireless Box IV.
   Source: `GoddersUK at English Wikipedia, via Wikimedia Commons <https://commons.wikimedia.org/wiki/File:O2_Wireless_Box_IV.jpg>`_.
   Licensed under `CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>`_.

This article documents how to turn an O2 Wireless Box IV into a modem/bridge so
that a different device may be used as the router for your internet connection.
In my case that other device is an ALIX 2D3 box running pfsense, but that
doesn't really affect the instructions given below.

This guide is largely based on
"`Bridge/modem only mode for Thomson routers (TG587nv2 / O2 wireless box IV) <https://m01.eu/blog/2012/07/bridging-thomson-routers>`_"
written by Michiel. That's a fantastic guide and should also be consulted, this
article of mine really just gives my take on following that proceedure and what
worked for me. These instructions are written from memory...

I provide NO WARRANTY OF ANY KIND for these instructions and they are intended
for educational use only. If you wish to follow these instructions with your own
device, you do so at your own risk. You may not hold me responsible if you brick
your router!

Available Interfaces
--------------------

There are several interfaces available on the O2 Wireless Box IV. The important
ones are listed as follows:

* "atm" (and "atm_llu"): These interfaces represent the Asynchronous Transfer Mode (ATM) connection over your phone line to your ISP.

* "eth": This is a bridging Ethernet interface, likely as O2 use ETHoA (Ethernet over ATM) for internet connections.

* "O2_ADSL2plus": This is the high level internet connection.

* "ethport1" to "ethport4": These represent each network port on your router.

* "bridge": This interface connects all 4 network ports together over a bridge so that network traffic is passed between the ports without routing.

The basic plan is to remove the "eth" and "O2_ADSL2plus" interfaces which will
no longer be used, remove "ethport4" from "bridge" so that it is no longer part
of the local network and instead connect it via a new bridge to "atm". Thus the
O2 Wireless Box IV will act as a media converter between the Ethernet interface
on network port 4 and the ATM interface on your telephone line. The new router
will then be connected to port 4 and should see a direct connection to the
internet (it will be assigned your publically visible IP address).

Removing Interfaces
-------------------

To remove the settings which were no longer needed, I connected to the O2
Wireless Box IV by telnet and used the built-in command line. It may have been
possible to upload these commands as part of the configuration file changes
which were made later, but I didn't get chance to try that.

You need to login to the telnet interface of the O2 router using the "SuperUser"
account, which has a default password of the device's serial number if you have
not changed it. If you do not have any telnet software, I would recommend using
PuTTY. Once you're logged in, you'll see a prompt.

At this point, it is useful to note that backspace will not work on this telnet
connection and you should instead use CTRL+H to delete a character. The "help"
command is always useful, and if you have entered a command group (for example
by executing "ip") you can return to the higher config level by executing "..".
It can also be seen from the initial prompt that the O2 Wireless Box IV is based
on a Thomson TG587n v2 platform.

If you now execute "interface list" you should be given a list of all the
interfaces currently configured on your device, including the important ones
listed above. Our first port of call is the delete the "O2_ADSL2plus" and "eth"
interfaces to free up the "atm" interface for later use. Note that "eth help"
and "ip help" can be used to list available commands for eth and ip interfaces,
and if ifdelete is not given any arguments you will be prompted for the
interface to delete.

::

    eth ifdelete intf=eth
    ip ifdelete intf=O2_ADSL2plus

That should be it. There doesn't seem to be a way to detach "ethport4" from
"bridge" via the command line so we shall simply remove the relevant config
settings in the next stage. You may now disconnect from the O2 Wireless Box IV.

Configuration File Changes
--------------------------

The remainder of the changes will be made by downloading a configuration file
from the O2 Wireless Box IV, modifying it and then uploading it back to the
device. Firstly, connect to the device via the web interface and login as
SuperUser using the password you used on telnet. You should navigate to "O2
Wireless Box" -> "Configuration" -> "Save or Restore Configuration" and click
"Backup Configuration Now...". Once you have downloaded this file, open it in a
text editor and make the following changes:

* Remove all entries in the "[ eth.ini ]" group.

* Remove all entries relating to "O2_ADSL2plus" in the "[ ip.ini ]" group.
  Ensure you leave the "loop" and "LocalNetwork" and other entries alone as
  these are probably needed.

* Remove all existing entries relating to "ethport4" from "[ bridge.ini ]" to
  detach "ethport4" from "bridge". Add the following entries to this group in
  order to create a new bridge titled "direct_bridge" between "atm" and
  "ethport4"::

    add brname=direct_bridge
    ifadd brname=direct_bridge intf=ethport4 dest=ethif4 logging=disabled
    ifadd brname=direct_bridge intf=atm
    ifconfig brname=direct_bridge intf=ethport4 wan=disabled logging=disabled
    ifconfig brname=direct_bridge intf=atm dest=atm_llu wan=enabled
    ifattach brname=direct_bridge intf=atm
    ifattach brname=direct_bridge intf=ethport4 logging=disabled
    config brname=direct_bridge age=300 filter=no_WAN_broadcast vlan=disabled

Now go back to the "Save or Restore Configuration" page on the web interface,
use "Choose File" to select this modified configuration file and click "Restore
Configuration Now...". The device will now reload its configuration and you may
need to reboot the device in order to ensure everything is applied correctly.

At this point network port 4 will be bridged directly to the internet and will
no longer be part of the local network so it is important that the computer you
use to perform these modifications is not plugged into that socket. Instead you
now want to connect your alternative router's WAN port to network port 4 and
configure that router appropriately. That part is left as an exersize for the
reader...

Here is the resulting configuration file contents, with a few bits sanitised to
remove sensitive information::

    [ sntpc.ini ]
    add name=ntp.broadband.o2.co.uk version=3
    config state=enabled poll=60 pollpresync=5 wanSubscribe=disabled
    debug traceconfig state=enabled

    [ xdsl.ini ]
    debug traceconfig level=0
    config adslmultimode=adsl2plus syslog=disabled

    [ cac.ini ]
    config port=dsl0 state=enabled
    config port=dsl1 state=enabled
    config port=atm2 state=enabled
    config port=aal5 state=disabled
    config port=atm5 state=disabled
    overbooking rt=0 nrt=0

    [ language.ini ]
    config language=en complete=no

    [ script.ini ]
    add name=autopvc_add_qos index=0 command="atm qosbook ctdadd name _auto_$1_$2_tx conformance $3 peakrate $4 sustrate $5 maxburst $6 minrate $7 maxframe $8 celldelay $9 realtime $10 dynamic enabled"
    add name=autopvc_add_qos index=1 command="atm qosbook ctdadd name _auto_$1_$2_rx conformance $11 peakrate $12 sustrate $13 maxburst $14 minrate $15 maxframe $16 celldelay $17 realtime $18 dynamic enabled"
    add name=autopvc_add_qos index=2 command="atm qosbook add name _auto_$1_$2 txctd _auto_$1_$2_tx rxctd _auto_$1_$2_rx dynamic enabled"
    add name=autopvc_delete_qos index=0 command="atm qosbook delete name _auto_$1_$2"
    add name=autopvc_delete_qos index=1 command="atm qosbook ctddelete name _auto_$1_$2_tx"
    add name=autopvc_delete_qos index=2 command="atm qosbook ctddelete name _auto_$1_$2_rx"
    add name=autopvc_add_bridge index=0 command="atm qosbook ctdadd name _auto_$1_$2_tx conformance $3 peakrate $4 sustrate $5 maxburst $6 minrate $7 maxframe $8 celldelay $9 realtime $10 dynamic enabled"
    add name=autopvc_add_bridge index=1 command="atm qosbook ctdadd name _auto_$1_$2_rx conformance $11 peakrate $12 sustrate $13 maxburst $14 minrate $15 maxframe $16 celldelay $17 realtime $18 dynamic enabled"
    add name=autopvc_add_bridge index=2 command="atm qosbook add name _auto_$1_$2 txctd _auto_$1_$2_tx rxctd _auto_$1_$2_rx dynamic enabled"
    add name=autopvc_add_bridge index=3 command="atm phonebook add name _auto_$1_$2 addr $1.$2 dynamic enabled maxFwdCPCS_PDU $21 maxBwdCPCS_PDU $22"
    add name=autopvc_add_bridge index=4 command="atm ifadd intf _auto_$1_$2_atm dest _auto_$1_$2 dynamic enabled"
    add name=autopvc_add_bridge index=5 command="atm ifconfig intf _auto_$1_$2_atm qos _auto_$1_$2 encaps $19 fcs $20 ulp mac"
    add name=autopvc_add_bridge index=6 command="atm ifattach intf _auto_$1_$2_atm"
    add name=autopvc_add_bridge index=7 command="eth bridge ifadd intf _auto_$1_$2_eth dest _auto_$1_$2_atm dynamic enabled"
    add name=autopvc_add_bridge index=8 command="eth bridge ifconfig intf _auto_$1_$2_eth"
    add name=autopvc_add_bridge index=9 command="eth bridge ifattach intf _auto_$1_$2_eth"
    add name=autopvc_delete_bridge index=0 command="eth bridge ifdetach intf _auto_$1_$2_eth"
    add name=autopvc_delete_bridge index=1 command="eth bridge ifdelete intf _auto_$1_$2_eth"
    add name=autopvc_delete_bridge index=2 command="atm ifdetach intf _auto_$1_$2_atm"
    add name=autopvc_delete_bridge index=3 command="atm ifdelete intf _auto_$1_$2_atm"
    add name=autopvc_delete_bridge index=4 command="atm phonebook delete name _auto_$1_$2"
    add name=autopvc_delete_bridge index=5 command="atm qosbook delete name _auto_$1_$2"
    add name=autopvc_delete_bridge index=6 command="atm qosbook ctddelete name _auto_$1_$2_tx"
    add name=autopvc_delete_bridge index=7 command="atm qosbook ctddelete name _auto_$1_$2_rx"
    add name=autopvc_add_pppoerelay index=0 command="atm qosbook ctdadd name _auto_$1_$2_tx conformance $3 peakrate $4 sustrate $5 maxburst $6 minrate $7 maxframe $8 celldelay $9 realtime $10 dynamic enabled"
    add name=autopvc_add_pppoerelay index=1 command="atm qosbook ctdadd name _auto_$1_$2_rx conformance $11 peakrate $12 sustrate $13 maxburst $14 minrate $15 maxframe $16 celldelay $17 realtime $18 dynamic enabled"
    add name=autopvc_add_pppoerelay index=2 command="atm qosbook add name _auto_$1_$2 txctd _auto_$1_$2_tx rxctd _auto_$1_$2_rx dynamic enabled"
    add name=autopvc_add_pppoerelay index=3 command="atm phonebook add name _auto_$1_$2 addr $1.$2 dynamic enabled maxFwdCPCS_PDU $21 maxBwdCPCS_PDU $22"
    add name=autopvc_add_pppoerelay index=4 command="atm ifadd intf _auto_$1_$2_atm dest _auto_$1_$2 dynamic enabled"
    add name=autopvc_add_pppoerelay index=5 command="atm ifconfig intf _auto_$1_$2_atm qos _auto_$1_$2 ulp mac"
    add name=autopvc_add_pppoerelay index=6 command="atm ifattach intf _auto_$1_$2_atm"
    add name=autopvc_add_pppoerelay index=7 command="eth ifadd intf _auto_$1_$2_eth dest _auto_$1_$2_atm dynamic enabled"
    add name=autopvc_add_pppoerelay index=8 command="eth ifattach intf _auto_$1_$2_eth"
    add name=autopvc_add_pppoerelay index=9 command="ppp relay ifadd intf _auto_$1_$2_eth"
    add name=autopvc_delete_pppoerelay index=0 command="ppp relay ifdelete intf _auto_$1_$2_eth"
    add name=autopvc_delete_pppoerelay index=1 command="eth ifdetach intf _auto_$1_$2_eth"
    add name=autopvc_delete_pppoerelay index=2 command="eth ifdelete intf _auto_$1_$2_eth"
    add name=autopvc_delete_pppoerelay index=3 command="atm ifdetach intf _auto_$1_$2_atm"
    add name=autopvc_delete_pppoerelay index=4 command="atm ifdelete intf _auto_$1_$2_atm"
    add name=autopvc_delete_pppoerelay index=5 command="atm phonebook delete name _auto_$1_$2"
    add name=autopvc_delete_pppoerelay index=6 command="atm qosbook delete name _auto_$1_$2"
    add name=autopvc_delete_pppoerelay index=7 command="atm qosbook ctddelete name _auto_$1_$2_tx"
    add name=autopvc_delete_pppoerelay index=8 command="atm qosbook ctddelete name _auto_$1_$2_rx"
    add name=autopvc_add_ipoa index=0 command="atm qosbook ctdadd name _auto_$1_$2_tx conformance $3 peakrate $4 sustrate $5 maxburst $6 minrate $7 maxframe $8 celldelay $9 realtime $10 dynamic enabled"
    add name=autopvc_add_ipoa index=1 command="atm qosbook ctdadd name _auto_$1_$2_rx conformance $11 peakrate $12 sustrate $13 maxburst $14 minrate $15 maxframe $16 celldelay $17 realtime $18 dynamic enabled"
    add name=autopvc_add_ipoa index=2 command="atm qosbook add name _auto_$1_$2 txctd _auto_$1_$2_tx rxctd _auto_$1_$2_rx dynamic enabled"
    add name=autopvc_add_ipoa index=3 command="atm phonebook add name _auto_$1_$2 addr $1.$2 dynamic enabled maxFwdCPCS_PDU $21 maxBwdCPCS_PDU $22"
    add name=autopvc_add_ipoa index=4 command="atm ifadd intf _auto_$1_$2_atm dest _auto_$1_$2 dynamic enabled"
    add name=autopvc_add_ipoa index=5 command="atm ifconfig intf _auto_$1_$2_atm qos _auto_$1_$2 encaps $19 fcs $20 ulp ip"
    add name=autopvc_add_ipoa index=6 command="atm ifattach intf _auto_$1_$2_atm"
    add name=autopvc_add_ipoa index=7 command="ip ifadd intf _auto_$1_$2 dest _auto_$1_$2_atm dynamic enabled"
    add name=autopvc_add_ipoa index=8 command="ip ifattach intf _auto_$1_$2"
    add name=autopvc_delete_ipoa index=0 command="ip ifdetach intf _auto_$1_$2"
    add name=autopvc_delete_ipoa index=1 command="ip ifdelete intf _auto_$1_$2"
    add name=autopvc_delete_ipoa index=2 command="atm ifdetach intf _auto_$1_$2_atm"
    add name=autopvc_delete_ipoa index=3 command="atm ifdelete intf _auto_$1_$2_atm"
    add name=autopvc_delete_ipoa index=4 command="atm phonebook delete name _auto_$1_$2"
    add name=autopvc_delete_ipoa index=5 command="atm qosbook delete name _auto_$1_$2"
    add name=autopvc_delete_ipoa index=6 command="atm qosbook ctddelete name _auto_$1_$2_tx"
    add name=autopvc_delete_ipoa index=7 command="atm qosbook ctddelete name _auto_$1_$2_rx"
    add name=autopvc_add_ethoa index=0 command="atm qosbook ctdadd name _auto_$1_$2_tx conformance $3 peakrate $4 sustrate $5 maxburst $6 minrate $7 maxframe $8 celldelay $9 realtime $10 dynamic enabled"
    add name=autopvc_add_ethoa index=1 command="atm qosbook ctdadd name _auto_$1_$2_rx conformance $11 peakrate $12 sustrate $13 maxburst $14 minrate $15 maxframe $16 celldelay $17 realtime $18 dynamic enabled"
    add name=autopvc_add_ethoa index=2 command="atm qosbook add name _auto_$1_$2 txctd _auto_$1_$2_tx rxctd _auto_$1_$2_rx dynamic enabled"
    add name=autopvc_add_ethoa index=3 command="atm phonebook add name _auto_$1_$2 addr $1.$2 dynamic enabled maxFwdCPCS_PDU $21 maxBwdCPCS_PDU $22"
    add name=autopvc_add_ethoa index=4 command="atm ifadd intf _auto_$1_$2_atm dest _auto_$1_$2 dynamic enabled"
    add name=autopvc_add_ethoa index=5 command="atm ifconfig intf _auto_$1_$2_atm qos _auto_$1_$2 encaps $19 fcs $20 ulp mac"
    add name=autopvc_add_ethoa index=6 command="atm ifattach intf _auto_$1_$2_atm"
    add name=autopvc_add_ethoa index=7 command="eth ifadd intf _auto_$1_$2_eth dest _auto_$1_$2_atm dynamic enabled"
    add name=autopvc_add_ethoa index=8 command="eth ifattach intf _auto_$1_$2_eth"
    add name=autopvc_add_ethoa index=9 command="ip ifadd intf _auto_$1_$2 dest _auto_$1_$2_eth dynamic enabled"
    add name=autopvc_add_ethoa index=10 command="ip ifattach intf _auto_$1_$2"
    add name=autopvc_delete_ethoa index=0 command="ip ifdetach intf _auto_$1_$2"
    add name=autopvc_delete_ethoa index=1 command="ip ifdelete intf _auto_$1_$2"
    add name=autopvc_delete_ethoa index=2 command="eth ifdetach intf _auto_$1_$2_eth"
    add name=autopvc_delete_ethoa index=3 command="eth ifdelete intf _auto_$1_$2_eth"
    add name=autopvc_delete_ethoa index=4 command="atm ifdetach intf _auto_$1_$2_atm"
    add name=autopvc_delete_ethoa index=5 command="atm ifdelete intf _auto_$1_$2_atm"
    add name=autopvc_delete_ethoa index=6 command="atm phonebook delete name _auto_$1_$2"
    add name=autopvc_delete_ethoa index=7 command="atm qosbook delete name _auto_$1_$2"
    add name=autopvc_delete_ethoa index=8 command="atm qosbook ctddelete name _auto_$1_$2_tx"
    add name=autopvc_delete_ethoa index=9 command="atm qosbook ctddelete name _auto_$1_$2_rx"
    add name=autopvc_add_pppoa index=0 command="atm qosbook ctdadd name _auto_$1_$2_tx conformance $3 peakrate $4 sustrate $5 maxburst $6 minrate $7 maxframe $8 celldelay $9 realtime $10 dynamic enabled"
    add name=autopvc_add_pppoa index=1 command="atm qosbook ctdadd name _auto_$1_$2_rx conformance $11 peakrate $12 sustrate $13 maxburst $14 minrate $15 maxframe $16 celldelay $17 realtime $18 dynamic enabled"
    add name=autopvc_add_pppoa index=2 command="atm qosbook add name _auto_$1_$2 txctd _auto_$1_$2_tx rxctd _auto_$1_$2_rx dynamic enabled"
    add name=autopvc_add_pppoa index=3 command="atm phonebook add name _auto_$1_$2 addr $1.$2 dynamic enabled maxFwdCPCS_PDU $21 maxBwdCPCS_PDU $22"
    add name=autopvc_add_pppoa index=4 command="atm ifadd intf _auto_$1_$2_atm dest _auto_$1_$2 dynamic enabled"
    add name=autopvc_add_pppoa index=5 command="atm ifconfig intf _auto_$1_$2_atm qos _auto_$1_$2 encaps $19 fcs $20 ulp ppp"
    add name=autopvc_add_pppoa index=6 command="atm ifattach intf _auto_$1_$2_atm"
    add name=autopvc_add_pppoa index=7 command="ppp ifadd intf _auto_$1_$2 dest _auto_$1_$2_atm dynamic enabled"
    add name=autopvc_add_pppoa index=8 command="ppp ifattach intf _auto_$1_$2"
    add name=autopvc_add_pppoa index=9 command="nat ifconfig intf _auto_$1_$2 translation enabled"
    add name=autopvc_delete_pppoa index=0 command="ppp ifdetach intf _auto_$1_$2"
    add name=autopvc_delete_pppoa index=1 command="ppp ifdelete intf _auto_$1_$2"
    add name=autopvc_delete_pppoa index=2 command="atm ifdetach intf _auto_$1_$2_atm"
    add name=autopvc_delete_pppoa index=3 command="atm ifdelete intf _auto_$1_$2_atm"
    add name=autopvc_delete_pppoa index=4 command="atm phonebook delete name _auto_$1_$2"
    add name=autopvc_delete_pppoa index=5 command="atm qosbook delete name _auto_$1_$2"
    add name=autopvc_delete_pppoa index=6 command="atm qosbook ctddelete name _auto_$1_$2_tx"
    add name=autopvc_delete_pppoa index=7 command="atm qosbook ctddelete name _auto_$1_$2_rx"
    add name=autopvc_add_pppoe index=0 command="atm qosbook ctdadd name _auto_$1_$2_tx conformance $3 peakrate $4 sustrate $5 maxburst $6 minrate $7 maxframe $8 celldelay $9 realtime $10 dynamic enabled"
    add name=autopvc_add_pppoe index=1 command="atm qosbook ctdadd name _auto_$1_$2_rx conformance $11 peakrate $12 sustrate $13 maxburst $14 minrate $15 maxframe $16 celldelay $17 realtime $18 dynamic enabled"
    add name=autopvc_add_pppoe index=2 command="atm qosbook add name _auto_$1_$2 txctd _auto_$1_$2_tx rxctd _auto_$1_$2_rx dynamic enabled"
    add name=autopvc_add_pppoe index=3 command="atm phonebook add name _auto_$1_$2 addr $1.$2 dynamic enabled maxFwdCPCS_PDU $21 maxBwdCPCS_PDU $22"
    add name=autopvc_add_pppoe index=4 command="atm ifadd intf _auto_$1_$2_atm dest _auto_$1_$2 dynamic enabled"
    add name=autopvc_add_pppoe index=5 command="atm ifconfig intf _auto_$1_$2_atm qos _auto_$1_$2 encaps $19 fcs $20 ulp mac"
    add name=autopvc_add_pppoe index=6 command="atm ifattach intf _auto_$1_$2_atm"
    add name=autopvc_add_pppoe index=7 command="eth ifadd intf _auto_$1_$2_eth dest _auto_$1_$2_atm dynamic enabled"
    add name=autopvc_add_pppoe index=8 command="eth ifattach intf _auto_$1_$2_eth"
    add name=autopvc_add_pppoe index=9 command="ppp ifadd intf _auto_$1_$2 dest _auto_$1_$2_eth dynamic enabled"
    add name=autopvc_add_pppoe index=10 command="ppp ifattach intf _auto_$1_$2"
    add name=autopvc_add_pppoe index=11 command="nat ifconfig intf _auto_$1_$2 translation enabled"
    add name=autopvc_delete_pppoe index=0 command="ppp ifdetach intf _auto_$1_$2"
    add name=autopvc_delete_pppoe index=1 command="ppp ifdelete intf _auto_$1_$2"
    add name=autopvc_delete_pppoe index=2 command="eth ifdetach intf _auto_$1_$2_eth"
    add name=autopvc_delete_pppoe index=3 command="eth ifdelete intf _auto_$1_$2_eth"
    add name=autopvc_delete_pppoe index=4 command="atm ifdetach intf _auto_$1_$2_atm"
    add name=autopvc_delete_pppoe index=5 command="atm ifdelete intf _auto_$1_$2_atm"
    add name=autopvc_delete_pppoe index=6 command="atm phonebook delete name _auto_$1_$2"
    add name=autopvc_delete_pppoe index=7 command="atm qosbook delete name _auto_$1_$2"
    add name=autopvc_delete_pppoe index=8 command="atm qosbook ctddelete name _auto_$1_$2_tx"
    add name=autopvc_delete_pppoe index=9 command="atm qosbook ctddelete name _auto_$1_$2_rx"
    add name=autopvc_change_qos index=0 command="atm ifconfig intf $1 qos $2"
    add name=wlbrintfadd index=0 command="eth bridge ifadd intf WL_$1_$2 dynamic enabled"
    add name=wlbrintfadd index=1 command="eth bridge ifconfig intf WL_$1_$2 dest wl_ssid$1_$2"
    add name=wlbrintfadd index=2 command="eth bridge ifattach intf WL_$1_$2"
    add name=wlbrintfdel index=0 command="eth bridge ifdetach intf WL_$1_$2"
    add name=wlbrintfdel index=1 command="eth bridge ifdelete intf WL_$1_$2"

    [ env.ini ]
    set var=CONF_COND_ENCRYPT value=enabled
    set var=CONF_REGION value=UK
    set var=CONF_PROVIDER value=O2BB
    set var=CONF_DESCRIPTION value="O2 Default Routed PPP/IPoEoA connection"
    set var=HOST_SETUP value=auto
    set var=HOST_LANGUAGE value=en
    set var=CONF_VERSION value=\"\"
    set var=COLUMNS value=80
    set var=ROWS value=24
    set var=SESSIONTIMEOUT value=120
    set var=CONF_SERVICE value="O2 Standard"
    set var=CWMPUSER value=${_OUI}-${_PROD_SERIAL_NBR}
    set var=O2Postfix value=F150BF
    set var=SSID_O2 value=O2wireless${O2Postfix}
    set var=SEPARATOR value=.
    set var=BUILDSUFFIX value=${SEPARATOR}${_CUSTOVARIANT}
    set var=CONF_DATE value="Configuration modified manually"
    set var=ACS_URL value=http://acs.broadband.o2.co.uk:7547/ACS-server/ACS
    set var=CONF_TPVERSION value=2.0.0

    [ wizard.ini ]

    [ phone.ini ]
    add name=pvc_Internet addr=0*38
    add name=llu_Internet addr=0*101

    [ ipqos.ini ]
    config dest=pvc_Internet state=enabled maxbytes=128
    config dest=llu_Internet state=enabled maxbytes=128
    queue config dest=pvc_Internet queue=0 maxbytes=64 hold=2000 loprio=0 hiprio=5
    queue config dest=pvc_Internet queue=1 ackfiltering=enabled maxpackets=40 maxbytes=100 hold=2000 loprio=6 hiprio=7
    queue config dest=pvc_Internet queue=2 hold=2000 loprio=8 hiprio=9
    queue config dest=pvc_Internet queue=3 hold=2000 loprio=10 hiprio=11
    queue config dest=pvc_Internet queue=4 hold=2000 loprio=12 hiprio=13
    queue config dest=pvc_Internet queue=5 maxpackets=30 maxbytes=12 hold=2000 loprio=14 hiprio=15
    queue config dest=llu_Internet queue=0 maxbytes=64 hold=2000 loprio=0 hiprio=5
    queue config dest=llu_Internet queue=1 ackfiltering=enabled maxpackets=40 maxbytes=100 hold=2000 loprio=6 hiprio=7
    queue config dest=llu_Internet queue=2 hold=2000 loprio=8 hiprio=9
    queue config dest=llu_Internet queue=3 hold=2000 loprio=10 hiprio=11
    queue config dest=llu_Internet queue=4 hold=2000 loprio=12 hiprio=13
    queue config dest=llu_Internet queue=5 maxpackets=30 maxbytes=12 hold=2000 loprio=14 hiprio=15

    [ qos.ini ]
    config format=bytes
    ctdadd name=default conformance=UBR
    add name=default txctd=default rxctd=default

    [ atm.ini ]
    ifadd intf=atm_llu
    ifconfig intf=atm_llu dest=llu_Internet ulp=mac
    ifattach intf=atm_llu
    debug traceconfig len=100

    [ oam.ini ]
    config clp=1 loopbackid=6a6a6a6a6a6a6a6a6a6a6a6a6a6a6a6a
    modify port=dsl0 blocking=enabled
    modify port=dsl1 blocking=enabled
    modify port=atm2 blocking=enabled
    modify port=atm3 blocking=enabled
    modify port=aal5 blocking=enabled
    modify port=atm5 blocking=enabled

    [ wireless.ini ]
    <...>

    [ vlan_res.ini ]

    [ vlan_priomap.ini ]
    config entry=prio_0_7_2vlan priomap=1,1,2,2,0,0,3,3
    config entry=prio_8_15_2vlan priomap=4,4,5,5,5,5,6,7
    config entry=prio_0_7_2de priomap=0,0,0,0,0,0,0,0
    config entry=prio_8_15_2de priomap=0,0,0,0,0,0,0,0
    config entry=vlan2prio_de_0 priomap=4,0,2,6,8,10,14,15
    config entry=vlan2prio_de_1 priomap=4,0,2,6,8,10,14,15

    [ bridge.ini ]
    ifadd brname=bridge intf=ethport2 dest=ethif2 logging=disabled
    ifadd brname=bridge intf=ethport3 dest=ethif3 logging=disabled
    ifadd brname=bridge intf=virt dest=ethif5 logging=disabled
    ifadd brname=bridge intf=WLAN dest=wlif1 logging=disabled
    ifconfig brname=bridge intf=ethport1 wan=disabled logging=disabled
    ifconfig brname=bridge intf=ethport2 wan=disabled logging=disabled
    ifconfig brname=bridge intf=ethport3 wan=disabled logging=disabled
    ifconfig brname=bridge intf=virt wan=disabled logging=disabled
    ifconfig brname=bridge intf=WLAN wan=disabled logging=disabled
    ifattach brname=bridge intf=ethport2 logging=disabled
    ifattach brname=bridge intf=ethport3 logging=disabled
    ifattach brname=bridge intf=virt logging=disabled
    ifattach brname=bridge intf=WLAN logging=disabled
    config brname=bridge age=300 filter=no_WAN_broadcast vlan=disabled
    ippriomap brname=bridge type=tos tostable=Default precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=bridge type=tos tostable=MinimizeDelay precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=bridge type=tos tostable=MaximizeThroughput precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=bridge type=tos tostable=MaximizeReliability precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=bridge type=tos tostable=MinimizeCost precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=bridge type=dscp dscpidx=dscp_0_7 precedencemap=4,4,4,4,4,4,4,4
    ippriomap brname=bridge type=dscp dscpidx=dscp_8_15 precedencemap=7,7,7,7,6,6,6,6
    ippriomap brname=bridge type=dscp dscpidx=dscp_16_23 precedencemap=9,9,9,9,8,8,8,8
    ippriomap brname=bridge type=dscp dscpidx=dscp_24_31 precedencemap=11,11,11,11,10,10,10,10
    ippriomap brname=bridge type=dscp dscpidx=dscp_32_39 precedencemap=13,13,13,13,12,12,12,12
    ippriomap brname=bridge type=dscp dscpidx=dscp_40_47 precedencemap=14,14,14,14,14,14,14,14
    ippriomap brname=bridge type=dscp dscpidx=dscp_48_55 precedencemap=15,15,15,15,15,15,15,15
    ippriomap brname=bridge type=dscp dscpidx=dscp_56_63 precedencemap=15,15,15,15,15,15,15,15
    add brname=direct_bridge
    ifadd brname=direct_bridge intf=ethport4 dest=ethif4 logging=disabled
    ifadd brname=direct_bridge intf=atm
    ifconfig brname=direct_bridge intf=ethport4 wan=disabled logging=disabled
    ifconfig brname=direct_bridge intf=atm dest=atm_llu wan=enabled
    ifattach brname=direct_bridge intf=atm
    ifattach brname=direct_bridge intf=ethport4 logging=disabled
    config brname=direct_bridge age=300 filter=no_WAN_broadcast vlan=disabled
    ippriomap brname=direct_bridge type=tos tostable=Default precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=direct_bridge type=tos tostable=MinimizeDelay precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=direct_bridge type=tos tostable=MaximizeThroughput precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=direct_bridge type=tos tostable=MaximizeReliability precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=direct_bridge type=tos tostable=MinimizeCost precedencemap=4,7,9,11,13,14,15,15
    ippriomap brname=direct_bridge type=dscp dscpidx=dscp_0_7 precedencemap=4,4,4,4,4,4,4,4
    ippriomap brname=direct_bridge type=dscp dscpidx=dscp_8_15 precedencemap=7,7,7,7,6,6,6,6
    ippriomap brname=direct_bridge type=dscp dscpidx=dscp_16_23 precedencemap=9,9,9,9,8,8,8,8
    ippriomap brname=direct_bridge type=dscp dscpidx=dscp_24_31 precedencemap=11,11,11,11,10,10,10,10
    ippriomap brname=direct_bridge type=dscp dscpidx=dscp_32_39 precedencemap=13,13,13,13,12,12,12,12
    ippriomap brname=direct_bridge type=dscp dscpidx=dscp_40_47 precedencemap=14,14,14,14,14,14,14,14
    ippriomap brname=direct_bridge type=dscp dscpidx=dscp_48_55 precedencemap=15,15,15,15,15,15,15,15
    ippriomap brname=direct_bridge type=dscp dscpidx=dscp_56_63 precedencemap=15,15,15,15,15,15,15,15

    [ filter_operand.ini ]

    [ filter_template.ini ]

    [ filter_sync.ini ]
    loadobjects dmtree=atomic path=Bridge
    loadobjects dmtree=atomic path=Interface

    [ filter_brfilter.ini ]

    [ vlanbridge.ini ]

    [ bridgevlan.ini ]
    ifconfig brname=direct_bridge intf=OBC1 vlan=1
    ifconfig brname=direct_bridge intf=ethport4 vlan=1
    ifconfig brname=direct_bridge intf=atm vlan=1

    [ vlanbridge_del.ini ]

    [ vlanbridgerule.ini ]

    [ bridgeintfxtratag.ini ]

    [ bridgeunknownvlan.ini ]

    [ dvm_res.ini ]
    config timeout=90

    [ igmpsnooping.ini ]
    ifconfig brname=bridge intf=OBC portmode=Auto fastleave=enabled exptrack=disabled mrdp=enabled rgmp=disabled
    ifconfig brname=bridge intf=ethport1 portmode=Auto fastleave=disabled exptrack=disabled mrdp=enabled rgmp=disabled
    ifconfig brname=bridge intf=ethport2 portmode=Auto fastleave=disabled exptrack=disabled mrdp=enabled rgmp=disabled
    ifconfig brname=bridge intf=ethport3 portmode=Auto fastleave=disabled exptrack=disabled mrdp=enabled rgmp=disabled
    ifconfig brname=bridge intf=virt portmode=Auto fastleave=disabled exptrack=disabled mrdp=enabled rgmp=disabled
    ifconfig brname=bridge intf=WLAN portmode=Auto fastleave=disabled exptrack=disabled mrdp=enabled rgmp=disabled
    config brname=bridge state=disabled floodrp=disabled floodmcast=disabled
    config brname=direct_bridge state=disabled floodrp=disabled floodmcast=disabled

    [ eth.ini ]

    [ pptp.ini ]

    [ ppprelay.ini ]

    [ dhcspool.ini ]
    pool add name=LAN_private
    pool add name=LAN_Virt

    [ label.ini ]
    add name=Blank
    add name=DSCP
    add name=Interactive
    add name=Management
    add name=Video
    add name=VoIP-RTP
    add name=VoIP-Signal
    add name=default
    modify name=Blank
    modify name=DSCP classification=overwrite defclass=dscp ackclass=prioritize
    modify name=Interactive classification=increase defclass=8 ackclass=6
    modify name=Management classification=increase defclass=12 ackclass=12
    modify name=Video classification=increase defclass=10 ackclass=10 bidirectional=enabled
    modify name=VoIP-RTP classification=overwrite defclass=14 ackclass=14 bidirectional=enabled tosmarking=enabled
    modify name=VoIP-Signal classification=overwrite defclass=12 ackclass=12 bidirectional=enabled tosmarking=enabled
    modify name=default classification=increase defclass=default ackclass=prioritize

    [ ppp.ini ]
    <...>

    [ ip.ini ]
    ifadd intf=LocalNetwork dest=bridge
    ifconfig intf=loop mtu=65535 group=local symmetric=enabled
    ifconfig intf=LocalNetwork mtu=1500 group=lan linksensing=disabled primary=enabled
    ifattach intf=LocalNetwork
    config forwarding=enabled redirects=enabled netbroadcasts=disabled ttl=64 fraglimit=64 defragmode=enabled addrcheck=dynamic mssclamping=enabled acceleration=enabled
    config checkoptions=enabled
    config natloopback=enabled
    config arpclass=12
    config arpcachetimeout=900
    ipadd intf=LocalNetwork addr=<...> addroute=enabled
    rtadd dst=255.255.255.255/32 gateway=127.0.0.1

    [ autoip.ini ]
    debug traceconfig state=disabled

    [ ipqosmeter.ini ]

    [ igmh.ini ]
    config requirera=disabled

    [ mcast.ini ]

    [ diagnostics.ini ]
    config pingtimeout=1000 pingpacketsize=32

    [ dnsc.ini ]
    config timeout=5 retry=4 search=enabled trace=disabled
    dnsadd addr=127.0.0.1 port=53

    [ dnss.ini ]
    config domain=lan timeout=15 suppress=0 state=enabled trace=disabled syslog=disabled WANDownSpoofing=enabled WDSpoofedIP=198.18.1.0
    host add name=O2wirelessbox addr=0.0.0.0 ttl=1200
    host add name=dsldevice addr=0.0.0.0 ttl=1200

    [ dhcrule.ini ]
    debug traceconfig state=disabled

    [ dhcs.ini ]
    <...>

    [ dhcr.ini ]
    ifconfig intf=LocalNetwork relay=enabled
    add name=LocalNetwork_to_127.0.0.1
    modify name=LocalNetwork_to_127.0.0.1 addr=127.0.0.1 intf=LocalNetwork

    [ dhcc.ini ]
    debug traceconfig state=disabled

    [ dhcsp.ini ]
    debug traceconfig state=disabled
    config state=disabled

    [ dyndns.ini ]
    service modify name=dyndns server=members.dyndns.org port=www-http request=/nic/update updateinterval=2097120 retryinterval=30 max_retry=3
    service modify name=statdns server=members.dyndns.org port=www-http request=/nic/update retryinterval=30 max_retry=3
    service modify name=custom server=members.dyndns.org port=www-http request=/nic/update retryinterval=30 max_retry=3
    service modify name=No-IP server=dynupdate.no-ip.com port=www-http request=/ducupdate.php updateinterval=86400 retryinterval=30 max_retry=3
    service modify name=DtDNS server=dtdns.com port=www-http request=/api/autodns.cfm updateinterval=86400 retryinterval=30 max_retry=3
    service modify name=gnudip port=www-http

    [ expr.ini ]
    add name=wan type=intf intfgroup=wan
    add name=local type=intf intfgroup=local
    add name=lan type=intf intfgroup=lan
    add name=tunnel type=intf intfgroup=tunnel
    add name=dmz type=intf intfgroup=dmz
    add name=guest type=intf intfgroup=guest
    add name=private type=ip addr=10.0.0.0/8 mask=0
    add name=private type=ip addr=172.[16-31].*.* mask=0
    add name=private type=ip addr=192.168.1.0/24 mask=0
    add name=ssdp_ip type=ip addr=239.255.255.250 mask=0
    add name=mdap_ip type=ip addr=224.0.0.103 mask=0
    add name=icmp type=serv proto=icmp
    add name=igmp type=serv proto=igmp
    add name=ftp type=serv proto=tcp dstport=ftp
    add name=ftp type=serv proto=tcp dstport=21800 dstportend=21805
    add name=telnet type=serv proto=tcp dstport=telnet
    add name=http type=serv proto=tcp dstport=www-http
    add name=httpproxy type=serv proto=tcp dstport=httpproxy
    add name=https type=serv proto=tcp dstport=443
    add name=RPC type=serv proto=tcp dstport=135
    add name=NBT type=serv proto=udp dstport=netbios-ns
    add name=NBT type=serv proto=udp dstport=netbios-dgm
    add name=NBT type=serv proto=tcp dstport=netbios-ssn
    add name=SMB type=serv proto=tcp dstport=445
    add name=imap type=serv proto=tcp dstport=imap2
    add name=imap3 type=serv proto=tcp dstport=imap3
    add name=imap4-ssl type=serv proto=tcp dstport=585
    add name=imaps type=serv proto=tcp dstport=993
    add name=pop2 type=serv proto=tcp dstport=pop2
    add name=pop3 type=serv proto=tcp dstport=pop3
    add name=pop3s type=serv proto=tcp dstport=995
    add name=smtp type=serv proto=tcp dstport=smtp
    add name=ssh type=serv proto=tcp dstport=22
    add name=dns type=serv proto=tcp dstport=dns
    add name=dns type=serv proto=udp dstport=dns
    add name=nntp type=serv proto=tcp dstport=nntp
    add name=ipsec type=serv proto=ah
    add name=ipsec type=serv proto=esp
    add name=ipsec type=serv proto=udp dstport=ike
    add name=ipsec type=serv proto=udp dstport=4500
    add name=esp type=serv proto=esp
    add name=ah type=serv proto=ah
    add name=ike type=serv proto=udp dstport=ike
    add name=DiffServ type=serv dscp=!cs0
    add name=sip type=serv proto=udp dstport=sip
    add name=sip type=serv proto=tcp dstport=sip
    add name=h323 type=serv proto=tcp dstport=h323
    add name=h323 type=serv proto=udp dstport=h323
    add name=h323 type=serv proto=tcp dstport=1718
    add name=h323 type=serv proto=udp dstport=1718
    add name=h323 type=serv proto=tcp dstport=1719
    add name=h323 type=serv proto=udp dstport=1719
    add name=dhcp type=serv proto=udp dstport=bootpc
    add name=dhcp type=serv proto=udp dstport=bootps
    add name=rtsp type=serv proto=udp dstport=rtsp
    add name=rtsp type=serv proto=tcp dstport=rtsp
    add name=ssdp_serv type=serv proto=udp dstport=1900
    add name=mdap_serv type=serv proto=udp dstport=3235
    add name=syslog type=serv proto=udp dstport=syslog

    [ labelrule.ini ]
    chain add chain=rt_user_labels
    chain add chain=rt_default_labels
    chain add chain=qos_user_labels
    chain add chain=qos_default_labels
    rule add chain=qos_default_labels index=1 serv=h323 log=disabled state=enabled label=VoIP-Signal
    rule add chain=qos_default_labels index=2 serv=sip log=disabled state=enabled label=VoIP-Signal
    rule add chain=qos_default_labels index=3 serv=ah log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=4 serv=esp log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=5 serv=http log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=6 serv=httpproxy log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=7 serv=https log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=8 serv=imap log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=9 serv=imap3 log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=10 serv=imap4-ssl log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=11 serv=imaps log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=12 serv=pop2 log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=13 serv=pop3 log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=14 serv=pop3s log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=15 serv=smtp log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=16 serv=telnet log=disabled state=enabled label=Interactive
    rule add chain=qos_default_labels index=17 serv=dns log=disabled state=enabled label=Management
    rule add chain=qos_default_labels index=18 serv=icmp log=disabled state=enabled label=Management
    rule add chain=qos_default_labels index=19 serv=ike log=disabled state=enabled label=Management
    rule add chain=qos_default_labels index=20 serv=igmp log=disabled state=enabled label=Video
    rule add chain=qos_default_labels index=21 serv=rtsp log=disabled state=enabled label=Video
    rule add chain=qos_default_labels index=22 serv=DiffServ log=disabled state=enabled label=DSCP
    rule add chain=qos_default_labels index=23 name=default log=disabled state=enabled label=default

    [ ids.ini ]
    config state=enabled trace=disabled
    signature modify signature=spoofed_packet state=disabled

    [ ids_threshold.ini ]
    modify index=1 window=1 limit=10 scaling=disabled
    modify index=2 window=20 limit=20 scaling=enabled
    modify index=3 window=2 limit=100 scaling=disabled
    modify index=4 window=1 limit=200 scaling=disabled
    modify index=5 window=1 limit=200 scaling=disabled
    modify index=6 window=1 limit=200 scaling=disabled
    modify index=7 window=1 limit=200 scaling=disabled

    [ cwmp.ini ]
    <...>

    [ syslog.ini ]
    config activate=disabled timeout=0 format=welf
    bootup

    [ grp.ini ]

    [ rip.ini ]
    config state=disabled

    [ nat.ini ]
    ifconfig intf=O2_ADSL translation=enabled
    config

    [ igmp.ini ]
    config state=enabled qi=125 qri=10 lmqi=1 rv=2 advinter=20 initadvinter=2 initadvcount=3 requirera=disabled localgroup=disabled
    ifconfig intf=LocalNetwork state=downstream version=IGMPv3 fastleave=disabled exptrack=disabled mrd=disabled
    ifconfig intf=O2_ADSL state=inactive

    [ ipqosef.ini ]

    [ connection.ini ]
    appconfig application=IP6TO4 trace=disabled
    appconfig application=PPTP trace=disabled timeout=300
    appconfig application=ESP timeout=900
    appconfig application=IKE trace=disabled timeout=900 floating=enabled
    appconfig application=SIP trace=disabled timeout=600 childqos=VoIP-RTP
    appconfig application=SIP childqos=VoIP-RTP snooping=enabled translate-predict=enabled
    appconfig application=JABBER trace=disabled timeout=120 snooping=enabled translate-predict=enabled
    appconfig application=CU/SeeMe trace=disabled snooping=enabled translate-predict=enabled
    appconfig application=RAUDIO(PNA) trace=disabled snooping=enabled translate-predict=enabled
    appconfig application=RTSP trace=disabled timeout=120 childqos=Video snooping=enabled translate-predict=enabled
    appconfig application=ILS timeout=300 snooping=enabled translate-predict=enabled
    appconfig application=H245 timeout=300 snooping=enabled translate-predict=enabled
    appconfig application=H323 trace=disabled snooping=enabled translate-predict=enabled
    appconfig application=IRC trace=disabled timeout=300 snooping=enabled translate-predict=enabled
    appconfig application=DHCP trace=disabled timeout=60 snooping=enabled translate-predict=enabled
    appconfig application=GAME(UDP) trace=disabled timeout=60 snooping=enabled translate-predict=enabled
    appconfig application=CONE(UDP) trace=disabled timeout=300 snooping=enabled translate-predict=enabled
    appconfig application=LOOSE(UDP) trace=disabled timeout=300 snooping=enabled translate-predict=enabled
    appconfig application=SNMP_TRAP trace=enabled snooping=enabled translate-predict=enabled
    appconfig application=FTP trace=disabled childqos=None snooping=enabled translate-predict=enabled
    bind application=IP6TO4
    bind application=PPTP port=1723-1723
    bind application=ESP
    bind application=IKE port=500-500
    bind application=SIP port=5060-5060
    bind application=CU/SeeMe port=7648-7648
    bind application=RAUDIO(PNA) port=7070-7070
    bind application=RTSP port=554-554
    bind application=ILS port=389-389
    bind application=ILS port=1002-1002
    bind application=H323 port=1720-1720
    bind application=IRC port=6660-6669
    bind application=FTP port=21-21
    bind application=JABBER port=5222-5222
    bind application=JABBER port=15222-15222
    bind application=DHCP port=67-67
    bind application=CONE(UDP) port=69-69
    bind application=CONE(UDP) port=88-88
    bind application=CONE(UDP) port=3074-3074
    bind application=CONE(UDP) port=3478-3479
    config configchangemode=immediate probes=disabled
    debug trace=disabled
    timerconfig timer=tcpidle value=900
    timerconfig timer=tcpneg value=120
    timerconfig timer=tcpkill value=3600
    timerconfig timer=udpidle value=1
    timerconfig timer=udpkill value=124
    timerconfig timer=icmpkill value=60
    timerconfig timer=ipidle value=60
    timerconfig timer=ipkill value=0
    flow add name=Blank_Flow
    flow qoslabeladd flow=Blank_Flow qoslabel=Blank
    reserve flow=Blank_Flow amount=20

    [ switch.ini ]
    group delete group=0 port=4
    mirror capture port=1
    qos config state=disabled nbrOfQueues=0 realtime=disabled threshold=9
    storm ifconfig port=1 state=disabled rate=100 burstsize=2 broadcast=disabled multicast=disabled unknown=disabled
    storm ifconfig port=2 state=disabled rate=100 burstsize=2 broadcast=disabled multicast=disabled unknown=disabled
    storm ifconfig port=3 state=disabled rate=100 burstsize=2 broadcast=disabled multicast=disabled unknown=disabled
    storm ifconfig port=4 state=disabled rate=100 burstsize=2 broadcast=disabled multicast=disabled unknown=disabled

    [ upnp.ini ]
    config maxage=1800 writemode=full safenat=disabled upnpautosave=disabled dslfautosave=disabled autosavedelay=40 onlydefault=enabled

    [ tls.ini ]
    acs-client config state=enabled auth-serv=enabled valid-date=disabled valid-domain=disabled
    https-server config state=disabled auth-client=disabled valid-date=disabled valid-domain=disabled

    [ system.ini ]
    settime timezone=+00:00 daylightsaving=enabled gtzn=(UTC)
    dst mode=Relative startdate=24/01/2000 starttime=00:00:00 enddate=24/01/2000 endtime=00:16:40 startweekday=Sunday starthour=0 startweek=5 startmonth=3 endweekday=Sunday endhour=0 endweek=5 endmonth=10
    config upnp=enabled tr64=enabled tr64auth=disabled mdap=enabled resetbutton=enabled
    config autosave=enabled autosavedelay=10
    config WANMode=ADSL WANEthPort=""
    locale dec_symbol=. group_symbol=, date_separator=- date_format=ddmmyyyy time_format=iso datetime_format=date+time duration_format=dhmmss

    [ system_debug.ini ]
    autosave trace=disabled

    [ system_ipc.ini ]
    config prio-level=9

    [ dsd.ini ]
    intercept config WDSpoofedIP=198.18.1.1 servertimeout=10 connecterrorurl=/cgi/b/ic/connect/ categoryerrorurl=/cgi/b/ic/connect/ monitorintercepturl=/cgi/b/ic/connect/ unauthorizedrequrl=/cgi/b/ic/blocked/ imageredirect=enabled imageredirecturl=/images/spacer.gif alwaysuseip=disabled
    urlfilter config state=disabled blockproxy=disabled blockipaddress=disabled blockobscuredip=disabled defaultaction=accept
    syslog config syslog=unauthorized
    debug config turbomode=disabled
    debug proxy state=disabled dest=0.0.0.0 port=undefined
    debug recycling state=enabled interval=5 httpidle=1 otheridle=12
    config state=disabled

    [ webfilter.ini ]
    config serverunreachable=block-all uncategorized=block license=none ticket="" sessionkey=""
    server config retries=3 servertimeout=2 timeoutmultiplier=2 renewfrequency=23 useproxy=disabled
    standard config stdmax=0 validcatmask=000000000000000000000000
    professional config validcatmask=000000000000000000000000
    config state=disabled

    [ hostmgr.ini ]
    <...>

    [ wansensing.ini ]
    mode add name=NONE maininterval=5 scriptname=O2-auto-sensing-script
    mode add name=PPP maininterval=60 scriptname=ppp-script
    mode add name=MER maininterval=60 scriptname=mer-script
    requestmode mode=MER
    config state=enabled errorinterval=0 errorscript=O2-error-script

    [ mlp.ini ]

    [ mlpuser.ini ]
    <...>

    [ argroupmember.ini ]

    [ tod.ini ]
    :mbus debug loadobjects dmtree atomic path Hosts.Host
    config acchain=""
    config state=enabled

    [ system_raccess.ini ]
    config state=disabled secure=enabled port=8340 timeout=20 mode=Temporary ipintf="" randompassword=enabled randomport=disabled group="" user="" todschedule=""

    [ statecheck.ini ]

    [ ptrace.ini ]

    [ service.ini ]
    add name="AIM Talk" mode=client
    add name=BearShare mode=server
    add name=BitTorrent mode=client
    add name="Checkpoint FW1 VPN" mode=server
    add name="Counter Strike" mode=server
    add name="DirectX 7" mode=server
    add name="DirectX 8" mode=server
    add name="DirectX 9" mode=server
    add name=eMule mode=server
    add name="FTP Server" mode=server
    add name="Gamespy Arcade" mode=server
    add name="HTTP Server (World Wide Web)" mode=server
    add name="HTTPS Server" mode=server
    add name=iMesh mode=server
    add name=KaZaA mode=server
    add name="Mail Server (SMTP)" mode=server
    add name="Microsoft Remote Desktop" mode=server
    add name="MSN Game Zone" mode=server
    add name="MSN Game Zone (DX)" mode=server
    add name="NNTP Server" mode=server
    add name="PPTP Server" mode=server
    add name="PS3 Remote Play" mode=server
    add name="Secure Shell Server (SSH)" mode=server
    add name="Steam Games" mode=server
    add name="Telnet Server" mode=server
    add name=VNC mode=server
    add name="Xbox Live" mode=server
    rule add name="AIM Talk" protocol=tcp portrange=5190-5190 triggerport=4099 triggerprotocol=tcp
    rule add name=BearShare protocol=tcp portrange=6346-6346
    rule add name=BitTorrent protocol=tcp portrange=6881-6889
    rule add name="Checkpoint FW1 VPN" protocol=tcp portrange=2599-2599
    rule add name="Checkpoint FW1 VPN" protocol=udp portrange=2599-2599
    rule add name="Counter Strike" protocol=udp portrange=1200-1200
    rule add name="Counter Strike" protocol=udp portrange=27000-27015
    rule add name="Counter Strike" protocol=tcp portrange=27030-27039
    rule add name="DirectX 7" protocol=udp portrange=2302-2400
    rule add name="DirectX 7" protocol=udp portrange=47624-47624
    rule add name="DirectX 8" protocol=udp portrange=2302-2400
    rule add name="DirectX 8" protocol=udp portrange=6073-6073
    rule add name="DirectX 9" protocol=udp portrange=2302-2400
    rule add name="DirectX 9" protocol=udp portrange=6073-6073
    rule add name=eMule protocol=tcp portrange=4662-4662
    rule add name=eMule protocol=udp portrange=4672-4672
    rule add name="FTP Server" protocol=tcp portrange=21-21
    rule add name="Gamespy Arcade" protocol=udp portrange=6500-6500
    rule add name="Gamespy Arcade" protocol=udp portrange=6700-6700
    rule add name="Gamespy Arcade" protocol=udp portrange=12300-12300
    rule add name="Gamespy Arcade" protocol=udp portrange=27900-27900
    rule add name="Gamespy Arcade" protocol=tcp portrange=28900-28900
    rule add name="Gamespy Arcade" protocol=udp portrange=23000-23009
    rule add name="HTTP Server (World Wide Web)" protocol=tcp portrange=80-80
    rule add name="HTTPS Server" protocol=tcp portrange=443-443
    rule add name=iMesh protocol=tcp portrange=1214-1214
    rule add name=KaZaA protocol=tcp portrange=1214-1214
    rule add name="Mail Server (SMTP)" protocol=tcp portrange=25-25
    rule add name="Mail Server (SMTP)" protocol=udp portrange=25-25
    rule add name="Microsoft Remote Desktop" protocol=tcp portrange=3389-3389
    rule add name="Microsoft Remote Desktop" protocol=udp portrange=3389-3389
    rule add name="MSN Game Zone" protocol=tcp portrange=6667-6667
    rule add name="MSN Game Zone" protocol=udp portrange=6667-6667
    rule add name="MSN Game Zone" protocol=tcp portrange=28800-29000
    rule add name="MSN Game Zone" protocol=udp portrange=28800-29000
    rule add name="MSN Game Zone (DX)" protocol=tcp portrange=2300-2400
    rule add name="MSN Game Zone (DX)" protocol=udp portrange=2300-2400
    rule add name="MSN Game Zone (DX)" protocol=tcp portrange=47624-47624
    rule add name="MSN Game Zone (DX)" protocol=udp portrange=47624-47624
    rule add name="NNTP Server" protocol=tcp portrange=119-119
    rule add name="NNTP Server" protocol=udp portrange=119-119
    rule add name="PPTP Server" protocol=tcp portrange=1723-1723
    rule add name="Secure Shell Server (SSH)" protocol=tcp portrange=22-22
    rule add name="Steam Games" protocol=tcp portrange=27030-27039
    rule add name="Steam Games" protocol=udp portrange=1200-1200
    rule add name="Steam Games" protocol=udp portrange=27000-27015
    rule add name="Telnet Server" protocol=tcp portrange=23-23
    rule add name=VNC protocol=tcp portrange=5500-5500
    rule add name=VNC protocol=udp portrange=5500-5500
    rule add name=VNC protocol=tcp portrange=5800-5800
    rule add name=VNC protocol=udp portrange=5800-5800
    rule add name=VNC protocol=tcp portrange=5900-5900
    rule add name=VNC protocol=udp portrange=5900-5900
    rule add name="Xbox Live" protocol=udp portrange=88-88
    rule add name="Xbox Live" protocol=tcp portrange=3074-3074
    rule add name="Xbox Live" protocol=udp portrange=3074-3074
    rule add name="PS3 Remote Play" protocol=tcp portrange=9293-9293
    rule add name="PS3 Remote Play" protocol=udp portrange=9293-9293
    assign name="FTP Server" host=192.168.1.253 log=disabled

    [ vfs.ini ]
    upnpavcontrolpoint config state=disabled

    [ fwlevel.ini ]
    add name=BlockAll index=1 readonly=enabled udptrackmode=strict service=disabled proxy=disabled text="Use this Security Level to block all traffic from and to the Internet. Game and Application sharing is not allowed by the firewall."
    add name=Standard index=2 readonly=enabled udptrackmode=loose service=enabled proxy=enabled text="Use this Security Level to allow all outgoing connections and block all incoming traffic. Game and Application sharing is allowed by the firewall."
    add name=Disabled index=3 readonly=enabled udptrackmode=loose service=enabled proxy=enabled text="Disable the firewall. All traffic is allowed to pass through your gateway. Game and Application sharing is allowed by the firewall."
    set name=Standard

    [ firewall.ini ]
    config state=enabled keep=disabled tcpchecks=none udpchecks=enabled icmpchecks=enabled logdefault=disabled logthreshold=enabled tcpwindow=65536
    debug traceconfig tcpchecks=disabled udpchecks=disabled icmpchecks=disabled sink=none forward=none source=none
    rule add chain=source_fire index=1 name=AnyTraffic log=disabled state=enabled action=accept
    rule add chain=forward_level_BlockAll index=1 name=AnyTraffic log=disabled state=enabled action=drop
    rule add chain=forward_level_Standard index=1 name=FromLAN srcintf=lan log=disabled state=enabled action=accept
    rule add chain=forward_level_Disabled index=1 name=AnyTraffic log=disabled state=enabled action=accept

    [ contentsharing.ini ]
    ftp config state=disabled
    cifs config state=enabled workgroup=WORKGROUP name=O2 comment="DSL Gateway"
    upnp config state=enabled friendlyname="O2 Wireless Box"
    upnp radiostation config state=disabled

    [ printersharing.ini ]
    LPD config state=enabled
    LPD queue add name=Printer type=Raw default=yes

    [ servmgr.ini ]
    ifadd name=PPTP group=lan
    ifadd name=HTTP group=lan
    ifadd name=HTTPs group=lan
    ifadd name=FTP group=lan
    ifadd name=TELNET group=lan
    ifadd name=DNS-S group=lan
    ifadd name=MDAP group=lan
    ifadd name=SSDP group=lan
    ifadd name=PING_RESPONDER group=lan
    modify name=Remote-MBus state=disabled
    modify name=PPTP state=enabled
    modify name=SNTP state=enabled
    modify name=SLA_ICMP_PING state=enabled
    modify name=SLA_UDP_PING state=disabled
    modify name=SYSLOG state=disabled
    modify name=HTTP state=enabled
    modify name=HTTPs state=disabled
    modify name=WEBF state=disabled
    modify name=FTP state=enabled
    modify name=TELNET state=enabled
    modify name=RIP state=disabled
    modify name=IGMP-Proxy state=enabled
    modify name=DNS-S state=enabled
    modify name=DNS-C state=enabled
    modify name=DHCP-S state=disabled
    modify name=MDAP state=enabled
    modify name=CWMP-C state=enabled qoslabel=Management
    modify name=CWMP-S state=enabled port=7547
    modify name=SSDP state=enabled
    modify name=IP_COMMANDS state=enabled
    modify name=PING_RESPONDER state=enabled
    mapadd name=HTTP port=www-http
    mapadd name=HTTPs port=443
    mapadd name=HTTPI intf=LocalNetwork port=www-http
    mapadd name=HTTPI intf=LocalNetwork port=1080
    mapadd name=HTTPI intf=LocalNetwork port=httpproxy
    mapadd name=FTP port=ftp
    mapadd name=TELNET port=telnet
    mapadd name=DNS-S port=dns
    mapadd name=MDAP port=3235
    mapadd name=SSDP port=1900

    [ pwr.ini ]
    wlan-pwr-options t-on=5 t-off=10 t-ext=2
    config eco-manager=disabled cpu-microsleep=enabled cpu-lowspeed=disabled usb-controller=enabled wlan-pwrcontrol=enabled
    debug traceconfig state=disabled

    [ mbus.ini ]
    debug traceconfig level=0
    debug commconfig pong-to=1500

    [ kta.ini ]

    [ kti.ini ]

    [ koa.ini ]
    a d="" l=yes

    [ koi.ini ]
    a d="" l=yes

    [ endofarch ]

Troubleshooting
---------------

If things go pear-shaped at any point, you need to get a pen or small
screw-driver and hold in the "Reset" button on the back of your O2 Wireless Box
IV for a minute or two while it is powered on. During this time the power LED
will begin to flash orange. After this, you may have to turn the device off and
on again. The factory defaults should now be restored, including the default
SuperUser password and default wireless and LAN settings. I recommend you backup
your existing configuration options using the "Save or Restore Configuration"
page before following any of these instructions.
