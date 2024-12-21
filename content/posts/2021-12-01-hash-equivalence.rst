..
   Copyright Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

An Overview of the Hash Equivalence & PR Services
=================================================

:date: 2021-12-01
:tags: yocto, conference-talk
:summary:
    I gave a talk on the hash equivalence and package revision (PR) services in
    Yocto Project at the `Yocto Project Summit 2021.11`_.

I gave a talk on the hash equivalence and package revision (PR) services in
Yocto Project at the `Yocto Project Summit 2021.11`_.

Slides from this talk are available in `PDF`_ format.

.. _Yocto Project Summit 2021.11: https://pretalx.com/yocto-project-summit-2021-11/
.. _PDF: https://pub.pbarker.dev/presentations/2021-12-01%20Yocto%20Project%20Summit%202021.11%20-%20An%20Overview%20of%20the%20Hash%20Equivalence%20%26%20PR%20Services/YPS2021.11_-_Hash__PR_Services_2sTYIuE.pdf

Abstract
--------

This talk will give an overview of the Yocto Project's Hash Equivalence Service
(hashserv) and PR Service (prserv). The use cases for these tools will be
explored and a demo of each will be given. The new features added to these
services since the initial dunfell release in April 2020 will then be discussed,
highlighting the read-only modes and the support for connecting to an upstream
service. The new features will be demonstrated and the new use cases which these
features enable will be presented. Finally, possible future developments will be
discussed.

This talk will be appropriate for attendees familiar with bitbake but with no
prior knowledge of these services. It will also be useful to those with
experience using these services who are unfamiliar with the new features added
since the dunfell release.

hashserv
~~~~~~~~

When bitbake looks at the inputs for a build task (the recipe, inherited
classes, relevant variables set by conf files and the inputs of other relevant
build tasks), a hash of the input data is generated. This is the basis of the
Shared State (sstate) caching provided by bitbake - if in a future build the
hash of the input data for a build task is the same, the previously generated
sstate can be reused instead of re-running the build task. This allows for
significant time savings in subsequent builds once the sstate cache is
populated.

The Hash Equivalence Service (hashserv) is a standalone service developed within
the bitbake project which can further improve sstate re-use. It maintains a
database of input hashes for build tasks and the hashes of their output data.
Traditionally, if the input hash for a build task changes then all dependent
tasks need to be re-executed even if the output data from the first task is
identical. However with hashserv enabled, bitbake can detect the case where
output data from a task is identical to a previous execution and it can mark the
two different input hashes as equivalent. This allows dependent tasks to be
skipped where sstate data is available for the previous input hash, potentially
giving significant improvements in sstate re-use and corresponding reductions in
build time.

prserv
~~~~~~

The PR Service (prserv) is a standalone service developed within the bitbake
project which maintains a database of input hashes for build tasks and a
corresponding package revision (PR) value. This allows bitbake to ensure that
the package revision increments each time a recipe is rebuilt with different
input data. This in turn ensures that on-device package upgrades work as
expected when a package is rebuilt

Video
-----

.. youtube:: NwMNv9EDl14
