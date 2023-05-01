import unittest
from AI.ai_utils import *
from AI.TrialAdapter import TrialAdapter
from AI.ai_plot import plot_trials, FigSaver
from AI.PDEP_Evaluator import PDEP_Evaluator
from AI.AS_functionals import *
from AI.ai_consts import *
from AI.AS_Estimate import ASD_Estimator
from dummy_client_handler import SimulatedClient
import time
import os
import winsound

BASE_PATH_FOR_PICS = ".\\experiments"
BASE_PATH_FOR_SAVING_TRIALS = ".\\AI\\precomputed_data"
PATH_FOR_CONST = ".\\AI\\precomputed_data\\PDEP\\consts\\C.npy"

if os.path.exists(BASE_PATH_FOR_PICS) == False:
    os.mkdir(BASE_PATH_FOR_PICS)
    pdep = os.path.join(BASE_PATH_FOR_PICS, "PDEP")
    default = os.path.join(BASE_PATH_FOR_PICS, "simple")

    os.mkdir(pdep)
    os.mkdir(default)


class SimulationsRunner(unittest.TestCase):
    def __init__(   self, 
                    days:int, 
                    trials_per_day:int, 
                    fig_interval: int, 
                    evaluator: str, 
                    kids_ds: bool, 
                    update_evaluator_stats:bool, 
                    update_child: bool, 
                    suite_name: str, 
                    target_prob: float, 
                    target_diff: Tuple[float,float], 
                    mode:str, 
                    save_trials: bool, 
                    save_plots: bool,
                    alphas: List[float], 
                    sigmas: List[float], 
                    mock: bool, 
                    estimate_step: int, 
                    target_Cs: np.ndarray,
                    make_plots: bool, 
                    save_ablation: bool,
                    estimation_duration: int,
                    estimator_type: str,
                    init_evaluator_stats: bool,
                    estimator_max_trials: int,
                    estimator_min_trials: int,
                    improver_type: str,
                    improver_parameters: List[float],
                    difficulty: str):
        
        self.days = days
        self.trials_per_day = trials_per_day
        self.interval = fig_interval
        self.evaluator = evaluator
        self.kids_ds = kids_ds
        self.add_date = False
        self.update_evaluator_stats = update_evaluator_stats
        self.update_child = update_child
        self.target_prob = target_prob
        self.target_diff = target_diff
        self.mode = mode
        self.save_trials = save_trials
        self.save_plots = save_plots
        self.alphas = alphas
        self.sigmas = sigmas
        self.mock = mock
        self.estimate_step = estimate_step
        self.target_C = target_Cs
        self.make_plots = make_plots
        self.save_ablation = save_ablation
        self.estimation_duration = estimation_duration
        self.estimator_type = estimator_type
        self.init_evaluator_stats = init_evaluator_stats
        self.estimator_max_trials = estimator_max_trials
        self.improver_type = improver_type
        self.improver_parameters = improver_parameters
        self.estimator_min_trials = estimator_min_trials
        self.difficulty = difficulty

        self.base_root = os.path.join(BASE_PATH_FOR_PICS, self.evaluator)
        self.base_root = os.path.join(self.base_root, suite_name)
        if os.path.exists(self.base_root) == False and self.save_plots:
            os.mkdir(self.base_root)

        self.save_root = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, self.evaluator)
        self.save_root = os.path.join(self.save_root, suite_name)
        if os.path.exists(self.save_root) == False and (self.save_trials or self.save_ablation):
            os.mkdir(self.save_root)
        
    
    def simulation_suite(self):
        sim_alpha_hist = []
        sim_sigma_hist = []
        e_alpha_hist = []
        e_sigma_hist = []
        trials = []
        preds = []
        for alpha in self.alphas:
            for sigma in self.sigmas:
                exp_name = f"alpha_{alpha}_sigma_{int(sigma*100)}"
                save_file = os.path.join(self.save_root, exp_name) if self.save_trials else None
                handler = SimulatedClient(  0.5,0.5, alpha=alpha, sigma=sigma, evaluator=self.evaluator, kids_ds=kids_ds, 
                                            save_file=save_file, estimation_duration=self.estimation_duration, 
                                            estimator_type=self.estimator_type, init_evaluator=self.init_evaluator_stats,
                                            estimator_max_trials=self.estimator_max_trials, estimator_min_trials=self.estimator_min_trials,
                                            improver_type=self.improver_type, improver_parameters=self.improver_parameters, difficulty=self.difficulty)
                
                if self.evaluator == "PDEP":
                    handler.player_evaluator.target_error_prob = self.target_prob
                    handler.player_evaluator.trial_adapter.mock = self.mock
                    handler.player_evaluator.estimate_step = self.estimate_step
                else:
                    handler.player_evaluator.running_results['filtering_diff'] = self.target_diff[0]
                    handler.player_evaluator.running_results['sharpening_diff'] = self.target_diff[1]
                    handler.player_evaluator.mode = mode
                    handler.player_evaluator.always_update_step = True
                figsaver = FigSaver(self.base_root, exp_name, interval=self.interval) if self.save_plots else None
                (ea, es), (sa, ss),(ts, pds) = handler.simulate_player_cycle(self.days, self.trials_per_day, False, self.update_evaluator_stats,self.update_child, figsaver=figsaver, make_plots=self.make_plots)
                sim_alpha_hist.append(sa)
                sim_sigma_hist.append(ss)
                e_alpha_hist.append(ea)
                e_sigma_hist.append(es)
                trials.append(ts)
                preds.append(pds)

        
        return (e_alpha_hist, e_sigma_hist), (sim_alpha_hist, sim_sigma_hist), (trials, preds)

    def ablation_C(self, last_n_days: int, n_runs: int):
        target_C = np.array(self.target_C)
        i_C = np.arange(target_C.shape[0])

        alpha_errors_by_config = np.zeros((len(self.alphas)*len(self.sigmas), target_C.shape[0]))
        sigma_errors_by_config = np.zeros((len(self.alphas)*len(self.sigmas), target_C.shape[0]))

        configs = np.array([[alpha, sigma] for alpha in self.alphas for sigma in self.sigmas])
        i_configs = [i for i in range(0, len(configs))]
        
        print(f"starting config: {configs}")
        print(f"target Cs: {target_C}")

        for i_c, c in zip(i_C, target_C):
            np.save(PATH_FOR_CONST, np.array([c]))
            print(f">>> Making run with C = {c}")
            for _ in range(0,n_runs):
                (e_a_h, e_s_h), (s_a_h, s_s_h), _ = self.simulation_suite()
                e_a_h = np.array(e_a_h)[:, -last_n_days:]
                print(e_a_h.shape)
                e_s_h = np.array(e_s_h)[:, -last_n_days:]
                s_a_h = np.array(s_a_h)[:, -last_n_days:]
                s_s_h = np.array(s_s_h)[:, -last_n_days:]

                avg_error_a = np.abs(e_a_h-s_a_h).sum(axis = 1)/last_n_days
                avg_error_s = np.abs(e_s_h - s_s_h).sum(axis=1)/last_n_days

                for i, error_for_config in enumerate(avg_error_a):
                    alpha_errors_by_config[i, i_c] += error_for_config
            
                for i, error_for_config in enumerate(avg_error_s):
                    sigma_errors_by_config[i, i_c] += error_for_config

        alpha_errors_by_config = alpha_errors_by_config/MAX_ALPHA
        sigma_errors_by_config = sigma_errors_by_config/MAX_SIGMA

        best_Cs_by_config = np.argmin(alpha_errors_by_config, axis=1)

        if self.save_ablation:
            save_file = os.path.join(self.save_root, "best_Cs.npy")
            np.save(save_file, best_Cs_by_config)

            save_file = os.path.join(self.save_root, "configs.npy")
            np.save(save_file, configs)

            save_file = os.path.join(self.save_root, "Cs.npy")
            np.save(save_file, target_C)

            save_file = os.path.join(self.save_root, "alpha_errors_by_Cs.npy")
            np.save(save_file, alpha_errors_by_config)

            save_file = os.path.join(self.save_root, "sigma_errors_by_Cs.npy")
            np.save(save_file, sigma_errors_by_config)

        print(f"best Cs:")
        print(best_Cs_by_config)
        print("-------------")

    def ablation_n_trials(self, target_slopes: List[float], target_max_ns: List[float], n_runs:int):
        print(target_slopes)
        print(target_max_ns)
        
        target_slopes=np.array(target_slopes)
        target_max_ns = np.array(target_max_ns)
        alpha_errors_by_config = np.zeros((len(target_slopes), len(target_max_ns)))
        sigma_errors_by_config = np.zeros((len(target_slopes), len(target_max_ns)))
        configs = np.array([target_slopes])
        i_configs = [i for i in range(0, len(configs))]

        for i, ts in enumerate(target_slopes):
            self.improver_parameters = [ts*MAX_ALPHA, ts*MAX_SIGMA, 1]
            self.estimator_max_trials = 180
            print(f">>> Making run with slope = {ts}")
            for _ in range(0, n_runs):
                (e_a_h, e_s_h), (s_a_h, s_s_h), (gen_trials, gen_preds) = self.simulation_suite()

                s_a_h = np.array(s_a_h)
                s_s_h = np.array(s_s_h)

                for j, max_n in enumerate(target_max_ns):
                    estimator = ASD_Estimator(max_n, denoiser_type="simple_denoising")
                    estimator.trials = gen_trials[0]
                    estimator.predictions = gen_preds[0]

                    sp_a, sp_s, _ = estimator.second_pass_estimation(e_a_h[0], e_s_h[0])

                    avg_error_a = np.average(np.abs(sp_a-s_a_h[0]))
                    avg_error_s = np.average(np.abs(sp_s-s_s_h[0]))

                    alpha_errors_by_config[i, j] += avg_error_a
                    sigma_errors_by_config[i, j] += avg_error_s
                
            alpha_errors_by_config[i, :]/=n_runs
            sigma_errors_by_config[i, :]/=n_runs
            best_i = np.argmin(alpha_errors_by_config[i] + sigma_errors_by_config[i])
            print(f">>> best found is {target_max_ns[best_i]}")

        alpha_errors_by_config = alpha_errors_by_config/MAX_ALPHA
        sigma_errors_by_config = sigma_errors_by_config/MAX_SIGMA

        best_Ns_by_config = np.argmin(alpha_errors_by_config + sigma_errors_by_config, axis=1)

        if self.save_ablation:
            save_file = os.path.join(self.save_root, "best_n_trials_index.npy")
            np.save(save_file, best_Ns_by_config)

            save_file = os.path.join(self.save_root, "slope_configs.npy")
            np.save(save_file, configs)

            save_file = os.path.join(self.save_root, "n_trials.npy")
            np.save(save_file, target_max_ns)

            save_file = os.path.join(self.save_root, "alpha_errors_by_Ns.npy")
            np.save(save_file, alpha_errors_by_config)

            save_file = os.path.join(self.save_root, "sigma_errors_by_Ns.npy")
            np.save(save_file, sigma_errors_by_config)
        
        print(f"best Ns:")
        print(best_Ns_by_config)
        print("-------------")
    
