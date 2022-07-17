using System;
using System.Collections.Generic;
using UnityEngine;

public class TrialsManager : MonoBehaviour
{
    public static TrialsManager instance = null;
    private static ClientToServer client;
    
    private Stack<TrialData> upcomingTrials;
    public List<TrialData> completedTrials;
    public List<TrialResult> completedTrialResults { get; set; }

    public bool chickensReady;
    public bool trialStarted;
    public bool gameStarted;
    public bool connectionStarted=false;

    public float maxTrialTime;
    public float chickenShowTime;
    public int area1Value;
    public int area2Value;

    public int correctCount = 0;
    public int incorrectCount = 0;

    //For now they're used to check if the connection's established and when the trials're finished
    public GameObject errorImage;
    public GameObject finishImage;

    public void Start()
    {
        this.completedTrials = new List<TrialData>();
        this.completedTrialResults = new List<TrialResult>();
        
        errorImage.SetActive(false);
        
        instance = this;
        ConnectWithClient(); 
    }

    public void Reset()
    {
        trialStarted = false;
        chickensReady = false;
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
        TrialData nextTrial=null;

        if (upcomingTrials.Count > 1)
        {
            nextTrial = upcomingTrials.Pop();
            chickenShowTime = nextTrial.getChickenShowTime();
            maxTrialTime = nextTrial.getMaxTrialTime();
        }
        else if(upcomingTrials.Count == 1)
        {
            nextTrial = upcomingTrials.Pop();
            client.CompleteTrials();
            this.upcomingTrials = client.GetTrials();
        }
        else
        {
            Debug.Log("Trials finished for now");
            finishImage.SetActive(true);
        }

        if (nextTrial != null)
        {
            completedTrials.Add(nextTrial);
        }
        
        return nextTrial;
    }

    public void AddTrialResult(double decisionTime, bool correct)
    {
        this.completedTrialResults.Add(new TrialResult(decisionTime, correct, this.completedTrials[this.completedTrials.Count - 1]));
    }

    public void ClearResults()
    {
        this.completedTrialResults.Clear();
    }

    //Not used for now
    public Stack<TrialData> GetUpcomingTrials() { return upcomingTrials; }
    public void SetUpcomingTrials(Stack<TrialData> trials) { upcomingTrials = trials; }
}