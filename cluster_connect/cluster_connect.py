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
	CLUSTERS = {}

AVAILABLE = ['ClusterConnect']

class ClusterConnect(plugin.Plugin):
	capabilities = ['terminal_menu']


	def get_property(self, cluster, prop):
		#Check if property and Cluster exsist and return if true else return false

		if CLUSTERS.has_key(cluster):
			if CLUSTERS[cluster].has_key(prop):
				return CLUSTERS[cluster][prop]
			else:
				return False
		else:
			return False


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
				users.insert(0,'current')
				#Get servers and insert all for cluster connect
			servers = self.get_property(cluster, 'server')
			servers.sort()
			if len(servers) > 1:
				if not 'all' in servers:
					servers.insert(0, 'all')

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
						menuitem = gtk.MenuItem(user)
						if server != "all":
							menuitem.connect("activate", self.connect_cluster,
								terminal,cluster, user, server)
						else:
							menuitem.connect("activate", self.connect_cluster,
								terminal, cluster, user, 'cluster')
						cluster_sub_users.append(menuitem)
			else:
				#If there is just one server, don't add a server submenu
				cluster_menu_users = gtk.MenuItem(cluster)
				submenu.append(cluster_menu_users)
				cluster_sub_users = gtk.Menu()
				cluster_menu_users.set_submenu(cluster_sub_users)
				for user in users:
					menuitem = gtk.MenuItem(user)
					menuitem.connect("activate", self.connect_cluster, terminal,
							cluster, user, servers[0])
					cluster_sub_users.append(menuitem)


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

			if server_connect != 'cluster':
				#if there is just one server, connect to that server and dont split the terminal
				self.connect_server(focussed_terminal, user, server_connect, cluster)
			else:
				#Create a group, if the terminals should be grouped
				servers = self.get_property(cluster, 'server')
				servers.sort()

				#Remove all from server, there shouldn't be a server named all
				if 'all' in servers:
					servers.remove('all')

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


	def split_terminal(self, terminal, servers, user, window, cluster, groupname):
	# Splits the window, the split count is limited by
	# the count of servers given to the function
		if self.get_property(cluster,'groupby'):
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
			self.split_terminal(terminal, server1, user, window, cluster, groupname)
			self.split_terminal(terminal2, server2, user, window, cluster, groupname)

		elif server_count == 1:
			self.connect_server(terminal, user, servers[0], cluster)


	def connect_server(self, terminal, user, hostname, cluster):
		#Function to generate the ssh command, with specified options

		if hostname:
			command = "ssh"

			#get username, if user is current don't set user
			if user != "current":
				command = command + " -l " + user

			#check if ssh agent should be used, if not disable it
			if self.get_property(cluster,'agent'):
				command = command +  " -A"
			else:
				command = command +  " -a"

			#If port is configured, get that port
			port = self.get_property(cluster,'port')
			if port:
				command = command + " -p " + port

			#If ssh-key is specified, use that key
			key = self.get_property(cluster,'identity')
			if key:
				command = command + " -i " + identity

			#get verbosity level
			verbose = self.get_proptery(cluster,"verbose")
			if verbose:
				if verbose == 1:
					command = command + " -v"
				elif verbose == 2:
					command = command + " -vv"
				elif verbose == 3:
					command = command + " -vvv"

			#Check if a command was generated an pass it to the terminal
			if command[len(command) - 1] != '\n':
				command = command + '\n'
				terminal.vte.feed_child(command)
