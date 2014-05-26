ClusterConnect
==============
This plugin allows you to connect to different servers with a specified username.
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

2. Enable Plugin in 'Context-Menu -> Preferences -> Plugins -> ClusterConnect'

Setup
=====
1. Edit `~/.config/terminator/plugins/cluster_connect_config.py`,for example:


		CLUSTERS = {
			"test1" : {
				"user" : ["user1","user2"],
				"server" : ["server1","server2","server3","server4","server5","server6","server7","server8",],
				"groupby": True,
			},
			"test2" : {
				"user" : ["user3",],
				"server" : ["server1","server2","server3","server4",],
				"groupby": False,
			},
		}


2. Restart Terminator.

Use
===
Right click on Terminator window -> ClusterConnect -> choose a cluster to connect to
