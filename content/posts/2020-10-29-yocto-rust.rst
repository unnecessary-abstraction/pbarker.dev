..
   Copyright Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

Conference Talk: Using Rust with Yocto Project
==============================================

:date: 2020-10-29
:tags: yocto, conference-talk
:summary:
    I gave a talk on integrating software written in the Rust programming
    language with Yocto Project at the `Yocto Project Summit (Europe) 2020`_.
    This was a virtual conference due to the pandemic.

I gave a talk on integrating software written in the Rust programming language
with Yocto Project at the `Yocto Project Summit (Europe) 2020`_. This was a
virtual conference due to the pandemic.

Slides from this talk are available in `PDF`_ and `PowerPoint (pptx)`_ formats.

.. _Yocto Project Summit (Europe) 2020: https://pretalx.com/yocto-project-summit-2020/schedule/
.. _PDF: https://pub.pbarker.dev/presentations/2020-10-29%20Yocto%20Project%20Summit%20Europe%202020%20-%20Using%20Rust%20with%20Yocto%20Project/YP_Summit_2020_-_Rust_Demo_4M2OuqH.pdf
.. _PowerPoint (pptx): https://pub.pbarker.dev/presentations/2020-10-29%20Yocto%20Project%20Summit%20Europe%202020%20-%20Using%20Rust%20with%20Yocto%20Project/YP_Summit_2020_-_Rust_Demo_4M2OuqH.pdf

Abstract
--------

The Rust programming language has been named the "most loved programming
language" in the Stack Overflow Developer Survey every year since 2016. However,
many Embedded Linux developers are unfamiliar with this language and with the
benefits it can provide. There is also a knowledge gap on how to build and
deploy software written in Rust using OpenEmbedded and Yocto Project.

This session will focus on demonstrating how to use Rust with Yocto Project. Two
basic applications will be written along with the metadata needed by the Cargo
build tool.

Yocto Project recipes will be generated for each application and added to a
layer. An image will then be built containing both applications and this will be
tested out under qemu.

In addition some brief thoughts on how Rust and the Cargo build tool interact
with the license compliance features of Yocto Project will be discussed.

This talk is aimed at an intermediate audience. No familiarity with the Rust
programming language is assumed.

Video
-----

.. youtube:: aPsMuSU-Btw
