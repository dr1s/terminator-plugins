PROJECTS = {"Project 1": {"split": "vert",
                          "terminal1": {"split": "horiz",
                                        "terminal1": {"commands": ["dir"],
                                                      },
                                        "terminal2": {"commands": ["ls"],
                                                      }
                                        },
                          "terminal2": {"commands": ["dir"], 
                                        },
                          },
            "Project 2": {"enabled": False,
                          "split": "vert",
                          "terminal1": {"split": "horiz",
                                        "terminal1": {"commands": ["command 1",
                                                                   "command 2",
                                                                   "command 3"],
                                                      },
                                        "terminal2": {"commands": ["command"],
                                                      }
                                        },
                          "terminal2": {"split": "horiz",
                                        "terminal1": {"commands": ["command"],
                                                      },
                                        "terminal2": {"commands": ["command"],
                                                      }
                                        },
                          },
            "Project 3": {"commands": ["history", ] }
            }

EDITOR = "gedit"

