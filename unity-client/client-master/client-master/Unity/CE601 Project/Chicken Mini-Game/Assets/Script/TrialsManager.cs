using System;
using System.Collections.Generic;
using UnityEngine;
using System.Collections;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using Newtonsoft.Json;
using System.IO;
using System.Diagnostics;
using Debug = UnityEngine.Debug;

public class TrialsManager : MonoBehaviour
{
    public static TrialsManager instance = null;
    private static ClientToServer client;

    private Stack<TrialData> upcomingTrials;
    public List<TrialResult> completedTrialResults { get; set; }

    public bool animalsReady = false, trialStarted, connectionStarted = false;

    public float maxTrialTime, animalShowTime;
    public int area1Value, area2Value;

    public int correctCount = 0, incorrectCount = 0;
    public int maxTrialsNum;

    private TrialData currentTrial = null;
    
    //For now they're used to check if the connection's established and when the trials're finished
    public GameObject errorImage, finishImage;
    public Text AnswersText;

    public bool remote;
    public bool useLan;
    public string ip;

    public void Start()
    {
        this.completedTrialResults = new List<TrialResult>();

        errorImage.SetActive(false);
        finishImage.SetActive(false);

        instance = this;
        maxTrialsNum = StoreIPAddress.instance.numTrials;

        ConnectWithClient();
    }

    public void Reset()
    {
        trialStarted = false;
        animalsReady = false;
        area1Value = 0;
        area2Value = 0;
    }

    public void ConnectWithClient()
    {
        ip = StoreIPAddress.instance.ipAddress;

        try
        {
            client = new ClientToServer(remote, useLan, ip);
            Debug.Log("Logged in successfully");
            connectionStarted = true;
            errorImage.SetActive(false);
            errorImage.GetComponent<AudioSource>().Stop();
            client.AskTrials();
            this.upcomingTrials = client.GetTrials();

            //Debug.Log(upcomingTrials.ToString());
        }
        catch (Exception e)
        {
            Debug.Log(e.Message);
            errorImage.SetActive(true);
            errorImage.GetComponent<AudioSource>().Play();
            connectionStarted = false;
        }
    }

    public TrialData GetTrial()
    {
        if (upcomingTrials.Count != 0)
        {
            currentTrial = upcomingTrials.Pop();
            animalShowTime = currentTrial.getAnimalShowTime();
            maxTrialTime = currentTrial.getMaxTrialTime();
        }
        else
        {
            client.CompleteTrials();
            Debug.Log("FIND NEW TRIAL");
            client.AskTrials();
            this.upcomingTrials = client.GetTrials();
            Debug.Log(upcomingTrials.ToString());
            this.GetTrial();
        }

        return currentTrial;
    }

    public void AskNextTrial()
    {
        if (correctCount + incorrectCount != 0){
            client.CompleteTrials();
            client.AskTrials();
        }
        
    }

    public TrialData GetNextTrial()
    {
        if (correctCount + incorrectCount == maxTrialsNum)
        {
            //client.CompleteTrials();
            client.Dispose();
            finishImage.SetActive(true);
            finishImage.GetComponent<AudioSource>().Play();
            AnswersText.text = "Correct Answers: " + correctCount + "\nIncorrect Answers: " + incorrectCount;
            StartCoroutine(ReturnHome(finishImage.GetComponent<AudioSource>().clip.length+2f));
        }
        else
        {
            if (correctCount + incorrectCount != 0)
            {
                //client.CompleteTrials();
                this.upcomingTrials = client.GetTrials();
            }    
            
            //currentTrial = this.ChangeValuesForControls(upcomingTrials.Pop());
            currentTrial = upcomingTrials.Pop();

            animalShowTime = currentTrial.getAnimalShowTime();
            maxTrialTime = currentTrial.getMaxTrialTime();

            return currentTrial;
        }

        return null;
    }

    public void AddTrialResult(double decisionTime, bool correct)
    {
        this.completedTrialResults.Add(new TrialResult(decisionTime, correct, currentTrial));
    }

    public void ClearResults()
    {
        this.completedTrialResults.Clear();
        this.upcomingTrials.Clear();
    }

    IEnumerator ReturnHome(float timeAudio)
    {
        yield return new WaitForSeconds(timeAudio + 0.3f);
        SceneManager.LoadScene(0);
    }

    private TrialData ChangeValuesForControls(TrialData trial)
    {
        trial.area1Data.SetValuesForControls(1.2f, 5.5f, 1.1f, 4);
        trial.area2Data.SetValuesForControls(0.95f, 7f, 1.35f, 5);
        trial.SetTime(6f, 8f);

        return trial;
    }

    //Not used for now
    public Stack<TrialData> GetUpcomingTrials() { return upcomingTrials; }
    public void SetUpcomingTrials(Stack<TrialData> trials) { upcomingTrials = trials; }
}