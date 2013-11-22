#!/usr/bin/env python
# -*- coding: utf-8 -*-


import platform


class System(object):
	Win32 = 'WIN32'
	Win64 = 'WIN64'
	Linux32 = 'LINUX32'
	Linux64 = 'LINUX64'
	MacOSX = 'OSX'

	@staticmethod
	def platform():
		(system, node, release, version, machine, processor) = platform.uname()
		if system == 'Windows':
			if machine == 'x86_64':
				return System.Win64
			elif machine == 'x86_32':
				return System.Win32
		elif system == 'Linux':
			if machine == 'x86_64':
				return System.Linux64
			elif machine == 'x86_32':
				return System.Linux32
		elif system == 'Darwin':
			return System.MacOSX
		return None