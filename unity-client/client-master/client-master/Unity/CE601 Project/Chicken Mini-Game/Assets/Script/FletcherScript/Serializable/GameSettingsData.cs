using System;

[Serializable]
public class GameSettingsData
{
    public float TotalAreaOccupiedMin;
    public float TotalAreaOccupiedMax;
    public float RatioMin;
    public float RatioMax;
    public float AverageSpaceBetweenMin;
    public float AverageSpaceBetweenMax;
    public float SizeOfChickenMin;
    public float SizeOfChickenMax;

    public GameSettingsData(float totalAreaOccupiedMin, float totalAreaOccupiedMax, float ratioMin, float ratioMax, float averageSpaceBetweenMin, float averageSpaceBetweenMax, float sizeOfChickenMin, float sizeOfChickenMax)
    {
        this.TotalAreaOccupiedMin = totalAreaOccupiedMin;
        this.TotalAreaOccupiedMax = totalAreaOccupiedMin;
        this.RatioMin = sizeOfChickenMin;
        this.RatioMax = sizeOfChickenMax;
        this.AverageSpaceBetweenMin = averageSpaceBetweenMin;
        this.AverageSpaceBetweenMax = averageSpaceBetweenMax;
        this.SizeOfChickenMin = sizeOfChickenMin;
        this.SizeOfChickenMax = sizeOfChickenMax;
    }

}
