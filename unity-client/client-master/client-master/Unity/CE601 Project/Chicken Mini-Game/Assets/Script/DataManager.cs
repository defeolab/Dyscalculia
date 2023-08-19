using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Debug = UnityEngine.Debug;
using Random = UnityEngine.Random;

public class DataManager : MonoBehaviour
{
    public GameObject[] areas; //list of the areas inside the level 
    public GameObject[] fences; //list of the fences' models inside the level 
    public GameObject[] chickens_generators; //list of the generators of chickens
    public GameObject[] cows_generators; //list of the generators of cows

    //public GameObject[] lion_generators; // list of the generators of lions


    public List<GameObject> activeAnimals; //list of all the animals generated in the trial
    private List<Vector3> createdPositionsArea1; //list of all the possible positions inside Area1
    private List<Vector3> createdPositionsArea2; //list of all the possible positions inside Area2
    private List<Vector3> allFinalPositions; //list of all the real positions of animals

    //data used in a specific trial
    private AreaTrialData[] areasData; 
    public TrialData data;
    public GeneratorFlowers flowers;

    //control variables
    private float allAnimalsArrived;
    private bool fences_open;
    public int cowORchick;

    void Start()
    {
        activeAnimals = new List<GameObject>();
        allFinalPositions  = new List<Vector3>();
        createdPositionsArea1 = new List<Vector3>();
        createdPositionsArea2 = new List<Vector3>();
        areasData = new AreaTrialData[2];
        allAnimalsArrived = 0f;
    }
    public void SetNewTrialData(TrialData trialData)
    {
        Random.InitState((int)System.DateTime.Now.Ticks);

        //Random prototype for scene on distraction with flowers
        if (SceneManager.GetActiveScene().name == "TwoFences_Flowers")
        {
            flowers.DistractionGenerator();
        }

        data = trialData;
        areasData[0] = trialData.area1Data;
        areasData[1] = trialData.area2Data;

        //calculation of new value of average_space_between
        for (int i = 0; i < areas.Length; i++)
        {
            float newASB = (float)Math.Round(areasData[i].getAverageSpaceBetween(), 2);
            areasData[i].setAverageSpaceBetween(newASB);
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

        //Initialize Animals
        cowORchick = Random.Range(0, 2);
        Debug.Log("cowORchick");
        Debug.Log(cowORchick);
        for (int i = 0; i < areasData.Length; i++)
        {
            if(cowORchick == 1 && (areasData[0].sizeOfChicken >= 5f && areasData[1].sizeOfChicken >= 5f))
            {                
                for (int j = 0; j < areasData[i].getNumberOfAnimals(); j++)
                {
                    GameObject newAnimal = Instantiate(cows_generators[i]);
                    newAnimal.GetComponent<Animals>().SetAnimal(areas[i], i + 1, areasData[i]);
                    activeAnimals.Add(newAnimal);
                }
            }
            else
        
            {
                if(cowORchick == 0)
                {
                    for (int j = 0; j < areasData[i].getNumberOfAnimals(); j++)
                    {
                        //GameObject newAnimal = Instantiate(cows_generators[i]);
                        //GameObject newAnimal = Instantiate(lion_generators[i]);
                        GameObject newAnimal = Instantiate(chickens_generators[i]);           // @AK COWS GENERATOR
                        newAnimal.GetComponent<Animals>().SetAnimal(areas[i], i + 1, areasData[i]);
                        activeAnimals.Add(newAnimal);
                    }
                }
                else
                {
                    for (int j = 0; j < areasData[i].getNumberOfAnimals(); j++)
                    {
                        GameObject newAnimal = Instantiate(cows_generators[i]);
                        //GameObject newAnimal = Instantiate(lion_generators[i]);
                        //GameObject newAnimal = Instantiate(chickens_generators[i]);           // @AK COWS GENERATOR
                        newAnimal.GetComponent<Animals>().SetAnimal(areas[i], i + 1, areasData[i]);
                        activeAnimals.Add(newAnimal);
                    }
                }
            }
            

        }

        TrialsManager.instance.area1Value = areasData[0].getNumberOfAnimals();
        TrialsManager.instance.area2Value = areasData[1].getNumberOfAnimals();
        TrialsManager.instance.trialStarted = true; //Start Trial
    }

    void FixedUpdate()
    {
        allAnimalsArrived = 0;

        if (TrialsManager.instance.trialStarted)
        {
            foreach (GameObject c in activeAnimals)
            {
                if (!c.GetComponent<Animals>().findFinalPos)
                {
                    this.FindFinalPosition(c);
                }
                else
                {
                    if (!c.GetComponent<Animals>().startWalk)
                    {
                        StartCoroutine(WaitOpenFence());

                        if (fences_open)
                        {
                            StartCoroutine(WaitStartWalk(c.GetComponent<Animals>()));
                        }
                    }
                    else if (c.GetComponent<Animals>().arrived)
                    {
                        allAnimalsArrived++;
                    }
                }
            }
        }

        if (allAnimalsArrived == activeAnimals.Count)
        {
            this.OpenFence(false); //start animation to close the fences
            TrialsManager.instance.animalsReady = true; //start the timer and enable the buttons (see script ButtonsManager)
        }
    }

    private void FindFinalPosition(GameObject animal)
    {
        try
        {
            List<Vector3> determinatedPos = new List<Vector3>();
            Animals an = animal.GetComponent<Animals>();

            if (an.area == areas[0]) determinatedPos = createdPositionsArea1;
            else determinatedPos = createdPositionsArea2;

            // First position in center of each area
            Vector3 firstpos = new Vector3(an.area.transform.position.x, an.area.transform.position.y, 0);
            if (!allFinalPositions.Contains(firstpos) && !an.findFinalPos)
            {
                an.positionFinal = firstpos;
                an.findFinalPos = true;
                allFinalPositions.Add(firstpos);
            }

            // Find another position random
            int d_p = Random.Range(0, determinatedPos.Count);
            if (!allFinalPositions.Contains(determinatedPos[d_p]) && !an.findFinalPos)
            {
                an.positionFinal = determinatedPos[d_p];
                an.findFinalPos = true;
                allFinalPositions.Add(determinatedPos[d_p]);
            }
        }
        catch (Exception e){Debug.Log(e);}  
    }

    IEnumerator WaitOpenFence()
    {
        yield return new WaitForSeconds(1f);
        fences_open = true;
    }

    IEnumerator WaitStartWalk(Animals animals)
    {
        if (!animals.startWalk)
        {
            yield return new WaitForSeconds(0.01f / animals.number);
            animals.startWalk = true;
        }
    }

    public void OpenFence(bool open)
    {
        foreach (GameObject f in fences) f.GetComponent<Animator>().SetBool("open", open);
    }

    public void Reset()
    {
        OpenFence(false);

        foreach(GameObject c in activeAnimals)
        {
            Destroy(c);
        }

        activeAnimals.Clear();
        allFinalPositions.Clear();
        allAnimalsArrived = 0f;
        createdPositionsArea1.Clear();
        createdPositionsArea2.Clear();
        fences_open = false; 
        foreach(GameObject a in areas) a.transform.localScale = new Vector3(1, 1, 1);
    }

    private void CreateGrid(GameObject area, AreaTrialData areaData)
    {
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
            //calculation points around the center
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
        float newASB = (float) Math.Round(areaData.getAverageSpaceBetween(), 2);
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
                if (vectors_final.Count >= areaData.getNumberOfAnimals())
                {
                    newASB += num * areaData.getAverageSpaceBetween();
                }
                else if (vectors_final.Count < areaData.getNumberOfAnimals())
                {
                    newASB -= (num/0.5f) * areaData.getAverageSpaceBetween();
                }
            }
            else if (vectors_final.Count < areaData.getNumberOfAnimals())
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
        return areas[0].name + ": " + areasData[0].getCircleRadius() + " " + areasData[0].getSizeOfAnimal() + " " + +areasData[0].getAverageSpaceBetween() + " " + createdPositionsArea1.Count + " - " +
               areas[1].name + ": " + areasData[1].getCircleRadius() + " " + areasData[1].getSizeOfAnimal() + " " + +areasData[1].getAverageSpaceBetween() + " " + createdPositionsArea2.Count;
    }
}