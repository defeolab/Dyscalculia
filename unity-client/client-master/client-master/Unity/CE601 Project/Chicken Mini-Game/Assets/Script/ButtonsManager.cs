using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using Newtonsoft.Json;
using System.IO;
using System.Collections.Generic;
using System.Diagnostics;
using Debug = UnityEngine.Debug;

public class ButtonsManager : MonoBehaviour
{
    public Button area1Button;
    public Button area2Button;
    public Button pauseButton;

    public Slider timer;
    public SpriteRenderer clockImage;
    public Sprite[] clockSprite;
    private Stopwatch stopwatch;

    public Text gameText;
    public GameObject[] UIImage; 
    
    public GameObject menu;

    private bool buttonsEnabled;
    private bool elapsedChickenShowTime;
    private bool firstTrial;
    private bool isCoroutine;

    private TrialData trialData;
    private DataManager istance_DataManager;

    void Start()
    {
        istance_DataManager = gameObject.GetComponent<DataManager>();
        
        stopwatch = new Stopwatch();

        this.Buttons(false);
        buttonsEnabled = false;
        firstTrial = false;
        elapsedChickenShowTime = false;
        foreach (GameObject i in UIImage) i.SetActive(false);
        menu.SetActive(false);
        gameText.text = "";
        isCoroutine = false;

        timer.gameObject.transform.Find("Fill Area").Find("Fill").GetComponent<Image>().color = Color.green;
    }

    void Update()
    {
        if(!TrialsManager.instance.trialStarted)
        {
            if (!firstTrial)
            {
                firstTrial = true;
                StartCoroutine(NewTrial());
                isCoroutine = true;
            }
        }
        else if (TrialsManager.instance.chickensReady)
        {
            if (!buttonsEnabled)
            {
                this.Buttons(true);
                buttonsEnabled = true;

                //Start timer
                timer.maxValue = TrialsManager.instance.chickenShowTime * 1000;
                timer.value = TrialsManager.instance.chickenShowTime * 1000;
                stopwatch.Start();
                timer.gameObject.GetComponent<AudioSource>().Play();

                gameText.text = "Click on the fence that contains more chickens";
                gameText.GetComponent<AudioSource>().Play();
            }

            //Decrement timer
            timer.value = timer.maxValue - stopwatch.ElapsedMilliseconds;

            //Controll if time is > of ChickenShowTime
            if (stopwatch.IsRunning && stopwatch.ElapsedMilliseconds > (TrialsManager.instance.chickenShowTime * 1000) && !elapsedChickenShowTime)
            {
                foreach(GameObject c in istance_DataManager.activeChickens)
                {
                    c.SetActive(false);
                }
                
                //set value and color of slider
                clockImage.sprite = clockSprite[0];
                timer.maxValue = TrialsManager.instance.maxTrialTime * 1000;
                timer.value = TrialsManager.instance.maxTrialTime * 1000;
                timer.gameObject.transform.Find("Fill Area").Find("Fill").GetComponent<Image>().color = Color.yellow;
                elapsedChickenShowTime = true;
            }

            //Controll if time is > of maxTrialTime --> incorrect answer for trail
            else if (stopwatch.IsRunning && stopwatch.ElapsedMilliseconds >= (TrialsManager.instance.maxTrialTime * 1000))
            {
                stopwatch.Stop();
                timer.gameObject.GetComponent<AudioSource>().Stop();
                double elapsedTime = stopwatch.Elapsed.TotalMilliseconds;
                TrialsManager.instance.AddTrialResult(elapsedTime, false);
                gameText.text = "";
                this.HandleLoss();
                this.Buttons(false);
                
                StartCoroutine(NewTrial());
                isCoroutine = true;
            }
        }  
    }

    public void Area1Selected()
    {
        ButtonSelected(TrialsManager.instance.area1Value, TrialsManager.instance.area2Value);
    }

    public void Area2Selected()
    {
        ButtonSelected(TrialsManager.instance.area2Value, TrialsManager.instance.area1Value);
    }

    private void ButtonSelected(int selectedArea, int unselectedArea)
    {
        stopwatch.Stop();
        timer.gameObject.GetComponent<AudioSource>().Stop();

        Debug.Log("Area selected: "+ selectedArea + " Time elapsed: " + stopwatch.Elapsed);

        bool correct = selectedArea > unselectedArea;
        double elapsedTime = stopwatch.Elapsed.TotalMilliseconds;
        TrialsManager.instance.AddTrialResult(elapsedTime, correct);
        gameText.text = "";
        gameText.GetComponent<AudioSource>().Stop();

        if (correct)
        {
            HandleWin();
        }
        else
        {
            HandleLoss();
        }
        
        this.Buttons(false);
        
        StartCoroutine(NewTrial());
        isCoroutine = true;

    }

    private void Buttons(bool flag)
    {
        area1Button.interactable = flag;
        area2Button.interactable = flag;
    }

    private void HandleWin()
    {
        UIImage[0].SetActive(true);
        UIImage[0].GetComponent<AudioSource>().Play();
        TrialsManager.instance.correctCount += 1;
    }

    private void HandleLoss()
    {
        UIImage[1].SetActive(true);
        UIImage[1].GetComponent<AudioSource>().Play();
        TrialsManager.instance.incorrectCount += 1;
    }

    IEnumerator NewTrial() 
    {
        Debug.Log("NEW TRIAL");
        yield return new WaitForSeconds(4);

        //Reset all the Managers
        TrialsManager.instance.Reset();
        istance_DataManager.Reset();
        this.Reset();

        TrialData nextTrial = TrialsManager.instance.GetNextTrial();
        
        if (nextTrial != null)
        {
            istance_DataManager.SetNewTrialData(nextTrial);
        }
        else
        {
            Debug.Log("Finished"); //it's used for not block the gameplay
        }
        isCoroutine = false;
    }

    public void PauseTrial()
    {
        Debug.Log(isCoroutine);
        if (!isCoroutine)
        {
            Debug.Log("PAUSE TRIAL");
            TrialsManager.instance.trialStarted = false;
            trialData = istance_DataManager.data;
            menu.SetActive(true);
            menu.GetComponent<Menu>().SetActiveSettingsMenu(false); //active only Pause Menu
            timer.gameObject.GetComponent<AudioSource>().Stop();
            gameText.GetComponent<AudioSource>().Stop();
            foreach (GameObject i in UIImage) i.GetComponent<AudioSource>().Stop();
        }

    }

    public void RestartTrial()
    {
        Debug.Log("RESTART TRIAL");
        menu.SetActive(false);
        
        //Reset all the values
        this.Reset();
        istance_DataManager.Reset();
        TrialsManager.instance.chickensReady = false;

        istance_DataManager.SetNewTrialData(trialData);
    }

    public void Reset()
    {
        stopwatch.Reset();
        this.Buttons(false);
        buttonsEnabled = false;
        timer.maxValue = 1;
        timer.value = timer.maxValue;
        clockImage.sprite = clockSprite[1];
        gameText.text = "";
        timer.gameObject.transform.Find("Fill Area").Find("Fill").GetComponent<Image>().color = Color.green;
        elapsedChickenShowTime = false;
        foreach (GameObject i in UIImage) i.SetActive(false);
        menu.SetActive(false);
    }
}
