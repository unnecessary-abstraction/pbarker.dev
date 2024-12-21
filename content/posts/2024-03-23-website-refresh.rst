..
   Copyright (c) 2023 Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

Website Refresh
===============

:date: 2024-03-23
:tags: meta, blog
:summary:
    Today I've deployed the new design for this website, built using `Pelican`_
    and `Tailwind CSS`_. After the changes I've made, I'm really pleased with
    the new design!

Today I've deployed the new design for this website, built using `Pelican`_ and
`Tailwind CSS`_.

.. figure:: https://img.pbarker.dev/misc/pelican.webp
   :width: 100%
   :alt: A Brown Pelican in flight against a background of grey clouds.

   Photo of a Brown Pelican in flight by Pamela Marie on `Pexels`_.

.. _Pexels: https://www.pexels.com/photo/black-and-white-bird-close-up-photography-2625816/

Pelican isn't new here, I've been using it for several years now and I've been
very happy with it. It's easy for me to work with as I'm familiar with Python
and with Jinja2 templating. I did briefly experiment with `Zola`_, but in the
end I came back to Pelican and I don't think I'll be switching away from it any
time soon.

Tailwind CSS, on the other hand, *is* new here. Previously I was using
Bootstrap, that worked pretty well but I ran into some limitations with it. I
wanted more flexibility in how I could design this site, and I wanted to fix
some mistakes I'd made in the previous design. I could probably have stayed
with Bootstrap and achieved the design improvements that I wanted, but once I
started looking into Tailwind CSS it became obvious that it was going to be
much easier for me to work with.

The new site design includes a much better looking dark mode, which is now
automatically selected based on your browser/system settings. I'm using the
`Typography`_ plugin for Tailwind CSS, which provides a clean text style for
the site. The top navigation bar no longer floats at the top of the screen as
you scroll down, improving readibility on small screens. I've also simplified
the front-page layout, so all pages on the site now share a single column
layout.

After these changes, I'm really pleased with the new design but I still have
some minor tweaks planned for the future.

For now, I'm still using `Iconify`_ to provide the `OpenMoji`_ icons and
other icons used on this site. Using iconify has kept things simple for me, but
it seems to be slowing down page loads for the site. So at some point I'll get
around to removing Iconify, and I'll instead self-host the icons that I'm using.

I also plan to improve the way my photography is hosted and displayed on this
site. That's a story for another day however...

So, I hope you enjoy the new design of my website! If you have any feedback,
you can reach out to me on `Mastodon`_ or drop me an `email`_.

.. _Pelican: https://getpelican.com/
.. _Tailwind CSS: https://tailwindcss.com/
.. _Zola: https://www.getzola.org/
.. _Typography: https://github.com/tailwindlabs/tailwindcss-typography
.. _Iconify: https://iconify.design/
.. _OpenMoji: https://openmoji.org/
.. _Mastodon: https://social.afront.org/@pbarker
.. _email: mailto:paul@pbarker.dev
