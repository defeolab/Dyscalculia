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
    public Button area1Button, area2Button, pauseButton;
    public Text gameText;
    public GameObject[] UIImage, UIImageErrors; 
    public GameObject menu;
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
        foreach (GameObject i in UIImage) i.SetActive(false);
        foreach (GameObject i in UIImageErrors) i.SetActive(false);

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
                    this.HandleLoss();
                    this.Buttons(false);                   
                }
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
        UIImage[0].SetActive(true);
        UIImage[0].GetComponent<AudioSource>().Play();
        TrialsManager.instance.correctCount += 1;
        
        StartCoroutine(NewTrial(UIImage[0].GetComponent<AudioSource>().clip.length));
        isCoroutine = true;
    }

    private void HandleLoss()
    {
        UIImage[1].SetActive(true);
        UIImage[1].GetComponent<AudioSource>().Play();
        TrialsManager.instance.incorrectCount += 1;

        StartCoroutine(startErrorTrial(UIImage[1].GetComponent<AudioSource>().clip.length));
        isCoroutine = true;
    }

    private void CorrectAnswer_ErrorTrial()
    {
        UIImageErrors[0].SetActive(true);
        UIImageErrors[0].GetComponent<AudioSource>().Play();
        
        StartCoroutine(EndErrorTrial(UIImageErrors[0].GetComponent<AudioSource>().clip.length));
        isCoroutine = true;
    }

    private void IncorrectAnswer_ErrorTrial()
    {
        UIImageErrors[1].SetActive(true);
        UIImageErrors[1].GetComponent<AudioSource>().Play();

        StartCoroutine(WaitAndThenDo(UIImageErrors[1].GetComponent<AudioSource>().clip.length));
        isCoroutine = true;
    }

    IEnumerator startErrorTrial(float timeAudio)
    {
        Debug.Log("ERROR TRIAL");
        yield return new WaitForSeconds(timeAudio + 0.3f);

        UIImage[1].SetActive(false);
        UIImage[2].SetActive(true);
        UIImage[2].GetComponent<AudioSource>().Play();

        yield return new WaitForSeconds(UIImage[1].GetComponent<AudioSource>().clip.length + 0.3f);

        TrialsManager.instance.trialStarted = false;

        foreach (GameObject c in istance_DataManager.activeAnimals) c.SetActive(true);

        istance_ErrorTrialManager.CollectData(istance_DataManager.data, istance_DataManager.activeAnimals, 2);

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

        UIImage[2].SetActive(false);

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

        UIImageErrors[1].SetActive(false);
        gameObject.GetComponent<ErrorTrialManager>().Retry();
    }

    IEnumerator NewTrial(float timeAudio) 
    {
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
            Debug.Log("waiting"); //it's used for not block the gameplay
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

        int number = TrialsManager.instance.incorrectCount + TrialsManager.instance.correctCount;
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
        TrialsManager.instance.animalsReady = false;

        istance_DataManager.SetNewTrialData(trialData);

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
        foreach (GameObject i in UIImage) i.SetActive(false);
        foreach (GameObject i in UIImageErrors) i.SetActive(false);
    }
}
