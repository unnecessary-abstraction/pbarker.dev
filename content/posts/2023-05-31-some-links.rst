..
   Copyright (c) 2023 Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

Some Links: May 2023
====================

:date: 2023-05-31
:tags: linkblog
:summary:
    Some interesting links I found in May 2023.

I'm still in the process of trying out different styles of blogging to see what
works for me. Today we'll be roleplaying as a link blog, but with one aggregate
post covering the month of May instead of one post per link. Let me know what
you think!

I built this list throughout the month on `Raindrop.io <https://raindrop.io>`__ - 
you can also see `this list <https://raindrop.io/pbarker/may-2023-34256215>`__
over there. You can even follow along as I build `June's list
<https://raindrop.io/pbarker/june-2023-34256326>`__ if you want to!

Kernel
------

- Linux 6.3 was released at the end of April.
  See the `Linux Kernel Newbies page <https://kernelnewbies.org/Linux_6.3>`__
  and `Linus' release email
  <https://lore.kernel.org/lkml/CAHk-=wg02PoScxDO0wwD5EkFpx50DF1c2TxXqyAnzGjdFf71jw@mail.gmail.com/>`__
  for more details.

- Rob Herring posted a `very welcome patch
  <https://lore.kernel.org/all/20230504-arm-dts-mv-v1-0-2c8e51a2b6c4@kernel.org/T>`__
  to organize the ARM device trees (1553 files and growing)
  into per-vendor subdirectories.
  I gave this my ack as maintainer of the SanCloud device trees
  and hope to see the new layout in Linux 6.5.

- The `fourth installment of "50 years in filesystems"
  <https://blog.koehntopp.info/2023/05/12/50-years-in-filesystems-1994.html>`__
  by Kristian Köhntopp
  takes us back to 1994 and the design of the XFS filesystem.
  XFS has been my filesystem of choice for most of the time I've been using Linux.
  I've not done any solid benchmarking but the support for large filesystems
  and the focus on bandwidth & concurrency
  are a good match to my needs.
  I've been really enjoying this series of articles!

C & C++
-------

- GCC 13.1 was released at the end of April.
  Red Hat have a good article on the `New C features in GCC 13
  <https://developers.redhat.com/articles/2023/05/04/new-c-features-gcc-13>`__.

- `Sourceware has joined Software Freedom Conservancy as a member project
  <https://sfconservancy.org/news/2023/may/15/sourceware-joins-sfc/>`__.
  This should provide improved infrastructure and resourcing
  ("fundraising, legal assistance and governance") for the benefit of
  Sourceware-hosted projects including GCC, glibc, binutils, cygwin (remember that?) and others.

Rust
----

- Olivier Faure wrote a `Report on platform-compliance for cargo directories
  <https://poignardazur.github.io/2023/05/23/platform-compliance-in-cargo/>`__.
  Platform compliance here refers to following the conventions on where to place
  binaries, config files and caches on each supported environment. I'm glad to
  see more discussion of this as I really want ``cargo`` to start placing files
  into ``~/.cache``, ``~/.config`` and ``~/.local`` as appropriate instead of
  having its own non-standard ``.cargo`` directory in my homedir.

  Call me an `XDG Base Directory Specification
  <https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`__
  maximalist if you must.

- In April, the Prossimo project launched a new initiative to
  `Bring Memory Safety to sudo and su <https://www.memorysafety.org/blog/sudo-and-su/>`__.
  I don't think this is just "re-write the world in rust" hype -
  it's important that critical software which enforces the boundary between different permission levels
  is written in a safer language than C.

  There's also `a longer post on this subject
  <https://tweedegolf.nl/en/blog/91/reimplementing-sudo-in-rust>`__
  from Marc at Tweede Golf.

- Google has `open-sourced their Rust crate audits
  <https://opensource.googleblog.com/2023/05/open-sourcing-our-rust-crate-audits.html>`__
  which can be used with `cargo-vet <https://github.com/mozilla/cargo-vet>`__.

Python
------

- I discovered the `Nobody has time for Python <https://www.bitecode.dev/>`__
  blog this month and I'm enjoying the posts there. In particular, I want to
  highlight `Happiness is a good PYTHONSTARTUP script
  <https://bitecode.substack.com/p/happiness-is-a-good-pythonstartup>`__ -
  this post discusses how to customise an interactive Python/IPython shell
  with a startup script. I wouldn't go as far as this post does, I think a 320
  line startup script is overkill, but I will be making use of some of the
  suggestions here.

- LWN explored `Ruff: a fast Python linter <https://lwn.net/Articles/930487>`__
  written in Rust.
  I don't think this is yet ready to replace ``flake8`` & ``isort`` for me,
  but I'll definitely be checking back in a year or so to see how this has progressed.

- Since pip v23.0, a Python environment can be marked as "Externally Managed"
  which will prevent installation of additional packages via pip. This has been
  enabled recently on Gentoo and on Debian Bookworm (currently in pre-release)
  to push users to install such Python packages with the system package manager,
  or use a venv where appropriate. The article `"Externally managed
  environments": when PEP 668 breaks pip
  <https://pythonspeed.com/articles/externally-managed-environment-pep-668/>`__
  covers this development well and suggests changes to your workflow if you're
  used to just ``pip install``-ing packages.

