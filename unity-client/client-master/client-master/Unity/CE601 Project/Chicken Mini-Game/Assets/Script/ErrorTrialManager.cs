using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

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

    private bool startError, isCoroutine;

    private int div;
    private float avg, sizeAnimals1, sizeAnimals2;

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
            foreach (GameObject c in gameObject.GetComponent<DataManager>().activeAnimals)
            {
                foreach (GameObject a in activeHays)
                {
                    if (c.transform.position == a.transform.position)
                    {
                        check++;
                    }
                }
            }


            if (check == gameObject.GetComponent<DataManager>().activeAnimals.Count && !isCoroutine)
            {
                //skipButton.SetActive(false);
                StartCoroutine(WaitAndThenDo());
                isCoroutine = true;
            }

            if (Input.GetKeyDown("space")) this.SpeedUpErrorTrial();
        }
    }

    public void SpeedUpErrorTrial()
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
        yield return new WaitForSeconds(2f);
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
    public void CollectData(TrialData data, List<GameObject> activeChickens)
    {
        fences.SetActive(true);

        if(data.area1Data.getNumberOfAnimals() < 10 && data.area2Data.getNumberOfAnimals() < 10)
        {
            ControllSize(data, data.area1Data.getNumberOfAnimals(), data.area2Data.getNumberOfAnimals());
        }
        else
        {
            ControllSize(data, 10, 10);
        }

        this.SetPositionsHays(data);

        foreach (GameObject c in activeChickens)
        {
            if (c.GetComponent<Animals>().area.name == "Area1")
            {
                gameObject.GetComponent<DragManager>().draggableAnimals1.Add(c);
                c.GetComponent<Animals>().setAnimalError();
            }
            else if (c.GetComponent<Animals>().area.name == "Area2")
            {
                gameObject.GetComponent<DragManager>().draggableAnimals2.Add(c);
                c.GetComponent<Animals>().setAnimalError();
            }
        }

        gameObject.GetComponent<DragManager>().active = true;
        startError = true;
    }

    private void ControllSize(TrialData data, int num1, int num2)
    {
        float d = 8.8f;
        float avg_1 = (data.area1Data.getSizeOfAnimal() * 0.007f * 24f);
        int div_1 = (int)((d / avg_1) + 1);
        float avg_2 = (data.area2Data.getSizeOfAnimal() * 0.007f * 24f);
        int div_2 = (int)((d / avg_2) + 1);

        sizeAnimals1 = data.area1Data.getSizeOfAnimal();
        sizeAnimals2 = data.area2Data.getSizeOfAnimal();

        if (div_1 < num1)
        {
            div_1 = num1;
            avg_1 = d / (div_1 + 1);
        }
        else if(div_2 < num2)
        {
            div_2 = num2;
            avg_2 = d / (div_2 + 1);
        }

        if(div_1 >= div_2)
        {
            if (Mathf.Abs (avg_1-avg_2) > 0.1f) 
            {
                SetNewSize(div_1, avg_1, 2);
            }
            else
            {
                SetNewSize(div_1, avg_1, 0);
            }
        }
        else
        {
            if (Mathf.Abs(avg_1 - avg_2) > 0.1f)
            {
                SetNewSize(div_2, avg_2, 1);
            }
            else
            {
                SetNewSize(div_2, avg_2, 0);
            }
        }
    }

    private void SetNewSize(int d, float a, int num_area)
    {
        div = d;
        avg = a;

        float newsize = (8.8f / 0.168f) / (d - 1);

        if (num_area == 1)
        {
            sizeAnimals1 = newsize;
        }
        else if (num_area == 2)
        {
            sizeAnimals2 = newsize;
        }
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
        if (positionsArea1.Count == 0)
        {
            positionsArea1.Add(new Vector3(-1.2f, -4.1f, 0f));
        }

        if (positionsArea2.Count == 0)
        {
            positionsArea2.Add(new Vector3(1.2f, -4.1f, 0f));
        }

        for (int i = 1; i < div; i++)
        {
            Vector3 v_i_1 = new Vector3(positionsArea1[0].x, positionsArea1[0].y + (i * avg), 0);
            positionsArea1.Add(v_i_1);

            Vector3 v_i_2 = new Vector3(positionsArea2[0].x, positionsArea2[0].y + (i * avg), 0);
            positionsArea2.Add(v_i_2);
        }

        int var_1 = 0;
        int var_2 = 0;

        if (data.area1Data.getNumberOfAnimals() >= 10) var_1 = (int)(data.area1Data.getNumberOfAnimals() / 10);
        int numAnimals_1 = data.area1Data.getNumberOfAnimals() - 10 * var_1;
        if (data.area2Data.getNumberOfAnimals() >= 10) var_1 = (int)(data.area2Data.getNumberOfAnimals() / 10);
        int numAnimals_2 = data.area2Data.getNumberOfAnimals() - 10 * var_1;

        foreach (Vector3 v in positionsArea1.OrderByDescending(p => p.x).ThenBy(p => p.y))
        {
            if (pointsOfHays1.Count < data.area1Data.getNumberOfAnimals())
            {
                GameObject newHay = Instantiate(hay);
                newHay.transform.localScale = new Vector3(sizeAnimals1 * 0.007f, sizeAnimals1 * 0.007f, 0);
                newHay.transform.position = v;
                newHay.SetActive(true);
                pointsOfHays1.Add(newHay);
            }
        }

        foreach (Vector3 v in positionsArea2.OrderBy(p => p.x).ThenBy(p => p.y))
        {
            if (pointsOfHays2.Count < data.area2Data.getNumberOfAnimals())
            {
                GameObject newHay = Instantiate(hay);
                newHay.transform.localScale = new Vector3(sizeAnimals2 * 0.007f, sizeAnimals2 * 0.007f, 0);
                newHay.transform.position = v;
                newHay.SetActive(true);
                pointsOfHays2.Add(newHay);
            }
        }
    }
}

