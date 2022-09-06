using System;
using System.Collections.Generic;

[Serializable]
public class TrialsResults
{
    public TrialResult[] results;

    public TrialsResults(List<TrialResult> resultsList)
    {
        this.results = resultsList.ToArray();
    }
}
