import argparse
from typing import List
from argparse import Namespace

#simple parser to collect the arguments of the server
#arguments are used by launching the main.py script from the command line and by adding parameters in the format "--<argument_name> <value>"
def parse_arguments(args_list: List[str]) -> Namespace:
    parser = argparse.ArgumentParser(description="Server for the chicken minigame",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    

    #arguments for normal usage
    parser.add_argument("--use_lan", help="specify that server is being launched from the pc in the lab using LAN connection",
                        action="store_true")
    
    parser.add_argument("--use_remote", help="specify that server is being launched from Franco's pc using remote connection",
                        action="store_true")

    parser.add_argument("--disable_shutdown", help="specify if the server has to stay on even if there are no clients connected",
                        action="store_true")

    parser.add_argument("--evaluator", choices=["PDEP", "simple"], default="PDEP", help="the evaluator that should be used")

    #arguments for simulated child (unused, simulation has been moved to simulate_main.py)
    parser.add_argument("--sim_child", help="specify that you are not expecting a client connection and just want to use the simulated child",
                        action="store_true")

    parser.add_argument("--sim_n_trials", help="number of trials for the simulation",
                        type=int, default=32)
    
    parser.add_argument("--sim_plot", help="option to enable plots at the end of the simulation", action="store_true")

    parser.add_argument("--sim_alpha", help="simulated filtering angle", type=float, default=10.0)
    parser.add_argument("--sim_sigma", help="simulated sharpening standard deviation", type=float, default=0.2)

    parser.add_argument("--sim_mock_trials", help="pick mock trials for the simulation (not fetched from lookup table)", 
                        action= "store_true")
    

    #miscellanea arguments
    parser.add_argument("--normalized_features", help= "specify that the nd-nnd space is not normalized in the range [-1,1]",
                        choices=["y","n"], default="y")
    parser.add_argument("--always_new_player", help= "if enabled, the server creates a new player in the database for every connection without trying to locate their info first",
                        action="store_true")

    parser.add_argument("--usability_test", help="set this parameter to automatically set the environment for the usability test",
                        action="store_true")

    parser.add_argument("--kids_dataset", help="use the reduced lookup table with more balanced values for kids",
                        action="store_true")

    parser.add_argument("--difficulty", choices=["regular", "easy"], default="easy", help="difficulty balance for PDEP evaluator. Should converge to an accuracy of around 65 percent for easy and 50 percent for regular")

    

    args = parser.parse_args(args_list)


    #process arguments
    args.normalized_features = True if args.normalized_features == "y" else False

    if args.use_lan and args.use_remote: 
        parser.error("you can only specify either lan or remote connection") 

    if args.usability_test:
        args.use_remote = False
        args.use_lan = True
        args.always_new_player = True
        args.disable_shutdown = True
        args.evaluator = "PDEP"
        args.kids_dataset = True

    if args.use_remote:
        args.host = '192.168.56.1'
    elif args.use_lan:
        args.host = '10.0.1.16'
    else:
        args.host = '127.0.0.1'

    print(args.host)
    args.port = 65432



    return args

    