/*public class ErrorTrialManager : MonoBehaviour
{
    private List<Vector3> positionsArea1, positionsArea2;
    public List<GameObject> pointsOfHays1, pointsOfHays2, activeHays, refSlidersAnimals;
    public Vector3 hay_area1_pos, hay_area2_pos;
    
    public GameObject fences, hay, skipButton, canvasSliders;
    public Slider sliderArea1, sliderArea2;
    public bool setHays_noSliders;
    private bool startError, isCoroutine;
    private int sliderMaxValue = 370, sliderMinValue = 0;
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
        if (startError)
        {
            if (setHays_noSliders)
            {
                int check = 0;
                foreach (GameObject c in gameObject.GetComponent<DataManager>().activeAnimals)
                {
                    foreach (GameObject a in activeHays)
                    {
                        if (c.transform.position == a.transform.position) check++;
                    }
                }

                if (activeHays.Count > 5) skipButton.SetActive(true);

                if (check == gameObject.GetComponent<DataManager>().activeAnimals.Count && !isCoroutine)
                {
                    skipButton.SetActive(false);
                    StartCoroutine(WaitAndThenDo());
                    isCoroutine = true;
                }
            }
            else
            {
                if (count > 5 && !isCoroutine) skipButton.SetActive(true);

                if (count == gameObject.GetComponent<DataManager>().activeAnimals.Count && !isCoroutine)
                {
                    skipButton.SetActive(false);
                    StartCoroutine(WaitAndThenDo());
                    isCoroutine = true;
                }
            }

            if (Input.GetKeyDown("space")) this.SpeedUpErrorTrial();
        }
    }

    public void SpeedUpErrorTrial()
    {
        if (setHays_noSliders)
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
        else
        {
            TrialData data = gameObject.GetComponent<DataManager>().data;
            sliderArea1.value = sliderStep * data.getArea1Data().getNumberOfAnimals();
            sliderArea2.value = sliderStep * data.getArea2Data().getNumberOfAnimals();
            count = gameObject.GetComponent<DataManager>().activeAnimals.Count;

            foreach (GameObject c in gameObject.GetComponent<DataManager>().activeAnimals) c.SetActive(false);
        }
    }

    IEnumerator WaitAndThenDo()
    {
        yield return new WaitForSeconds(2f);
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

        this.SetPositionsHaysAndCheckThem(data);

        if (setHays_noSliders)
        {
            foreach (Vector3 v in positionsArea1.OrderBy(p => p.y))
            {
                if (pointsOfHays1.Count < data.area1Data.getNumberOfAnimals())
                {
                    GameObject newHay = Instantiate(hay);
                    newHay.transform.localScale = new Vector3(data.area1Data.getSizeOfAnimal() * 0.007f, data.area1Data.getSizeOfAnimal() * 0.007f, 0);
                    newHay.transform.position = v;
                    newHay.SetActive(false);
                    pointsOfHays1.Add(newHay);
                }
            }

            foreach (Vector3 v in positionsArea2.OrderBy(p => p.y))
            {
                if (pointsOfHays2.Count < data.area2Data.getNumberOfAnimals())
                {
                    GameObject newHay = Instantiate(hay);
                    newHay.transform.localScale = new Vector3(data.area2Data.getSizeOfAnimal() * 0.007f, data.area2Data.getSizeOfAnimal() * 0.007f, 0);
                    newHay.transform.position = v;
                    newHay.SetActive(false);
                    pointsOfHays2.Add(newHay);
                }
            }

            this.ActiveHays(1);
            this.ActiveHays(2);
        }
        else
        {
            canvasSliders.SetActive(true);

            if(data.getArea1Data().getNumberOfAnimals() > data.getArea2Data().getNumberOfAnimals())
            {
                sliderStep = (float) ((float)sliderMaxValue / (float)data.getArea1Data().getNumberOfAnimals());
            }
            else
            {
                sliderStep = (float) ((float)sliderMaxValue / (float)data.getArea2Data().getNumberOfAnimals());
            }

        }
        
        foreach (GameObject c in activeAnimals)
        {
            if (c.GetComponent<Animals>().area.name == "Area1")
            {
                gameObject.GetComponent<DragManager>().draggableAnimals1.Add(c);
                c.GetComponent<Animals>().setAnimalError();

                if (refSlidersAnimals.Count == 0 && setHays_noSliders==false)
                {
                    GameObject newAnimal = Instantiate(c);
                    newAnimal.transform.position = new Vector3(-1.21f, -4.25f, 0f);
                    newAnimal.transform.rotation = Quaternion.Euler(new Vector3(-90f, 270f, 90f));
                    newAnimal.GetComponent<Animator>().SetBool("walk", true);
                    newAnimal.GetComponent<Animals>().errorStarted = false;
                    refSlidersAnimals.Add(newAnimal);
                }

            }
            else if(c.GetComponent<Animals>().area.name == "Area2")
            {
                gameObject.GetComponent<DragManager>().draggableAnimals2.Add(c);
                c.GetComponent<Animals>().setAnimalError();

                if (refSlidersAnimals.Count == 1 && setHays_noSliders == false)
                {
                    GameObject newAnimal = Instantiate(c);
                    newAnimal.transform.position = new Vector3(1.21f, -4.25f, 0f);
                    newAnimal.transform.rotation = Quaternion.Euler(new Vector3(-90f, 270f, 90f));
                    newAnimal.GetComponent<Animator>().SetBool("walk", true);
                    newAnimal.GetComponent<Animals>().errorStarted = false;
                    refSlidersAnimals.Add(newAnimal);
                }
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
        foreach (GameObject a in refSlidersAnimals) Destroy(a);

        positionsArea1.Clear();
        positionsArea2.Clear();
        pointsOfHays1.Clear();
        pointsOfHays2.Clear();
        activeHays.Clear();

        count = 0;
        sliderStep = 0.00f;
        fences.SetActive(false);
        startError = false;
        skipButton.SetActive(false);
        isCoroutine = false;
        canvasSliders.SetActive(false);
        setHays_noSliders = false;
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

    private void SetPositionsHaysAndCheckThem(TrialData data)
    {
        float d = 8.8f;
        float avg = 0.0f;
        int div_y = 0;

        float avg_1 = (data.area1Data.getSizeOfAnimal() * 0.007f * 24f);
        int div_1 = (int)(d / avg_1);
        float avg_2 = (data.area2Data.getSizeOfAnimal() * 0.007f * 24f);
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
            if (i != div_y + 1)
            {
                Vector3 v_i_1 = new Vector3(positionsArea1[0].x, positionsArea1[0].y + (i * avg), 0);
                positionsArea1.Add(v_i_1);

                Vector3 v_i_2 = new Vector3(positionsArea2[0].x, positionsArea2[0].y + (i * avg), 0);
                positionsArea2.Add(v_i_2);
            }
        }

        if (positionsArea1.Count >= data.area1Data.getNumberOfAnimals())
        {
            if (positionsArea2.Count >= data.area2Data.getNumberOfAnimals())
            {
                setHays_noSliders=true;
            }
        }
    }
}*/
