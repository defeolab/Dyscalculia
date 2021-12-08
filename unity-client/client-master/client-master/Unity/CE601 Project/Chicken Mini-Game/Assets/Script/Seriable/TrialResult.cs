using System;

[Serializable]
public class TrialResult
{
    public double DecisionTime;
    public bool Correct;
    public TrialData TrialData;

    public TrialResult(double decisionTime, bool correct, TrialData trialData)
    {
        this.DecisionTime = decisionTime;
        this.Correct = correct;
        this.TrialData = trialData;
    }
}
