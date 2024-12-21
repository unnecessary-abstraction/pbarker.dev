..
   Copyright Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

A quick bash/zsh tip
====================

:date: 2024-04-19
:tags: linux, bash, blog
:summary:
    ``!`` is a valid character you can use in a bash/zsh alias. And as a bonus,
    it's not used in the name of any common commands!

Here's a quick tip to improve your bash/zsh life.

``!`` is a valid character you can use in an alias. I use it to mark aliases which
run under sudo, for example on my Debian box I have:

.. code-block:: shell

   alias e!="sudo ${EDITOR}"
   alias a!="sudo apt"
   alias s!="sudo systemctl"
   alias in!="sudo apt install"

As a bonus, ``!`` doesn't seem to be used in the names of any other commands I
have installed. I can't remember ever seeing a command with ``!`` in its name, so
you should be safe with this. If I'm wrong, please `put me right on Mastodon
<https://social.afront.org/@pbarker>`__!

That's it. That's the post. I usually write longer things, but I posted this tip
on Mastodon and people seemed to like it, so it should also exist here.
