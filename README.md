# srch.py
_srch_ is a power tool that combines the web-searching power of [_bangs_](https://duckduckgo.com/bang) with the speed and ease of the [`dmenu`](https://tools.suckless.org/dmenu/) GUI.

![](https://media.giphy.com/media/57sBXVtmPpGGcWhxp6/giphy.gif)

With _srch_ you can select which search engine to use for every search, _quickly_.

## Features
- high configurability
- automatically sort search engines by number of times used (alphabetically on ties)

## Dependencies
- Python module `XDG`
- `dmenu` is called by default, but [`rofi`](https://github.com/davatorium/rofi) can be configured for use in its place.

## Installing
- place `srch.py` in your executable path
- place _srch.json_ in your XDG compatible config directory (most-likely $HOME/.config/ if you are unsure)

## Configuring
Changes can be made to _srch.json_ to change the `dmenu` calls, the enabled search engines, and the web browser to use.

### Changing `dmenu` calls
In _srch.json_, the `"search_menu"` and `"engine_menu"` keys both describe `dmenu` calls. By default their values are `"dmenu -p search"` and `"dmenu -p engine -i"`, respectfully. These can be modified like normal `dmenu` commands or replaced with `rofi` commands (in `dmenu` mode).

### Changing the enabled search engines
The search engines shown to the user are stored as an object labeled `"bangs"`. Key:values in `"bangs"` are of the form:

    "A readable display name" : "some bang"

where `"some bang"` is a valid bang associated with a search engine e.g. `!?`, `!g`, `!w`, etc.

See [this page](https://duckduckgo.com/bang) for a list of supported search engines and their associated _bangs_.

#### Setting the default search engine
You can also set the first-most displayed search engine by setting the value of the `"default"` key to a key existing in the `"bangs"` object e.g. `"default" : "DuckDuckGo"` or `"default" : "Google"`.

### Changing the web browser
The web browser to use can be specified with the `"browser"` key. Its value by default is `"xdg-open"`. To set firefox as the default browser, for example:

    "browser" : "firefox"
