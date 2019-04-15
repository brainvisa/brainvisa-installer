#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Methods to format the string."""

import six


def ifw_version(string):
    "Format to specify the version in QT"
    res = string.strip()
    res = res.replace(r'<<', r'<')
    res = res.replace(r'>>', r'>')
    res = res.replace(r';', r' ')
    return res


def ifw_name(string):
    res = string.strip()
    res = res.lower()
    res = res.replace('-', '_')
    res = res.replace(' ', '_')
    res = res.replace('.', '_')
    return res


def xml_escape(string):
    "Escape the invalid characters."
    res = string.strip()
    res = res.replace("&", "&amp;")
                      # must be first! Else &quot; => &amp;quot; etc.
    characters = {
        "\"": "&quot;",
        "'": "&apos;",
        "<": "&lt;",
        ">": "&gt;",
        " ": ""}
    for char, escape in six.iteritems(characters):
        res = res.replace(char, escape)
    return res
