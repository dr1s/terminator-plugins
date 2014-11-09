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

import gtk
import random
import terminatorlib.plugin as plugin



try:
	from cluster_connect_config import CLUSTERS
except ImportError:
	CLUSTERS = { "Config not found": " "}

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
			#Get users and add current to connect with current user
			users = self.get_property(cluster, 'user')
			users.sort()
			if not 'current' in users:
				users.insert(0, 'current')
				#Get servers and insert cluster for cluster connect
			servers = self.get_property(cluster, 'server')
			servers.sort()
			if len(servers) > 1:
				if not 'cluster' in servers:
					servers.insert(0, 'cluster')

			#Add a submenu for cluster servers
			if len(servers) > 1:
				#Add a submenu for server, if there is more than one
				cluster_menu_servers = gtk.MenuItem(cluster)
				submenu.append(cluster_menu_servers)
				cluster_sub_servers = gtk.Menu()
				cluster_menu_servers.set_submenu(cluster_sub_servers)
				for server in servers:
				#add submenu for users
					cluster_menu_users = gtk.MenuItem(server)
					cluster_sub_servers.append(cluster_menu_users)
					cluster_sub_users = gtk.Menu()
					cluster_menu_users.set_submenu(cluster_sub_users)
					for user in users:
						if server != 'cluster':
							self.add_split_submenu(terminal, cluster,
								user, servers, cluster_sub_users)
						else:
							menuitem = gtk.MenuItem(user)
							menuitem.connect('activate', self.connect_cluster,
								terminal, cluster, user, 'cluster')
							cluster_sub_users.append(menuitem)
			else:
				#If there is just one server, don't add a server submenu
				cluster_menu_users = gtk.MenuItem(cluster)
				submenu.append(cluster_menu_users)
				cluster_sub_users = gtk.Menu()
				cluster_menu_users.set_submenu(cluster_sub_users)
				for user in users:
					#Add menu for split and new tab
					self.add_split_submenu(terminal, cluster, user,
						servers, cluster_sub_users)


	def add_split_submenu(self, terminal, cluster, user, servers, cluster_menu_sub):
		#Add a menu if you connect to just one server

		cluster_menu_split = gtk.MenuItem(user)
		cluster_menu_sub.append(cluster_menu_split)
		cluster_sub_split = gtk.Menu()
		cluster_menu_split.set_submenu(cluster_sub_split)

		menuitem = gtk.MenuItem('Horizontal Split')
		menuitem.connect('activate', self.connect_server,
			terminal,cluster, user, servers[0], 'H')
		cluster_sub_split.append(menuitem)

		menuitem = gtk.MenuItem('Vertical Split')
		menuitem.connect('activate', self.connect_server,
			terminal, cluster, user, servers[0], 'V')
		cluster_sub_split.append(menuitem)

		menuitem = gtk.MenuItem('New Tab')
		menuitem.connect('activate', self.connect_server,
			terminal, cluster, user, servers[0], 'T')
		cluster_sub_split.append(menuitem)


	def connect_cluster(self, widget, terminal, cluster, user, server_connect):

		if CLUSTERS.has_key(cluster):
			# get the first tab and add a new one so you don't need to care
			# about which window is focused
			focussed_terminal = None
			term_window = terminal.terminator.windows[0]
			#add a new window where we connect to the servers, and switch to this tab
			term_window.tab_new(term_window.get_focussed_terminal())
			visible_terminals = term_window.get_visible_terminals()
			for visible_terminal in visible_terminals:
				if visible_terminal.vte.is_focus():
					focussed_terminal = visible_terminal

			#Create a group, if the terminals should be grouped
			servers = self.get_property(cluster, 'server')
			servers.sort()

			#Remove cluster from server, there shouldn't be a server named cluster
			if 'cluster' in servers:
				servers.remove('cluster')

			old_group = terminal.group
			if self.get_property(cluster, 'groupby'):
				groupname = cluster + "-" + str(random.randint(0, 999))
				terminal.really_create_group(term_window, groupname)
			else:
				groupname = 'none'
			self.split_terminal(focussed_terminal, servers, user,
				term_window, cluster, groupname)
			# Set old window back to the last group, as really_create_group
			# sets the window to the specified group
			terminal.set_group(term_window, old_group)


	def connect_server(self, widget, terminal, cluster, user,
			server_connect, option):

		focussed_terminal = None
		term_window = terminal.terminator.windows[0]
		#if there is just one server, connect to that server and dont split the terminal
		visible_terminals_temp = term_window.get_visible_terminals()

		if option == 'H':
			terminal.key_split_horiz()
		elif option == 'V':
			terminal.key_split_vert()
		elif option == 'T':
			term_window.tab_new(term_window.get_focussed_terminal())

		visible_terminals = term_window.get_visible_terminals()
		for visible_terminal in visible_terminals:
			if not visible_terminal in visible_terminals_temp:
				terminal2 = visible_terminal
		self.start_ssh(terminal2, user, server_connect, cluster)


	def split_terminal(self, terminal, servers, user, window, cluster, groupname):
	# Splits the window, the split count is limited by
	# the count of servers given to the function
		if self.get_property(cluster, 'groupby'):
			terminal.set_group(window, groupname)
		server_count = len(servers)

		if server_count > 1:
			visible_terminals_temp = window.get_visible_terminals()
			server1 = servers[:server_count/2]
			server2 = servers[server_count/2:]

		if server_count > 5 :
			terminal.key_split_vert()
		elif server_count > 1:
			terminal.key_split_horiz()

		if server_count > 1:
			visible_terminals = window.get_visible_terminals()
			for visible_terminal in visible_terminals:
				if not visible_terminal in visible_terminals_temp:
					terminal2 = visible_terminal
			self.split_terminal(terminal, server1, user, window,
				cluster, groupname)
			self.split_terminal(terminal2, server2, user, window,
				cluster, groupname)

		elif server_count == 1:
			self.start_ssh(terminal, user, servers[0], cluster)


	def get_property(self, cluster, prop):
		#Check if property and Cluster exsist and return if true else return false

		if CLUSTERS.has_key(cluster):
			if CLUSTERS[cluster].has_key(prop):
				return CLUSTERS[cluster][prop]
			else:
				return False
		else:
			return False


	def start_ssh(self, terminal, user, hostname, cluster):
		#Function to generate the ssh command, with specified options

		if hostname:
			command = "ssh"

			#get username, if user is current don't set user
			if user != 'current':
				command = command + " -l " + user

			#check if ssh agent should be used, if not disable it
			if self.get_property(cluster, 'agent'):
				command = command +  " -A"
			else:
				command = command +  " -a"

			#If port is configured, get that port
			port = self.get_property(cluster, 'port')
			if port:
				command = command + " -p " + port

			#If ssh-key is specified, use that key
			key = self.get_property(cluster, 'identity')
			if key:
				command = command + " -i " + key

			#get verbosity level
			verbose = self.get_property(cluster, 'verbose')
			if verbose:
				if verbose == 1:
					command = command + " -v"
				elif verbose == 2:
					command = command + " -vv"
				elif verbose == 3:
					command = command + " -vvv"

			command = command + " " + hostname

			#Check if a command was generated an pass it to the terminal
			if command[len(command) - 1] != '\n':
				command = command + '\n'
				terminal.vte.feed_child(command)
