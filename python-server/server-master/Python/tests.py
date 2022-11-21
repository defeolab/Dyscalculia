import unittest
from AI.ai_utils import *
from AI.TrialAdapter import TrialAdapter
from AI.ai_plot import plot_trials, FigSaver, plot_player_cycle3D
from AI.PDEP_Evaluator import PDEP_Evaluator
from dummy_client_handler import SimulatedClient
from AI.PlayerSimulator import PlayerSimulator
import time
import os

BASE_PATH_FOR_PICS = "C:\\Users\\fblan\\Desktop\\thesis_pics"

def to_trial(nd, nnd):
    return [-1,-1,-1,-1,-1,-1,-1,-1,nd,nnd]

class TestAI(unittest.TestCase):

    def __init__(self):
        self.trial_adapter = TrialAdapter(False, True)
        self.alpha = 30
        self.sigma = 0.2
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
        trials = get_mock_trials(32)
        probs = []
        corrects = []
        for t in trials:
            prob = compute_error_probability(t[8], t[9], self.sigma, self.integral_bound,self.ax)
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

        plot_trials(self.boundary_vector, trials, corrects, prob_diffs, ann_str=True, sharp_std=self.sigma)
    
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
        adapter = TrialAdapter(False, norm_feats=False)
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
        plot_trials(vec, raw, corrects, anns, ann_str=True)

    def test_3D_plot(self):
        player = PlayerSimulator(45, 0.01)
        days = 60
        tpd = 2
        trials = []
        corrects = []
        
        bvsig = []
        for i in range(0, days):
            for j in range(0, tpd):
                trial = to_mock_trial(np.random.normal(scale=0.5),np.random.normal(scale=0.5))
                trials.append(trial)
                corrects.append(player.predict(trial)[0])
            bvsig.append(player.random_improvement())


        bvs = list(map(lambda x: x[0],bvsig))
        sigmas = list(map(lambda x: x[1],bvsig))
        #trials = [to_mock_trial(np.random.normal(scale=0.5),np.random.normal(scale=0.5)) for i in range(0, days) for j in range(0, tpd)]
        #trials = [to_mock_trial(0.5,0.5) for i in range(0, days) for j in range(0, tpd)]
        
        #corrects = [np.random.choice([False, True]) for i in range(0, days) for j in range(0, tpd)]
        
        plot_player_cycle3D(bvs,sigmas, trials, corrects, tpd)

if __name__ == "__main__":
    tc = TestAI()

    start_time = time.time()

    #tc.test_probability()
    #tc.test_PDEP_Evaluator()
    #tc.test_player_cycle_simple()
    #tc.test_player_cycle_PDEP()
    #tc.test_trial_adapter()
    tc.test_3D_plot()
    print("--- %s seconds ---" % (time.time() - start_time))
