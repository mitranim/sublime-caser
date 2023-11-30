## Overview

Sublime Text plugin for converting between cases:

* `lower sentence case`
* `Title Sentence Case`
* `UPPER SENTENCE CASE`
* `lowerCamelCase`
* `TitleCamelCase`
* `lower_snake_case`
* `Title_snake_sase`
* `UPPER_SNAKE_CASE`
* `lower-kebab-case`
* `Title-Kebab-Case`
* `UPPER-KEBAB-CASE`
* lower initials: `li`
* upper initials: `UI`

## Installation

Navigate to Sublime's Packages folder:

    menu -> Preferences -> Browse Packages

On MacOS, this is usually:

    "/Users/<user>/Library/Application Support/Sublime Text 3/Packages"

Clone or download the repo into the Packages folder.

## Usage

* Select a few words
* Open the Command Palette via `⌘⇪P` or `^⇪P`
* Type "caser"
* Pick one of the commands
* Enjoy!

## Hotkeys

To avoid conflicts, Caser doesn't define any hotkeys. To define a hotkey:

* open menu → Preferences → Key Bindings
* insert something like the following:

```json
{
  "keys": ["ctrl+shift+c"],
  "command": "caser_lower_camel_case"
}
```

See the [`sublime-caser.sublime-commands`](sublime-caser.sublime-commands) file for the available command names.

## License

https://unlicense.org

## Misc

I'm receptive to suggestions. If this tool _almost_ satisfies you but needs changes, open an issue or chat me up. Contacts: https://mitranim.com/#contacts
