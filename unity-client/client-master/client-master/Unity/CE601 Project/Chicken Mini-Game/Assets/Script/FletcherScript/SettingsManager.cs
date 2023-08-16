using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SettingsManager : MonoBehaviour
{
    public InputField RatioMinInput;
    public InputField RatioMaxInput;
    public InputField AverageSpaceBetweenMinInput;
    public InputField AverageSpaceBetweenMaxInput;
    public InputField SizeOfChickenMinInput;
    public InputField SizeOfChickenMaxInput;
    public InputField TotalAreaOccupiedMinInput;
    public InputField TotalAreaOccupiedMaxInput;
    public GameObject SettingsObject;

    public float ratioMin;
    public float ratioMax;
    public float averageSpaceBetweenMin;
    public float averageSpaceBetweenMax;
    public float sizeOfChickenMin;
    public float sizeOfChickenMax;
    public float totalAreaOccupiedMin;
    public float totalAreaOccupiedMax;

    public static SettingsManager instance = null;

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            this.ratioMin = 0.5f;
            this.ratioMax = 0.9f;
            this.averageSpaceBetweenMin = 0.7f;
            this.averageSpaceBetweenMax = 1.7f;
            this.sizeOfChickenMin = 1.2f;
            this.sizeOfChickenMax = 2f;
            this.totalAreaOccupiedMin = 5f;
            this.totalAreaOccupiedMax = 15f;
            DontDestroyOnLoad(this);
        }
        else if (instance != this)
        {
            Destroy(gameObject);
        }
        SettingsManager.instance.GetSettingsObject(); 
        SettingsManager.instance.Hide();
    }
    public void SaveSettings()
    {
        this.ratioMin = float.Parse(RatioMinInput.text);
        this.ratioMax = float.Parse(RatioMaxInput.text);
        this.averageSpaceBetweenMin = float.Parse(AverageSpaceBetweenMinInput.text);
        this.averageSpaceBetweenMax = float.Parse(AverageSpaceBetweenMaxInput.text);
        this.sizeOfChickenMin = float.Parse(SizeOfChickenMinInput.text);
        this.sizeOfChickenMax = float.Parse(SizeOfChickenMaxInput.text);
        this.totalAreaOccupiedMin = float.Parse(TotalAreaOccupiedMinInput.text);
        this.totalAreaOccupiedMax = float.Parse(TotalAreaOccupiedMaxInput.text);
        if (!GameManager.instance.demoMode)
        {
            GameSettingsData settings = new GameSettingsData(this.totalAreaOccupiedMin, this.totalAreaOccupiedMax, this.ratioMin, this.ratioMax, this.averageSpaceBetweenMin, this.averageSpaceBetweenMax, this.sizeOfChickenMin, this.sizeOfChickenMax);
            GameManager.instance.SaveSettings(settings);
        }
        this.Hide();
    }

    public void GetSettingsObject()
    {
        this.SettingsObject = GameObject.FindGameObjectWithTag("Settings");
    }

    public void Hide()
    {
        this.SettingsObject.SetActive(false);
    }

    public void Show()
    {
        this.SettingsObject.SetActive(true);
    }
}
