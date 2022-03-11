using System;
using System.Collections.Generic;

[Serializable]
public class GameTrialResults
{
    public GameTrialResult[] results;

    public GameTrialResults(List<GameTrialResult> resultsList)
    {
        this.results = resultsList.ToArray();
    } 
}
