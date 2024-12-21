..
   Copyright (c) 2021 Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

Rebooting meta-linux-mainline
=============================

:date: 2021-06-22
:tags: yocto, embedded-linux, meta-linux-mainline, blog
:summary: `meta-linux-mainline <https://github.com/unnecessary-abstraction/meta-linux-mainline>`_
          is a Yocto Project layer I created in May 2020 when I needed to test a
          few hardware boards with unpatched, upstream kernel sources. The
          project has undergone a few changes recently so now is a good time to
          give an updated overview of how the layer works and when you might
          want to use it.

Introduction
------------

The meta-linux-mainline Yocto Project layer contains recipes for building the
Linux kernel from unmodified sources as released on kernel.org. It can be used
to develop a BSP which uses a mainline kernel by default, to replace the default
vendor kernel in an existing BSP (which may be obsolete, insecure or otherwise
broken), to support upstream kernel development or simply for testing. It
provides ``linux-stable`` recipes for all stable release series (including LTS
releases) currently supported upstream as well as a ``linux-mainline`` recipe
for those who want to live on the bleeding edge. It is compatible with all
currently supported Yocto Project releases ("dunfell" and "hardknott" at the
time of this post) as well as the Yocto Project master branch. Further details
can be found in the project's `readme file
<https://github.com/unnecessary-abstraction/meta-linux-mainline/blob/main/README.md>`_.

Use Cases
---------

The meta-linux-mainline layer has two primary use cases: supporting the
development of new BSPs which use upstream kernel sources by default and
overriding the kernel recipes in existing BSPs to use upstream kernel sources
instead of vendor kernel sources.

When developing a new Yocto Project BSP for a hardware platform supported by the
mainline kernel, it should not be necessary to maintain your own mainline kernel
recipe. Users should be given the option of using the latest stable kernel, an
LTS release series or even a bleeding-edge mainline kernel without the BSP
maintainer needing to implement all these options. Users should also get regular
updates to the kernel recipes without needing to distract the maintainer from
focusing on the hardware-specific details of their BSP. These objectives can be
achieved by using meta-linux-mainline as a dependency of the BSP layer and where
necessary specifying the earliest mainline kernel version required to support
the target hardware.

Many existing BSPs default to the use of a "vendor kernel" which incorporates
many (sometimes several thousand) patches which have not been subject to
upstream review, testing and integration by the kernel community. In many cases
the target hardware is supported well enough by the mainline kernel for the
intended use-case without the need for such patching. This can be particularly
frustrating when the vendor kernel in question is obsolete, doesn't receive
security updates or introduces compatibility issues. To switch away from a
vendor kernel, the meta-linux-mainline layer can be added to the build alongside
the relevant BSP layer(s) and the relevant upstream kernel can be selected in
the local or distro config.

In both of these cases the linux-yocto recipes present in the core Yocto Project
metadata could be used instead of the recipes in meta-linux-mainline. However,
linux-yocto recipes are typically provided for a narrower set of kernel releases
than those currently supported upstream and recipes are not added to stable
Yocto Project branches for newer kernel release series (as the kernel community
places an incredibly high value on backwards compatibility it is generally safe
to update to new stable kernel releases). The linux-yocto kernels also include
many patches which may not have been through a full upstream review by the
kernel community. Using unpatched upstream kernel sources also has major
benefits when supporting multiple Linux distributions on the target hardware as
it is then possible to standardise on the upstream kernel. Lastly, if you have
customer requirements or preferences for a mainline kernel then these can be met
using the meta-linux-mainline layer.

This layer also supports two other secondary use cases. The mainline kernel
recipe provided in this layer can be used to support upstream kernel development
as it can be easily modified to point to an alternative source repository and
branch or commit. The recipes may also be used as part of a regular testing
process to ensure that an embedded device works as expected with new upstream
kernel releases.

Defining Goals and non-Goals
----------------------------

