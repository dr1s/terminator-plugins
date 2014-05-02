#!/usr/bin/python
#
#	Copyright (C) 2014 Daniel Schmitz
#	This program is free software; you can redistribute it and/or
#	modify it under the terms of the GNU General Public License
#	as published by the Free Software Foundation; either version 2
#	of the License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program; if not, write to the Free Software
#	Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import gtk
import random
import terminatorlib.plugin as plugin
from terminatorlib.translation import _


try:
	from cluster_connect_config import CLUSTERS
except ImportError:
	CLUSTERS = {}

AVAILABLE = ['ClusterConnect']

class ClusterConnect(plugin.Plugin):
	capabilities = ['terminal_menu']

	def callback(self, menuitems, menu, terminal):

		item = gtk.MenuItem('ClusterConnect')
		menuitems.append(item)
		
		submenu = gtk.Menu()
		item.set_submenu(submenu)
		
		clusters = CLUSTERS.keys()
		clusters.sort()
		for cluster in clusters:
			if not CLUSTERS[cluster].get('enabled', True):
				continue
			#If there are more then one users defined we have to split the selection for those usernames
			if len(CLUSTERS[cluster]['user']) > 1:
				users = CLUSTERS[cluster]['user']
				for user in users:
					name = cluster+" - "+user
					menuitem = gtk.MenuItem(name)
					menuitem.connect("activate", self.connect_cluster, terminal, cluster, user)
					submenu.append(menuitem)
			else:
				menuitem = gtk.MenuItem(cluster)
				menuitem.connect("activate", self.connect_cluster, terminal, cluster, CLUSTERS[cluster]['user'][0])
				submenu.append(menuitem)

		menuitem = gtk.SeparatorMenuItem()
		submenu.append(menuitem)

	
	def connect_cluster(self, widget, terminal, cluster, user):
		if CLUSTERS.has_key(cluster):
			#get the first tab and add a new one so you don't need to care about which window is focused
			focussed_terminal = None
			term_window = terminal.terminator.windows[0]
			#add a new window where we connect to the servers, and switch to this tab
			term_window.tab_new(term_window.get_focussed_terminal())
			visible_terminals = term_window.get_visible_terminals()
			for visible_terminal in visible_terminals:
				if visible_terminal.vte.is_focus():
					focussed_terminal = visible_terminal

			config = CLUSTERS[cluster]
			server_count = len(config['server'])
			servers = config['server']
			servers.sort()
			#Create a group, if the terminals should be grouped
			old_group=terminal.group
			if CLUSTERS[cluster]['groupby'] == True:
				groupname = str(random.randint(0, 1000))+"-"+cluster
				terminal.really_create_group(term_window,groupname)
			else:
				groupname='none'
			self.split_terminal(focussed_terminal, servers, user, term_window, cluster,groupname)
			#Set old window back to the last group, as really_create_group sets the window to the specified group
			terminal.set_group(term_window,old_group)


	def split_terminal(self, terminal, servers, user, window, cluster, groupname):
	# Splits the window horizontal, the split count is limited by the count of servers given to the function
		if CLUSTERS[cluster]['groupby'] == True:
			terminal.set_group(window,groupname)
		server_count=len(servers)
		if server_count == 1:
			self.connect_server(terminal, user, servers)
			server_count-=1
		if server_count > 1:
			server1=servers[:len(servers)/2]
			server2=servers[len(servers)/2:]

		visible_terminals_temp = window.get_visible_terminals()

		if server_count > 5 :
			terminal.key_split_vert()
		elif server_count-1 > 0:
			terminal.key_split_horiz()

		visible_terminals = window.get_visible_terminals()

		if server_count > 1:
			for visible_terminal in visible_terminals:
				if not visible_terminal in visible_terminals_temp:
					terminal2 = visible_terminal

		if server_count > 1:
			self.split_terminal(terminal,server1,user,window,cluster,groupname)
			self.split_terminal(terminal2,server2,user,window,cluster,groupname)
		elif server_count == 1:
			self.split_terminal(terminal,servers,user,window,cluster,groupname)


	def connect_server(self, terminal, user, hostname):
		if hostname:
			if user:
				command = "ssh " + " -l " + user + " " + hostname[0]
				if command[len(command)-1] != '\n':
					command = command + '\n'
				terminal.vte.feed_child(command)
