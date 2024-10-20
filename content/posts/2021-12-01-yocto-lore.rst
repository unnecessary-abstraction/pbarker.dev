..
   Copyright Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

Conference Talk: Yocto Project lore: New mailing list tools
===========================================================

:date: 2021-12-01
:tags: yocto, conference-talk
:summary:
    I gave a short talk on using the `lore.kernel.org`_ public inbox instance
    with Yocto Project at the `Yocto Project Summit 2021.11`_.

I gave a short talk on using the `lore.kernel.org`_ public inbox instance with
Yocto Project at the `Yocto Project Summit 2021.11`_.

Slides from this talk are available in `PDF`_ format.

.. _lore.kernel.org: https://lore.kernel.org
.. _Yocto Project Summit 2021.11: https://pretalx.com/yocto-project-summit-2021-11/
.. _PDF: https://pub.pbarker.dev/presentations/2021-12-01%20Yocto%20Project%20Summit%202021.11%20-%20Yocto%20Project%20Lore/YPS2021.11_-_Lore_J7Mey1G.pdf

Abstract
--------

This short talk will present the new tools we can make use of now that the Yocto
Project mailing list is mirrored to lore.kernel.org. The b4 tool will be
introduced and a demo will be given of how this tool can be used to quickly
apply patches from the mailing list to a local repository, show differences
between patch versions and autogenerate thank you messages. The talk will also
briefly touch on the patatt patch attestation tool which can be used to
cryptographically sign patches sent via a mailing list.

Recently the Yocto Project & OpenEmbedded mailing lists have been added to the
lore.kernel.org public-inbox server. This allows us to make use of new tools
developed within the Linux kernel community to simplify the process of
reviewing, testing and accepting patches submitted via mailing lists. This talk
is presented in the hope that these tools can become more widely used within the
Yocto Project community now that they are available, hopefully making life
easier for maintainers!

Video
-----

.. youtube:: nHtcDqnO2zY
