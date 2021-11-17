using System;
using System.Collections.Generic;
using UnityEngine;

/*
 @Author: Fletcher Hurn (1806938)
 */
public class GameManager : MonoBehaviour
{
    public static GameManager instance = null;

    public bool chickensReady;
    public bool demoMode;
    public bool gameStarted;

    public int area1Chickens;
    public int area2Chickens;

    public int correctCount = 0;
    public int incorrectCount = 0;

    public int numberOfTrialsToGenerate = 0;
    public float chickenShowTime;
    public float maxTrialTime;

    private Stack<GameTrialData> upcomingTrials;
    private List<GameTrialData> completedTrials;
    public List<GameTrialResult> completedTrialResults { get; set; }

    private static Client client;

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            if (!demoMode)
            {
                ConnectToClient();
            }
            this.upcomingTrials = this.generateTrials();
            this.completedTrials = new List<GameTrialData>();
            this.completedTrialResults = new List<GameTrialResult>();
            this.gameStarted = false;
            DontDestroyOnLoad(this);
        } else if (instance != this) {
            Destroy(gameObject);
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        Reset();
    }

    public void Reset()
    {
        chickensReady = false;
        area1Chickens = 0;
        area2Chickens = 0;
    }

    public void StartGame()
    {
        this.gameStarted = true;
    }

    // Update is called once per frame
    void Update()
    {
    }

    public GameTrialData getNextTrial()
    {
        GameTrialData nextTrial;
        if (upcomingTrials.Count > 0)
        {
            nextTrial = upcomingTrials.Pop();
            chickenShowTime = nextTrial.getChickenShowTime();
            maxTrialTime = nextTrial.getMaxTrialTime();
        } else
        {
            if (!demoMode)
            {
                client.CompleteTrials();
            }
            upcomingTrials = generateTrials();
            nextTrial = upcomingTrials.Pop();
        }
        completedTrials.Add(nextTrial);
        return nextTrial;
    }
    private Stack<GameTrialData> generateTrials()
    {
        if (demoMode) {
            Stack<GameTrialData> upcomingTrials = new Stack<GameTrialData>();
            for (int i = 0; i < numberOfTrialsToGenerate; i++)
            {
                upcomingTrials.Push(generateNewRandomTrial());
            }
            return upcomingTrials;
        } else
        {
            return GameManager.client.GetTrials();
        }
    }

    public void SaveSettings(GameSettingsData settings)
    {
        GameManager.client.SaveSettings(settings);
    }

    public void AddTrialResult(double decisionTime, bool correct)
    {
        this.completedTrialResults.Add(new GameTrialResult(decisionTime, correct, this.completedTrials[this.completedTrials.Count - 1]));
    }

    // The below method is for testing/demo purposes only
    private GameTrialData generateNewRandomTrial()
    {
        SettingsManager settings = SettingsManager.instance;
        float ratio = UnityEngine.Random.Range(settings.ratioMin, settings.ratioMax);
        float averageSpaceBetween = UnityEngine.Random.Range(settings.averageSpaceBetweenMin, settings.averageSpaceBetweenMax);
        float sizeOfChicken = UnityEngine.Random.Range(settings.sizeOfChickenMin, settings.sizeOfChickenMax);
        float totalAreaOccupied = UnityEngine.Random.Range(settings.totalAreaOccupiedMin, settings.totalAreaOccupiedMax);
        float circleRadius = (float)Math.Sqrt(totalAreaOccupied / Math.PI);
        float chickenShowTime = UnityEngine.Random.Range(4, 6);
        int numberOfChickens = UnityEngine.Random.Range(2, 8);
        return new GameTrialData(circleRadius, sizeOfChicken, averageSpaceBetween, ratio, chickenShowTime, numberOfChickens);
    }

    public Stack<GameTrialData> getUpcomingTrials()
    {
        return upcomingTrials;
    }

    public void setUpcomingTrials(Stack<GameTrialData> trials)
    {
        upcomingTrials  = trials;
    }

    public void clearResults()
    {
        this.completedTrialResults.Clear();
    }

    private void ConnectToClient()
    {
        try
        {
            client = new Client();
            Debug.Log("Logged in successfully.");
        }
        catch (Exception e)
        {
            Debug.Log(e.Message);
        }
    }
}
