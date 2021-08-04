using System;
using UnityEngine;

[Serializable]
public class GameTrialData
{
    public AreaTrialData area1Data;
    public AreaTrialData area2Data;
    public float ratio;
    public float chickenShowTime;
    public float maxTrialTime;
    public int ratioArea;

    public GameTrialData(AreaTrialData area1Data, AreaTrialData area2Data, float ratio, float chickenShowTime, int ratioArea)
    {
        this.area1Data = area1Data;
        this.area2Data = area2Data;
        this.ratio = ratio;
        this.chickenShowTime = chickenShowTime;
        this.ratioArea = ratioArea;
    }

    public GameTrialData(float circleRadius, float sizeOfChicken, float averageSpaceBetween, float ratio, float chickenShowTime, int numberOfChickens)
    {
        if (UnityEngine.Random.value >= 0.5)
        {
            int area2Chickens = (int)ratio * numberOfChickens;
            if (area2Chickens == numberOfChickens)
            {
                if (ratio >= 1.0f)
                {
                    area2Chickens++;
                } else
                {
                    numberOfChickens++;
                }
            }
            this.area1Data = new AreaTrialData(circleRadius, sizeOfChicken, averageSpaceBetween, numberOfChickens);
            this.area2Data = new AreaTrialData(circleRadius * ratio, sizeOfChicken * ratio, averageSpaceBetween * ratio, area2Chickens);
            this.ratioArea = 1;
        } else
        {
            int area1Chickens = (int)ratio * numberOfChickens;
            if (area1Chickens == numberOfChickens)
            {
                if (ratio >= 1.0f)
                {
                    numberOfChickens++;
                }
                else
                {
                    area1Chickens++;
                }
            }
            this.area1Data = new AreaTrialData(circleRadius * ratio, sizeOfChicken * ratio, averageSpaceBetween * ratio, area1Chickens);
            this.area2Data = new AreaTrialData(circleRadius, sizeOfChicken, averageSpaceBetween, numberOfChickens);
            this.ratioArea = 0;
        }
        this.ratio = ratio;
        this.chickenShowTime = chickenShowTime;
    }

    public AreaTrialData getArea1Data()
    {
        return area1Data;
    }

    public AreaTrialData getArea2Data()
    {
        return area2Data;
    }

    public float getRatio()
    {
        return ratio;
    }

    public float getChickenShowTime()
    {
        return chickenShowTime;
    }

    public float getMaxTrialTime()
    {
        return maxTrialTime;
    }

}
