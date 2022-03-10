using System;
using System.Collections.Generic;
using UnityEngine;

public class TrialsManager : MonoBehaviour
{
    public static TrialsManager instance = null;
    private static ClientToServer client;
    public GameObject errorImage;
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

    public void Start()
    {
        errorImage.SetActive(false);
        instance = this;
        ConnectToClient();
        this.completedTrials = new List<TrialData>();
        this.completedTrialResults = new List<TrialResult>();
            
    }

    public void Reset()
    {
        trialStarted = false;
        chickensReady = false;
        area1Value = 0;
        area2Value = 0;
    }

    public void ConnectToClient()
    {
        try
        {
            client = new ClientToServer();
            Debug.Log("Logged in successfully.");
            connectionStarted = true;
            errorImage.SetActive(false);
            this.upcomingTrials = client.GetTrials();

        }
        catch (Exception e)
        {
            Debug.Log(e.Message);
            errorImage.SetActive(true);
            connectionStarted = false;

        }
    }

    public TrialData GetNextTrial()
    {
        TrialData nextTrial=null;
        if (upcomingTrials.Count > 0)
        {
            nextTrial = upcomingTrials.Pop();
            chickenShowTime = nextTrial.getChickenShowTime();
            maxTrialTime = nextTrial.getMaxTrialTime();
        }
        else
        {
            Debug.Log("Finish Trials"); //it's used for not block the gameplay
            client.CompleteTrials();
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

    //it's not use for now
    public Stack<TrialData> GetUpcomingTrials() { return upcomingTrials; }
    public void SetUpcomingTrials(Stack<TrialData> trials) { upcomingTrials = trials; }

    public void stamp()
    {
        Debug.Log("button press");
    }

}
