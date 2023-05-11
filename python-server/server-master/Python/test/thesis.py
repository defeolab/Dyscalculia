import unittest
from AI.ai_utils import *
from AI.TrialAdapter import TrialAdapter
from AI.ai_plot import *
from AI.ImprovementHandler import *
from AI.PDEP_Evaluator import PDEP_Evaluator
from server_utils.dummy_client_handler import SimulatedClient
from AI.PlayerSimulator import PlayerSimulator
from AI.AS_Estimate import ASD_Estimator, ASE_Estimator
from AI.PDEP_functionals import *
from AI.AS_functionals import *
from sklearn.svm import LinearSVC
import time
import os
import functools
import scipy as sp
import matplotlib.pyplot as plt
from AI.ai_consts import *

import winsound

BASE_PATH_FOR_PICS = ".\\experiments"
BASE_PATH_FOR_CASUAL_PICS = "C:\\Users\\fblan\\Desktop\\thesis pics\\test"

BASE_PATH_FOR_SAVING_TRIALS = ".\\AI\\precomputed_data"

class MakePlots():
    def __init__(self):
        pass

        
    def test_joint_plots(self):
        root_path = os.path.join(BASE_PATH_FOR_PICS, "PDEP")
        target_slopes = -np.logspace(-4, -2, 10, base=10)
        target_slopes = target_slopes[6:]
        labels = [f"Daily Slope = {round(t, 2)}°" for t in target_slopes*MAX_ALPHA]
        labels.append("Null slope")
        folder_prefix = "unified_plots_easy_v3_"
        subfolder_name="alpha_55_sigma_30"

        plot_comparisons(root_path, labels, monthly=True, folder_prefix=folder_prefix, suffix_set=[str(i) for i in range(6,10+1)], title="Second Pass alpha", xlabel="day", plot_dists=True, subfolder_name=subfolder_name)

        labels = [f"Daily Slope = {round(t, 4)} units" for t in target_slopes*MAX_SIGMA]
        labels.append("Null slope")
        plot_comparisons(root_path, labels, monthly=True, suffix_set=[str(i) for i in range(6,10+1)], title="Second Pass Sigma", xlabel="day", metric_name="second_pass_sigma", main_stat="sigma", subfolder_name=subfolder_name, plot_dists=True,folder_prefix=folder_prefix)

        labels = [f"Daily Unified Slope = {round(t, 4)} units" for t in target_slopes]
        labels.append("Null slope")
        plot_comparisons(root_path, labels, monthly=False, suffix_set=[str(i) for i in range(6,10+1)], title="Accuracy (easy mode)", xlabel="day", metric_name="cumulative_accuracy", main_stat="accuracy", subfolder_name=subfolder_name, xlength=60,folder_prefix=folder_prefix)

        labels = [f"Daily Unified Slope = {round(t, 4)} units" for t in target_slopes]
        labels.append("Null slope")
        plot_comparisons(root_path, labels, monthly=False, suffix_set=[str(i) for i in range(6,10+1)], title="Accuracy (regular mode)", xlabel="day", metric_name="cumulative_accuracy", main_stat="accuracy", subfolder_name=subfolder_name, xlength=60,folder_prefix=folder_prefix)
        """
        plot_comparisons(root_path, labels, monthly=True, folder_prefix=folder_prefix, suffix_set=[str(i) for i in range(6,10+1)], title="Second Pass alpha", xlabel="day", plot_dists=True)

        labels = [f"Daily Slope = {round(t, 4)} units" for t in target_slopes*MAX_SIGMA]
        labels.append("Null slope")
        plot_comparisons(root_path, labels, monthly=True, suffix_set=[str(i) for i in range(6,10+1)], title="Second Pass Sigma", xlabel="day", metric_name="second_pass_sigma", main_stat="sigma", subfolder_name="alpha_30_sigma_30", plot_dists=True)

        labels = [f"Daily Unified Slope = {round(t, 4)} units" for t in target_slopes]
        labels.append("Null slope")
        plot_comparisons(root_path, labels, monthly=False, suffix_set=[str(i) for i in range(6,10+1)], title="Accuracy (easy mode)", xlabel="day", metric_name="cumulative_accuracy", main_stat="accuracy", subfolder_name="alpha_75_sigma_40", xlength=65)

        labels = [f"Daily Unified Slope = {round(t, 4)} units" for t in target_slopes]
        labels.append("Null slope")
        plot_comparisons(root_path, labels, monthly=False, suffix_set=[str(i) for i in range(6,10+1)], title="Accuracy (regular mode)", xlabel="day", metric_name="cumulative_accuracty", main_stat="accuracy", subfolder_name="alpha_80_sigma_40", xlength=65)
        """
    def test_joint_plots_6M(self):
        root_path = os.path.join(BASE_PATH_FOR_PICS, "PDEP")
        target_slopes = -np.logspace(-4, -2, 10, base=10)
        from_index = 7
        target_slopes = target_slopes[from_index:]
        target_slopes = target_slopes/3
        labels = [f"Daily Slope = {round(t, 2)}°" for t in target_slopes*MAX_ALPHA]
        labels.append("Null slope")
        folder_prefix = "unified_plots_easy_v2_"
        subfolder_name="alpha_55_sigma_30"
        xlength = 65

        target_slopes = target_slopes/3
        plot_comparisons(root_path, labels, monthly=True, folder_prefix=folder_prefix, suffix_set=[str(i) for i in range(from_index,10+1)], xlength=xlength,
                         title="Second Pass alpha", xlabel="day", plot_dists=False, subfolder_name=subfolder_name, monthlyfy=True)

        labels = [f"Daily Slope = {round(t, 4)} units" for t in target_slopes*MAX_SIGMA]
        labels.append("Null slope")
        plot_comparisons(root_path, labels, monthly=True, suffix_set=[str(i) for i in range(from_index,10+1)], xlength=xlength,
                         title="Second Pass Sigma", xlabel="day", metric_name="second_pass_sigma", main_stat="sigma", 
                         subfolder_name=subfolder_name, plot_dists=False,folder_prefix=folder_prefix, monthlyfy=True)

        labels = [f"Daily Unified Slope = {round(t, 4)} units" for t in target_slopes]
        labels.append("Null slope")
        plot_comparisons(root_path, labels, monthly=False, suffix_set=[str(i) for i in range(from_index,10+1)], xlength=xlength,
                         title="Accuracy (easy mode)", xlabel="day", metric_name="cumulative_accuracy", main_stat="accuracy", 
                         subfolder_name=subfolder_name,folder_prefix=folder_prefix, monthlyfy=True)

        labels = [f"Daily Unified Slope = {round(t, 4)} units" for t in target_slopes]
        labels.append("Null slope")
        plot_comparisons(root_path, labels, monthly=False, suffix_set=[str(i) for i in range(from_index,10+1)], xlength=xlength,
                         title="Accuracy (regular mode)", xlabel="day", metric_name="cumulative_accuracy", main_stat="accuracy", 
                         subfolder_name=subfolder_name,folder_prefix=folder_prefix, monthlyfy=True)

 
    def test_unified_plots(self):
        root_path = os.path.join(BASE_PATH_FOR_PICS, "PDEP")
        n = 10
        root_path = os.path.join(root_path, f"unified_plots_easy_v2_{n}", "alpha_55_sigma_30")

        f_accs = os.path.join(root_path, "cumulative_accuracy.npy")
        cumulative_accuracies = np.load(f_accs)

        f_sp_alpha = os.path.join(root_path, "second_pass_alpha.npy")
        sp_alpha = np.load(f_sp_alpha)

        f_a_alpha = os.path.join(root_path, "actual_alpha.npy")
        a_alpha = np.load(f_a_alpha)

        f_sp_sigma = os.path.join(root_path, "second_pass_sigma.npy")
        sp_sigma = np.load(f_sp_sigma)

        f_a_sigma = os.path.join(root_path, "actual_sigma.npy")
        a_sigma = np.load(f_a_sigma)

        target_slopes = -np.logspace(-4, -2, 10, base=10)
        target_slope = 0.0 if n == 10 else target_slopes[n] 
        norm_slope_alpha = abs(round(target_slope,4))*100
        norm_slope_sigma = abs(round(target_slope,4))*100

        trials_per_day = 30


        plot_stats  (   [   
                            average_by_day(sp_alpha, trials_per_day)/MAX_ALPHA,
                            1-(average_by_day(sp_sigma, trials_per_day)/MAX_SIGMA),
                            cumulative_accuracies
                        ],
                        65,
                        ["Estimated Non-Numerical Interference (NNI)", "Estimated Numerical Acuity (NA)", "Cumulative Accuracy"], 
                        main_stat="NNI Score - NA score - Accuracy %",
                        lim_bounds=[-0.1, 1.1],
                        save_as_ndarray=False,
                        title= f"Daily NNI decrease = {norm_slope_alpha}%; Daily NA gain = {norm_slope_sigma}%",
                        xlabel="days",
                    )

        plot_stats  (   [   
                            average_by_day(sp_alpha, trials_per_day)/MAX_ALPHA,
                            1-(average_by_day(sp_sigma, trials_per_day)/MAX_SIGMA),
                            average_by_day(a_alpha, trials_per_day)/MAX_ALPHA,
                            1-(average_by_day(a_sigma, trials_per_day)/MAX_SIGMA),
                            cumulative_accuracies
                        ],
                        65,
                        ["Estimated Non-Numerical Interference (NNI)",  "Estimated Numerical Acuity (NA)", "Actual NNI", "Actual NA", "Cumulative Accuracy"], 
                        main_stat="NNI Score - NA score - Accuracy %",
                        lim_bounds=[-0.1, 1.1],
                        save_as_ndarray=False,
                        title= f"Daily NNI decrease = {norm_slope_alpha}%; Daily NA gain = {norm_slope_sigma}%",
                        xlabel="days",
                    )
        
    def test_unified_plots_6M(self):
        root_path = os.path.join(BASE_PATH_FOR_PICS, "PDEP")
        n = 8
        root_path = os.path.join(root_path, f"unified_plots_easy_v2_{n}", "alpha_55_sigma_30")

        f_accs = os.path.join(root_path, "cumulative_accuracy.npy")
        cumulative_accuracies_o = np.load(f_accs)

        f_sp_alpha = os.path.join(root_path, "second_pass_alpha.npy")
        sp_alpha = np.load(f_sp_alpha)

        f_a_alpha = os.path.join(root_path, "actual_alpha.npy")
        a_alpha = np.load(f_a_alpha)

        f_sp_sigma = os.path.join(root_path, "second_pass_sigma.npy")
        sp_sigma = np.load(f_sp_sigma)

        f_a_sigma = os.path.join(root_path, "actual_sigma.npy")
        a_sigma = np.load(f_a_sigma)

        target_slopes = -np.logspace(-4, -2, 10, base=10)
        target_slope = 0.0 if n == 10 else target_slopes[n] 
        norm_slope_alpha = abs(round(target_slope/3,4))*100
        norm_slope_sigma = abs(round(target_slope/3,4))*100

        trials_per_day = 10
        n_days = 195
        cumulative_accuracies = np.zeros(n_days)
        j=0
        for i, c in enumerate(cumulative_accuracies_o):
            cl = np.linspace(c, cumulative_accuracies_o[i+1],3) if i != cumulative_accuracies_o.shape[0]-1 else [c,c,c]
            for i in range(0,3):
                cumulative_accuracies[j] = cl[i] 
                j+=1          



        plot_stats  (   [   
                            average_by_day(sp_alpha, trials_per_day)/MAX_ALPHA,
                            1-(average_by_day(sp_sigma, trials_per_day)/MAX_SIGMA),
                            cumulative_accuracies
                        ],
                        195,
                        ["Estimated Non-Numerical Interference (NNI)", "Estimated Numerical Acuity (NA)", "Cumulative Accuracy"], 
                        main_stat="NNI Score - NA score - Accuracy %",
                        lim_bounds=[-0.1, 1.1],
                        save_as_ndarray=False,
                        title= f"Daily NNI decrease = {round(norm_slope_alpha,4)}%; Daily NA gain = {round(norm_slope_sigma,4)}%",
                        xlabel="months",
                        months_as_x=True,
                        n_months=6.5
                    )

        plot_stats  (   [   
                            average_by_day(sp_alpha, trials_per_day)/MAX_ALPHA,
                            1-(average_by_day(sp_sigma, trials_per_day)/MAX_SIGMA),
                            average_by_day(a_alpha, trials_per_day)/MAX_ALPHA,
                            1-(average_by_day(a_sigma, trials_per_day)/MAX_SIGMA),
                            cumulative_accuracies
                        ],
                        195,
                        ["Estimated Non-Numerical Interference (NNI)",  "Estimated Numerical Acuity (NA)", "Actual NNI", "Actual NA", "Cumulative Accuracy"], 
                        main_stat="NNI Score - NA score - Accuracy %",
                        lim_bounds=[-0.1, 1.1],
                        save_as_ndarray=False,
                        title= f"Daily NNI decrease = {round(norm_slope_alpha,4)}%; Daily NA gain = {round(norm_slope_sigma,4)}%",
                        xlabel="months",
                        months_as_x=True,
                        n_months=6.5
                    )
        
    def test_plots_for_thesis(self):
        trials =    [
                        [0.4, 0.6],
                        [-0.7, -0.5],
                        [-0.5, 0.5],
                        [-0.2, 0.8],
                        [-0.4, 0.5],
                        [0.6, -0.4]
                    ]
        trials = [to_mock_trial(t[0],t[1]) for t in trials]
        corrects = [True, False, False, True, True, True]
        anns = ["" for t in trials]
        std = 0.2
        plot_trials([-1, 2], trials, corrects, anns, ann_str=True, sharp_std=std)
        #plot_gaussian_3D([0.2, 0.3], 0.3)
        #plot_trials([-1,1], [to_mock_trial(-0.1,-0.1)], [True], [""],ann_str=True, sharp_std=0.3, plot_fs=True, plot_norm=True)
        
        trials =    [
                        [-0.8, -0.7],
                        [-0.6, 0.2],
                        [ 0.5, 0.5],
                        [ 0.3, -0.3],
                    ]
        mt=[to_mock_trial(t[0],t[1]) for t in trials]
        std = 0.3
        corrects = [True for t in trials]
        #anns = [f"{i+1}" for i in range(0, len(trials))]
        anns = ["" for i in range(0, len(trials))]
        plot_trials([-1, 1], mt, corrects, anns, ann_str=True, sharp_std=std, plot_fs=True)

        for i,t in enumerate(trials):
            a = i
            #plot_1d_gaussians(t, unit_vector([-1,1]), std, i+1) 
        bv=unit_vector([-1,1])
        transform_mat = np.linalg.inv(np.array([[bv[0], bv[1]], [bv[1], -bv[0]]]))
        max_dec_score = 2*math.sqrt(2)
        anns = [f"{compute_perceived_difficulty(np.array(t), transform_mat, max_dec_score)}" for t in trials]
        plot_trials(unit_vector([-1, 1]), mt, corrects, anns, ann_str=True, plot_dist=True, plot_fs=True)
        #eval = PDEP_Evaluator(self.alpha, self.sigma, self.target_error_prob, self.target_perceived_diff, self.norm_feats)

        target_error_prob = 0.8
        anns = []
        for t in trials:
            score = global_fitness_score(np.array(t), target_error_prob, 0.1, std, transform_mat, max_dec_score)
            anns.append(f"S: {round(score, 2)}")

        #plot_trials(unit_vector([-1, 1]), mt, corrects, anns, ann_str=True, plot_fs=True,sharp_std=std, title=f"Target error probability: {target_error_prob}")


    def test_plot_generic_comparison(self):
        root_path = os.path.join(BASE_PATH_FOR_PICS, "PDEP")

        root_path_1 = os.path.join(root_path, f"unified_plots_regular_v2_10", "alpha_55_sigma_30")
    
        f_a_alpha_1 = os.path.join(root_path_1, "actual_alpha.npy")
        a_alpha_1 = np.load(f_a_alpha_1)

        root_path_2 = os.path.join(root_path, f"unified_plots_regular_v2_7", "alpha_55_sigma_30")
    
        f_a_alpha_2 = os.path.join(root_path_2, "actual_alpha.npy")
        a_alpha_2 = np.load(f_a_alpha_2)

        root_path_3 = os.path.join(root_path, f"unified_plots_regular_v2_9", "alpha_55_sigma_30")
    
        f_a_alpha_3 = os.path.join(root_path_3, "actual_alpha.npy")
        a_alpha_3 = np.load(f_a_alpha_3)

        target_slopes = -np.logspace(-4, -2, 10, base=10)
        
        trials_per_day = 30

        l = 1500
        plot_stats  (   [   
                            a_alpha_1[0:l] + 20,
                            a_alpha_2[0:l] + 20,
                            a_alpha_3[0:l] + 20
                        ],
                        l,
                        [f"lr = {0.0} deg/it", f"lr = {round(target_slopes[7]*MAX_ALPHA, 2)} deg/it", f"lr = {round(target_slopes[9]*MAX_ALPHA, 2)} deg/it"], 
                        main_stat="Alpha (degrees)",
                        lim_bounds=[-5, 95],
                        save_as_ndarray=False,
                        title= f"Alpha improvement",
                        xlabel="iterations (it)",
                    )

    def test_plot_lls(self):
        sigmas = np.linspace(0.05, 0.3, 10)

        trials =    [
                            [0.4, 0.6],
                            [-0.7, -0.5],
                            [-0.4, 0.15],
                            [-0.2, 0.8],
                            [-0.4, 0.5],
                            [0.7, -0.3],
                            [0.1, -0.7],
                            [-0.3, -0.6],
                            [0.4, -0.3]
                        ]
        mt=[to_mock_trial(t[0],t[1]) for t in trials]
        mt = np.array(mt)
        corrects = [True, False, True, True, True, False, False,False, False]
        anns = ["" for i in range(0, len(trials))]
        trials = np.array(trials)
        looks_right = trials[:, 0] >0
        corrects = np.array(corrects)

        norm = [-1,1]
        transform_mat=np.linalg.inv(np.array([[norm[0], norm[1]], [norm[1], -norm[0]]]))

        dists = np.dot(transform_mat, trials.T)[1, :]
        looks_right = dists >0
        wrong_side = looks_right != corrects
        c_dists = dists[wrong_side]
        d = [c for c in c_dists]
        for i in range(0, 10):
            d.append(0.2)
        c_dists = np.array(d)
        w_dists = dists[wrong_side]
        #anns = np.array([f"{round(dists[i],2)}" for i in range(0, len(trials))])
        
        #c_dists = np.dot(transform_mat, trials[corrects == looks_right].T)[1, :]
        #w_dists = np.dot(transform_mat, trials[corrects != looks_right].T)[1, :]
        
        #plot_trials([-1, 1], mt, corrects, anns, ann_str=True, sharp_std=0.1, plot_fs=True)    
        #plot_trials([-1, 1], mt[looks_right == False], corrects[looks_right==False], anns[looks_right==False], ann_str=True, sharp_std=0.1, plot_fs=True)    
        for s in sigmas:
            std = 0.3
            #corrects = [True for t in trials]
            #anns = [f"{i+1}" for i in range(0, len(trials))]
            ll = compute_log_likelihood(c_dists, w_dists, s)
            plot_trials([-1, 1], mt, corrects, anns, ann_str=True, sharp_std=s, plot_fs=True, title=f"sigma: {round(s,2)}, Log-Likelihood = {round(ll, 2)}")    

if __name__ == "__main__":
    tc = MakePlots()
    start_time = time.time()

    #tc.test_joint_plots()
    #tc.test_joint_plots_6M()
    #tc.test_unified_plots()
    tc.test_unified_plots_6M()
    #tc.test_plots_for_thesis()
    #tc.test_plot_generic_comparison()
    #tc.test_plot_lls()

    duration = 1000  # milliseconds
    freq = 440  # Hz
    #winsound.Beep(freq, duration)
    print("--- %s seconds ---" % (time.time() - start_time))
