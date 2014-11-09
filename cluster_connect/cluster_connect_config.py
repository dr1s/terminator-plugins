CLUSTERS = {

	"test8" : {
		"user" : ["user1","user2","user3",],
		"server" : ["test1","test2","test3","test4","test5","test6","test7","test8"],
		"groupby": True,
		"agent": True,
	},

	"test6" : {
		"user" : ["user1","user2","user3",],
		"server" : ["test1","test2","test3","test4","test5","test6",],
		"groupby": True,
		"agent": False,
		"identity": "~/.ssh/test_rsa"
	},

	"test3" : {
		"user" : ["user1","user2","user3",],
		"server" : ["test1","test2","test3",],
		"groupby": True,
		"agent": True,
		"port": 2223,
		"verbose": 2,
	},

}
