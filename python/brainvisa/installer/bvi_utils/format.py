#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Methods to format the string."""


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
	characters = {
		"\"" : "&quot;",
		"'" : "&apos;",
		"<" : "&lt;",
		">" : "&gt;",
		"&" : "&amp;",
		" " : ""}
	for char, escape in characters.iteritems():
		res = res.replace(char, escape)
	return res