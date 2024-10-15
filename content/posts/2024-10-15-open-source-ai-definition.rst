..
   Copyright Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

The Open Source AI Definition is not fit for purpose
====================================================

:date: 2024-10-15
:tags: open-source, ai
:summary:
    The `Open Source Initiative`_ have published a release candidate version of
    their `Open Source AI Definition`_ and I expect that a version 1.0 release
    will be published soon.

    Unfortunately, I don't think that this is a good definition in its current
    form. By requiring "data information" instead of the complete corresponding
    training data, the definition cannot achieve its stated goals. This choice
    also calls into question the purpose of the definition, and may lead to a
    loss of respect for the existing Open Source definition.

    If the Open Source Initiative insists on releasing an Open Source AI
    definition, the definition must require Open Source AI Systems to include
    the release of complete corresponding training data under an open license.

The `Open Source Initiative`_ have published a release candidate version of
their `Open Source AI Definition`_ and I expect that a version 1.0 release will
be published soon.

Unfortunately, I don't think that this is a good definition in its current
form. By requiring "data information" instead of the complete corresponding
training data, the definition cannot achieve its stated goals. This choice
also calls into question the purpose of the definition, and may lead to a
loss of respect for the existing Open Source definition.

If the Open Source Initiative insists on releasing an Open Source AI definition,
the definition must require Open Source AI Systems to include the release of
complete corresponding training data under an open license.

.. _Open Source Initiative: https://opensource.org
.. _Open Source AI Definition: https://opensource.org/deepdive/drafts/the-open-source-ai-definition-1-0-rc1

.. note::
    I led a well attended and productive `discussion on the Open Source AI
    Definition at OggCamp 2024
    </posts/2024-10-13/conference-talk-lets-talk-about-the-open-source-ai-definition/>`_.
    I briefly made the same arguments I make below, and then invited others to
    contribute their opinions. I will make clear in the text which points come
    from this discussion - all other opinions shared here are my own.

    `Jamie Tanna <https://www.jvt.me/>`__ also shared `his notes from this
    discussion
    <https://www.jvt.me/posts/2024/10/13/oggcamp/#lets-talk-about-the-open-source-ai-definition>`__
    which I greatly appreciate.

Call to Action
--------------

The OSI's Open Source AI Definition is currently at the release candidate stage
and we may soon see a version 1.0 release. Now is the time to give feedback to
OSI, both directly and indirectly.

Direct feedback can be made to OSI. If you share my concerns, do not endorse the
Open Source AI Definition in its current form. Instead, `leave comments on the
text <https://hackmd.io/@opensourceinitiative/osaid-1-0-RC1>`__ and if you're
able to, `attend the upcoming town hall sessions
<https://opensource.org/deepdive#townhalls>`__ to share your feedback.

Indirect feedback can be made by sharing your own thoughts in conference talks,
blog posts, on the Fediverse, on social media sites such as LinkedIn and in
individual discussions. Such debate and consensus building needs to continue
regardless of whether the OSI releases their Open Source AI Definition in its
current form.

My argument in detail
---------------------

Will it be effective?
~~~~~~~~~~~~~~~~~~~~~

The stated aim of this definition is to identify AI systems made available under
terms which allow free (*libre*) Use, Study, Modification and Sharing. I do not
think the definition is effective in this aim.

The definition of the "Preferred form to make modifications to machine-learning
systems" specifically excludes the need to make the full training data available
under a free or open license. Instead, it requires the provision of "Data
information". At the risk of stating the obvious, "data information" is not
"data". Possessing a description of the training data and how it was obtained
does not guarantee that the recipient has the legal or technical ability to
exactly re-create the training data. And if the training process for an AI model
is followed using a similar but not exactly identical set of training data, the
resulting model weights will differ. This is not a purely academic concern -
without the ability to exactly re-run the training process and arrive at the
exact same AI model, we cannot say that we have the preferred form to make
modifications to the system. We can't answer questions like "How would the
resulting model differ if we exclude some subset of the training data" or "How
would the resulting model differ if we extend the training data", etc, if
re-training the model also introduces other differences due to our inability to
start with the exact same set of training data.

That is to say - the *effective* rights to study and modify an AI system require
access to the complete corresponding training data.

This view was shared by most of the folks who contributed to the discussion
session at OggCamp 2024. There was one counter argument that the training data
was similar to "working out" or research notes made while developing software,
and that software can be Open Source without the need to share those private
notes. There was disagreement with this analogy from others in the room.

Why is training data excluded?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given the above, and that this view seems to be widely shared, why would the
need to share training data under an open license be explicitly excluded from
the Open Source AI Definition?

The current AI hype cycle is focused on Large Language Models (LLMs) and other
large-scale generative AI models. These models require vast amounts of data to
train - so much data that no combination of truly open data sets can provide
even a fraction of the required data volume.  Instead, training data is scraped
from the internet at large without regard to the consent of authors, artists or
users. Even if training AI models on this data is considered fair use under
copyright legislation, distributing this data set in its full and original form
could never qualify as fair use.

If the OSI stated that complete corresponding training data must be shared under
an open license for an AI System to be considered Open Source, no LLM or
large-scale generative AI model could ever meet this requirement. So no LLM
could be an Open Source AI system.

And if the OSI argued that no LLM could be considered Open Source, they would
have to contend with a fear of missing out (FOMO) or fear of becoming irrelevant
if they aren't able to somehow attach themselves the current AI hype cycle.

It's worth noting that there are no freestanding community projects developing
such models - the training costs in both data and compute resources are simply
too high for such community projects to exist independently from a corporate
effort to train an AI model. These are mega-projects on the scale of a nuclear
power station or an aircraft carrier.

Smaller and more special purpose AI models do exist and do have freestanding
communities, but they are not the subject of the current hype cycle.

I would argue that this definition is targeted at the AI mega-projects, not at
the developers of smaller AI models. It is a direct attempt to stop companies
like Meta misusing the term "open source" to describe their AI systems - a thing
that they are simply not going to do. They don't respect authors, artists or
user consent, so why will they respect an Open Source AI Definition?

How does this compare to the original Open Source definition?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The original Open Source definition back in 1998 built on existing community
efforts, licenses and policies such as the Debian Free Software Guidelines. It
packaged these community values and best practices in a business-friendly way so
that could reach a new audience - it was an invitation to join an existing and
vibrant community.

This Open Source AI definition attempts to define such a community into
existence where I don't think one exists. The definition should be downstream of
the long process of community development and consensus building, not upstream
of it.

What are the likely consequences of a bad Open Source AI Definition?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I expect that the most likely outcome if the Open Source AI Definition is
released in its current form will be that it is not respected by the community.
This does actually matter! It will damage the reputation of the Open Source
Initiative and damage the integrity of Open Source as a coherent and well
understood shared vision. It will also split the efforts of the OSI between two
definitions which don't mesh together as well as they seem to think that they
do.

In the discussion session at OggCamp 2024 it was also pointed out that such a
definition would be a gift to companies like Meta, OpenAI, Anthropic, etc and
their lobbyists. It would be an independent document from a respected non-profit
organisation which they can take with them when they talk to governments about
how AI systems should be regulated.  Meta especially could argue that their AI
system meets this gold standard of being open source without having to change
their behaviour around the non-consensual collection of training data. So this
definition could weaken the position of individuals and organisations trying to
argue against these data collection practices.
