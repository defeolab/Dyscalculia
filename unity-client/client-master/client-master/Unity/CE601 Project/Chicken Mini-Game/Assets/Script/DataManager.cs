using System;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using Debug = UnityEngine.Debug;
using Random = UnityEngine.Random;
using System.Collections;

public class DataManager : MonoBehaviour
{
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

    private AreaTrialData area1Data;
    private AreaTrialData area2Data;
    public TrialData data;

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
    }
    public void SetNewTrialData(TrialData trialData)
    {
        Random.InitState((int)System.DateTime.Now.Ticks);

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
        TrialsManager.instance.trialStarted = true;
    }

    void FixedUpdate()
    {
        allChickenArrived = 0;

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
                    else if (c.GetComponent<Chickens>().arrived)
                    {
                        allChickenArrived++;
                    }
                }
            }
        }

        /*if ((createdPositions1.Count + createdPositions2.Count) == activeChickens.Count)
        {
            allChickenArrived = 0;

            foreach (GameObject c in activeChickens)
            {
                if (c.GetComponent<Chickens>().arrived)
                {
                    allChickenArrived++;
                }
            }
        }*/

        if (allChickenArrived == activeChickens.Count)
        {
            this.OpenFence(false);
            TrialsManager.instance.chickensReady = true;
        }

        /*if (TrialsManager.instance.trialStarted)
        {
            foreach (GameObject c in activeChickens)
            {
                if (!c.GetComponent<Chickens>().findFinalPos)
                {
                    this.FindFinalPosition(c);
                }
            }
        }

        if ((createdPositions1.Count + createdPositions2.Count) == activeChickens.Count)
        {
            allChickenArrived = 0;

            foreach (GameObject c in activeChickens)
            {
                if (c.GetComponent<Chickens>().findFinalPos)
                {
                    if (!c.GetComponent<Chickens>().startWalk)
                    {
                        StartCoroutine(WaitStartWalk(c.GetComponent<Chickens>()));
                    }
                    else if (c.GetComponent<Chickens>().arrived)
                    {
                        allChickenArrived++;
                    }

                }
            }
        }
        else
        {
            if (!controll)
            {
                controll = true;
                ControllPosition();
            }
        }

        if (allChickenArrived == activeChickens.Count)
        {
            this.OpenFence(false);
            TrialsManager.instance.chickensReady = true;
        }*/

    }

    private void FindFinalPosition(GameObject chicken)
    {
        List<Vector3> createdPos = new List<Vector3>();
        List<Vector3> determinatedPos = new List<Vector3>();
        //List<int> usedValues = new List<int>();
        Chickens c = chicken.GetComponent<Chickens>();
                
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
        //Vector3 position = determinatedPos[d_p];
        //int i = 0;

        //Debug.Log(c.area + " "+ d_p + "/" + determinatedPos.Count);

        /* if (createdPos.Count == 0)
         {
             i = 0;
         }
         else
         {
             foreach (Vector3 p in createdPos)
             {
                 if (Vector2.Distance(position, p) >= c.areaData.getAverageSpaceBetween()) i++;
                 else i--;
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
         }*/

        if (!createdPos.Contains(determinatedPos[d_p]))
        {
            c.positionFinal = determinatedPos[d_p];
            c.findFinalPos = true;

            if (c.area == area1)
            {
                createdPositions1.Add(determinatedPos[d_p]);
                createdPositionsArea1.RemoveAt(d_p);
            }
            else
            {
                createdPositions2.Add(determinatedPos[d_p]);
                createdPositionsArea2.RemoveAt(d_p);
            }
        }
    }

   /* IEnumerator ControllPosition()
    {
        yield return new WaitForSeconds(1);
        
        if (createdPositions1.Count != area1Data.getNumberOfChickens())
        {
            foreach (GameObject c in activeChickens)
            {
                if (c.GetComponent<Chickens>().areaData == area1Data)
                {
                    c.GetComponent<Chickens>().findFinalPos = false;
                    createdPositions1.Clear();
                    Debug.Log("RESTART POS 1");
                }
            }
        }else if (createdPositions2.Count != area2Data.getNumberOfChickens())
        {
            Debug.Log("ALL POS 1 FIND");

            foreach (GameObject c in activeChickens)
            {
                if (c.GetComponent<Chickens>().areaData == area2Data)
                {
                    c.GetComponent<Chickens>().findFinalPos = false;
                    createdPositions2.Clear();
                    Debug.Log("RESTART POS 2");
                }
            }
        }
        Debug.Log("ALL POS 1-2 FIND");
    }*/

    IEnumerator WaitStartWalk(Chickens chickens)
    {
        if (!chickens.startWalk)
        {
            yield return new WaitForSeconds(0.5f / chickens.number);
            chickens.startWalk = true;
        }
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
    }

    private void CreateGrid(GameObject area, AreaTrialData areaData)
    {
        //float radius_chicken = (areaData.getSizeOfChicken() * 0.28f) / 2;
        float radius_area = area.transform.lossyScale.x * 3f;
        int div = (int)((2 * radius_area) / areaData.getAverageSpaceBetween());
        Vector3 centre_area = area.transform.position;
        List<Vector3> vectors = new List<Vector3>();

        if (vectors.Count == 0)
        {
            vectors.Add(new Vector3((centre_area.x - radius_area), (centre_area.y + radius_area), 0));
        }

        for (int i = 1; i <= div; i++)
        {
            for (int j = 1; j < div; j++)
            {
                Vector3 v_j = new Vector3((vectors[vectors.Count - 1].x + areaData.getAverageSpaceBetween()), vectors[vectors.Count - 1].y, 0);
                vectors.Add(v_j);
            }

            if (i <= div-1)
            {
                Vector3 v_i = new Vector3(vectors[0].x, vectors[0].y - (i * areaData.getAverageSpaceBetween()), 0);
                vectors.Add(v_i);
            }
        }

        Debug.Log(area.name + vectors.Count);

        foreach (Vector3 v in vectors)
        {
            float d_x = (v.x - centre_area.x) * (v.x - centre_area.x);
            float d_y = (v.y - centre_area.y) * (v.y - centre_area.y);

            if ((Math.Sqrt(d_x + d_y) < radius_area)||(vectors.Count<=4))
            {
                if (area == area1) createdPositionsArea1.Add(v);
                else createdPositionsArea2.Add(v);
            }
        }

        Debug.Log(area.name + createdPositionsArea1.Count);
        Debug.Log(area.name + createdPositionsArea2.Count);
    }
}