using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using Newtonsoft.Json;
using System.IO;
using System.Collections.Generic;
using System.Diagnostics;

/*
 @Author: Fletcher Hurn (1806938)
 */
public class ButtonManager : MonoBehaviour
{
    public Button area1Button;
    public Button area2Button;
    public Button startButton;

    public Button importButton;
    public Button exportButton;
    public Button settingsButton;

    public Text gameText;

    private bool buttonsEnabled;

    private Stopwatch stopwatch;

    // Start is called before the first frame update
    void Start()
    {
        this.hideButtons();
        buttonsEnabled = false;
        stopwatch = new Stopwatch();
        if (GameManager.instance.gameStarted)
        {
            startButton.gameObject.SetActive(false);
        } else
        {
            area1Button.gameObject.SetActive(false);
            area2Button.gameObject.SetActive(false);
        }
        if (GameManager.instance.demoMode)
        {
            importButton.gameObject.SetActive(false);
            exportButton.gameObject.SetActive(false);
            //settingsButton.gameObject.SetActive(false);
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (!buttonsEnabled && GameManager.instance.chickensReady)
        {
            area1Button.interactable = true;
            area2Button.interactable = true;
            buttonsEnabled = true;
            stopwatch.Start();
        }
        if (stopwatch.IsRunning && stopwatch.ElapsedMilliseconds > (GameManager.instance.maxTrialTime * 1000))
        {
            stopwatch.Stop();
            double elapsedTime = stopwatch.Elapsed.TotalMilliseconds;
            GameManager.instance.AddTrialResult(elapsedTime, false);
            this.handleLoss();
            this.hideButtons();
            StartCoroutine(handleReload());
        }
    }

    public void StartGame()
    {
        GameManager.instance.StartGame();
        area1Button.gameObject.SetActive(true);
        area2Button.gameObject.SetActive(true);
        startButton.gameObject.SetActive(false);
    }

    public void Exit()
    {
        Application.Quit();
        UnityEngine.Debug.Break();
    }

    public void Area1Selected()
    {
        ButtonSelected(GameManager.instance.area1Chickens, GameManager.instance.area2Chickens);
    }

    public void Area2Selected()
    {
        ButtonSelected(GameManager.instance.area2Chickens, GameManager.instance.area1Chickens);
        
    }

    private void ButtonSelected(int selectedChickens, int unselectedChickens)
    {
        stopwatch.Stop();
        UnityEngine.Debug.Log("Time elapsed: " + stopwatch.Elapsed);
        bool correct = selectedChickens > unselectedChickens;
        double elapsedTime = stopwatch.Elapsed.TotalMilliseconds;
        GameManager.instance.AddTrialResult(elapsedTime, correct);
        if (correct)
        {
            handleWin();
        }
        else
        {
            handleLoss();
        }
        this.hideButtons();
        StartCoroutine(handleReload());
    }

    private void handleLoss()
    {
        gameText.text = "Incorrect Answer!";
        GameManager.instance.incorrectCount += 1;
    }

    private void handleWin()
    {
        gameText.text = "Correct Answer!";
        GameManager.instance.correctCount += 1;
    }

    private void hideButtons()
    {
        area1Button.interactable = false;
        area2Button.interactable = false;
    }

    public void ExportSelected()
    {
        string fileName = "trails.json";
        string jsonString = JsonConvert.SerializeObject(GameManager.instance.getUpcomingTrials());
        File.WriteAllText(fileName, jsonString);
    }

    public void ImportSelected()
    {
        string fileName = "trails.json";
        string jsonString = File.ReadAllText(fileName);
        Stack<GameTrialData> trials = JsonConvert.DeserializeObject<Stack<GameTrialData>>(jsonString);
        GameManager.instance.setUpcomingTrials(trials);
    }

    IEnumerator handleReload()
    {
        yield return new WaitForSeconds(2);
        SceneManager.LoadScene("SimpleChickenGame");
        GameManager.instance.Reset();
    }
}
