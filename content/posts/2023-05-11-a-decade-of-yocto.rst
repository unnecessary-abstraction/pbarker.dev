..
   Copyright (c) 2023 Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

A decade of contribution to OpenEmbedded & the Yocto Project
============================================================

:date: 2023-05-11
:tags: yocto, embedded-linux, blog
:summary:
    I realised recently that I have now been involved in OpenEmbedded and the
    Yocto Project for over a decade! I thought I'd take the opportunity to look
    back at how I first got involved with the project and my early
    contributions.

Back in 2013, I was a research student at Loughborough University working on an
underwater acoustic recording platform, the UDAQ, based around the `BeagleBoard
xM`_ Single Board Computer. I had built a daughterboard for this platform which
connected a Texas Instruments ADS1672 ADC to the Multi-channel Buffered Serial
Port (McBSP) of the AM37x processor on the BeagleBoard xM, and I had started
work on a Linux kernel driver for this Analog-to-Digital Converter (ADC) which
could be loaded as a module.  What I needed next was to configure the pin
multiplexing (pinmux) on the processor to enable the McBSP. As this was in the
Bad Old Days™ before device trees were universal [1]_, to do this I had to
modify a board file in the Linux kernel source tree and rebuild the whole
kernel.

The software image for the BeagleBone xM used the `Ångström Linux
distribution`_. This image was written to an SD card which was then inserted
into the BeagleBoard xM. Once the system was booted you could connect over a
serial port and make normal use of the Linux command line. Additional packages
could be installed via the opkg package manager, with the Ångström distribution
providing a feed of pre-built binary packages via their website. But what if you
wanted to rebuild a software package such as the Linux kernel, or to build and
install your own custom software packages? This is what I needed to do, but the
system performance and the space available on an SD card in 2013 really didn't
lend themselves to building software on the BeagleBone xM itself.

