#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 12:30:03 2018

@author: Tyler Johnson
"""

class clubs():
	
	def __init__(self, name):
		global infoList
		
		infoList  = {
			"Interact": "Description for Interact",
			"LEO Club": "Description for LEO Club",
			"Friends of Rachel": "Description for Friends of Rachel",
			"National Honor Society": "Description for National Honor Society",
			"Spanish Honor Society": "Description for Spanish Honor Society",
			"Math Honor Society": "Description for Math Honor Society",
			"History Honor Society": "Description for History Honor Society",
			"Student Council": "Description for Student Council",
			"Tri-M": "Description for Tri-M",
			}
		
		self.name = name
		self.desc = infoList[name]
		
	def __str__(self):
		return (self.name + ": " + self.desc)