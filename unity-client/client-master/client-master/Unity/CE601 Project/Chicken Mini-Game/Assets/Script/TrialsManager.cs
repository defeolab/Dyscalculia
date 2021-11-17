using System;
using System.Collections.Generic;
using UnityEngine;

public class TrialsManager : MonoBehaviour
{
    public static TrialsManager instance = null;

    private static ClientToServer client;

    private Stack<TrialData> upcomingTrials;
    private List<TrialData> completedTrials;
    public List<TrialResult> completedTrialResults { get; set; }

    public bool chickensReady;
    public bool trialStarted;
    public bool gameStarted;

    public float maxTrialTime;
    public float chickenShowTime;
    public int area1Value;
    public int area2Value;

    public int correctCount = 0;
    public int incorrectCount = 0;
    public int outTimeCount = 0;

    public void Start()
    {
        if (instance == null)
        {
            instance = this;
            ConnectToClient();
            this.upcomingTrials = client.GetTrials();
            this.completedTrials = new List<TrialData>();
            this.completedTrialResults = new List<TrialResult>();
            DontDestroyOnLoad(this);
        }
        else if (instance != this)
        {
            Destroy(gameObject);
        }
    }


    public void Reset()
    {
        trialStarted = false;
        chickensReady = false;
        area1Value = 0;
        area2Value = 0;
        gameObject.GetComponent<DataManager>().Reset();
        gameObject.GetComponent<ButtonsManager>().Reset();
    }

    private void ConnectToClient()
    {
        try
        {
            client = new ClientToServer();
            Debug.Log("Logged in successfully.");
        }
        catch (Exception e)
        {
            Debug.Log(e.Message);
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
            Debug.Log("Finito");
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

    public Stack<TrialData> GetUpcomingTrials()
    {
        return upcomingTrials;
    }

    public void SetUpcomingTrials(Stack<TrialData> trials)
    {
        upcomingTrials = trials;
    }

    public void ClearResults()
    {
        this.completedTrialResults.Clear();
    }
}
