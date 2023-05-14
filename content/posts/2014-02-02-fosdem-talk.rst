..
   Copyright (c) 2012 Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

Conference Talk: Underwater Acoustics to Opkg, via The Yocto Project
====================================================================

:date: 2014-02-02
:tags: necropost, conference-talk, embedded-linux, yocto-project, open-source
:summary:
    This was my first conference talk, presented at FOSDEM 2014.

.. note::
    As this talk was delivered at FOSDEM 2014, the abstract and video are licensed under the
    `Creative Commons Attribution 2.0 Belgium License <http://creativecommons.org/licenses/by/2.0/be/>`__.

Video
-----

.. youtube:: QzsFphJACYc

Abstract
--------

Underwater noise produced by human activities in the ocean is a serious problem
for marine mammals and fish. To produce the data needed to address this problem,
an underwater noise monitoring device (the UDAQ) and a software toolkit for
noise analysis (named TUNA) has been developed. Both of these components act as
open platforms for the further development of noise monitoring and analysis
methods. An initial prototype of the UDAQ platform has been produced using a
Beagleboard xM single board computer along with an appropriate analog-to-digital
converter, preamplfier, battery pack and pressure housing.

The Beagleboard xM runs a custom Linux image producing using the OpenEmbedded
build system.

The first half of this talk will focus on how OpenEmbedded has been used in the
development of the UDAQ platform and how the unique challenges of developing
software for a device that must operate unattended in the ocean for long time
durations have been addressed. These challenges include the fact that sending an
engineer to fix a device requires hiring a ship, giving some of the most
expensive call-out rates of any industry! The abilities of OpenEmbedded to
tightly control what software is executed on the device and to provide updates
from a customised package feed are critical in this application. As this
platform is designed to be open and customisable for further research, the
ability to produce a cross-development toolchain for other developers to use is
also a great benefit.

The second half of this talk will discuss how I began contributing patches to
OpenEmbedded due to its use in the above project and how I've became maintainer
of opkg, a package manager for embedded Linux. This is the default package
manager for both OpenEmbedded and OpenWRT and is also used by several other
projects and is a fork of the older ipkg package manager. Development had slowed
down due to the maintainer having other time commitments and so I stepped in
around August 2013 and have been reviving the project. It has recently seen many
new patches and bug fixes and is again attracting active development. The
history, current status and future directions of opkg will be outlined and
opportunities for people to contribute to this project will be highlighted.

Slides
------

I believe these are lost to history, but I will add them here if I ever find them.

Other links
-----------

* `FOSDEM 2014 schedule entry <https://archive.fosdem.org/2014/schedule/event/underwater_acoustics_to_opkg/>`__

* `FOSDEM 2014 speaker entry <https://archive.fosdem.org/2014/schedule/speaker/paul_barker/>`__

* `Raw FOSDEM video recording (skip to 26 min for the start of my talk) <https://video.fosdem.org/2014/UB2252A_Lameere/Sunday/Underwater_Acoustics_to_Opkg.webm>`__
