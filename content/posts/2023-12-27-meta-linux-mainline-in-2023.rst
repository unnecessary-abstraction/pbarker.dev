..
   Copyright (c) 2023 Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

meta-linux-mainline in 2023
===========================

:date: 2023-12-27
:tags: yocto, embedded-linux, meta-linux-mainline
:summary:
   It's time for a year end review of `meta-linux-mainline
   <https://github.com/betafive/meta-linux-mainline>`__, a `Yocto Project
   <https://www.yoctoproject.org>`__ layer which contains recipes for the
   currently supported Linux kernel release series and the latest mainline
   kernel. This year the project has seen various improvments as well as the
   regular flow of new Linux kernel & Yocto Project releases. The layer is now
   updated most weeks, more closely tracking the kernel release cycle but
   there's still more we can do with additional resources.

I maintain `meta-linux-mainline
<https://github.com/betafive/meta-linux-mainline>`__, a `Yocto Project
<https://www.yoctoproject.org>`__ layer which contains recipes for all currently
supported Linux kernel release series and the latest mainline kernel (see
`kernel.org <https://kernel.org>`__ for the current list). This is a side
project for me, but it has seen usage in both my current day job with Renesas
and my previous work with SanCloud.

This year the project has seen various improvments as well as the regular flow
of new Linux kernel & Yocto Project releases. The layer is now updated most
weeks, more closely tracking the kernel release cycle but there's still more we
can do with additional resources.

I'll be taking a break from updating meta-linux-mainline over the holidays -
there will be no update over the Christmas or New Year weeks, regular updates
will resume from the week of Monday 8th January 2024.

A quick introduction on use cases
---------------------------------

If you're not familiar with meta-linux-mainline, the goal of this project is to
complement the work on the Yocto Project reference kernel (linux-yocto), rather
than to compete with it. I recommend looking at meta-linux-mainline for the
following use cases:

* You need to closely track the latest mainline kernel, including release
  candidates, without any downstream patches. This can be vital when preparing
  patches to send upstream, trying to report bugs to the kernel development
  community and testing to ensure that your product will be fully supported in
  future kernel releases.

* You need to stay on an older LTS kernel series while moving to a more recent
  Yocto Project release.

* Conversely, you need to use a newer kernel series while staying on an older
  (but still supported) Yocto Project release.

For other use cases I recommend looking at the linux-yocto recipes in the
openembedded-core layer or the appropriate vendor kernel recipes in the BSP
layer for your target machine.

Funding
-------

My work on meta-linux-mainline is unpaid, and this year I invested in
updating my development machine (now using a Ryzen 7 7700 CPU, 64GB RAM and 2TB
gen4 NVMe storage) so that the full matrix of 216 Yocto Project builds (4
supported Yocto Project releases x 6 qemu machine targets x 9 supported kernel
series) can complete in a reasonable time.

I'd like to setup a proper CI loop for meta-linux-mainline, but this will
require renting a build machine in a data center (at a cost of around €59.00 per
month if I use Hetzner) as the free runners provided with GitHub Actions don't
have enough storage or compute power for full Yocto Project builds and I can't
setup a GitHub Actions runner on my development machine at home for security
reasons.

I'd also like to do boot testing with each image we build, at least in qemu, but
that would further increase the build and test time for each update to the
layer. Given sufficient interest and financial support, we could extend the
build matrix to include real development boards (not just qemu machines) and
setup a board farm using labgrid to boot test each image we build.

I currently try to keep a fairly light time commitment on meta-linux-mainline.
The layer gets updated most weeks using the automated ``update-layer`` script,
but if anything fails to build I may not be able to address this immediately.
I've recently sent
`a <https://lore.kernel.org/stable/20231031172217.27147-1-paul.barker.ct@bp.renesas.com/>`__
`few <https://lore.kernel.org/stable/20231031173255.28666-1-paul.barker.ct@bp.renesas.com/>`__
`backport <https://lore.kernel.org/stable/20231031173501.28992-1-paul.barker.ct@bp.renesas.com/>`__
`requests <https://lore.kernel.org/stable/20231031173524.29161-1-paul.barker.ct@bp.renesas.com/>`__
for the stable kernel (based on fixes in mainline from other contributors), but
I'd like to be able to do more.

I'm happy to continue work on meta-linux-mainline in its current form without
any external funding, but if you'd like to see the project grow then more
resources will be needed. If you use this layer, please consider supporting
ongoing development via `Ko-fi <https://ko-fi.com/pbarker>`__ or `PayPal
<https://paypal.me/betafiveltd>`__. Alternatively, please `send me an email
<mailto:paul@betafive.dev>`__ if you'd like to discuss a more formal
business-to-business agreement for consulting or sponsorship of this development
work.

A URL change
------------

The meta-linux-mainline git repository was recently moved to
https://github.com/betafive/meta-linux-mainline as part of a plan to
consolidate my projects under the Beta Five company name. A redirect from the
old URL will be maintained indefinitely so hopefully this change won't cause any
disruption.

Keeping it building
-------------------

This year saw two new Yocto Project releases,
`4.2 "mickledore" <https://docs.yoctoproject.org/migration-guides/release-4.2.html>`__ and
`4.3 "nanbield" <https://docs.yoctoproject.org/migration-guides/release-4.3.html>`__.
The meta-linux-mainline layer was updated to support each new release as they
came out. Support for the "mickledore" release has now been dropped as it is
end-of-life.

