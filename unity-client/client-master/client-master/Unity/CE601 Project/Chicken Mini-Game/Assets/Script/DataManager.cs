using System;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using Debug = UnityEngine.Debug;
using Random = UnityEngine.Random;
using System.Collections;
using UnityEngine.UI;

public class DataManager : MonoBehaviour
{
    public GameObject[] areas; //list of the areas inside the level 
    public GameObject[] fences; //list of the fences' models inside the level 
    public GameObject[] chickens_generators; //list of the generators of chickens

    public List<GameObject> activeChickens; //list of all the chickens generated in the trial
    private List<Vector3> createdPositionsArea1; //list of all the possible positions inside Area1
    private List<Vector3> createdPositionsArea2; //list of all the possible positions inside Area2
    private List<Vector3> allFinalPositions; //list of all the real positions of chicken

    //data used in the specific trial
    private AreaTrialData[] areasData; 
    public TrialData data; 
    
    private float allChickenArrived;
    private bool fences_open;

    void Start()
    {
        activeChickens = new List<GameObject>();
        allFinalPositions  = new List<Vector3>();
        createdPositionsArea1 = new List<Vector3>();
        createdPositionsArea2 = new List<Vector3>();
        areasData = new AreaTrialData[2];
        allChickenArrived = 0f;
    }
    public void SetNewTrialData(TrialData trialData)
    {
        Random.InitState((int)System.DateTime.Now.Ticks);
       
        chickens_generators[0].transform.position = new Vector3(-4, 7, 0);
        chickens_generators[1].transform.position = new Vector3(4, 7, 0);

        data = trialData;
        areasData[0] = trialData.area1Data;
        areasData[1] = trialData.area2Data;

        //calculation of new value of average_space_between
        for (int i = 0; i < areas.Length; i++)
        {
            this.CalculationAverageSpaceBetween(areas[i], areasData[i]);
        }

        //set right radius in areas
        areas[0].transform.localScale = new Vector3(areasData[0].getCircleRadius(), areasData[0].getCircleRadius(), areasData[0].getCircleRadius());
        areas[1].transform.localScale = new Vector3(areasData[1].getCircleRadius(), areasData[1].getCircleRadius(), areasData[1].getCircleRadius());

        //Find Points Inside Areas
         for (int i=0; i< areas.Length; i++)
         {
             this.CreateGrid(areas[i], areasData[i]);
         }

        //Start Animation to open the fences
        this.OpenFence(true);

        //Initialize Chickens
        for (int i = 0; i < areasData.Length; i++)
        {
            for (int j = 0; j < areasData[i].getNumberOfChickens(); j++)
            {
                GameObject newChicken = Instantiate(chickens_generators[i]);
                newChicken.GetComponent<Chickens>().SetChicken(areas[i], i + 1, areasData[i]);
                activeChickens.Add(newChicken);
            }
        }

        TrialsManager.instance.area1Value = areasData[0].getNumberOfChickens();
        TrialsManager.instance.area2Value = areasData[1].getNumberOfChickens();
        TrialsManager.instance.trialStarted = true; //Start Trial
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
                        StartCoroutine(WaitOpenFence());

                        if (fences_open)
                        {
                            StartCoroutine(WaitStartWalk(c.GetComponent<Chickens>()));
                        }
                    }
                    else if (c.GetComponent<Chickens>().arrived)
                    {
                        allChickenArrived++;
                    }
                }
            }
        }

        if (allChickenArrived == activeChickens.Count)
        {
            this.OpenFence(false); //start animation to close the fences
            TrialsManager.instance.chickensReady = true; //start the timer and enable the buttons (see script ButtonsManager)
        }
    }

    private void FindFinalPosition(GameObject chicken)
    {
        try
        {
            List<Vector3> determinatedPos = new List<Vector3>();
            Chickens c = chicken.GetComponent<Chickens>();

            if (c.area == areas[0]) determinatedPos = createdPositionsArea1;
            else determinatedPos = createdPositionsArea2;

            // First position in center of each area
            Vector3 firstpos = new Vector3(c.area.transform.position.x, c.area.transform.position.y, 0);
            if (!allFinalPositions.Contains(firstpos) && !c.findFinalPos)
            {
                c.positionFinal = firstpos;
                c.findFinalPos = true;
                allFinalPositions.Add(firstpos);
            }

            // Find other position random
            int d_p = Random.Range(0, determinatedPos.Count);
            if (!allFinalPositions.Contains(determinatedPos[d_p]) && !c.findFinalPos)
            {
                c.positionFinal = determinatedPos[d_p];
                c.findFinalPos = true;
                allFinalPositions.Add(determinatedPos[d_p]);
            }
        }
        catch (Exception e)  {
            Debug.Log(e);
        }  
    }

    IEnumerator WaitOpenFence()
    {
        yield return new WaitForSeconds(1f);
        fences_open = true;
    }

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
        foreach (GameObject f in fences) f.GetComponent<Animator>().SetBool("open", open);

    }

    public void Reset()
    {
        OpenFence(false);

        foreach(GameObject c in activeChickens)
        {
            Destroy(c);
        }

        activeChickens.Clear();
        allFinalPositions.Clear();
        allChickenArrived = 0f;
        createdPositionsArea1.Clear();
        createdPositionsArea2.Clear();
        fences_open = false;

        chickens_generators[0].transform.position = new Vector3(-4, 7, 0);
        chickens_generators[1].transform.position = new Vector3(4, 7, 0);

        foreach(GameObject a in areas) a.transform.localScale = new Vector3(1, 1, 1);
    }

    private void CreateGrid_old(GameObject area, AreaTrialData areaData)
    {
        

        float radius_area = areaData.getCircleRadius() * 3f; //3f because the radius of area usable is (you can see it also in unity) 0.5*6=3
        int div = (int)((2 * radius_area) / areaData.getAverageSpaceBetween()); //how much you can divide the diametre in same space with same distance between (=getAverageSpaceBetween)
        Vector3 centre_area = area.transform.position;
        List<Vector3> vectors = new List<Vector3>();

        if (vectors.Count == 0)
        {
            vectors.Add(new Vector3((centre_area.x - radius_area), (centre_area.y + radius_area), 0));
        }

        //Calculate all the point usable in the grid
        for (int i = 1; i <= div; i++) 
        {
            //calculate the horrizontal points
            for (int j = 1; j <= div; j++) 
            {
                Vector3 v_j = new Vector3((vectors[vectors.Count - 1].x + areaData.getAverageSpaceBetween()), vectors[vectors.Count - 1].y, 0);
                vectors.Add(v_j);
            }

           /* //calculate the vertical points
            if (i <= div-1) 
            {
                Vector3 v_i = new Vector3(vectors[0].x, vectors[0].y - (i * areaData.getAverageSpaceBetween()), 0);
                vectors.Add(v_i);
            }*/

            Vector3 v_i = new Vector3(vectors[0].x, vectors[0].y - (i * areaData.getAverageSpaceBetween()), 0);
            vectors.Add(v_i);
        }

        //Take only the points that are inside the circle
        foreach (Vector3 v in vectors)
        {
            float d_x = (v.x - centre_area.x) * (v.x - centre_area.x);
            float d_y = (v.y - centre_area.y) * (v.y - centre_area.y);

            if ((Math.Sqrt(d_x + d_y) <= radius_area)/*||(vectors.Count<=4)*/)
            {
                if (area == areas[0]) createdPositionsArea1.Add(v);
                else createdPositionsArea2.Add(v);
            }
        }
    }

    private void CreateGrid(GameObject area, AreaTrialData areaData)
    {
        //Debug.Log(areaData.getAverageSpaceBetween());
        float radius_area = areaData.getCircleRadius() * 3f; //3f because the radius of area usable is (you can see it also in unity) 0.5*6=3
        int div = (int)(radius_area / areaData.getAverageSpaceBetween()); //how much you can divide the radius in same space with same distance between (=getAverageSpaceBetween)
        Vector3 centre_area = area.transform.position;
        List<Vector3> vectors= new List<Vector3>();

        if (vectors.Count == 0)
        {
            vectors.Add(new Vector3(centre_area.x, centre_area.y, 0));
        }

        //calculation all the point usable in the grid
        for (int i = 0; i < div+1; i++)
        {
            //calculation of points around the center
            for (int j = 1; j <= div; j++)
            {
                float x_plus = vectors[0].x + (j * areaData.getAverageSpaceBetween());
                float x_minus = vectors[0].x - (j * areaData.getAverageSpaceBetween());
                float y_plus = vectors[0].y + (i * areaData.getAverageSpaceBetween());
                float y_minus = vectors[0].y - (i * areaData.getAverageSpaceBetween());

                vectors.Add(new Vector3(x_plus, y_plus, 0));
                vectors.Add(new Vector3(x_minus, y_plus, 0));
                vectors.Add(new Vector3(x_plus, y_minus, 0));
                vectors.Add(new Vector3(x_minus, y_minus, 0));
            }

            if (i != 0)
            {
                Vector3 v_i_plus = new Vector3(vectors[0].x, vectors[0].y + (i * areaData.getAverageSpaceBetween()), 0);
                vectors.Add(v_i_plus);

                Vector3 v_i_minus = new Vector3(vectors[0].x, vectors[0].y - (i * areaData.getAverageSpaceBetween()), 0);
                vectors.Add(v_i_minus);
            }
        }

        //Take only the points that are inside the circle
        foreach (Vector3 v in vectors)
        {
            float d_x = (v.x - centre_area.x) * (v.x - centre_area.x);
            float d_y = (v.y - centre_area.y) * (v.y - centre_area.y);

            if ((Math.Sqrt(d_x + d_y) <= radius_area))
            {
                if (area == areas[0])
                {
                    if (!createdPositionsArea1.Contains(v)) createdPositionsArea1.Add(v);
                }
                else
                {
                    if (!createdPositionsArea2.Contains(v)) createdPositionsArea2.Add(v);
                }
            }
        }
    }

    private void CalculationAverageSpaceBetween(GameObject area, AreaTrialData areaData)
    {
        float newASB = areaData.getAverageSpaceBetween();
        float num = 1f;

        for (int a = 1; a < 6; a++)
        {
            float radius_area = areaData.getCircleRadius() * 3f;
            int div = (int)(radius_area / newASB);
            Vector3 centre_area = area.transform.position;
            List<Vector3> vectors = new List<Vector3>();
            List<Vector3> vectors_final = new List<Vector3>();

            if (vectors.Count == 0) vectors.Add(new Vector3(centre_area.x, centre_area.y, 0));
            for (int i = 0; i < div + 1; i++)
            {
                for (int j = 1; j <= div; j++)
                {
                    float x_plus = vectors[0].x + (j * newASB);
                    float x_minus = vectors[0].x - (j * newASB);
                    float y_plus = vectors[0].y + (i * newASB);
                    float y_minus = vectors[0].y - (i * newASB);

                    vectors.Add(new Vector3(x_plus, y_plus, 0));
                    vectors.Add(new Vector3(x_minus, y_plus, 0));
                    vectors.Add(new Vector3(x_plus, y_minus, 0));
                    vectors.Add(new Vector3(x_minus, y_minus, 0));
                }

                if (i != 0)
                {
                    Vector3 v_i_plus = new Vector3(vectors[0].x, vectors[0].y + (i * newASB), 0);
                    vectors.Add(v_i_plus);

                    Vector3 v_i_minus = new Vector3(vectors[0].x, vectors[0].y - (i * newASB), 0);
                    vectors.Add(v_i_minus);
                }
            }

            foreach (Vector3 v in vectors)
            {
                float d_x = (v.x - centre_area.x) * (v.x - centre_area.x);
                float d_y = (v.y - centre_area.y) * (v.y - centre_area.y);

                if ((Math.Sqrt(d_x + d_y) <= radius_area))
                {
                    if (!vectors_final.Contains(v)) vectors_final.Add(v);
                }
            }

            num *= 0.5f;

            if (a != 5)
            {
                if (vectors_final.Count >= areaData.numberOfChickens)
                {
                    newASB += num * areaData.getAverageSpaceBetween();
                }
                else if (vectors_final.Count < areaData.numberOfChickens)
                {
                    newASB -= (num/0.5f) * areaData.getAverageSpaceBetween();
                }
            }
            else if (vectors_final.Count < areaData.numberOfChickens)
            {
                newASB -= (num / 0.5f) * areaData.getAverageSpaceBetween();
            }

            vectors_final.Clear();
            vectors.Clear();
        }

        areaData.setAverageSpaceBetween(newASB);

    }

    public string StampForControllData()
    {
        return areas[0].name + ": " + areasData[0].getCircleRadius() + " " + areasData[0].getSizeOfChicken() + " " + +areasData[0].getAverageSpaceBetween() + " " + createdPositionsArea1.Count + " - " +
               areas[1].name + ": " + areasData[1].getCircleRadius() + " " + areasData[1].getSizeOfChicken() + " " + +areasData[1].getAverageSpaceBetween() + " " + createdPositionsArea2.Count;
    }
}