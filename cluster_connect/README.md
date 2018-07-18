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
The master branch currently features the GTK3 version of this plugin. The GTK2 version can be found in the branch 'gtk2'.

1. Put files in `~/.config/terminator/plugins/`:

        git clone https://github.com/dr1s/terminator-plugins.git
        mkdir -p ~/.config/terminator/plugins
        cp terminator-plugins/cluster_connect/cluster_connect.py ~/.config/terminator/plugins/
        cp -r terminator-plugins/cluster_connect/cluster_connect_config ~/.config/terminator/plugins/
	Add config to ~/.config/terminator/plugins/cluster_connect_config in json-format

2. Edit `~/.config/terminator/plugins/cluster_connect_config.py`, for example:

  See: cluster_connect_config/config.json

	Options:

		- user: Array of Usernames
		- server: Array of servers ip or hostnames. The plugin just passes it to ssh
		- groupby: True or False, If you specify as true the terminals will be grouped.
			Your sending the commands to the whole group from the start.
		- agent: True or False, if true then ssh agent is enabled and -A Option is added to command
		- port: set ssh port to something else than default
		- identity: specify path to a ssh-key-file
		- verbose: 1, 2 or 3 for -v, -vv or -vvv
		- current_user: True or False, if set to False user current, won't be displayed in submenu
			default: True
		- horiz_splits: Number of hoirzontal splits before doing a vertical split, default: 5
		- sudouser: Array of Usernames which will be called after the login with you user with `sudo -su`
		- group: Group name for submenu

3. Restart Terminator.

4. Enable Plugin in `Context-Menu -> Preferences -> Plugins -> ClusterConnect`


Use
===
Right click on `Terminator window -> ClusterConnect`
