using System;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using Debug = UnityEngine.Debug;
using Random = UnityEngine.Random;
using System.Collections;

public class DataManager : MonoBehaviour
{
    public DataManager instance;

    public GameObject area1;
    public GameObject area2;
    public GameObject fence1;
    public GameObject fence2;
    public GameObject chicken;

    public List<GameObject> activeChickens;
    private List<Vector3> createdPositions1;
    private List<Vector3> createdPositions2;

    private AreaTrialData area1Data;
    private AreaTrialData area2Data;
    public TrialData data;

    //private Stopwatch stopwatch;

    private float minScale = 0.8f;
    private float maxScale = 1.2f;
    private float totArea;
    private float AllChickenArrived = 0f;

    private Animator animFence1;
    private Animator animFence2;

    void Start()
    {
        animFence1 = fence1.GetComponent<Animator>();
        animFence2 = fence2.GetComponent<Animator>();
        activeChickens = new List<GameObject>();
        createdPositions1 = new List<Vector3>();
        createdPositions2 = new List<Vector3>();
    }
    public void SetNewTrialData(TrialData trialData)
    {

        data = trialData;
        area1Data = trialData.area1Data;
        area2Data = trialData.area2Data;

        //Set New Scale For Fences
        totArea = area1Data.getCircleRadius() + area2Data.getCircleRadius();
        float newScaleArea1 = (area1Data.getCircleRadius() * 2) / totArea;
        float newScaleArea2 = (area2Data.getCircleRadius() * 2) / totArea;

        if (newScaleArea1 > minScale && newScaleArea1 < maxScale)
        {
            area1.transform.localScale = new Vector3(newScaleArea1, newScaleArea1, newScaleArea1);
            area2.transform.localScale = new Vector3(newScaleArea2, newScaleArea2, newScaleArea2);
        }
        else
        {
            if (newScaleArea1 > maxScale)
            {
                area1.transform.localScale = new Vector3(maxScale, maxScale, maxScale);
                area2.transform.localScale = new Vector3(minScale, minScale, minScale);
            }
            else
            {
                area2.transform.localScale = new Vector3(maxScale, maxScale, maxScale);
                area1.transform.localScale = new Vector3(minScale, minScale, minScale);
            }

        }

        this.OpenFence(true);

        //Initialize Chickens

        for (int i = 0; i < area1Data.getNumberOfChickens(); i++)
        {
            GameObject newChicken = Instantiate(chicken);
            newChicken.GetComponent<Chickens>().SetChicken(area1, i + 1, area1Data);
            activeChickens.Add(newChicken);
        }

        for (int i = 0; i < area2Data.getNumberOfChickens(); i++)
        {
            GameObject newChicken = Instantiate(chicken);
            newChicken.GetComponent<Chickens>().SetChicken(area2, i + 1, area2Data);
            activeChickens.Add(newChicken);
        }

        TrialsManager.instance.area1Value = area1Data.getNumberOfChickens();
        TrialsManager.instance.area2Value = area2Data.getNumberOfChickens();

        instance = this;

        TrialsManager.instance.trialStarted = true;
    }


    void FixedUpdate()
    {
        if (TrialsManager.instance.trialStarted)
        {
            foreach (GameObject c in activeChickens)
            {
                if (!c.GetComponent<Chickens>().findFinalPos)
                {
                    this.FindFinalPosition(c);
                }
                else
                {
                    if (!c.GetComponent<Chickens>().startWalk)
                    {
                        StartCoroutine(WaitStartWalk(c.GetComponent<Chickens>()));
                    }

                }
            }
        }

        if (createdPositions1.Count + createdPositions2.Count == activeChickens.Count)
        {
            AllChickenArrived = 0;

            foreach (GameObject c in activeChickens)
            {
                if (c.GetComponent<Chickens>().arrived)
                {
                    AllChickenArrived++;
                }
            }
        }

        if (AllChickenArrived == activeChickens.Count)
        {
            this.OpenFence(false);
            TrialsManager.instance.chickensReady = true;
        }
    }


    private void FindFinalPosition(GameObject chicken)
    {
        Chickens c = chicken.GetComponent<Chickens>();
        Vector3 centre = c.area.transform.position;
        float radius = c.area.transform.lossyScale.x * 1.7f;

        List<Vector3> createdPos;
        int i = 0;

        float averageSpaceBetween = c.areaData.getAverageSpaceBetween();
        float minCircleX = centre.x - radius;
        float maxCircleX = centre.x + radius;
        float minCircleY = centre.y - radius;
        float maxCircleY = centre.y + radius;

        if (c.area == area1) createdPos = createdPositions1;
        else createdPos = createdPositions2;

        Vector3 position = new Vector3(RoundFloat(Random.Range(minCircleX, maxCircleX)), RoundFloat(Random.Range(minCircleY, maxCircleY)), 0);
        //Vector3 position = new Vector3((centre.x + Random.insideUnitCircle.x)*radius, (centre.y + Random.insideUnitCircle.y) * radius, 0);

        if (createdPos.Count == 0)
        {
            i = 0;
        }
        else
        {
            foreach (Vector3 p in createdPos)
            {
                if (Vector2.Distance(position, p) >= averageSpaceBetween)
                {
                    i++;
                }
                else
                {
                    i--;
                }
            }
        }

        if (i == createdPos.Count)
        {
            c.positionFinal = position;
            //c.transform.position = position;
            c.findFinalPos = true;

            Debug.Log("POLLO N°" + c.number + " " + c.area.name + " pos: " + c.transform.position);

            if (c.area == area1) createdPositions1.Add(position);
            else createdPositions2.Add(position);
        }
    }

    private float RoundFloat(float number)
    {
        return (float)Math.Round(number, 2);
    }

    IEnumerator WaitStartWalk(Chickens chickens)
    {
        yield return new WaitForSeconds(chickens.number * 0.02f);
        chickens.startWalk = true;
    }

    public void prova()
    {
        area1.transform.localScale = new Vector3(0.5f, 0.5f, 0.5f);
        area2.transform.localScale = new Vector3(0.5f, 0.5f, 0.5f);
    }

    public void OpenFence(bool open)
    {
        animFence1.SetBool("open", open);
        animFence2.SetBool("open", open);
    }

    public void Reset()
    {
        OpenFence(false);

        foreach(GameObject c in activeChickens)
        {
            Destroy(c);
        }


        activeChickens.Clear();
        createdPositions1.Clear();
        createdPositions2.Clear();
        AllChickenArrived = 0f;
    }

}
