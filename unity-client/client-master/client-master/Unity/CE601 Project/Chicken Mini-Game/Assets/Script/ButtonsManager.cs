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
    public Text gameText;
    public Sprite[] spriteArray;

    private bool buttonsEnabled;

    private Stopwatch stopwatch;

    private bool newTrial = false;
    private bool elapsedChickenShowTime = false;

    private TrialData trialData;
    private DataManager dm;


    // Start is called before the first frame update
    void Start()
    {
        dm = gameObject.GetComponent<DataManager>();

        stopwatch = new Stopwatch();

        this.Buttons(false);
        buttonsEnabled = false;

        timer.gameObject.transform.Find("Fill Area").Find("Fill").GetComponent<Image>().color = Color.green;
    }

    // Update is called once per frame
    void Update()
    {
        if(!TrialsManager.instance.trialStarted)
        {
            if(!newTrial)
            {
                newTrial = true;
                StartCoroutine(NewTrial());
            } 
        }
        else if (TrialsManager.instance.chickensReady)
        {
            if (!buttonsEnabled)
            {
                this.Buttons(true);
                buttonsEnabled = true;
                timer.maxValue = TrialsManager.instance.chickenShowTime * 1000;
                timer.value = TrialsManager.instance.chickenShowTime * 1000;
                stopwatch.Start();
                timer.gameObject.GetComponent<AudioSource>().Play();
                gameText.text = "Please now select the area which has the most chickens";
            }

            timer.value = timer.maxValue - stopwatch.ElapsedMilliseconds;

            if (stopwatch.IsRunning && stopwatch.ElapsedMilliseconds > (TrialsManager.instance.chickenShowTime * 1000) && !elapsedChickenShowTime)
            {
                foreach(GameObject c in dm.activeChickens)
                {
                    c.SetActive(false);
                }

                clockImage.sprite = spriteArray[0];
                timer.maxValue = TrialsManager.instance.maxTrialTime * 1000;
                timer.value = TrialsManager.instance.maxTrialTime * 1000;
                timer.gameObject.transform.Find("Fill Area").Find("Fill").GetComponent<Image>().color = Color.yellow;
                elapsedChickenShowTime = true;
            }
            else if (stopwatch.IsRunning && stopwatch.ElapsedMilliseconds >= (TrialsManager.instance.maxTrialTime * 1000))
            {
                stopwatch.Stop();
                timer.gameObject.GetComponent<AudioSource>().Stop();
                double elapsedTime = stopwatch.Elapsed.TotalMilliseconds;
                TrialsManager.instance.AddTrialResult(elapsedTime, false);
                this.HandleLoss();
                this.Buttons(false);
                StartCoroutine(NewTrial());
            }
        }  
    }

    public void Area1Selected()
    {
        Debug.Log("Area1");
        ButtonSelected(TrialsManager.instance.area1Value, TrialsManager.instance.area2Value);
    }

    public void Area2Selected()
    {
        Debug.Log("Area2");
        ButtonSelected(TrialsManager.instance.area2Value, TrialsManager.instance.area1Value);

    }

    private void ButtonSelected(int selectedArea, int unselectedArea)
    {
        stopwatch.Stop();
        timer.gameObject.GetComponent<AudioSource>().Stop();
        Debug.Log("Time elapsed: " + stopwatch.Elapsed);
        bool correct = selectedArea > unselectedArea;
        double elapsedTime = stopwatch.Elapsed.TotalMilliseconds;
        TrialsManager.instance.AddTrialResult(elapsedTime, correct);
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
    }

    private void Buttons(bool flag)
    {
        area1Button.interactable = flag;
        area2Button.interactable = flag;
    }

    private void HandleWin()
    {
        gameText.text = "Correct Answer!";
        TrialsManager.instance.correctCount += 1;
    }

    private void HandleLoss()
    {
        gameText.text = "Incorrect Answer!";
        TrialsManager.instance.incorrectCount += 1;
    }

    IEnumerator NewTrial() 
    {
        Debug.Log("NEW TRIAL");
        yield return new WaitForSeconds(1);
        TrialsManager.instance.Reset();
        TrialData nextTrial = TrialsManager.instance.GetNextTrial();
        
        if (nextTrial != null)
        {
            dm.SetNewTrialData(nextTrial);
        }
        else
        {
            Debug.Log("FINITO");
        }
        
    }

    public void PauseTrial()
    {
        TrialsManager.instance.trialStarted = false;
        trialData = dm.data;
        Debug.Log("PAUSA");
        dm.prova();

    }

    public void RestartTrial()
    {
        Debug.Log("RESTART");
        stopwatch.Reset();
        dm.SetNewTrialData(trialData);

    }

    public void Reset()
    {
        stopwatch.Reset();
        this.Buttons(false);
        buttonsEnabled = false;
        timer.maxValue = 1;
        timer.value = timer.maxValue;
        clockImage.sprite = spriteArray[1];
        gameText.text = "";
        timer.gameObject.transform.Find("Fill Area").Find("Fill").GetComponent<Image>().color = Color.green;
        elapsedChickenShowTime = false;
    }
}
