using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class ErrorTrialManager : MonoBehaviour
{
    private List<Vector3> positionsArea1;
    private List<Vector3> positionsArea2;
    private List<GameObject> pointsOfHays1;
    private List<GameObject> pointsOfHays2;
    public List<GameObject> activeHays;

    public Vector3 hay_area1_pos, hay_area2_pos;
    public GameObject fences;
    public GameObject hay;

    private bool startError;

    // Start is called before the first frame update
    void Start()
    {
        positionsArea1 = new List<Vector3>();
        positionsArea2 = new List<Vector3>();
        pointsOfHays1 = new List<GameObject>();
        pointsOfHays2 = new List<GameObject>();
        activeHays = new List<GameObject>();

        fences.SetActive(false);


    }

    private void Update()
    {
        if (startError)
        {
            int check = 0;
            foreach (GameObject c in gameObject.GetComponent<DataManager>().activeChickens)
            {
                foreach(GameObject a in activeHays)
                {
                    if (c.transform.position == a.transform.position)
                    {
                        check++;
                    }
                }    
            }
            
            
            if (check == gameObject.GetComponent<DataManager>().activeChickens.Count)
            {
                gameObject.GetComponent<ButtonsManager>().endErrorTrial();
            }
        }
    }

    public void ActiveHays(int area)
    {
        if (area == 1)
        {
            pointsOfHays1[0].SetActive(true);
            hay_area1_pos = pointsOfHays1[0].transform.position;
            activeHays.Add(pointsOfHays1[0]);
            pointsOfHays1.Remove(pointsOfHays1[0]);
        }
        else if (area == 2)
        {
            pointsOfHays2[0].SetActive(true);
            hay_area2_pos = pointsOfHays2[0].transform.position;
            activeHays.Add(pointsOfHays2[0]);
            pointsOfHays2.Remove(pointsOfHays2[0]);
        }
    }
    public void CollectData(TrialData data, GameObject[] areas, List<GameObject> activeChickens)
    {
        fences.SetActive(true);

        this.SetPositionsHays(data);

        foreach (GameObject c in activeChickens)
        {
            if (c.GetComponent<Chickens>().area.name == "Area1")
            {
                gameObject.GetComponent<DragManager>().draggableChickens1.Add(c);
                c.GetComponent<Chickens>().setChickenError();
            }
            else if(c.GetComponent<Chickens>().area.name == "Area2")
            {
                gameObject.GetComponent<DragManager>().draggableChickens2.Add(c);
                c.GetComponent<Chickens>().setChickenError();
            }
        }

        gameObject.GetComponent<DragManager>().active = true;
        startError = true;
    }

    public void Reset()
    {
        foreach (GameObject p1 in pointsOfHays1) Destroy(p1);
        foreach (GameObject p2 in pointsOfHays1) Destroy(p2);
        foreach (GameObject p in activeHays) Destroy(p);

        positionsArea1.Clear();
        positionsArea2.Clear();
        pointsOfHays1.Clear();
        pointsOfHays2.Clear();
        activeHays.Clear();
        fences.SetActive(false);
        startError = false;
    }

    private void SetPositionsHays(TrialData data)
    {
        float d = 8.8f;
        float avg = 0.0f;
        int div_y = 0;
        int div_x = 0;

        float avg_1 = (data.area1Data.sizeOfChicken * 0.007f * 26f);
        int div_1 = (int)(d / avg_1);
        float avg_2 = (data.area2Data.sizeOfChicken * 0.007f * 26f);
        int div_2 = (int)(d / avg_2);

        if (div_1 <= div_2)
        {
            avg = avg_1;
            div_y = div_1;
        }
        else
        {
            avg = avg_2;
            div_y = div_2;
        }

        Debug.Log(div_y);

        float numberOfChichens1 = data.area1Data.numberOfChickens + 0.0f;
        float numberOfChichens2 = data.area2Data.numberOfChickens + 0.0f;
        float num_1 = (float)(numberOfChichens1 / (div_y+1)) + 0.45f;
        float num_2 = (float)(numberOfChichens2 / (div_y+1)) + 0.45f;

        div_1 = Mathf.RoundToInt(num_1);
        div_2 = Mathf.RoundToInt(num_2);

        Debug.Log(div_1 + "  " + div_2);

        if (div_1 >= div_2)
        {
            div_x = div_1;
        }
        else
        {
            div_x = div_2;
        }

        if (positionsArea1.Count == 0)
        {
            positionsArea1.Add(new Vector3(-1.2f, -4.1f, 0f));
        }

        if (positionsArea2.Count == 0)
        {
            positionsArea2.Add(new Vector3(1.2f, -4.1f, 0f));
        }

        for (int i = 1; i <= div_y + 1; i++)
        {
            for (int j = 1; j < div_x; j++)
            {
                Vector3 v_j_1 = new Vector3((positionsArea1[positionsArea1.Count - 1].x - avg), positionsArea1[positionsArea1.Count - 1].y, 0);
                positionsArea1.Add(v_j_1);

                Vector3 v_j_2 = new Vector3((positionsArea2[positionsArea2.Count - 1].x + avg), positionsArea2[positionsArea2.Count - 1].y, 0);
                positionsArea2.Add(v_j_2);
            }

            if (i != div_y + 1)
            {
                Vector3 v_i_1 = new Vector3(positionsArea1[0].x, positionsArea1[0].y + (i * avg), 0);
                positionsArea1.Add(v_i_1);

                Vector3 v_i_2 = new Vector3(positionsArea2[0].x, positionsArea2[0].y + (i * avg), 0);
                positionsArea2.Add(v_i_2);
            }
        }

        foreach(Vector3 v in positionsArea1.OrderBy(p => p.y).ThenByDescending(p => p.x))
        {
            if(pointsOfHays1.Count < numberOfChichens1)
            {
                GameObject newHay = Instantiate(hay);
                newHay.transform.localScale = new Vector3(data.area1Data.sizeOfChicken * 0.007f, data.area1Data.sizeOfChicken * 0.007f, 0);
                newHay.transform.position = v;
                newHay.SetActive(false);
                pointsOfHays1.Add(newHay);
            }
        }

        foreach (Vector3 v in positionsArea2.OrderBy(p => p.y).ThenBy(p => p.x))
        {
            if (pointsOfHays2.Count < numberOfChichens2)
            {
                GameObject newHay = Instantiate(hay);
                newHay.transform.localScale = new Vector3(data.area2Data.sizeOfChicken * 0.007f, data.area2Data.sizeOfChicken * 0.007f, 0);
                newHay.transform.position = v;
                newHay.SetActive(false);
                pointsOfHays2.Add(newHay);
            }
        }
    }
}
