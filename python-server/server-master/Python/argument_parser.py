import argparse
from typing import List
from argparse import Namespace

#simple parser to collect the arguments of the server
#arguments are used by launching the main.py script from the command line and by adding parameters in the format "--<argument_name> <value>"
def parse_arguments(args_list: List[str]) -> Namespace:
    parser = argparse.ArgumentParser(description="Server for the chicken minigame",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--use_lan", help="specify that server is being launched from the pc in the lab using LAN connection",
                        action="store_true")
    
    parser.add_argument("--use_remote", help="specify that server is being launched from Franco's pc using remote connection",
                        action="store_true")

    parser.add_argument("--disable_shutdown", help="specify if the server has to stay on even if there are no clients connected",
                        action="store_true")
    
    parser.add_argument("--always_new_player", help= "if enabled, the server creates a new player in the database for every connection without trying to locate their info first",
                        action="store_true")

    parser.add_argument("--usability_test", help="set this parameter to automatically set the environment for the usability test",
                        action="store_true")

    parser.add_argument("--kids_dataset", help="use the reduced lookup table with more balanced values for kids",
                        action="store_true")

    args = parser.parse_args(args_list)

    if args.use_lan and args.use_remote: 
        parser.error("you can only specify either lan or remote connection") 

    if args.usability_test:
        args.use_remote = False
        args.use_lan = True
        args.always_new_player = True
        args.disable_shutdown = True
        args.kids_dataset = True

    if args.use_remote:
        args.host = '192.168.1.30'
    elif args.use_lan:
        args.host = '192.168.1.30'
    else:
        args.host = '127.0.0.1'

    print(args.host)
    args.port = 65432



    return args

    