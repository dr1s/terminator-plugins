#!/usr/bin/python
# Written by Guido Castillo Gomez <gcasgo@gmail.com>
# GPL v2 only

import os
import gtk
import terminatorlib.plugin as plugin
from terminatorlib.translation import _

try:
    from projects import PROJECTS
except ImportError:
    PROJECTS = {}

try:
    from projects import EDITOR
except ImportError:
    EDITOR = "gedit"

AVAILABLE = ['AppLauncher']


class AppLauncher(plugin.Plugin):
    capabilities = ['terminal_menu']
    
    def callback(self, menuitems, menu, terminal):
        """Add our menu item to the menu"""
        
        item = gtk.MenuItem('AppLauncher')
        menuitems.append(item)
        
        submenu = gtk.Menu()
        item.set_submenu(submenu)
        
        projects = PROJECTS.keys()
        projects.sort()
        for project in projects:
            if not PROJECTS[project].get('enabled', True):
                continue
            menuitem = gtk.MenuItem(project)
            menuitem.connect("activate", self.launch_project, terminal, project)
            submenu.append(menuitem)
        
        menuitem = gtk.SeparatorMenuItem()
        submenu.append(menuitem)
        
        menuitem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
        menuitem.connect("activate", self.configure)
        submenu.append(menuitem)
        
        #if config.has_key("default"):
        #    self.launch_project("widget", terminal, DEFAULT_PROJECT)
    
    def launch_project(self, widget, terminal, project):
        
        if PROJECTS.has_key(project):
            
            focussed_terminal = None
            widget_win = terminal.terminator.windows[0]
            widget_win.set_maximised(True)
            widget_win.tab_new(widget_win.get_focussed_terminal())
            visible_terminals = widget_win.get_visible_terminals()
            for visible_terminal in visible_terminals:
                if visible_terminal.vte.is_focus():
                    focussed_terminal = visible_terminal
            
            project_config = PROJECTS[project]
            self.split_terminal(focussed_terminal, project_config, widget_win)
    
    def split_terminal(self, terminal, terminal_config, window):
        self.execute_command(terminal, terminal_config.get('commands'))
        
        if terminal_config.has_key('split'):
            visible_terminals_temp = window.get_visible_terminals()
            if terminal_config['split'].lower().count("vert"):
                terminal.key_split_vert()
            else:
                terminal.key_split_horiz()
            visible_terminals = window.get_visible_terminals()
            
            for visible_terminal in visible_terminals:
                if not visible_terminal in visible_terminals_temp:
                    terminal2 = visible_terminal
            
            if terminal_config.has_key('terminal1'):
                self.split_terminal(terminal, terminal_config['terminal1'], window)
            if terminal_config.has_key('terminal2'):
                self.split_terminal(terminal2, terminal_config['terminal2'], window)
    
    def execute_command(self, terminal, command):
        if command:
            if isinstance(command, list):
                command = "\n".join(command)
            else:
                command = command
            if command[len(command)-1] != '\n':
                command = command + '\n'
            terminal.vte.feed_child(command)
    
    def configure(self, widget):
        filename = os.path.realpath(os.path.join(os.path.dirname(__file__), 'projects.py'))
        editor = os.getenv('EDITOR') or EDITOR
        os.system('%s %s' % (editor, filename))

