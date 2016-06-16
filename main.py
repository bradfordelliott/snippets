#!/usr/bin/env python
import string
import sqlite3

from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web import static
import cgi
import shutil
import os

import random
import os
import sys
import shutil

import libs.snippets
root = Resource()
snippets = libs.snippets.snippets()
root.putChild("", snippets)
root.putChild("snippets", snippets)
root.putChild("css", static.File("./css"))
root.putChild("js", static.File("./js"))
root.putChild("codemirror", static.File("./codemirror"))
reactor.listenTCP(8089, server.Site(root))
reactor.run()
