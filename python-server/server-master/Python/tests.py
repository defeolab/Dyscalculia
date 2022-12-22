import unittest
from AI.ai_utils import *
from AI.TrialAdapter import TrialAdapter
from AI.ai_plot import plot_trials, FigSaver, plot_player_cycle3D, plot_ablation_C
from AI.PDEP_Evaluator import PDEP_Evaluator
from dummy_client_handler import SimulatedClient
from AI.PlayerSimulator import PlayerSimulator
from AI.AS_Estimate import ASD_Estimator, ASE_Estimator
from AI.PDEP_functionals import PDEP_find_trial, compute_error_probability_2d
from AI.AS_functionals import *
import time
import os
import functools
import scipy as sp


import winsound


BASE_PATH_FOR_PICS = "C:\\Users\\fblan\\Desktop\\thesis_pics"
BASE_PATH_FOR_CASUAL_PICS = "C:\\Users\\fblan\\Desktop\\thesis pics\\test"

BASE_PATH_FOR_SAVING_TRIALS = "C:\\Users\\fblan\\Dyscalculia\\python-server\\server-master\\Python\\AI\\precomputed_data"

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
        eval = PDEP_Evaluator(self.alpha, self.sigma, self.target_error_prob, self.target_perceived_diff, self.norm_feats)

        error_probs = np.linspace(0, 1, num=5)
        trials = []
        prob_diffs = []
        corrects = []
        for p in error_probs:
            nd,nnd,diff =PDEP_find_trial(p, self.target_perceived_diff, self.transform_mat, self.boundary_vector,self.sigma, self.norm_feats)
            print(f"{p}-{nd}-{nnd}-{diff}")
            trials.append(to_trial(nd,nnd))
            prob_diffs.append(f"{round(p,2)} - {round(diff,2)}")
            corrects.append(True)

        #plot_trials(self.boundary_vector, trials, corrects, prob_diffs, ann_str=True, sharp_std=self.sigma)
    
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
        plot_trials(vec, raw, corrects, anns, ann_str=True, norm_lim=True)

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
        print(CONFIGS)
        #print(CS)
        #print(ERR_CS)

        #plot_ablation_C(CONFIGS, CS, BEST_CS)

    
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
        
        


    
        

if __name__ == "__main__":
    tc = TestAI()

    start_time = time.time()

    #tc.test_probability()
    #tc.test_PDEP_Evaluator()
    #tc.test_player_cycle_simple()
    #tc.test_player_cycle_PDEP()
    #tc.test_trial_adapter()
    #tc.test_3D_plot()
    #tc.test_precompute()
    #tc.test_AS()
    #tc.test_AS_extensively()
    #tc.test_misc()
    #tc.test_PDEP_update()
    #tc.test_std_loglikelihood()
    #tc.test_study_optimal_C()
    tc.test_ASE()


    duration = 1000  # milliseconds
    freq = 440  # Hz
    #winsound.Beep(freq, duration)
    print("--- %s seconds ---" % (time.time() - start_time))
