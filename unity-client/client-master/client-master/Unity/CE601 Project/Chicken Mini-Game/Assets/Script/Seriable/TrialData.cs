using System;
using UnityEngine;

[Serializable]
public class TrialData
{
    public AreaTrialData area1Data;
    public AreaTrialData area2Data;
    public float chickenShowTime;
    public float maxTrialTime;

    public TrialData(AreaTrialData area1Data, AreaTrialData area2Data, float chickenShowTime, float maxTrialTime)
    {
        this.area1Data = area1Data;
        this.area2Data = area2Data;
        this.chickenShowTime = chickenShowTime;
        this.maxTrialTime = maxTrialTime;
    }

    public AreaTrialData getArea1Data()
    {
        return area1Data;
    }

    public AreaTrialData getArea2Data()
    {
        return area2Data;
    }

    public float getAnimalShowTime()
    {
        return chickenShowTime;
    }

    public float getMaxTrialTime()
    {
        return maxTrialTime;
    }
}

