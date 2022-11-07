import unittest
from AI.ai_utils import *
from AI.TrialAdapter import TrialAdapter
from AI.ai_plot import plot_trials
from AI.PAD_Evaluator import PAD_Evaluator
from dummy_client_handler import SimulatedClient

def to_trial(nd, nnd):
    return [-1,-1,-1,-1,-1,-1,-1,-1,nd,nnd]

class TestAI(unittest.TestCase):

    def __init__(self):
        self.trial_adapter = TrialAdapter(False, True)
        self.alpha = 60
        self.sigma = 1
        self.target_error_prob = 0.1
        self.target_perceived_diff = 0.1

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
    
    def test_PAD_Evaluator(self):
        eval = PAD_Evaluator(self.alpha, self.sigma, self.target_error_prob, self.target_perceived_diff)

        error_probs = np.linspace(0, 1, num=5)
        trials = []
        prob_diffs = []
        corrects = []
        for p in error_probs:
            nd,nnd,diff =PAD_find_trial(p, self.target_perceived_diff, self.transform_mat, self.boundary_vector,self.sigma)
            print(f"{p}-{nd}-{nnd}-{diff}")
            trials.append(to_trial(nd,nnd))
            prob_diffs.append(f"{round(p,2)} - {round(diff,2)}")
            corrects.append(True)

        plot_trials(self.boundary_vector, trials, corrects, prob_diffs, ann_str=True)
    
    def test_player_cycle(self):
        client = SimulatedClient(0.5, 0.5, alpha = 20, sigma= 0.2)

        client.simulate_player_cycle(10, 5, True)
        

if __name__ == "__main__":
    tc = TestAI()

    #tc.test_probability()
    #tc.test_PAD_Evaluator()
    tc.test_player_cycle()