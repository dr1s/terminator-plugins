ClusterConnect
==============
This plugin allows you to connect to servers in configured clusters with a specified username.
You are able to connect to single servers in a cluster or the whole cluster.
It adds a new tab to Terminator and splits the window as needed.



If you specify groupby as True the plugin adds the new terminals to a group.
You will be able to send the same commands to all servers.
Be carful in using this feature, as you are probably typing to a lot of servers simultaneously!
Autocomplete and such should be used very carefully.


Installation
============
1. Put files in `~/.config/terminator/plugins/`:

        mkdir -p ~/.config/terminator/plugins
        cp cluster_connect.py ~/.config/terminator/plugins/
        cp cluster_connect_config.py ~/.config/terminator/plugins/


2. Edit `~/.config/terminator/plugins/cluster_connect_config.py`,for example:
Options:
  - user: Array of Usernames
  - server: Array of servers ip or hostnames. The plugin just passes it to ssh
  - groupby: True or False, If you specify as true the terminals will be grouped.
           Your sending the commands to the whole group from the start.
  - agent: True or False, if true then ssh agent is enabled and -A Option is added to command



		CLUSTERS = {
			"test1" : {
				"user" : ["user1","user2"],
				"server" : ["server1","server2","server3","server4","server5","server6","server7","server8",],
				"groupby": True,
        "agent": False,
			},
			"test2" : {
				"user" : ["user3",],
				"server" : ["server1","server2","server3","server4",],
				"groupby": False,
        "agent": True,
			},
		}

3. Restart Terminator.

4. Enable Plugin in `Context-Menu -> Preferences -> Plugins -> ClusterConnect`


Use
===
Right click on `Terminator window -> ClusterConnect`
