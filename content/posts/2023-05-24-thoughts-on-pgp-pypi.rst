..
   Copyright (c) 2023 Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

Thoughts on PyPI, PGP and Sigstore
==================================

:date: 2023-05-24
:tags: python, pgp
:summary:
    A recent grumble about PGP signatures on PyPI has quickly led to PyPI
    dropping support for PGP. While I agree that there are major issues with
    PGP, I don't agree that its use in PyPI is "worse than useless" and I'm
    disappointed to see support dropped before a replacement has been deployed.
    Sigstore seems to be a promising replacement, but I think further work is
    needed before this can become a key pillar for securing the open source
    ecosystem.

PGP: Grumbles & Footguns
------------------------

A recent `grumble about PGP signatures on PyPI
<https://blog.yossarian.net/2023/05/21/PGP-signatures-on-PyPI-worse-than-useless>`__
has quickly led to `PyPI dropping support for PGP
<https://blog.pypi.org/posts/2023-05-23-removing-pgp/>`__.
I'm a little torn on what to make of this.

The PGP ecosystem is difficult to make the best use of and suffers from a
conceptual design which is stuck in the 90's. This isn't helped by the most
commonly used tool, gnupg, being rather obtuse. Improvements have definitely
been made in recent years though - for example key discoverability and questions
of how much trust to give to unknown keys have been made easier by the
introduction of `keys.openpgp.org <https://keys.openpgp.org/about>`__ which
vefifies ownership of email addresses before indexing PGP keys. And the
`Sequoia-PGP <https://sequoia-pgp.org/>`__ library and command line tools bring
memory safety (Rust FTW), a cleaner API and a simpler command line interface to
users. But are these infrastructure and tooling improvements enough?

It's just fundamentally non-trivial to make use of PGP to securely sign software
releases, backup archive and other such artifacts
(we'll be ignoring the use of PGP to sign & encrypt email here as this is
another can of worms which could take up a full blog post).
For the Linux kernel, there is an extensive `Kernel Maintainer PGP guide
<https://docs.kernel.org/process/maintainer-pgp-guide.html>`__
based on the Linux Foundation's `Protecting code integrity with PGP
<https://github.com/lfit/itpol/blob/master/protecting-code-integrity.md>`__
IT policy document. There's a lot to take in here, and footguns abound.

Minisign
--------

I've seen many people point at `Minisign <https://jedisct1.github.io/minisign/>`__
as the solution. It's certainly easier to use! And somewhat harder to misuse
since it only supports a single known-good signing algorithm instead of trying
to support everything under the sun. But it lacks key features which I think are
critical to the intended use-case:

* key expiry & revocation features are needed to limit the damage which may
  occur if key material is leaked to unauthorised users.

* support for crypto smart cards & Hardware Security Modules (HSMs) is needed to
  reduce the likelihood of leaking key material in the first place.

* integration with git is needed to be able to sign commits during development
  and to sign tags at release time.

Sigstore
--------

A better solution would be `sigstore <https://www.sigstore.dev/>`__, which
simplifies the process of both signing and verifying packages without
compromising on the security of key material. It does this by using a
centralized certificate authority which issues ephemeral signing keys each time
you want to make a signature. The signer's problem then becomes one of
authentication instead of one of key management, and this problem is delegated
to OpenID Connect (OIDC) identity providers. Assuming you already have an
account with an OIDC provider supported by sigstore (Google, GitHub, etc), you
simply authenticate with your chosen ID provider to allow you to create a
sigstore signature tied to your identity. And sigstore also provides `support
for signing git commits <https://docs.sigstore.dev/gitsign/overview>`__, which
Minisign lacks.

The key assumption here is that you're willing to delegate trust to both the
sigstore root-of-trust and the limited number of existing OIDC providers. The
first of those two seems somewhat reasonable on first look, and it helps that
their `root signing tools <https://github.com/sigstore/root-signing>`__ are
open. The second is a larger assumption in my view - do we want to further
centralise the security of the open source ecosystem [1]_ around the platform
oligopoly of Microsoft, Google and co? I don't think we do. Instead, if OIDC is
going to be used in this way, we need to see a variety of other OIDC hosts who
can act as privacy-preserving, open and non-commercial identity providers for
the community. We will also need to see well-supported options for both
individuals and projects to self-host an OIDC identidy provider.

It's also worth reviewing `What Sigstore Doesn't Guarantee
<https://docs.sigstore.dev/security/#what-sigstore-doesnt-guarantee>`__. The
main issue here to me is that there is no way to mitigate compromise of an OIDC
identity or provider.

Sigstore also integrates with `Rekor <https://github.com/sigstore/rekor>`__ to
provide "an immutable tamper resistant ledger" (quoting from the readme) of
signatures. This is an excellent feature, but the benefit isn't exclusive to
sigstore as other signature types (such as Minisign signatures) can be uploaded
to the Rekor transparancy log.

On balance, I'm feeling positive about sigstore. More work is definitely needed,
both in integration with hosts like PyPI & GitHub and with support for a more
decentralised identity model. But the current state is a very good start. I'm
going to try it out for my next release of `mirrorshades
<https://pypi.org/project/mirrorshades/>`__.

Coming back to Python
---------------------

To loop back round to PyPI, my complaint is that the (somewhat poor and
atrophied) support for PGP is being dropped before a replacement has been
integrated. If sigstore does prove to be the way forward then that's great, but
I would have preferred PyPI to keep the exisiting PGP support as-is until
sigstore integration can be deployed. I don't agree that the status quo is
"worse than useless", though I do agree that it has major issues.

While we're here, we should also talk briefly about the other recent improvement
to the PyPI trust model: "Trusted Publishing", as discussed in the `PyPI Blog
<https://blog.pypi.org/posts/2023-04-20-introducing-trusted-publishers/>`__ and
the `Trail of Bits Blog
<https://blog.trailofbits.com/2023/05/23/trusted-publishing-a-new-benchmark-for-packaging-security/>`__.
Trusted Publishing allows package uploaders to authenticate with an OIDC
identity instead of a long-lived API key. My thoughts here are similar to those
above for sigstore - removing the need to manage a long-lived secret is very
welcome, but we need to have a wide array of non-commercial OIDC providers if
OIDC is going to become a foundational piece of infrastructure for open source
development.

.. rubric:: Footnotes

.. [1]
    I've deliberately avoided using the phrase "supply chain" in relation to
    open source software here.