For a project like meta-linux-mainline to succeed, it needs a clearly defined
set of goals and non-goals. Goals identify the features and attributes which I
want to see in this project, non-goals identify things which may in theory be
possible to achieve but which I have chosen to exclude from the scope of this
project and which will not be implemented or accepted as contributions without a
major change to the project's scope. The goals are obviously important, they
should be aligned with the intended use cases for the layer and drive the
project forwards. The non-goals for a project are often overlooked but I think
they are equally important, they help the project to avoid bloat and stay on
track. Potential contributors can review the project's goals and non-goals and
find out upfront if their changes are likely to be accepted into the project.
The goals and non-goals for meta-linux-mainline are listed prominently in the
project's `readme
<https://github.com/unnecessary-abstraction/meta-linux-mainline/blob/main/README.md#goals-and-non-goals-of-this-layer>`_
file.

The current goals for meta-linux-mainline are as follows:

* We provide recipes for all Linux kernel releases currently supported on
  kernel.org. These recipes are regularly updated to make it easy to follow
  mainline releases, the latest stable series or a chosen LTS release series.

* We aim to be compatible with all currently supported Yocto Project releases as
  well as the upstream master branch.

* We provide examples of how to use this layer in the form of BSP configurations
  for various QEMU and Raspberry Pi targets.

The current non-goals for meta-linux-mainline are as follows:

* We do not carry patches against upstream kernel releases without a documented,
  exceptionally good reason.

* We do not support obsolete kernel versions. Recipes are only provided for the
  latest patch release within a given release series. Once a release series
  becomes End-Of-Life (EOL) on kernel.org, the corresponding recipe will be
  removed from this layer.

* We provide no guarantees that kernels built with this layer will boot
  successfully on your hardware or that particular features (e.g. perf) will
  work out of the box. The example BSP configurations are not intended to be
  directly used in production. To use this layer in production, create your own
  layer for configuration & integration and use this layer as a dependency.

* We do not aim to replace the linux-yocto kernel from the Yocto Project.

Recent Changes
--------------

Project maintenance is now focused on a single main branch which aims to be
compatible with the master branch and all currently maintained releases of the
Yocto Project. The "master" and stable branches ("dunfell", etc) of
meta-linux-mainline will simply follow the "main" branch. This simplification,
along with improved automation of updates to the kernel recipes, should result
in more regular updates to this layer while ensuring that the level of
maintainer effort required remains small and sustainable.

Several other changes have been made to the project as highlighted in the
project's `ChangeLog
<https://github.com/unnecessary-abstraction/meta-linux-mainline/blob/main/ChangeLog.md>`_.
These include switching the example hardware BSP to Raspberry Pi 4, adding more
QEMU example targets, switching the default LTS kernel series to 5.10, improving
how stable kernels are downloaded and overhauling the scripts used to test and
update this layer.

Future Plans
------------

At this point the meta-linux-mainline layer is in a pretty good shape and meets
the use cases which I have. Project maintenance is expected to be fairly
straightforward as updates to the kernel recipes are fully automated. There are
no major changes expected in the near future, the project will just tick over
with minor improvements and regular recipe updates as needed.  If you have any
feature requests, please feel free to submit them via the `issue tracker
<https://github.com/unnecessary-abstraction/meta-linux-mainline/issues>`__.

At some point I would like to see recipes for RT kernels added to the layer.
This isn't something I immediately need myself, so I'd encourage anyone who has
an immediate need for vanilla RT kernel recipes to contribute this feature to
the project. I'm actually hoping that by the time I next need to play with
realtime features I'll find that the RT patches have been merged fully into
mainline Linux and no separate kernel recipes are actually needed in this layer.

The next Yocto Project release, 3.4 "honister", is expected in October this
year. It's expected that upstream support for the 3.3 "hardknott" release series
will end in November. This layer will be updated around those times to add
support for the "honister" release and remove support for the "hardknott"
release. The current Yocto Project LTS release, 3.1 "dunfell", is expected to be
supported upstream until at least April 2022 and my intention is to continue
supporting the "dunfell" release in this layer until upstream support ends.