if __name__ == "__main__":

    alphas = [
        [10, 30, 60],
        [45],
        [65],
        [10, 20,30,40,50,60, 70, 80],
        [10],
        [MAX_ALPHA-10],
        [30],
        [75],
        [55],
        ]
    sigmas = [
        [0.10, 0.20, 0.4],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5],
        [0.2],
        [0.1],
        [0.3],
        [MAX_SIGMA-0.1],
        [0.10, 0.4]
        ]
    alpha_i = 8
    sigma_i = 5


    probs = [0.10, 0.30, 0.80]
    diffs = [(0.1,0.1), (0.4, 0.4), (0.8, 0.8), (0.95,0.95)]
    modes = ["filtering", "sharpening"]

    days =15
    trials_per_day = 15
    interval = 15

    evaluator = "PDEP"
    kids_ds = False
    add_date = False
    update_evaluator_stats = True
    init_evaluator_stats = False

    target_prob = probs[2]
    target_diff = diffs[0]
    mode = modes[0]
    save_trials = False
    save_plots = True

    mock = True
    estimate_step = 1
    target_C = np.logspace(-2, 3, 6, base=10)
    last_n_days = 500

    target_n_trials = np.linspace(100, 1800, 18)
    target_slopes = -np.logspace(-4, -2, 10, base=10)/trials_per_day
    
    local_target_slope = target_slopes[8]
    update_child = True
    improver_parameters_options =   [
                                        [0.45, 0.003, 1],
                                        [-0.3/trials_per_day, -0.002/trials_per_day, 1],
                                        [-0.05/trials_per_day, -0.0002/trials_per_day, 1],
                                        [-0.7/trials_per_day, -0.005/trials_per_day, 1],
                                        [local_target_slope*MAX_ALPHA, local_target_slope*MAX_SIGMA, 1]                                  
                                    ]

    pars_i = 4
    improver_type_options = ["normal", "linear", "linear", "linear", "linear"]
    improver_type = improver_type_options[pars_i]


    estimation_duration = 1
    estimator_type = "ASD"
    estimator_max_trials = 180
    estimator_min_trials = 50

    make_plots = True
    save_ablation = False
    n_runs = 2
    suite_name = "example_sim"
    difficulties = ["regular", "easy"]
    diff_i = 1

    sr = SimulationsRunner( days, trials_per_day, interval, evaluator, kids_ds, update_evaluator_stats, update_child, suite_name, 
                            target_prob, target_diff, mode, save_trials, save_plots, alphas[alpha_i], sigmas[sigma_i], mock, estimate_step,
                            target_C, make_plots, save_ablation, estimation_duration, 
                            estimator_type, init_evaluator_stats, estimator_max_trials, estimator_min_trials,improver_type, 
                            improver_parameters_options[pars_i], difficulties[diff_i])

    start_time = time.time()

    sr.simulation_suite()
    #sr.ablation_C(last_n_days, n_runs)
    #sr.ablation_n_trials(target_slopes, target_n_trials, n_runs)
    discarded_slopes_i = [0,1,2,3,4,5]

    perform_multiple_suites = False
    for i in range(0,len(target_slopes)+1):
        if perform_multiple_suites == False:
            break
        if i in discarded_slopes_i:
            continue
        if i == len(target_slopes):
            update_child = False
            print("slope is none")
        else:
            local_target_slope = target_slopes[i]
            print(f">>>>> slope is {local_target_slope}")
        

        suite_name = f"unified_plots_easy_v3_{i}"
        sr = SimulationsRunner( days, trials_per_day, interval, evaluator, kids_ds, update_evaluator_stats, update_child, suite_name, 
                            target_prob, target_diff, mode, save_trials, save_plots, alphas[alpha_i], sigmas[sigma_i], mock, estimate_step,
                            target_C, make_plots, save_ablation, estimation_duration, 
                            estimator_type, init_evaluator_stats, estimator_max_trials, estimator_min_trials,improver_type, 
                            [local_target_slope*MAX_ALPHA, local_target_slope*MAX_SIGMA, 1], difficulties[diff_i])
        sr.simulation_suite()


    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    print("--- %s seconds ---" % (time.time() - start_time))