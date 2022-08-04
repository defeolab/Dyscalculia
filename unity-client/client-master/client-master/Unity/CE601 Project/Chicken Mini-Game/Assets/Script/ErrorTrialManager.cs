using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class ErrorTrialManager : MonoBehaviour
{
    private List<Vector3> positionsArea1, positionsArea2;
    private List<GameObject> pointsOfHays1, pointsOfHays2, activeHays;
    public Vector3 hay_area1_pos, hay_area2_pos;
    
    public GameObject fences, hay, skipButton, canvasSliders;
    public Slider sliderArea1, sliderArea2;
    private bool startError, isCoroutine;
    private int sliderMaxValue = 210, sliderMinValue = 0;
    private float sliderStep = 0.00f;
    private int count = 0;

    // Start is called before the first frame update
    void Start()
    {
        positionsArea1 = new List<Vector3>();
        positionsArea2 = new List<Vector3>();
        pointsOfHays1 = new List<GameObject>();
        pointsOfHays2 = new List<GameObject>();
        activeHays = new List<GameObject>();

        fences.SetActive(false);
        skipButton.SetActive(false);
        isCoroutine = false;
        canvasSliders.SetActive(false);
    }

    private void Update()
    {
        /*if (startError)
        {
            int check = 0;
            foreach (GameObject c in gameObject.GetComponent<DataManager>().activeAnimals)
            {
                foreach(GameObject a in activeHays)
                {
                    if (c.transform.position == a.transform.position)
                    {
                        check++;
                    }
                }    
            }

            if(activeHays.Count > 5)
            {
                skipButton.SetActive(true);
            }

            if (Input.GetKeyDown("space"))
            {
                //this.SpeedUpErrorTrial(); 
            }


            if (check == gameObject.GetComponent<DataManager>().activeAnimals.Count && !isCoroutine)
            {
                StartCoroutine(WaitAndThenDo());
                isCoroutine = true;
            }
        }*/

        if (startError)
        {

            if (count > 5 && !isCoroutine)
            {
                skipButton.SetActive(true);
            }

            if (Input.GetKeyDown("space"))
            {
                this.SpeedUpErrorTrial(); 
            }


            if (count == gameObject.GetComponent<DataManager>().activeAnimals.Count && !isCoroutine)
            {
                skipButton.SetActive(false);
                StartCoroutine(WaitAndThenDo());
                isCoroutine = true;                
            }
        }
    }

    public void SpeedUpErrorTrial()
    {
        TrialData data = gameObject.GetComponent<DataManager>().data;
        sliderArea1.value = sliderStep * data.getArea1Data().getNumberOfAnimals();
        sliderArea2.value = sliderStep * data.getArea2Data().getNumberOfAnimals();
        count = gameObject.GetComponent<DataManager>().activeAnimals.Count;

        foreach (GameObject c in gameObject.GetComponent<DataManager>().activeAnimals) c.SetActive(false);
    }

    public void SpeedUpErrorTrialOld()
    {
        foreach (GameObject a in gameObject.GetComponent<DataManager>().activeAnimals)
        {
            if (a.GetComponent<Animals>().errorStarted)
            {
                if (a.GetComponent<Animals>().area.name == "Area1")
                {
                    a.transform.position = hay_area1_pos;
                    a.GetComponent<Animator>().SetBool("eat", false);
                    a.GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(180f, 270f, 90f));
                    a.GetComponent<Animals>().errorStarted = false;
                    if (pointsOfHays1.Count != 0) this.ActiveHays(1);
                }
                else if (a.GetComponent<Animals>().area.name == "Area2")
                {
                    a.transform.position = hay_area2_pos;
                    a.GetComponent<Animator>().SetBool("eat", false);
                    a.GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(0f, 270f, 90f));
                    a.GetComponent<Animals>().errorStarted = false;
                    if (pointsOfHays2.Count != 0) this.ActiveHays(2);
                }
            }
            
        }
    }

    IEnumerator WaitAndThenDo()
    {
        yield return new WaitForSeconds(5f);
        gameObject.GetComponent<ButtonsManager>().EndErrorTrial();
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

    public void CollectData(TrialData data, List<GameObject> activeAnimals)
    {
        fences.SetActive(true);
        sliderArea1.value = sliderMinValue;
        sliderArea2.value = sliderMinValue;

        canvasSliders.SetActive(true);

        //this.SetPositionsHays(data);
        
        foreach (GameObject c in activeAnimals)
        {
            if (c.GetComponent<Animals>().area.name == "Area1")
            {
                gameObject.GetComponent<DragManager>().draggableAnimals1.Add(c);
                c.GetComponent<Animals>().setAnimalError();
            }
            else if(c.GetComponent<Animals>().area.name == "Area2")
            {
                gameObject.GetComponent<DragManager>().draggableAnimals2.Add(c);
                c.GetComponent<Animals>().setAnimalError();
            }
        }

        if(data.getArea1Data().getNumberOfAnimals() > data.getArea2Data().getNumberOfAnimals())
        {
            sliderStep = (float) ((float)sliderMaxValue / (float)data.getArea1Data().getNumberOfAnimals());
        }
        else
        {
            sliderStep = (float) ((float)sliderMaxValue / (float)data.getArea2Data().getNumberOfAnimals());
        }

        gameObject.GetComponent<DragManager>().active = true;
        startError = true;

        Debug.Log(sliderStep);
    }

    public void Reset()
    {
        /*foreach (GameObject p1 in pointsOfHays1) Destroy(p1);
        foreach (GameObject p2 in pointsOfHays1) Destroy(p2);
        foreach (GameObject p in activeHays) Destroy(p);

        positionsArea1.Clear();
        positionsArea2.Clear();
        pointsOfHays1.Clear();
        pointsOfHays2.Clear();
        activeHays.Clear();
        */

        count = 0;
        sliderStep = 0.00f;
        fences.SetActive(false);
        startError = false;
        skipButton.SetActive(false);
        isCoroutine = false;
        canvasSliders.SetActive(false);
    }

    public void IncreaseSlider(Collider collider, int a)
    {
        float newSizeY = collider.GetComponent<BoxCollider>().size.y + sliderStep;
        
        if (a == 1)
        {
            sliderArea1.value += sliderStep;
        }
        else if (a == 2)
        {
            sliderArea2.value += sliderStep;
        }

        collider.GetComponent<BoxCollider>().size = new Vector3(collider.GetComponent<BoxCollider>().size.x, newSizeY, collider.GetComponent<BoxCollider>().size.z);
        count++;
    }

    private void SetPositionsHays(TrialData data)
    {
        float d = 8.8f;
        float avg = 0.0f;
        int div_y = 0;
        int div_x = 0;

        float avg_1 = (data.area1Data.getSizeOfAnimal() * 0.007f * 26f);
        int div_1 = (int)(d / avg_1);
        float avg_2 = (data.area2Data.getSizeOfAnimal() * 0.007f * 26f);
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

        float numberOfAnimals1 = data.area1Data.getNumberOfAnimals() + 0.0f;
        float numberOfAnimals2 = data.area2Data.getNumberOfAnimals() + 0.0f;
        float num_1 = (float)(numberOfAnimals1 / (div_y + 1)) + 0.45f;
        float num_2 = (float)(numberOfAnimals2 / (div_y + 1)) + 0.45f;

        div_1 = Mathf.RoundToInt(num_1);
        div_2 = Mathf.RoundToInt(num_2);

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

        foreach (Vector3 v in positionsArea1.OrderBy(p => p.y).ThenByDescending(p => p.x))
        {
            if (pointsOfHays1.Count < numberOfAnimals1)
            {
                GameObject newHay = Instantiate(hay);
                newHay.transform.localScale = new Vector3(data.area1Data.getSizeOfAnimal() * 0.007f, data.area1Data.getSizeOfAnimal() * 0.007f, 0);
                newHay.transform.position = v;
                newHay.SetActive(false);
                pointsOfHays1.Add(newHay);
            }
        }

        foreach (Vector3 v in positionsArea2.OrderBy(p => p.y).ThenBy(p => p.x))
        {
            if (pointsOfHays2.Count < numberOfAnimals2)
            {
                GameObject newHay = Instantiate(hay);
                newHay.transform.localScale = new Vector3(data.area2Data.getSizeOfAnimal() * 0.007f, data.area2Data.getSizeOfAnimal() * 0.007f, 0);
                newHay.transform.position = v;
                newHay.SetActive(false);
                pointsOfHays2.Add(newHay);
            }
        }
    }
}
