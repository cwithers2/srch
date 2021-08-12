#!/usr/bin/env python3
# A quick web search interface.

import argparse
import json
import math
import subprocess
import urllib.parse

from xdg import xdg_config_home, xdg_cache_home

class Program:
    config      = "srch.json"
    cache       = "srch.json"
    address     = "https://www.duckduckgo.com/?"

    #user config
    search_menu = "dmenu -p search"
    engine_menu = "dmenu -p engine -i"
    browser     = "xdg-open"

    def __init__(self):
        self.priority = {}

        self.load_config()
        self.load_cache()

        for key in self.bangs:
            if key not in self.priority:
                self.priority[key] = 1
            else:
                self.priority[key] = max(1, self.priority[key])

        highest = 1
        for key in self.bangs:
            highest = max(highest, self.priority[key])
        self.max_bytes = int(math.log2(highest)/8)+2

    def main(self, args):
        """Run the program.

        First, the user is prompted to enter a search query.
        On success, the user is prompted to select a search engine.
        Finally, the query is opened in the web-browser.

        args : dict
            A dict of settings to override at runtime.

            key="search_menu" : str
                A program to run as the search menu.

            key="engine_menu" : str
                A program to run as the engine menu.

            key="browser" : str
                A program to run as the browser.
        """
        def setval(name):
            val = getattr(args, name)
            if val:
                setattr(self, name, val[0])
        setval("search_menu")
        setval("engine_menu")
        setval("browser")

        query = self.search()
        if not len(query):
            return

        key = self.engine()
        if not len(key) or key not in self.bangs:
            return

        if key != self.default:
            self.priority[key] += 1
            self.save_cache()

        url = self.url(key, query)
        self.open(url)

    def load_config(self):
        filename = "/".join([str(xdg_config_home()), self.config])
        with open(filename) as f:
            j = json.load(f)
            self.bangs = j["bangs"]
            def setval(name):
                val = j.get(name, None)
                if val:
                    setattr(self, name, val)

            setval("default")
            setval("search_menu")
            setval("engine_menu")
            setval("browser")

    def load_cache(self):
        filename = "/".join([str(xdg_cache_home()), self.cache])
        try:
            with open(filename) as f:
                self.priority = json.load(f)
        except json.decoder.JSONDecodeError:
            #This is managable, all priorities will be set to zero later
            pass
        except FileNotFoundError:
            #touch
            with open(filename, "w") as f:
                pass

    def save_cache(self):
        filename = "/".join([str(xdg_cache_home()), self.cache])
        with open(filename, 'w') as f:
            json.dump(self.priority, f)

    def url(self, key, query):
        """Build a URL for a web-search.

        Parameters
        ----------
        key : str
            A key for dict bangs.
        query : str
            A search query.

        Raises
        ------
        KeyError
            key does not exist in bangs.

        Returns
        -------
        str
              A URL for search results."""
        params = { "q" : f"{self.bangs[key]} {query}"}
        return f"{self.address}{urllib.parse.urlencode(params)}"

    def sort(self, value):
        """Sort by priority, but keep the default value first."""
        if value == self.default:
            return b""
        else:
            prefix = (-self.priority[value]).to_bytes(
                self.max_bytes,
                byteorder="big",
                signed=True
            )
            return b"".join([prefix, value.encode()])

    def search(self):
        """Invoke the search query UI."""
        process = subprocess.Popen(
            self.search_menu,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            shell=True
        )
        process.stdin.close()
        return process.stdout.read().decode()[:-1]

    def engine(self):
        """Invoke the search engine selection UI."""
        process = subprocess.Popen(
            self.engine_menu,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            shell=True
        )
        for k in sorted(self.bangs.keys(), key=self.sort):
            process.stdin.write(f"{k}\n".encode())
        process.stdin.close()
        return process.stdout.read().decode()[:-1]

    def open(self, url):
        """Open a URL with the default web browser."""
        process = subprocess.Popen(
            " ".join([self.browser, url]),
            shell=True
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--search_menu", type=str, nargs=1,
        help="the menu command to use while prompting the user for"
        " a search query")
    parser.add_argument(
        "--engine_menu", type=str, nargs=1,
        help="the menu command to use while prompting the user for"
        " a search engine")
    parser.add_argument(
        "--browser", type=str, nargs=1,
        help="the web-browser to use")
    args = parser.parse_args()
    program = Program()
    program.main(args)