Enter the `OpenEmbedded`_ build system, and the Linux Foundation's `Yocto
Project`_ collaboration built around it. The Ångström distribution was not
compiled on the BeagleBoard xM itself, instead it was cross-compiled on a more
powerful desktop or server computer using the Yocto Project. I realised that I
did not have to settle for minor additions to the Ångström distribution and a
rebuilt kernel - using Yocto Project I could build a completely custom software
image for the UDAQ device. This was a huge boon for the project I was working on
as a tightly controlled software environment with minimal background services
running would increase the reliability when trying to capture and analyse
acoustic data in real time. With luck it would also increase the battery life of
the device, although I didn't actually test that in the end.

So, I set up a build environment on my desktop PC and I jumped into version 1.4
of the Yocto Project, codenamed "Dylan". I remember there being a lot to learn,
but I also remember quickly making progress. As I've often done, I learned my
way around Yocto Project by experimenting and by seeing if I could fix issues as
I came across them. After a couple of early attempts on the mailing list, I
landed my first contribution in March 2013: `a one-line fix for the gnupg recipe`_.

.. figure:: https://img.pbarker.dev/misc/udaq1.webp
   :width: 100%

   An early prototype of the UDAQ hardware. From left to right, you can see the
   end cap of the UDAQ housing, the signal amplification & conditioning board,
   and the BeagleBoard xM. This version lacked the ADS1672 ADC and used the
   audio line input to the BeagleBoard xM to digitise the signals from a
   hydrophone, limiting the bandwidth which could be captured.

.. figure:: https://img.pbarker.dev/misc/udaq2.webp
   :width: 100%

   A later prototype of the UDAQ hardware (in glorious potato-camera quality).
   From top to bottom, this PCB stack consists on an ADS1672 evaluation module,
   a custom interposer board which I designed, and the BeagleBoard xM.

In June of 2013 I began to organise the software for the UDAQ project into git
repositories (I think I was using Subversion before this) and push them to
BitBucket. These repositories are still online today, though managing them is no
longer possible due to changes Atlassian has made to BitBucket in recent years [2]_.
I also don't trust that they'll always remain available on BitBucket, so I've
copied the code over to GitHub to make it more available:

- `tuna`_: Toolkit for Underwater Noise Analysis, the user space service used to
  record and analyse data on the UDAQ.

- `ads1672`_: The driver for the TI ADS1672 ADC.

- `meta-udaq`_: The Yocto Project BSP and distro layer for the UDAQ.

- `udaq-build`_: Build configuration and scripting.

.. note::
   This code is obsolete and only of historical interest now, most of it won't
   build.

In parallel to my work on the UDAQ, I continued contributing to Yocto Project.
After attempting to get a couple of bugfixes applied to the opkg package
manager, I was given commit access to the source repository for this tool in
August 2013. The first thing I did was commit someone else's bugfix patch for an
issue which I felt was more urgent than my own. I then had a sudden "oh shit"
moment when I realised that committing code from another contributor effectively
made me a maintainer of opkg. Two weeks later I cut a release candidate and in
September 2013 I made my first release as the new opkg maintainer (``v0.2.0``).
I continued maintaining opkg until 2015 when I became too busy with my new job
at CommAgility to devote much time to opkg.

I consider my work on opkg to have been a huge success - I took a project which
was struggling, was weighed down by technical debt and was difficult to
contribute to and I passed it on to the next maintainer in a much cleaner state.
My biggest achievement here was removing legacy code and replacing it with a
dependency on a well maintained external library which implemented the functions
we needed - for a small cost in binary size we closed many of the open issues
and made ongoing work on opkg much less painful.

Another thing I remember well from my early years with Yocto Project was my
first visit to FOSDEM in January 2014. I met a few people at the OpenEmbedded
stand and this was my first opportunity to put faces to some of the names I'd
been talking to on the mailing list for several months. Everyone I met was
incredibly welcoming and encouraging and I think it has been this community of
contributors from various organisations which has kept me contributing and
coming back to the project ever since.

At FOSDEM 2014 I also gave my first presentation to an open source conference,
titled "Underwater Acoustics to Opkg, via The Yocto Project". I couldn't find
the video of this talk on YouTube so I have extracted it from the FOSDEM video
archives and uploaded it to YouTube for your viewing pleasure.

.. youtube:: QzsFphJACYc

My contributions to Yocto Project have waxed and waned over the years, depending
on how busy I have been and on where my focus has been. Even during the times I
haven't been making regular upstream contributions of any significance I have
been using Yocto Project extensively in my day-to-day work. At this point, it's
a critical part of my Embedded Linux toolkit and I don't expect it to go away
any time soon!

.. rubric:: Footnotes

.. [1]
    In these halcyon days, life is much easier. To change pinmux settings you
    can rebuild just the device tree which is loaded by the kernel at runtime,
    rather than having to rebuild the whole kernel.

.. [2]
    All BitBucket repositories are now organised into "workspaces", but
    these repositories pre-date the workspaces feature of BitBucket. They aren't
    listed anywhere in the web interface after I've logged in and the only way
    to find them is to navigate directly to the repository URL. Let this serve
    as a warning - repositories stored on third-party hosting services can and
    do break over time. Always keep backups!

.. _BeagleBoard xM: https://beagleboard.org/beagleboard-xm
.. _Ångström Linux distribution: https://en.wikipedia.org/wiki/%C3%85ngstr%C3%B6m_distribution
.. _OpenEmbedded: https://www.openembedded.org/wiki/Main_Page
.. _Yocto Project: https://www.yoctoproject.org/
.. _a one-line fix for the gnupg recipe: https://git.yoctoproject.org/poky/commit/?id=d12980ff1d47df0b6b8c10c595779af16cb76ffa
.. _tuna: https://github.com/unnecessary-abstraction/tuna
.. _ads1672: https://github.com/unnecessary-abstraction/ads1672
.. _meta-udaq: https://github.com/unnecessary-abstraction/meta-udaq
.. _udaq-build: https://github.com/unnecessary-abstraction/udaq-build
