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

    parser.add_argument("--sim_child", help="specify that you are not expecting a client connection and just want to use the simulated child",
                        action="store_true")

    parser.add_argument("--sim_n_trials", help="number of trials for the simulation",
                        type=int, default=32)
    
    parser.add_argument("--sim_plot", help="option to enable plots at the end of the simulation", action="store_true")

    parser.add_argument("--sim_alpha", help="simulated filtering angle", type=float, default=10.0)
    parser.add_argument("--sim_sigma", help="simulated sharpening standard deviation", type=float, default=0.2)

    parser.add_argument("--sim_mock_trials", help="pick mock trials for the simulation (not fetched from lookup table)", 
                        action= "store_true")
    
    args = parser.parse_args(args_list)

    if args.use_lan and args.use_remote: 
        parser.error("you can only specify either lan or remote connection") 

    if args.use_remote:
        args.host = '192.168.1.30'
    elif args.use_lan:
        args.host = 'INSERT_LOCAL_LAB_ADDRESS_HERE'
    else:
        args.host = '127.0.0.1'

    args.port = 65432

    return args

    