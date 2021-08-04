using System;

[Serializable]
public class GameTrialResult
{
    public double DecisionTime;
    public bool Correct;
    public GameTrialData TrialData;

    public GameTrialResult(double decisionTime, bool correct, GameTrialData trialData)
    {
        this.DecisionTime = decisionTime;
        this.Correct = correct;
        this.TrialData = trialData;
    }
}