- I've started switching from ``markdownlint`` (written in Ruby) to
  `PyMarkdown <https://pypi.org/project/pymarkdownlnt/>`__
  for linting my readmes, changelogs and other Markdown documents. It's much
  easier for me to deploy Python development tools as they can be easily installed in a venv.
  This project is still very much beta quality, but it's working for me so far!

- A lot has happened this month in the world of PyPI. I wrote `Thoughts on PyPI,
  PGP and Sigstore </posts/2023-05-24/thoughts-on-pypi-pgp-and-sigstore/>`__
  in response to the removal of PGP signature support. We've also learned that
  `PyPI was subpoenaed <https://blog.pypi.org/posts/2023-05-24-pypi-was-subpoenaed/>`__
  and that `every account that maintains any project or organization on PyPI will be required
  to enable 2FA on their account by the end of 2023
  <https://blog.pypi.org/posts/2023-05-25-securing-pypi-with-2fa/>`__.

Other Topics
------------

- Bootlin have release `Snagboot: a cross-vendor recovery tool for embedded platforms
  <https://bootlin.com/blog/releasing-snagboot-a-cross-vendor-recovery-tool-for-embedded-platforms/>`__.
  I hope to get a chance to try this out in the near future!
  It will be good to reduce the number of vendor-specific tools in use in the Embedded Linux world.

- The Voices of Open Source blog discussed
  `Another issue with the EU Cyber Resilience Act:
  European standards bodies are inaccessible to Open Source projects
  <https://blog.opensource.org/another-issue-with-the-cyber-resilience-act-european-standards-bodies-are-inaccessible-to-open-source-projects/>`__.
  Back in April, the Python Software Foundation also posted a news item on how
  `The EU's Proposed CRA Law May Have Unintended Consequences for the Python Ecosystem
  <https://pyfound.blogspot.com/2023/04/the-eus-proposed-cra-law-may-have.html>`__.
  If you're in the EU (*grumble grumble Brexit grumble*), I'd definitely recommend
  reaching out to your MEPs and other relevant folks to raise the profile of these issues.

- Intel have posted an article on `Envisioning a simplified x86_64 architecture
  <https://www.intel.com/content/www/us/en/developer/articles/technical/envisioning-future-simplified-architecture.html>`__
  which would drop support for 32-bit operating systems and other "legacy" features
  from the Intel/AMD 64-bit architecture. I don't expect these changes to take
  place soon, but it'd be great to see reduced complexity in this area when it
  does come around.

- `AI machines aren't "hallucinating". But their makers are
  <https://www.theguardian.com/commentisfree/2023/may/08/ai-machines-hallucinating-naomi-klein>`__ -
  Naomi Klein has long been one of my favourite authors and journalists,
  it's great to see new writing from her on the subject of AI hype.
  Naomi is now a `regular columnist for Guardian US
  <https://www.theguardian.com/gnm-press-office/2023/may/08/naomi-klein-joins-guardian-us-as-a-regular-columnist>`__
  and has a `new book, "Doppelganger", out later in the year <https://naomiklein.org/doppelganger/>`__.

- Also on the subject of AI, I highly recommend Ted Chiang's article in The New Yorker,
  `Will A.I. Become the New McKinsey?
  <https://www.newyorker.com/science/annals-of-artificial-intelligence/will-ai-become-the-new-mckinsey>`__.
  I spoke to Cory Doctorow at an event last night and he described Ted as "full
  of piss and vinegar" about AI which is entirely appropriate. This article is
  fantastic, it draws together a lot of ideas and helps to crystallise them
  together. I read this one twice, and it's not a short piece!

- It's great to see that `Thunderbird Is Thriving
  <https://blog.thunderbird.net/2023/05/thunderbird-is-thriving-our-2022-financial-report>`__!
  This financial report for the calendar year 2022 is a welcome read
  given that Thunderbird is my day-to-day email client.
  See `this comment
  <https://blog.thunderbird.net/2023/05/thunderbird-is-thriving-our-2022-financial-report/#comment-3523>`__
  if you want a brief breakdown on the donations made to the project in 2022.

- Never trust an offer of "free forever" pricing on a cloud-hosted service - 
  many folks are now learning what happens
  `when “free forever” means “free for the next 4 months”
  <https://blog.zulip.com/2023/05/04/when-free-forever-is-4-months/>`__.
  By all means make use of free online services,
  but have a plan in place for the day that they start charging
  and be careful that you're not already paying with your data.

- Kenneth Finnegan wrote up an article on `Building the Micro Mirror Free Software CDN
  <https://blog.thelifeofkenneth.com/2023/05/building-micro-mirror-free-software-cdn.html>`__.
  As usual for Kenneth, this is a great tale of a project that quickly got out of
  hand in the very best way.
