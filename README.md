# syntax-highlighting (NG)

[![Release](https://img.shields.io/github/downloads/cav71/syntax-highlighting-ng/total?logo=github&label=downloads)](https://github.com/cav71/syntax-highlighting-ng/releases)
[![License - GNU AGPLv3](https://img.shields.io/badge/license-%20%20GNU%20AGPLv3%20-green)](https://spdx.org/licenses/AGPL-3.0-only.html)
[![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy)

This is a new fork from the original "*Syntax Highlighting for Code*" (see [License and Credits](#license-and-credits) below).

This add-on allows you to insert syntax-highlighted code snippets into the spaced-repetition flashcard app [Anki](https://apps.ankiweb.net/).

The main reasons are:
* to fix these issues:
  [PR46](https://github.com/glutanimate/syntax-highlighting/issues/46),
  [PR47](https://github.com/glutanimate/syntax-highlighting/issues/47)
* clean port to python 3
* support for mypy/ruff linters
* adds unittests
* always target the latest Anki version (eg. 2.1) and the latest Anki python version (at the moment 3.9)

<p align="center"><img src="screenshots/screenshot_python.png"></p>


### Table of Contents <!-- omit in toc -->

<!-- MarkdownTOC levels="1,2,3" -->

- [Installation](#installation)
- [Documentation](#documentation)
- [Building](#building)
- [Contributing](#contributing)
- [License and Credits](#license-and-credits)

<!-- /MarkdownTOC -->

### Installation

#### AnkiWeb <!-- omit in toc -->

The easiest way to install Syntax Highlighting is through [AnkiWeb](https://ankiweb.net/shared/info/566351439) code `566351439`.

#### Manual installation <!-- omit in toc -->

Please click on the entry corresponding to your Anki version:

<details>

<summary><i>Anki 2.1</i></summary>

1. Make sure you have the [latest version](https://apps.ankiweb.net/#download) of Anki 2.1 installed. Earlier releases (e.g. found in various Linux distros) do not support `.ankiaddon` packages.
2. Download the latest `.ankiaddon` package from the [releases tab](https://github.com/glutanimate/syntax-highlighting/releases) (you might need to click on *Assets* below the description to reveal the download links)
3. From Anki's main window, head to *Tools* → *Add-ons*
4. Drag-and-drop the `.ankiaddon` package onto the add-ons list
5. Restart Anki

</details>

<details>

<summary><i>Anki 2.0</i></summary>
**No support for 2.0**
</details>

### Documentation

For further information on the use of this add-on please check out [the description text](docs/description.md) for AnkiWeb.

### Building

With [Anki add-on builder](https://github.com/glutanimate/anki-addon-builder/) installed:

    git clone https://github.com/glutanimate/syntax-highlighting.git
    cd syntax-highlighting
    aab build

For more information on the build process please refer to [`aab`'s documentation](https://github.com/glutanimate/anki-addon-builder/#usage).

### Contributing

Contributions are welcome! Please review the [contribution guidelines](./CONTRIBUTING.md) on how to:

- Report issues
- File pull requests
- Support the project as a non-developer

### License and Credits

*Syntax Highlighting (NG)* is

*Copyright © 2023- [Antonio Cavallo](https://github.com/cav71)*

*Syntax Highlighting* is

*Copyright © 2018-2019 [Aristotelis P.](https://glutanimate.com/) (Glutanimate)*

*Copyright © 2015 [Tim Rae](https://github.com/timrae)*

*Copyright © 2012-2015 [Tiago Barroso](https://github.com/tmbb)*


*Syntax Highlighting* is based on [*Syntax Highlighting for Code*](https://github.com/tmbb/SyntaxHighlight) by [Tiago Barroso](https://github.com/tmbb). All credit for the original add-on goes to him. A major thanks is also due for [Tim Rae](https://github.com/timrae), who extended the original add-on with CSS support.

The present fork and update to Anki 2.1 was made possible through the generous support of a fellow Anki user who would like to remain anonymous.

*Syntax Highlighting* ships with the following third-party open-source software:

- [Pygments](http://pygments.org/) v2.17.2. Copyright (c) 2006-2023 by the Pygments Team. Licensed under the BSD license.

Syntax Highlighting is free and open-source software. The add-on code that runs within Anki is released under the GNU AGPLv3 license, extended by a number of additional terms. For more information please see the [LICENSE](https://github.com/glutanimate/syntax-highlighting/blob/master/LICENSE) file that accompanied this program.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.

----

<b>
<div align="center">The continued development of this add-on is made possible <br>thanks to my <a href="https://www.patreon.com/glutanimate">Patreon</a> and <a href="https://ko-fi.com/X8X0L4YV">Ko-Fi</a> supporters.
<br>You guys rock ❤️ !</div>
</b>

