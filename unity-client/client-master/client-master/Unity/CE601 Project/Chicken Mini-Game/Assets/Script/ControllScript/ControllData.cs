using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using Newtonsoft.Json;
using System.IO;
using System.Collections.Generic;
using System.Diagnostics;
using Debug = UnityEngine.Debug;

public class ControllData : MonoBehaviour
{
    public Stopwatch stopwatch1;
    public Stopwatch stopwatch2;

    public float value_timer1;
    public float value_timer2;

    private bool buttonsEnabled;
    private bool stopwatch1_start;
    private bool firstTrial;
    private DataManager istance_DataManager;

    void Start()
    {
        istance_DataManager = gameObject.GetComponent<DataManager>();

        stopwatch1 = new Stopwatch();
        stopwatch2 = new Stopwatch();

        buttonsEnabled = false;
        firstTrial = false;
    }

    void Update()
    {
        value_timer1 = stopwatch1.ElapsedMilliseconds/1000;
        value_timer2 = stopwatch2.ElapsedMilliseconds/1000;

        if (!TrialsManager.instance.trialStarted)
        {
            if (!firstTrial)
            {
                firstTrial = true;
                StartCoroutine(NewTrial());
            }
        }else if (TrialsManager.instance.trialStarted)
        {
            if (!stopwatch1_start)
            {
                stopwatch1.Start();
                stopwatch1_start = true;
            }
            
            if (stopwatch1.IsRunning && stopwatch1.ElapsedMilliseconds >= 10000)
            {
                stopwatch1.Stop();
                stopwatch2.Stop();

                double elapsedTime = stopwatch1.Elapsed.TotalMilliseconds;
                TrialsManager.instance.AddTrialResult(elapsedTime, false);
                this.HandleLoss();
                StartCoroutine(NewTrial());
                istance_DataManager.OpenFence(false);
            }

            else if (TrialsManager.instance.animalsReady)
            {
                if (!buttonsEnabled)
                {
                    //Start timer
                    stopwatch2.Start();

                    buttonsEnabled = true;
                }

                if (stopwatch2.IsRunning && stopwatch2.ElapsedMilliseconds >= (TrialsManager.instance.maxTrialTime * 1000))
                {
                    stopwatch1.Stop();
                    stopwatch2.Stop();
                    double elapsedTime = stopwatch2.Elapsed.TotalMilliseconds;
                    TrialsManager.instance.AddTrialResult(elapsedTime, true);
                    this.Reset();
                    this.HandleWin();
                    StartCoroutine(NewTrial());
                }
            }
        }
        
    }

    private void HandleWin()
    {
        TrialsManager.instance.correctCount += 1;
        Debug.Log(TrialsManager.instance.completedTrials.Count + ":  " + istance_DataManager.StampForControllData());
    }

    private void HandleLoss()
    {
        TrialsManager.instance.incorrectCount += 1;
        Debug.Log(TrialsManager.instance.completedTrials.Count + ":  " + istance_DataManager.StampForControllData());

        float c_1 = 0;
        float c_2 = 0;
        foreach(GameObject i in istance_DataManager.activeAnimals)
        {
            if (i.GetComponent<Animals>().area.name == "Area1")
            {
                if (i.GetComponent<Animals>().findFinalPos)
                {
                    c_1++;
                }
            }
            else
            {
                if (i.GetComponent<Animals>().findFinalPos)
                {
                    c_2++;
                }
            }
            
        }

        //Debug.Log("FENCE 1 Chickes find final pos " + c_1 + "/" + TrialsManager.instance.area1Value);
        //Debug.Log("FENCE 2 Chickes find final pos " + c_2 + "/" + TrialsManager.instance.area2Value);
    }

    IEnumerator NewTrial()
    {
        //Debug.Log("NEW TRIAL");
        yield return new WaitForSeconds(3);

        //Reset all the Managers
        TrialsManager.instance.Reset();
        istance_DataManager.Reset();
        this.Reset();

        TrialData nextTrial = TrialsManager.instance.GetNextTrial();

        if (nextTrial != null)
        {
            istance_DataManager.SetNewTrialData(nextTrial);
            //Debug.Log( "RUN:  " + istance_DataManager.Stamp());
        }
        else
        {
            Debug.Log("Finished"); //it's used for not block the gameplay
        }
    }

   

    public void Reset()
    {
        buttonsEnabled = false;
        stopwatch1_start = false;
        value_timer1 = 0;
        value_timer2 = 0;
        stopwatch1.Reset();
        stopwatch2.Reset();
    }


}