At the beginning of 2023 the meta-linux-mainline layer was still advertising
compatibility with the "gatesgarth", "hardknott", "honister" and "langdale"
Yocto Project releases via the ``layer.conf`` file. These have all now been
dropped as they are obsolete and no longer supported upstream.

Next year will see both the "nanbield" release and the old LTS "dunfell" release
reach end-of-life. In their place we'll have a new LTS release in April
(tentatively called 5.0 "scarthgap") and a regular release in October/November
(as yet unnamed).

As we've moved to newer Yocto Project releases, minor updates were needed to the
``LICENSE`` reference in the kernel recipes to align with the current SPDX
license naming.

The autobuild infrastructure for meta-linux-mainline has been overhauled this
year to improve build reliability and simplify maintenance. We're now using
the `kas <https://kas.readthedocs.io/en/latest/>`__ wrapper to fetch layers,
write configuration files and invoke bitbake for our test builds.

Side note: Adding meta-linux-mainline to your build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provided that you're using a currently supported Yocto Project release series,
it's very simple to add the meta-linux-mainline layer to your build. Once
your build environment has been initialised, run the following command::

    bitbake-layers layerindex-fetch meta-linux-mainline

If this all sounds interesting, but you're unfamiliar with the Yocto Project, I
recommend starting with the `Quick Build guide
<https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html>`__.

Reference machines
------------------

This year I dropped the Raspberry Pi 4 (both 32-bit & 64-bit modes) from the
build matrix for meta-linux-mainline, giving me room to include ``qemuriscv32``
and ``qemuriscv64`` to the matrix instead. With strong interest in RISC-V across
the industry, it's important to ensure that this architecture is supported. To
avoid excessive integration work, RISC-V support is only tested for Linux v5.15
or later and Yocto Project 4.0 "Kirkstone" or later.

Since we're building vanilla kernels using the in-tree ``defconfig``
configuration, there isn't really any difference between a ``qemuarm`` (or
``qemuarm64``) kernel build and a ``raspberrypi4`` (or ``raspberrypi4-64``)
kernel build with meta-linux-mainline. To support booting on the Raspberry Pi,
we do need some additional integration to select an appropriate device tree,
configure the bootloader for booting an upstream kernel and drop features which
aren't yet supported with an upstream kernel. This integration remains in the
meta-linux-mainline layer, and can be enabled by including
``conf/linux-mainline/bsp/raspberrypi4.inc`` or
``conf/linux-mainline/bsp/raspberrypi4-64.inc`` as needed in your ``local.conf``
file, but it is no longer built regularly and so may be subject to some bitrot.
I'd like to restore this support fully in the future, with automated boot
testing on real hardware, but that's definitely going to need some funding as
outlined above.

Side note: BSP configuration in meta-linux-mainline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The recommended way to configure meta-linux-mainline for a particular
``MACHINE`` is to use a ``.inc`` file under the ``conf/linux-mainline/bsp``
directory, with the filename matching the machine name (e.g. ``qemuarm.inc`` for
the ``MACHINE = "qemuarm"``). For the supported QEMU targets and the Raspberry
Pi 4, these files already exist in the layer itself. For other target machines,
we suggest that you create these files in the appropriate BSP layer or in a
separate integration layer.

This then allows you to enable meta-linux-mainline integration by adding the
following to your ``local.conf`` file or distro configuration::

    require conf/linux-mainline/bsp/${MACHINE}.inc

Kernels old and new
-------------------

The default LTS kernel in meta-linux-mainline has changed twice this year - back
in March the layer was updated to use the v6.1 LTS series, then in November it
was announced that `v6.6 would be the new LTS series
<https://www.phoronix.com/news/Linux-6.6-Goes-LTS>`__ and the layer was updated
again.

The new LTS series will be maintained until December 2026, meaning that
the end-of-life for the last 4 LTS series are all aligned. The support period
for LTS kernels is slowly reducing in line with the annoucement earlier in the
year, it's expected that future LTS series will be supported for 2 years each.
This will definitely reduce the number of kernel recipes in meta-linux-mainline
over the next couple of years and should make maintaining this layer a little
easier.

On the subject of old LTS series, the recipe for the 4.9 series was dropped
early this year as it reached EOL. Next year it's expected that we'll be
dropping the recipe for v4.14 after it goes EOL in January, and then v4.19 after
it goes EOL in December.

Side note: Following a kernel series in your build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To follow the latest mainline kernel from Linus (including release candidates)
using this layer, you can add the following to your ``local.conf`` file or
distro configuration::

    require conf/linux-mainline/mainline.inc

If you don't want to track the bleeding edge of development, you can instead use
the following to get the latest stable release from Greg K-H and move to a new
stable series every 9 or so weeks::

    require conf/linux-mainline/stable.inc

To follow the latest LTS kernel series and move to a new LTS series each year,
you can use the following::

    require conf/linux-mainline/lts.inc

And lastly, if you want to stay on a particular LTS series for the long haul,
for example v6.1, you can add the following instead (replacing ``6.1`` with
whichever LTS series you want to track)::

    require conf/linux-mainline/stable.inc
    PREFERRED_VERSION_linux-stable = "6.1%"
