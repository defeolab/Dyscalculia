using System;
using System.Collections.Generic;
using UnityEngine;

public class TrialsManager : MonoBehaviour
{
    public static TrialsManager instance = null;
    private static ClientToServer client;

    private Stack<TrialData> upcomingTrials;
    //public List<TrialData> completedTrials;
    public List<TrialResult> completedTrialResults { get; set; }

    public bool animalsReady = false, trialStarted, connectionStarted = false;

    public float maxTrialTime, animalShowTime;
    public int area1Value, area2Value;

    public int correctCount = 0, incorrectCount = 0, totalCount;

    public TrialData currentTrial = null;

    //For now they're used to check if the connection's established and when the trials're finished
    public GameObject errorImage, finishImage;

    public void Start()
    {
        //this.completedTrials = new List<TrialData>();
        this.completedTrialResults = new List<TrialResult>();

        errorImage.SetActive(false);

        instance = this;
        ConnectWithClient();
        totalCount = 0;
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
        try
        {
            client = new ClientToServer();
            Debug.Log("Logged in successfully");
            connectionStarted = true;
            errorImage.SetActive(false);
            errorImage.GetComponent<AudioSource>().Stop();
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

    public TrialData GetNextTrial()
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
            this.upcomingTrials = client.GetTrials();
        }

        return currentTrial;
    }

    public void AddTrialResult(double decisionTime, bool correct)
    {
        this.completedTrialResults.Add(new TrialResult(decisionTime, correct, currentTrial));
    }

    public void ClearResults()
    {
        this.completedTrialResults.Clear();
        //this.completedTrials.Clear();
        //this.upcomingTrials.Clear();
    }

    //Not used for now
    public Stack<TrialData> GetUpcomingTrials() { return upcomingTrials; }
    public void SetUpcomingTrials(Stack<TrialData> trials) { upcomingTrials = trials; }
}