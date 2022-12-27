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
    public Button area1Button, area2Button;
    public Text gameText;
    public GameObject UIImageCorrect, UIImageIncorrect, UIImageTimeOut, UIImageWhy, UIImageErrorRight, UIImageErrorWrong; 
    public GameObject menu, pauseButton;
    private Stopwatch stopwatch;
    private TrialData trialData;
    private DataManager istance_DataManager;
    private ErrorTrialManager istance_ErrorTrialManager;
    private bool buttonsEnabled, elapsedAnimalShowTime, firstTrial, isCoroutine;

    void Start()
    {
        istance_DataManager = gameObject.GetComponent<DataManager>();
        istance_ErrorTrialManager = gameObject.GetComponent<ErrorTrialManager>();

        stopwatch = new Stopwatch();

        this.Buttons(false);
        menu.SetActive(false);
        UIImageCorrect.SetActive(false);
        UIImageIncorrect.SetActive(false);
        UIImageTimeOut.SetActive(false);
        UIImageWhy.SetActive(false);
        UIImageErrorRight.SetActive(false);
        UIImageErrorWrong.SetActive(false);

        gameText.text = "";
        isCoroutine = false;
        buttonsEnabled = false;
        firstTrial = false;
        elapsedAnimalShowTime = false;
    }

    void Update()
    {
        if (TrialsManager.instance.connectionStarted)
        {
            if (!TrialsManager.instance.trialStarted)
            {
                if (!firstTrial)
                {
                    firstTrial = true;
                    this.FirstTrial();
                }
            }
            else if (TrialsManager.instance.animalsReady)
            {
                if (!buttonsEnabled)
                {
                    this.Buttons(true);
                    buttonsEnabled = true;

                    stopwatch.Start();

                    gameText.text = "Click on the fence where there are more animals";
                    gameText.GetComponent<AudioSource>().Play();
                }

                //Check if the time is greater than AnimalShowTime
                if (stopwatch.IsRunning && stopwatch.ElapsedMilliseconds > (TrialsManager.instance.animalShowTime * 1000) && !elapsedAnimalShowTime)
                {
                    foreach (GameObject c in istance_DataManager.activeAnimals) c.SetActive(false);
                    elapsedAnimalShowTime = true;
                }

                //Check if the time is greater than maxTrialTime -> incorrect answer for trial
                else if (stopwatch.IsRunning && stopwatch.ElapsedMilliseconds >= (TrialsManager.instance.maxTrialTime * 1000))
                {
                    stopwatch.Stop();
                    double elapsedTime = stopwatch.Elapsed.TotalMilliseconds;
                    TrialsManager.instance.AddTrialResult(elapsedTime, false);
                    gameText.text = "";
                    this.HandleLossForTime();
                    this.Buttons(false);                   
                }
            }

            if (isCoroutine) pauseButton.SetActive(false);
            else pauseButton.SetActive(true);
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
        if (!gameObject.GetComponent<ErrorTrialManager>().startError)
        {
            stopwatch.Stop();
            Debug.Log("Number of Animals in area selected: " + selectedArea + " Time elapsed: " + stopwatch.Elapsed);

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
        }
        else
        {
            foreach (GameObject i in gameObject.GetComponent<ErrorTrialManager>().UIImage)
            {
                i.SetActive(false);
                i.GetComponent<AudioSource>().Stop();
            }

            if (selectedArea > unselectedArea)
            {
                CorrectAnswer_ErrorTrial();
            }
            else
            {
                IncorrectAnswer_ErrorTrial();
            }

            this.Buttons(false);

        }
        
    }

    public void Buttons(bool flag)
    {
        area1Button.interactable = flag;
        area2Button.interactable = flag;
    }

    private void HandleWin()
    {
        UIImageCorrect.SetActive(true);
        UIImageCorrect.GetComponent<AudioSource>().Play();
        TrialsManager.instance.correctCount += 1;
        
        StartCoroutine(NewTrial(UIImageCorrect.GetComponent<AudioSource>().clip.length));
        isCoroutine = true;
    }

    private void HandleLoss()
    {
        UIImageIncorrect.SetActive(true);
        UIImageIncorrect.GetComponent<AudioSource>().Play();
        TrialsManager.instance.incorrectCount += 1;

        StartCoroutine(startErrorTrial(UIImageIncorrect.GetComponent<AudioSource>().clip.length));
        isCoroutine = true;
    }

    private void HandleLossForTime()
    {
        UIImageTimeOut.SetActive(true);
        UIImageTimeOut.GetComponent<AudioSource>().Play();
        TrialsManager.instance.incorrectCount += 1;

        StartCoroutine(startErrorTrial(UIImageTimeOut.GetComponent<AudioSource>().clip.length));
        isCoroutine = true;
    }

    private void CorrectAnswer_ErrorTrial()
    {
        UIImageErrorRight.SetActive(true);
        UIImageErrorRight.GetComponent<AudioSource>().Play();
        if (gameObject.GetComponent<ErrorTrialManager>().version == 1 && !gameObject.GetComponent<ErrorTrialManager>().setHays_noSliders) gameObject.GetComponent<ErrorTrialManager>().canvasSliders.SetActive(false);

        StartCoroutine(EndErrorTrial(UIImageErrorRight.GetComponent<AudioSource>().clip.length));
        isCoroutine = true;
    }

    private void IncorrectAnswer_ErrorTrial()
    {
        UIImageErrorWrong.SetActive(true);
        UIImageErrorWrong.GetComponent<AudioSource>().Play();
        if(gameObject.GetComponent<ErrorTrialManager>().version==1 && !gameObject.GetComponent<ErrorTrialManager>().setHays_noSliders) gameObject.GetComponent<ErrorTrialManager>().canvasSliders.SetActive(false);

        StartCoroutine(WaitAndThenDo(UIImageErrorWrong.GetComponent<AudioSource>().clip.length));
        isCoroutine = true;
    }

    IEnumerator startErrorTrial(float timeAudio)
    {
        Debug.Log("ERROR TRIAL");
        yield return new WaitForSeconds(timeAudio + 0.3f);

        UIImageTimeOut.SetActive(false);
        UIImageIncorrect.SetActive(false);
        UIImageWhy.SetActive(true);
        UIImageWhy.GetComponent<AudioSource>().Play();

        yield return new WaitForSeconds(UIImageWhy.GetComponent<AudioSource>().clip.length + 0.3f);

        TrialsManager.instance.trialStarted = false;

        foreach (GameObject c in istance_DataManager.activeAnimals) c.SetActive(true);

        istance_ErrorTrialManager.CollectData(istance_DataManager.data, istance_DataManager.activeAnimals, 3);

        /*
        version 1 = if the animals are on a line the child should place them hay after hay; if not create the slider
        version 2 = place the animals only a line ten after ten and every ten creates an animal that indicates 10
        version 3 = place the animals only one row ten after ten column after column (to be implemented) 
        */

        foreach (GameObject f in istance_DataManager.fences)
        {
            f.SetActive(false);
        }

        foreach (GameObject a in istance_DataManager.areas)
        {
            a.SetActive(false);
        }

        UIImageWhy.SetActive(false);

        isCoroutine = false;
    }

    IEnumerator EndErrorTrial(float timeAudio)
    {
        yield return new WaitForSeconds(timeAudio + 0.3f);

        istance_ErrorTrialManager.Reset();
        gameObject.GetComponent<DragManager>().Reset();
        StartCoroutine(NewTrial(-0.3f));
        isCoroutine = true;
    }

    IEnumerator WaitAndThenDo(float timeAudio)
    {
        yield return new WaitForSeconds(timeAudio + 0.3f);

        UIImageErrorWrong.SetActive(false);
        if (gameObject.GetComponent<ErrorTrialManager>().version == 1 && !gameObject.GetComponent<ErrorTrialManager>().setHays_noSliders) gameObject.GetComponent<ErrorTrialManager>().canvasSliders.SetActive(true);
        gameObject.GetComponent<ErrorTrialManager>().Retry();
        isCoroutine = false;
    }

    IEnumerator NewTrial(float timeAudio) 
    {
        TrialsManager.instance.AskNextTrial();
        yield return new WaitForSeconds(timeAudio + 0.3f);
        
        //Reset all the Managers
        TrialsManager.instance.Reset();
        istance_DataManager.Reset();
        this.Reset();

        TrialData nextTrial = TrialsManager.instance.GetNextTrial();
        
        if (nextTrial != null)
        {
            istance_DataManager.SetNewTrialData(nextTrial);

            int number = TrialsManager.instance.incorrectCount + TrialsManager.instance.correctCount;
            Debug.Log("TRIAL N°" + number);
        }
        else
        {
            Debug.Log("finish"); //it's used for not block the gameplay
        }

        isCoroutine = false;        
    }

    public void WaitNewTrial()
    {
        StartCoroutine(NewTrial(1f));
    }

    public void FirstTrial()
    {
        //Reset all the Managers
        TrialsManager.instance.Reset();
        istance_DataManager.Reset();
        this.Reset();

        TrialData nextTrial = TrialsManager.instance.GetNextTrial();
        istance_DataManager.SetNewTrialData(nextTrial);

        int number = (TrialsManager.instance.incorrectCount + TrialsManager.instance.correctCount) + 1;
        Debug.Log("TRIAL N°" + number);
    }

    public void PauseTrial()
    {
        if (!isCoroutine) //check that the coroutine for the new trial has not started
        {
            Debug.Log("PAUSE TRIAL");
            TrialsManager.instance.trialStarted = false;
            trialData = istance_DataManager.data;
            menu.SetActive(true);
            menu.GetComponent<Menu>().SetActiveSettingsMenu(false); //active only Pause Menu
            gameText.GetComponent<AudioSource>().Stop();
            //foreach (GameObject i in UIImage) i.GetComponent<AudioSource>().Stop();
        }

    }

    public void RestartTrial()
    {
        menu.SetActive(false);

        if (!gameObject.GetComponent<ErrorTrialManager>().startError)
        {

            Debug.Log("RESTART TRIAL");
            
            //Reset all the values
            this.Reset();
            istance_DataManager.Reset();
            TrialsManager.instance.animalsReady = false;

            istance_DataManager.SetNewTrialData(trialData);
        }
    }

    public void Reset()
    {
        stopwatch.Reset();
        this.Buttons(false);
        buttonsEnabled = false;
        elapsedAnimalShowTime = false;
        menu.SetActive(false);
        foreach (GameObject f in istance_DataManager.fences) f.SetActive(true);
        foreach (GameObject a in istance_DataManager.areas) a.SetActive(true);

        UIImageCorrect.SetActive(false);
        UIImageIncorrect.SetActive(false);
        UIImageTimeOut.SetActive(false);
        UIImageWhy.SetActive(false);
        UIImageErrorRight.SetActive(false);
        UIImageErrorWrong.SetActive(false);
    }
}
