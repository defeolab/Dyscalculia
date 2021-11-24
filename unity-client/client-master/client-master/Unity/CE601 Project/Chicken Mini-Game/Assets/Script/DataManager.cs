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
    private List<Vector3> createdPositionsArea1;
    private List<Vector3> createdPositionsArea2;
    //private List<Vector3> allFinalPositions;

    private AreaTrialData area1Data;
    private AreaTrialData area2Data;
    public TrialData data;

    //private Stopwatch stopwatch;

    private float minScale = 0.8f;
    private float maxScale = 1.2f;
    private float totArea;
    private float allChickenArrived = 0f;

    private Animator animFence1;
    private Animator animFence2;

    void Start()
    {
        animFence1 = fence1.GetComponent<Animator>();
        animFence2 = fence2.GetComponent<Animator>();
        activeChickens = new List<GameObject>();
        createdPositions1 = new List<Vector3>();
        createdPositions2 = new List<Vector3>();
        createdPositionsArea1 = new List<Vector3>();
        createdPositionsArea2 = new List<Vector3>();
        //allFinalPositions = new List<Vector3>();
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

        //Find Point Inside Areas
        this.CreateGrid(area1,area1Data);
        this.CreateGrid(area2,area2Data);

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

        Debug.Log("CREATE GRID: 1 GRID PITAGORAS: " + createdPositionsArea1.Count);
        Debug.Log("CREATE GRID: 2 GRID PITAGORAS: " + createdPositionsArea2.Count);
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

        //Debug.Log(allFinalPositions.Count + " " + activeChickens.Count);

        if ((createdPositions1.Count + createdPositions2.Count) == activeChickens.Count)
        {
            allChickenArrived = 0;

            foreach (GameObject c in activeChickens)
            {
                if (c.GetComponent<Chickens>().arrived)
                {
                    allChickenArrived++;
                }
            }
        }

        if (allChickenArrived == activeChickens.Count)
        {
            this.OpenFence(false);
            TrialsManager.instance.chickensReady = true;
        }

        /*if (createdPositions1.Count + createdPositions2.Count == activeChickens.Count)
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
        }*/
    }


   private void FindFinalPosition(GameObject chicken)
    {/*
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

            //Debug.Log("POLLO N°" + c.number + " " + c.area.name + " pos: " + c.transform.position);

            if (c.area == area1) createdPositions1.Add(position);
            else createdPositions2.Add(position);
        }*/




        List<Vector3> createdPos = new List<Vector3>();
        List<Vector3> determinatedPos = new List<Vector3>();
        Chickens c = chicken.GetComponent<Chickens>();
        int i = 0;
        

        if (c.area == area1)
        {
            determinatedPos = createdPositionsArea1;
            createdPos = createdPositions1;
        }
        else 
        { 
            determinatedPos = createdPositionsArea2;
            createdPos = createdPositions2;
        }

        int d_p = Random.Range(0, determinatedPos.Count);
        Vector3 position = determinatedPos[d_p];

        if (createdPos.Count == 0)
        {
            i = 0;
        }
        else
        {
            foreach (Vector3 p in createdPos)
            {
                if (Vector2.Distance(position, p) >= c.areaData.getAverageSpaceBetween())
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
            c.findFinalPos = true;
            
            if (c.area == area1)
            {
                createdPositions1.Add(position);
                createdPositionsArea1.RemoveAt(d_p);
            }
            else
            {
                createdPositions2.Add(position);
                createdPositionsArea2.RemoveAt(d_p);
            }
        }

       /* if (c.area == area1) createdPos = createdPositionsArea1;
        else createdPos = createdPositionsArea2;

        int pos = Random.Range(0, createdPos.Count);*/
        
        /*if (allFinalPositions.Count == 0)
        {
            allFinalPositions.Add(createdPos[pos]);
        }
        else
        {
            if (!(allFinalPositions.Contains(createdPos[pos]))){
                allFinalPositions.Add(createdPos[pos]);
                c.positionFinal = createdPos[pos];
                c.findFinalPos = true;
            }
        }*/
        /*if (!(allFinalPositions.Contains(createdPos[pos])))
        {
            allFinalPositions.Add(createdPos[pos]);
            c.positionFinal = createdPos[pos];
            c.findFinalPos = true;
        }*/


    }

    /*private float RoundFloat(float number)
    {
        return (float)Math.Round(number, 2);
    }*/

    IEnumerator WaitStartWalk(Chickens chickens)
    {
        yield return new WaitForSeconds(2f/chickens.number);
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
        allChickenArrived = 0f;
        createdPositionsArea1.Clear();
        createdPositionsArea2.Clear();
        //allFinalPositions.Clear();
    }

    private void CreateGrid(GameObject area, AreaTrialData areaData)
    {
        float radius_chicken = (areaData.getSizeOfChicken() * 0.28f) / 2;
        float radius_area = area.transform.lossyScale.x * 3f;
        int div = (int)((2 * radius_area) / radius_chicken);
        Vector3 centre_area = area.transform.position;
        List<Vector3> vectors = new List<Vector3>();

        Debug.Log("CREATE GRID: RADIUS-CENTER-K: " + radius_chicken + radius_area + centre_area + div);

        if (vectors.Count == 0)
        {
            vectors.Add(new Vector3((centre_area.x - radius_area), (centre_area.y + radius_area), 0));
        }

        for (int i = 1; i <= div; i++)
        {

            for (int j = 1; j < div; j++)
            {
                Vector3 v_j = new Vector3((vectors[vectors.Count - 1].x + radius_chicken), vectors[vectors.Count - 1].y, 0);
                vectors.Add(v_j);
            }

            if (i <= div-1)
            {
                Vector3 v_i = new Vector3(vectors[0].x, vectors[0].y - (i * radius_chicken), 0);
                vectors.Add(v_i);
            }
        }

        Debug.Log("CREATE GRID: " + vectors.Count);

       foreach (Vector3 v in vectors)
         {
            float d_x = (v.x - centre_area.x) * (v.x - centre_area.x);
            float d_y = (v.y - centre_area.y) * (v.y - centre_area.y);

            if (Math.Sqrt(d_x + d_y) <= radius_area)
             {
                 if (area == area1) createdPositionsArea1.Add(v);
                 else createdPositionsArea2.Add(v);
             }
         }

        Debug.Log("COUNT VECTORS: " + createdPositionsArea1.Count + " - " + createdPositionsArea2.Count);

       /* float a = (vectors[0].x - centre_area.x)*(vectors[0].x - centre_area.x);
        float b = (vectors[0].y - centre_area.y)*(vectors[0].y - centre_area.y);

        Debug.Log(vectors[0].x + " " + vectors[0].y + " " + a + " "+ b + " " + Math.Sqrt(a + b) + " " + radius_area);*/

        /*float radius = area.transform.lossyScale.x * 2f;
        Vector3 centre = area.transform.position;
        int k = (int)((2 * radius) / areaData.getAverageSpaceBetween());
        List<Vector3> vectors = new List<Vector3>();

        Debug.Log("CREATE GRID: RADIUS-CENTER-K: " + radius + centre + k);

        if (vectors.Count == 0)
        {
            vectors.Add(new Vector3((centre.x - radius), (centre.y + radius), 0));
        }


        for (int i = 1; i <= (k+1); i++){
            
            for (int j = 0; j < k; j++)
            {
                Vector3 v_j = new Vector3((vectors[vectors.Count-1].x + areaData.getAverageSpaceBetween()), vectors[vectors.Count - 1].y, 0);
                vectors.Add(v_j);
            }

            if (i <= k)
            {
                Vector3 v_i = new Vector3(vectors[0].x, vectors[0].y - (i * areaData.getAverageSpaceBetween()), 0);
                vectors.Add(v_i);
            }
        }
      
        Debug.Log("CREATE GRID: " + vectors.Count);

        if (area == area1) createdPositionsArea1=vectors;
        else createdPositionsArea2 = vectors;

        //chicken.transform.position = vectors[30];

        /* foreach (Vector3 v in vectors)
         {
             float d_x = Math.Abs(v.x - centre.x);
             float d_y = Math.Abs(v.y - centre.y);

             if (Math.Sqrt(d_x + d_y) < radius)
             {
                 if (area == area1) createdPositionsArea1.Add(v);
                 else createdPositionsArea2.Add(v);
             }
         }*/
    }
}
