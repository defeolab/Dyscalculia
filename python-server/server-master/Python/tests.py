import unittest
from AI.ai_utils import *
from AI.TrialAdapter import TrialAdapter
from AI.ai_plot import *
from AI.ImprovementHandler import *
from AI.PDEP_Evaluator import PDEP_Evaluator
from dummy_client_handler import SimulatedClient
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

def to_trial(nd, nnd):
    return [-1,-1,-1,-1,-1,-1,-1,-1,nd,nnd]

class TestAI(unittest.TestCase):

    def __init__(self):
        self.trial_adapter = TrialAdapter(False, True)
        self.alpha = 30
        self.sigma = 1
        self.target_error_prob = 0.1
        self.target_perceived_diff = 0.1

        self.norm_feats = True

        self.boundary_vector = unit_vector(np.array([-math.sin(math.radians(self.alpha)), math.cos(math.radians(self.alpha))]))

        #basis in the decision boundary space
        self.transform_mat =np.linalg.inv(np.array([[self.boundary_vector[0], self.boundary_vector[1]], [self.boundary_vector[1], -self.boundary_vector[0]]]))

        self.a = float(self.boundary_vector[1]/self.boundary_vector[0])
        self.ax = lambda x: x*self.a

        self.integral_bound = 5

        prec_path = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, "PDEP", "precompute_improving")

        path = os.path.join(prec_path, "alpha_65_sigma_50.npy")
        self.trial_data = np.load(path)

        path = os.path.join(prec_path, "fp_alpha.npy")
        self.fp_alpha = np.load(path)

        path = os.path.join(prec_path, "sp_alpha.npy")
        self.sp_alpha = np.load(path)
        
        path = os.path.join(prec_path, "sim_alpha.npy")
        self.sim_alpha = np.load(path)
        
        path = os.path.join(prec_path, "fp_sigma.npy")
        self.fp_sigma = np.load(path)
        
        path = os.path.join(prec_path, "sp_sigma.npy")
        self.sp_sigma = np.load(path)
        
        path = os.path.join(prec_path, "sim_sigma.npy")
        self.sim_sigma = np.load(path)






    def test_probability(self):
        trials = get_mock_trials(32, True)
        probs = []
        corrects = []
        for t in trials:
            prob = compute_error_probability_2d(t, self.sigma, self.integral_bound,self.ax)
            probs.append(prob)
            corrects.append(True)
        
        plot_trials(self.boundary_vector, trials,corrects, probs)
    
    def test_PDEP_Evaluator(self):

        error_prob = 0.1
        trials = []
        prob_diffs = []
        corrects = []
        n = 5
        sigma = 0.20
        alpha = 30

        eval = PDEP_Evaluator(alpha, sigma, error_prob, self.target_perceived_diff, self.norm_feats)
        for i in range(0,n):
            nd,nnd,diff =PDEP_find_trial(eval.target_error_prob, eval.target_perceived_diff,eval.transform_mat, eval.boundary_vector,eval.sigma, eval.norm_feats)
            #print(f"{p}-{nd}-{nnd}-{diff}")
            trials.append(to_mock_trial(nd,nnd))
            prob_diffs.append(f"S: {round(diff,2)}")
            corrects.append(True)

        plot_trials(eval.boundary_vector, trials, corrects, prob_diffs, ann_str=True, sharp_std=sigma, title=f"Target Error Prob = {error_prob}")
    
    def test_player_cycle_simple(self):
        client = SimulatedClient(0.5, 0.5, alpha = 20, sigma= 0.2, evaluator="simple", norm_feats=True)

        figsaver = FigSaver(BASE_PATH_FOR_PICS, "test", interval=1)
        client.simulate_player_cycle(10, 5, True,False,figsaver=figsaver )

    def test_player_cycle_PDEP(self):
        client = SimulatedClient(0.5, 0.5, alpha = 30, sigma= 0.2, evaluator="PDEP", norm_feats=True)

        client.player_evaluator.target_error_prob = 0.30
        #client.player_evaluator.target_perceived_diff = 0.5
        client.simulate_player_cycle(10, 6, False, False)
    
    def test_trial_adapter(self):
        adapter = TrialAdapter(False, norm_feats=True, kids_ds=True)
        n = 10
        nds = np.linspace(-0.95, 0.95, n)
        nnds = np.linspace(-0.95,0.95, n)

        raw = []
        adapted = []
        corrects = []
        anns = []

        for nd in nds:
            for nnd in nnds:
                raw.append(to_mock_trial(nd, nnd))
                raw.append(adapter.find_trial(nd, nnd)[0])
                corrects.append(True)
                corrects.append(False)
                anns.append("")
                anns.append("")

        vec = np.array([0,1])
        plot_trials(vec, raw, corrects, anns, ann_str=True, norm_lim=True, plot_links = True)

    def test_3D_plot(self):
        player = PlayerSimulator(45, 0.5)
        days = 60
        tpd = 10
        trials = []
        corrects = []

        e_bvsig = []
        bvsig = []
        for i in range(0, days):
            for j in range(0, tpd):
                trial = to_mock_trial(np.random.normal(scale=0.5),np.random.normal(scale=0.5))
                trials.append(trial)
                corrects.append(player.predict(trial)[0])
            
            e_bvsig.append((player.boundary_vector, player.sigma))
            bvsig.append(player.random_improvement())


        bvs = list(map(lambda x: x[0],bvsig))
        sigmas = list(map(lambda x: x[1],bvsig))

        e_bvs = list(map(lambda x: x[0],e_bvsig))
        e_sigmas = list(map(lambda x: x[1],e_bvsig))
        #trials = [to_mock_trial(np.random.normal(scale=0.5),np.random.normal(scale=0.5)) for i in range(0, days) for j in range(0, tpd)]
        #trials = [to_mock_trial(0.5,0.5) for i in range(0, days) for j in range(0, tpd)]
        
        #corrects = [np.random.choice([False, True]) for i in range(0, days) for j in range(0, tpd)]
        figsaver = FigSaver(BASE_PATH_FOR_CASUAL_PICS, f"", interval=1,figname=f"player_cycle_3D" )
        plot_player_cycle3D(bvs, e_bvs, sigmas, e_sigmas, trials, corrects, tpd, figsaver=figsaver)
    
    def test_precompute(self):
        save_file = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, "PDEP")
        save_file = os.path.join(save_file, "precompute_t30")
        save_file = os.path.join(save_file, "alpha_45_sigma_10.npy")

        ev = PDEP_Evaluator(0,0)

        t1 = to_mock_trial(0.1,0.1)
        t2 = to_mock_trial(0.2,0.2)
        t3 = to_mock_trial(0.3,0.3)


        #np.save(save_file, np.array(t1))
        #ev.save_trial(save_file, t1,True, 0.1)
        #ev.save_trial(save_file, t2,True, 0.1)
        #ev.save_trial(save_file, t3,True, 0.1, True)

        
        array = np.load(save_file)
        print(array)
        
    
    def test_AS(self):
        n=90
        n_part = 30
        e = ASD_Estimator(n, "simple_denoising")
        target_s = 30

        filename = f"alpha_45_sigma_{target_s}.npy"

        save_file1 = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, "PDEP")
        save_file1 = os.path.join(save_file1, "precompute_t30")
        save_file1 = os.path.join(save_file1, filename)
        l1 = np.load(save_file1)

        save_file2 = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, "PDEP")
        save_file2 = os.path.join(save_file2, "precompute_t10")
        save_file2 = os.path.join(save_file2, filename)
        l2 = np.load(save_file2)

        save_file3 = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, "PDEP")
        save_file3 = os.path.join(save_file3, "precompute_t80")
        save_file3 = os.path.join(save_file3, filename)
        l3 = np.load(save_file3)
        
        l1_part = l1[0:n_part, :]
        l2_part = l2[0:n_part, :]
        l3_part = l3[0:n_part, :]
        
        l1= np.concatenate((l1_part, l2_part, l3_part)) 

        looks_right = l1[0:n, 2] == 1
        looks_right = looks_right == (l1[0:n, 0] > 0)
        trials = l1[0:n, 0:2]

        t, c, a = return_plottable_list(trials, looks_right)
        plot_trials([-1,1], t, c, a, ann_str=True)

        e.trials = trials 
        e.predictions = looks_right

        print(e.produce_estimate(np.array(unit_vector([-1,1])), 0.3))


    def test_AS_extensively(self):
        n=90

        n_part = 30
        e = ASD_Estimator(n, denoiser_type="simple_denoising")
        target_s = 20

        filename = f"alpha_45_sigma_{target_s}.npy"

        save_file1 = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, "PDEP")
        save_file1 = os.path.join(save_file1, "precompute_t30")
        save_file1 = os.path.join(save_file1, filename)
        l1 = np.load(save_file1)

        save_file2 = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, "PDEP")
        save_file2 = os.path.join(save_file2, "precompute_t10")
        save_file2 = os.path.join(save_file2, filename)
        l2 = np.load(save_file2)

        save_file3 = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, "PDEP")
        save_file3 = os.path.join(save_file3, "precompute_t80")
        save_file3 = os.path.join(save_file3, filename)
        l3 = np.load(save_file3)

        l1_part = l1[0:n_part, :]
        l2_part = l2[0:n_part, :]
        l3_part = l3[0:n_part, :]
        
        l1= np.concatenate((l1_part, l2_part, l3_part)) 

        alphas = [10, 30, 45, 60, 80]
        sigmas = [0.1,0.2,0.4,0.5]

        p_alphas = []
        p_sigmas = []

        errors_alphas = []
        errors_sigmas = []

        debug = True

        for alpha in alphas:
            for sigma in sigmas:
                sim = PlayerSimulator(alpha, sigma)
                preds = []
                for t in l1:
                    _, (__, pred) = sim.predict(to_mock_trial(t[0], t[1])) 
                    preds.append(pred)
                
                preds = np.array(preds)

                e.trials = l1[:, 0:2]
                e.predictions = preds
                (p_alpha, p_sigma, p_norm), _ = e.produce_estimate()
                p_alphas.append(p_alpha)
                p_sigmas.append(p_sigma)

                errors_alphas.append(alpha - p_alpha)
                errors_sigmas.append(sigma - p_sigma)

                
                print(f"doing alpha {alpha}, sigma {sigma}")
                print(f"predicted were {p_alpha} - {p_sigma}")
                if debug:
                    figsaver = FigSaver(BASE_PATH_FOR_CASUAL_PICS, f"", interval=1,figname=f"a{int(alpha)}_s{int(sigma*100)}" )
                    m = 10
                    t, c, a = return_plottable_list(l1[0:m, :], preds[0:m])
                    plot_trials(sim.boundary_vector, t, c, a, ann_str=True, sharp_std=sim.sigma, estimated_boundary=p_norm, estimated_std=p_sigma, figsaver=figsaver)
        
        avg_error_alpha = functools.reduce(lambda a,b: np.abs(a) + np.abs(b), errors_alphas)
        avg_error_sigma = functools.reduce(lambda a,b: np.abs(a) + np.abs(b), errors_sigmas)
        
        avg_error_alpha = avg_error_alpha/len(errors_alphas)
        avg_error_sigma = avg_error_sigma/len(errors_sigmas)


        print(errors_alphas)
        print("-------")
        print(errors_sigmas)
        print("-------")
        print(f"{avg_error_alpha} - - - {avg_error_sigma}")

    def test_PDEP_update(self):
        e = PDEP_Evaluator(45, 0.5, update_step=1)

        e.estimator.trials.append([-1, 1])

        for i in range(0, 1000):
            e.update_statistics(True, 0.0)        

    def test_std_loglikelihood(self):
        ct = np.array([[1,1]])
        cp = np.array([True])
        wt = np.array([[0.1,0.1]])
        wp = np.array([False])

        norm = unit_vector([-1,1])
        compute_sharpening_std_loglikelihood(ct, cp, wt, wp, norm)

    def test_study_optimal_C(self):
        print(BEST_CS)
        #rint(CS[BEST_CS[1]])
        #print(find_expected_optimal_C(np.array([-0.6,0.4]), 0.50))
        #print(CONFIGS)
        #print(CS)
        #print(ERR_CS)

        plot_ablation_C(CONFIGS, CS, BEST_CS)

    
    def test_ASE(self):
        e = ASE_Estimator(30, 90)
        e.target_line = np.array(unit_vector([0.2, 0.6]))
        e.curr_sigma = 0.3
        n = 10
        t = []
        p = []
        anns = []
        for i in range(0, n):
            tr, ann = e.get_trial()
            t.append(tr)
            anns.append(ann)
            p.append(np.random.choice([True, False]))
        
        t, c, a = return_plottable_list(t, p)
        plot_trials(np.array([-0.6, 0.2]), t, c, a, ann_str= True)
        

    def test_monthly_plot(self):
        stat1 = [np.random.normal(0.5) for i in range(0, 120)]
        stat2 = [np.random.normal(0.5) for i in range(0, 120)]
        
        plot_monthly_stats([stat1, stat2], 4, 1, figsaver="asdsad")
    
    def test_table(self):
        
        base_root = os.path.join(BASE_PATH_FOR_PICS, "PDEP")
        figsaver = FigSaver(base_root, "test")

        n_stats = 2 
        tpd = 2
        n_months = 2
        main_stat = [i for i in range(0, n_months*30*tpd)]
        secondary_stats = [[-i for i in range(0, n_months*30*tpd)] for j in range(0,n_stats)]
        main_label = "alpha"
        secondary_labels=["first pass", "second pass"]

        make_tables(main_stat, secondary_stats, tpd, n_months, main_label = main_label, secondary_labels=secondary_labels, figsaver=figsaver)

    def test_misc(self):
        sigma = 0.8
        nd_variable = -0.3
        nnd_variable = 0.9
        integral_bound = 5
        boundary_vector = unit_vector([-1,0.1])

        transform_mat=np.linalg.inv(np.array([[boundary_vector[0], boundary_vector[1]], [boundary_vector[1], -boundary_vector[0]]]))

        dist = np.dot(transform_mat, vcol(np.array([nd_variable,nnd_variable])))[1, :]

        a = float(boundary_vector[1]/boundary_vector[0])
        ax = lambda x: x*a

        def custom_erf(x: np.ndarray) -> np.ndarray:
            return 0.5*sp.special.erf(x/(math.sqrt(2)*sigma)) - 0.5*sp.special.erf(-x/(math.sqrt(2)*sigma))
            #return 0.5 + 0.5*sp.special.erf(x/math.sqrt(2)*sigma)

        def correct_trial_likelihood(x: np.ndarray) -> np.ndarray:
            v = custom_erf(x)
            return np.clip(v + (1-v)/2, 0.0001, 0.9999)
    
        def wrong_trial_likelihood(x: np.ndarray) -> np.ndarray:
            v= 1-custom_erf(x)
            return np.clip(v/2, 0.0001, 0.9999)

        gauss_func = lambda y,x : math.exp(-0.5*(1/(sigma**2))*(((x-nd_variable)**2)+((y-nnd_variable)**2)))

        total_area, _ = integrate.dblquad(gauss_func, -integral_bound,integral_bound,-integral_bound,integral_bound)

        if nd_variable < 0:
            error_area, _ =  integrate.dblquad(gauss_func, -integral_bound, integral_bound, ax, integral_bound)
        else:
            error_area, _ =  integrate.dblquad(gauss_func, -integral_bound, integral_bound,-integral_bound, ax)
        
        p2d = error_area/total_area

        p1d = correct_trial_likelihood(dist)

        print(p2d)
        print(p1d)

    def test_improvement_1D(self):

        mock_trials = [[t[0], t[1]] for t in self.trial_data]

        correct_to_lr = lambda x,y: (y==1) == (x >0)
        mock_preds = [correct_to_lr(t[0], t[2]) for t in self.trial_data]

        e = ASD_Estimator(180, 30, "simple_denoising")
        
        data_x = np.linspace(1, self.fp_alpha.shape[0], self.fp_alpha.shape[0])

        e.trials = mock_trials
        e.predictions = mock_preds

        e.max_trials_to_consider = 90

        ad, sd, sn = e.second_pass_estimation(self.fp_alpha, self.fp_sigma)

        #assert True == False

        plt.plot(data_x, self.sim_alpha, color = "red")
        plt.plot(data_x, self.fp_alpha, color="orange")
        plt.plot(data_x, ad, color="blue")
        plt.ylim([-5,95])
        plt.show()

        plt.plot(data_x, self.sim_sigma, color="blue")
        plt.plot(data_x, self.fp_sigma, color="green")
        plt.plot(data_x, sd, color="purple")
        plt.ylim([-0.1,0.7])
        plt.show()
    
    def test_slopes(self):
        n = 5400
        data_x = np.linspace(1, n, n)
        norm_slope = -0.0001/30
        alpha_slope = norm_slope*MAX_ALPHA
        sigma_slope = norm_slope*MAX_SIGMA

        data_alpha = np.clip(data_x*alpha_slope + MAX_ALPHA, 0, 1000)
        data_sigma = np.clip(data_x*sigma_slope + MAX_SIGMA, 0, 1000)

        plt.plot(data_x, data_alpha, color="red")
        plt.ylim([-5,MAX_ALPHA+5])
        plt.show()
        
        plt.plot(data_x, data_sigma, color="green")
        plt.ylim([-0.1,MAX_SIGMA+0.1])
        plt.show()

        data_alpha = data_alpha/MAX_ALPHA
        data_sigma = data_sigma/MAX_SIGMA

        plt.plot(data_x, data_alpha, color="red")
        plt.plot(data_x, data_sigma, color="green")
        plt.show()
        
    def test_best_Ns(self):
        print("---------")
        print(BEST_N_INDEXES)
        print("---------")
        print(BEST_NS)
        print("---------")
        print(SLOPE_CONFIGS)
        print("---------")
        print(N_TRIALS)
        print("---------")
        alphamins=np.argmin(ERR_A_NS, axis=1)
        sigmamins = np.argmin(ERR_S_NS, axis=1)
        print(alphamins)
        print(sigmamins)
        print("---------")
        #print(ERR_S_NS[9])

        
        #filepath = os.path.join(PATH_FOR_N_ABLATION, "n_trials.npy")
        #nv = np.array([ 100,  200,  300,  400,  500,  600,  700,  800,  900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800])
        #np.save(filepath, nv)
        #filepath = os.path.join(PATH_FOR_N_ABLATION, "best_n_trials_index.npy")
        #nv = np.array([17,17,17, 13, 9, 9, 6, 4, 1, 0])
        #np.save(filepath, nv)

        x = np.abs(SLOPE_CONFIGS[0])
        y = N_TRIALS[BEST_N_INDEXES]

        valid_indexes = np.array([0,4,5,6,7,8,9])
        x = x[valid_indexes]
        y = y[valid_indexes]
        #fig = plt.figure()
        #ax = fig.gca()
        
        plt.scatter(x, y, color = "red")
        plt.plot(x, y, color = "blue")
        plt.xlabel("normalized unsigned slopes (unit/trial)")
        plt.ylabel("Optimal z")
        plt.xscale("log")
        plt.grid(True)
        plt.show()
    
    def test_trial_mirroring(self):
        n_trials_to_consider = 180
        mock_trials = [np.array([t[0], t[1]]) for t in self.trial_data[-n_trials_to_consider:]]
        correct_to_lr = lambda x,y: (y==1) == (x >0)
        mock_preds = [correct_to_lr(t[0], t[2]) for t in self.trial_data[-n_trials_to_consider:]]

        mirror_trials, mirror_preds = mirror_trials_list(mock_trials, mock_preds)
        model = LinearSVC(dual=False, C= 100)
        model.fit(mock_trials, mock_preds)
        norm1 = unit_vector(np.array([-model.coef_[0][1], model.coef_[0][0]]))

        print("regular")
        print(norm1)
        print(model.intercept_)

        model = LinearSVC(dual=False, C= 100)
        model.fit(mirror_trials, mirror_preds)
        norm2 = unit_vector(np.array([-model.coef_[0][1], model.coef_[0][0]]))

        print("mirror")
        print(norm2)
        print(model.intercept_)

        model = LinearSVC(dual=False, C= 100, fit_intercept=False)
        model.fit(mock_trials, mock_preds)
        norm3 = unit_vector(np.array([-model.coef_[0][1], model.coef_[0][0]]))

        print("no fit no mirror")
        print(norm3)
        print(model.intercept_)

        model = LinearSVC(dual=False, C= 100, fit_intercept=False)
        model.fit(mirror_trials, mirror_preds)
        norm4 = unit_vector(np.array([-model.coef_[0][1], model.coef_[0][0]]))

        print("no fit with mirror")
        print(norm4)
        print(model.intercept_)

        n_t = n_trials_to_consider
        t,c,a = return_plottable_list(mock_trials[0:n_t], mock_preds[0: n_t])
        plot_trials(norm1, t, c, a, ann_str=True, estimated_boundary=norm3)
        
        t,c,a = return_plottable_list(mirror_trials[0: n_t], mirror_preds[0: n_t])
        plot_trials(norm2, t, c, a, ann_str=True, estimated_boundary=norm4)
        
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
    def test_unified_plots(self):
        root_path = os.path.join(BASE_PATH_FOR_PICS, "PDEP")
        n = 8
        root_path = os.path.join(root_path, f"unified_plots_regular_v2_{n}", "alpha_55_sigma_30")

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
                        [-0.2, 0.6],
                        [ 0.5, 0.5],
                        [ 0.3, -0.3],
                    ]
        mt=[to_mock_trial(t[0],t[1]) for t in trials]
        std = 0.3
        corrects = [True for t in trials]
        anns = [f"{i+1}" for i in range(0, len(trials))]
        #plot_trials([-1, 1], mt, corrects, anns, ann_str=True, sharp_std=std)

        for i,t in enumerate(trials):
            a = i
            #plot_1d_gaussians(t, unit_vector([-1,1]), std, i+1) 
        bv=unit_vector([-1,1])
        transform_mat = np.linalg.inv(np.array([[bv[0], bv[1]], [bv[1], -bv[0]]]))
        max_dec_score = 2*math.sqrt(2)
        anns = [f"{compute_perceived_difficulty(np.array(t), transform_mat, max_dec_score)}" for t in trials]
        #plot_trials(unit_vector([-1, 1]), mt, corrects, anns, ann_str=True, plot_dist=True, plot_fs=True)
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

    def test_distance(self):
        root_path = os.path.join(BASE_PATH_FOR_PICS, "PDEP")

        root_path_1 = os.path.join(root_path, f"fp_sp_fixed_studies", "alpha_10_sigma_40")

        f_a_a = os.path.join(root_path_1, "actual_alpha.npy")
        aa = np.load(f_a_a)

        f_a_a = os.path.join(root_path_1, "estimated_alpha.npy")
        fp_a = np.load(f_a_a)

        print(np.sum(np.abs(fp_a - aa))/fp_a.shape[0])

        f_a_s = os.path.join(root_path_1, "actual_sigma.npy")
        a_s = np.load(f_a_s)

        f_a_s = os.path.join(root_path_1, "estimated_sigma.npy")
        fp_s = np.load(f_a_s)

        print(np.sum(np.abs(fp_s - a_s))/fp_s.shape[0])


        

if __name__ == "__main__":
    tc = TestAI()

    start_time = time.time()

    #tc.test_probability()
    #tc.test_PDEP_Evaluator()
    #tc.test_player_cycle_simple()
    #tc.test_player_cycle_PDEP()
    tc.test_trial_adapter()
    #tc.test_3D_plot()
    #tc.test_precompute()
    #tc.test_AS()
    #tc.test_AS_extensively()
    #tc.test_misc()
    #tc.test_PDEP_update()
    #tc.test_std_loglikelihood()
    #tc.test_study_optimal_C()
    #tc.test_ASE()
    #tc.test_monthly_plot()
    #tc.test_table()
    #tc.test_improvement_1D()
    #tc.test_slopes()
    #tc.test_best_Ns()
    #tc.test_trial_mirroring()
    #tc.test_joint_plots()
    #tc.test_unified_plots()
    #tc.test_plots_for_thesis()
    #tc.test_plot_generic_comparison()
    #tc.test_distance()

    duration = 1000  # milliseconds
    freq = 440  # Hz
    #winsound.Beep(freq, duration)
    print("--- %s seconds ---" % (time.time() - start_time))
