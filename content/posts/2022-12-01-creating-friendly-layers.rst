..
   Copyright Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

Conference Talk: Creating Friendly Layers, 2022 Edition
=======================================================

:date: 2022-12-01
:tags: yocto, conference-talk
:summary:
    I gave a revised and updated talk on creating friendly Yocto Project layers
    at the `Yocto Project Summit 2022.11`_.

I gave a revised and updated talk on creating friendly Yocto Project layers
at the `Yocto Project Summit 2022.11`_.

Slides from this talk are available in `PDF`_ and `PowerPoint (pptx)`_ formats.

.. _Yocto Project Summit 2022.11: https://pretalx.com/yocto-project-summit-2022-11/
.. _PDF: https://pub.pbarker.dev/presentations/2022-12-01%20Yocto%20Project%20Summit%202022.11%20-%20Creating%20Friendly%20Layers%202022%20Edition/Friendly%20Layers%202022.pdf
.. _PowerPoint (pptx): https://pub.pbarker.dev/presentations/2022-12-01%20Yocto%20Project%20Summit%202022.11%20-%20Creating%20Friendly%20Layers%202022%20Edition/Friendly%20Layers%202022.pptx

Abstract
--------

A typical software product build with Yocto Project makes use of several
different metadata layers. These layers may be maintained by hardware
manufacturers, software/service companies, or individual hobby developers.
Naturally there is some variation in layer quality and compatibility - some
layers play well with each other while others are in practice mutually
exclusive. For example, misbehaving layers may force the selection of particular
machine or distro or make unwanted changes to recipes defined in other layers.
This can result in broken builds (often with confusing error messages) or subtle
runtime errors and crashes which may be difficult to debug.

As a layer author you can apply straightforward design principles to maximise
the compatibility of your layer, or at least to ensure that useful error
messages are given if you layer is used incorrectly. Following these principles
effectively requires a good understanding of how variables, tasks, distro
features and overrides work within the Yocto Project.

This talk will collect the knowledge required to design and implement high
quality Yocto Project layers. Attention will be given to proper use of
bbappends, conditionals, distro & machine features and sanity checks. Examples
of well behaved layers will also be highlighted. Information presented in the
previous edition of this talk will be updated to target the Langdale (4.1) and
Kirkstone (4.0, LTS) releases.

Video
-----

.. youtube:: 6iGuKViITjg
