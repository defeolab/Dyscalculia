using System;

[Serializable]
public class AreaTrialData
{
    public float circleRadius;
    public float sizeOfChicken;
    public float averageSpaceBetween;
    public int numberOfChickens;

    public AreaTrialData(float circleRadius, float sizeOfChicken, float averageSpaceBetween, int numberOfChickens)
    {
        this.circleRadius = circleRadius;
        this.sizeOfChicken = sizeOfChicken;
        this.averageSpaceBetween = averageSpaceBetween;
        this.numberOfChickens = numberOfChickens;
    }

    public float getCircleRadius()
    {
        return circleRadius;
    }

    public float getSizeOfChicken()
    {
        return sizeOfChicken;
    }

    public float getAverageSpaceBetween()
    {
        return averageSpaceBetween;
    }

    public int getNumberOfChickens()
    {
        return numberOfChickens;
    }

    public void setAverageSpaceBetween(float asb)
    {
        this.averageSpaceBetween = asb;
    }
}
