..
   Copyright (c) 2022 Paul Barker <paul@pbarker.dev>
   SPDX-License-Identifier: CC-BY-NC-4.0

New release: mirrorshades v0.2.0
================================

:date: 2022-02-15
:tags: open-source, python, mirrorshades, release-announcement
:summary: I'm happy to announce that version 0.2.0 of
          `mirrorshades <https://pypi.org/project/mirrorshades/>`_,
          a tool for mirroring data from remote sources, has been released.

This release can be downloaded from
`PyPI <https://pypi.org/project/mirrorshades/0.2.0/>`_ or
`GitHub <https://github.com/unnecessary-abstraction/mirrorshades/releases/tag/v0.2.0>`_.

The following changes have been made since the previous release (v0.1.3):

* Moved the project to GitHub, the new project URL is
  https://github.com/unnecessary-abstraction/mirrorshades.

* Added GitHub mirroring support.

* Pruned deleted branches when updating a mirrored git repository.

* Added support for multiple attempts when running custom commands.

* Added config validation using `desert <https://pypi.org/project/desert/>`_ and
  `marshmallow <https://pypi.org/project/marshmallow/>`_.

* Updated and expanded README file.

* Improved developer & contributor workflows with the addition of automatic
  linting & formatting. These checks are ran in GitHub Actions when contributing
  to the project via a pull request. They can also be ran locally using
  `pre-commit <https://pre-commit.com/>`_.

* Satisfied the `REUSE Specification <https://reuse.software/spec/>`_ to ensure
  licensing is clear.

See the `full comparison between v0.1.3 and v0.2.0
<https://github.com/unnecessary-abstraction/mirrorshades/compare/v0.1.3...v0.2.0>`_
for more details.
