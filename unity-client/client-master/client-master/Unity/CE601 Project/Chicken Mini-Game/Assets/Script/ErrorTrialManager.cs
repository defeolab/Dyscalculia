using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class ErrorTrialManager : MonoBehaviour
{
    public List<GameObject> pointsOfHays1, pointsOfHays2, tensAnimals1, tensAnimals2, activeHays, refSlidersAnimals, positionedAnimals1, positionedAnimals2;
    public List<GameObject> textUnitArea1, textUnitArea2, textTensArea1, textTensArea2;

    public Vector3 hay_area1_pos, hay_area2_pos;
    public Slider sliderArea1, sliderArea2;
    public GameObject fences, hay, canvasSliders, skipButton, lineOfNumbers;
    public GameObject[] UIImage;

    private bool isCoroutine, changeOccurred;
    public bool setHays_noSliders, startError;

    public int intHays1, intHays2, version;
    private int sliderMaxValue = 370, sliderMinValue = 0;
    private float sliderStep = 0.00f;
    public float sizeAnimals1, sizeAnimals2;
    private int countSlider = 0;

    // Start is called before the first frame update
    void Start()
    {
        activeHays = new List<GameObject>();
        refSlidersAnimals = new List<GameObject>();

        pointsOfHays1 = new List<GameObject>();  pointsOfHays2 = new List<GameObject>();
        tensAnimals1 = new List<GameObject>();  tensAnimals2 = new List<GameObject>();
        positionedAnimals1 = new List<GameObject>();  positionedAnimals2 = new List<GameObject>();

        fences.SetActive(false);
        skipButton.SetActive(false);
        isCoroutine = false;
        canvasSliders.SetActive(false);
        lineOfNumbers.SetActive(false);
        UIImage[0].SetActive(false);
        UIImage[1].SetActive(false);
    }

    private void Update()
    {
        if (startError && Input.GetKeyDown("space")) this.SpeedUpErrorTrial();

        if (startError && version==1)
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

                if (activeHays.Count > 6 && check != gameObject.GetComponent<DataManager>().activeAnimals.Count) skipButton.SetActive(true);

                if (check == gameObject.GetComponent<DataManager>().activeAnimals.Count && !isCoroutine)
                {
                    skipButton.SetActive(false);
                    StartCoroutine(WaitAndThenDo(0.1f));
                    isCoroutine = true;
                }
            }
            else
            {
                if (countSlider > 6 && countSlider != gameObject.GetComponent<DataManager>().activeAnimals.Count) skipButton.SetActive(true);

                if (countSlider == gameObject.GetComponent<DataManager>().activeAnimals.Count && !isCoroutine)
                {
                    skipButton.SetActive(false);
                    StartCoroutine(WaitAndThenDo(0.1f));
                    isCoroutine = true;
                }
            } 
        }

        if (startError & version == 2)
        {
            if ((positionedAnimals1.Count + positionedAnimals2.Count) > 6 && (positionedAnimals1.Count + positionedAnimals2.Count) != gameObject.GetComponent<DataManager>().activeAnimals.Count) skipButton.SetActive(true);

            if ((positionedAnimals1.Count + positionedAnimals2.Count) == gameObject.GetComponent<DataManager>().activeAnimals.Count && !isCoroutine)
            {
                skipButton.SetActive(false);
                StartCoroutine(WaitAndThenDo(0.1f));
                isCoroutine = true;
            }
        }

        if (startError & version == 3)
        {
            int check = 0;
            foreach (GameObject c in gameObject.GetComponent<DataManager>().activeAnimals)
            {
                foreach (GameObject a in activeHays)
                {
                    if (c.transform.position == a.transform.position) check++;
                }
            }

            if (activeHays.Count > 6 && check != gameObject.GetComponent<DataManager>().activeAnimals.Count) skipButton.SetActive(true);

            if (check == gameObject.GetComponent<DataManager>().activeAnimals.Count && !isCoroutine)
            {
                skipButton.SetActive(false);
                StartCoroutine(WaitAndThenDo(0.1f));
                isCoroutine = true;
            }
        }
    }

    public void SpeedUpErrorTrial()
    {
        if ((version == 1 && setHays_noSliders) || (version==2) || (version==3))
        {
            foreach (GameObject a in gameObject.GetComponent<DataManager>().activeAnimals)
            {
                if (a.GetComponent<Animals>().errorStarted)
                {
                    if (a.GetComponent<Animals>().area.name == "Area1")
                    {
                        a.GetComponent<Animals>().setAnimalError(1, hay_area1_pos, sizeAnimals1);
                        if(!positionedAnimals1.Contains(a)) positionedAnimals1.Add(a);

                        if (version == 1 || version == 3 )
                        {
                            if (pointsOfHays1.Count != 0) this.ActiveHays_1_3(1);
                        }
                        else if (version == 2)
                        {
                            if (positionedAnimals1.Count() < gameObject.GetComponent<TrialsManager>().area1Value) this.ActiveHays_2(1);  
                        }

                    }
                    else if (a.GetComponent<Animals>().area.name == "Area2")
                    {
                        a.GetComponent<Animals>().setAnimalError(2, hay_area2_pos, sizeAnimals2);
                        if (!positionedAnimals2.Contains(a)) positionedAnimals2.Add(a);

                        if (version == 1 || version == 3)
                        {
                            if (pointsOfHays2.Count != 0) this.ActiveHays_1_3(2);

                        }
                        else if (version == 2)
                        {
                            if (positionedAnimals2.Count() < gameObject.GetComponent<TrialsManager>().area2Value) this.ActiveHays_2(2);                                
                            
                        }
                    }
                }
            }
        }
        else if (version == 1 && !setHays_noSliders)
        {
            TrialData data = gameObject.GetComponent<DataManager>().data;
            sliderArea1.value = sliderStep * data.getArea1Data().getNumberOfAnimals();
            sliderArea2.value = sliderStep * data.getArea2Data().getNumberOfAnimals();
            countSlider = gameObject.GetComponent<DataManager>().activeAnimals.Count;

            foreach (GameObject c in gameObject.GetComponent<DataManager>().activeAnimals) c.SetActive(false);
        }
    }

    IEnumerator WaitAndThenDo(float time)
    {
        yield return new WaitForSeconds(time);
        //gameObject.GetComponent<ButtonsManager>().EndErrorTrial();
        UIImage[0].SetActive(true);
        UIImage[0].GetComponent<AudioSource>().Play();

        gameObject.GetComponent<ButtonsManager>().Buttons(true);
    }

    public void Retry()
    {
        UIImage[1].SetActive(true);
        UIImage[1].GetComponent<AudioSource>().Play();


        gameObject.GetComponent<ButtonsManager>().Buttons(true);
    }

    public void ActiveHays_1_3(int area)
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

    public void ActiveHays_2(int area)
    {
        if (area == 1)
        {
            if (intHays1 == 10)
            {
                ActiveTensAnimal(1);
                intHays1 = 0;
            }
            pointsOfHays1[intHays1].SetActive(true);
            textUnitArea1[intHays1].SetActive(true);
            hay_area1_pos = pointsOfHays1[intHays1].transform.position;
            intHays1++;
        }
        else if (area == 2)
        {
            if (intHays2 == 10)
            {
                ActiveTensAnimal(2);
                intHays2 = 0;
            }
            pointsOfHays2[intHays2].SetActive(true);
            textUnitArea2[intHays2].SetActive(true);
            hay_area2_pos = pointsOfHays2[intHays2].transform.position;
            intHays2++;
        }
    }

    public void ActiveTensAnimal(int area)
    {
        if (area == 1)
        {
            foreach (GameObject h1 in pointsOfHays1) h1.SetActive(false);
            foreach (GameObject t1 in textUnitArea1) t1.SetActive(false);
            foreach (GameObject a1 in positionedAnimals1) a1.SetActive(false);

            bool setTens = false;
            
            for(int i=0; i < tensAnimals1.Count; i++)
            {
                if (!setTens)
                {
                    if (tensAnimals1[i].transform.position == new Vector3(-4, 7, 0))
                    {
                        tensAnimals1[i].transform.position = new Vector3(pointsOfHays1[i].transform.position.x -  1.5f, pointsOfHays1[i].transform.position.y, pointsOfHays1[i].transform.position.z);
                        textTensArea1[i].SetActive(true);
                        setTens = true;
                    }
                }
            }

            if (setTens && positionedAnimals1.Count() == gameObject.GetComponent<TrialsManager>().area1Value)
            {
                textUnitArea1[0].GetComponent<Text>().text = "0";
                textUnitArea1[0].SetActive(true);
            }
        }
        else if (area == 2)
        {            
            foreach (GameObject h2 in pointsOfHays2) h2.SetActive(false);
            foreach (GameObject t2 in textUnitArea2) t2.SetActive(false);
            foreach (GameObject a2 in positionedAnimals2) a2.SetActive(false);

            bool setTens = false;

            if (!changeOccurred)
            {
                List<GameObject> listUnit = new List<GameObject>();
                List<GameObject> listTens = new List<GameObject>();

                foreach (GameObject u in textUnitArea2) listUnit.Add(u);
                foreach (GameObject t in textTensArea2) listTens.Add(t);

                textUnitArea2.Clear();
                textTensArea2.Clear();

                foreach (GameObject u in listUnit)
                {
                    u.GetComponent<Text>().color = Color.white;
                    textTensArea2.Add(u);
                }

                foreach (GameObject t in listTens)
                {
                    t.GetComponent<Text>().color = Color.black;
                    textUnitArea2.Add(t);
                }

                foreach (GameObject p in pointsOfHays2)
                {
                    Vector3 beforePos = p.transform.position;

                    p.transform.position = new Vector3(beforePos.x + 1.5f, beforePos.y, beforePos.z);
                }

                changeOccurred = true;
            }

            for (int i = 0; i < tensAnimals2.Count; i++)
            {
                if (!setTens)
                {
                    if (tensAnimals2[i].transform.position == new Vector3(4, 7, 0))
                    {
                        tensAnimals2[i].transform.position = new Vector3(pointsOfHays2[i].transform.position.x - 1.5f, pointsOfHays2[i].transform.position.y, pointsOfHays2[i].transform.position.z);
                        textTensArea2[i].SetActive(true);
                        setTens = true;
                    }
                }
            }

            if (setTens && positionedAnimals2.Count() == gameObject.GetComponent<TrialsManager>().area2Value)
            {
                textUnitArea2[0].GetComponent<Text>().text = "0";
                textUnitArea2[0].SetActive(true);
            }
        }
    }

    public void CollectData(TrialData data, List<GameObject> activeAnimals, int v)
    {
        fences.SetActive(true);
        version = v;

        sizeAnimals1 = data.getArea1Data().getSizeOfAnimal();
        sizeAnimals2 = data.getArea2Data().getSizeOfAnimal();

        if (version == 1)
        {
            sliderArea1.value = sliderMinValue;
            sliderArea2.value = sliderMinValue;

            this.SetPositionsHays_1(data);

            if (setHays_noSliders)
            {
                this.ActiveHays_1_3(1);
                this.ActiveHays_1_3(2);
            }
            else
            {
                canvasSliders.SetActive(true);

                if (data.getArea1Data().getNumberOfAnimals() > data.getArea2Data().getNumberOfAnimals())
                {
                    sliderStep = (float)((float)sliderMaxValue / (float)data.getArea1Data().getNumberOfAnimals());
                }
                else
                {
                    sliderStep = (float)((float)sliderMaxValue / (float)data.getArea2Data().getNumberOfAnimals());
                }
            }

            foreach (GameObject c in activeAnimals)
            {
                if (c.GetComponent<Animals>().area.name == "Area1")
                {
                    gameObject.GetComponent<DragManager>().draggableAnimals1.Add(c);
                    c.GetComponent<Animals>().setAnimalError(0, c.GetComponent<Animals>().positionFinal, sizeAnimals1);

                    if (refSlidersAnimals.Count == 0 && setHays_noSliders == false)
                    {
                        GameObject newAnimal = Instantiate(c);
                        newAnimal.GetComponent<Animals>().setSliderAnimal(1);
                        refSlidersAnimals.Add(newAnimal);
                    }
                }
                else if (c.GetComponent<Animals>().area.name == "Area2")
                {
                    gameObject.GetComponent<DragManager>().draggableAnimals2.Add(c);
                    c.GetComponent<Animals>().setAnimalError(0, c.GetComponent<Animals>().positionFinal, sizeAnimals2);

                    if (refSlidersAnimals.Count == 1 && setHays_noSliders == false)
                    {
                        GameObject newAnimal = Instantiate(c);
                        newAnimal.GetComponent<Animals>().setSliderAnimal(2);
                        refSlidersAnimals.Add(newAnimal);
                    }
                }
            }
        }
        else if (version == 2)
        {
            AnimalSizeControl(data.area1Data, 1);
            AnimalSizeControl(data.area2Data, 2);
            this.SetPositionsHays_2_3(data);

            bool createTens1 = false;
            bool createTens2 = false;

            foreach (GameObject c in activeAnimals)
            {
                if (c.GetComponent<Animals>().area.name == "Area1")
                {
                    gameObject.GetComponent<DragManager>().draggableAnimals1.Add(c);
                    c.GetComponent<Animals>().setAnimalError(0, c.GetComponent<Animals>().positionFinal, sizeAnimals1);

                    if (!createTens1)
                    {
                        int tens = (int)(data.area1Data.getNumberOfAnimals() / 10);
                        for (int i = 1; i <= tens; i++)
                        {
                            GameObject newAnimal = Instantiate(c);
                            newAnimal.GetComponent<Animals>().setTensAnimal(1, sizeAnimals1+0.5f);
                            tensAnimals1.Add(newAnimal);
                        }
                        createTens1 = true;
                    }
                }
                else if (c.GetComponent<Animals>().area.name == "Area2")
                {
                    gameObject.GetComponent<DragManager>().draggableAnimals2.Add(c);
                    c.GetComponent<Animals>().setAnimalError(0, c.GetComponent<Animals>().positionFinal, sizeAnimals2);

                    if (!createTens2)
                    {
                        int tens = (int)(data.area1Data.getNumberOfAnimals() / 10);
                        for (int i = 1; i <= tens; i++)
                        {
                            GameObject newAnimal = Instantiate(c);
                            newAnimal.GetComponent<Animals>().setTensAnimal(2, sizeAnimals2);
                            tensAnimals2.Add(newAnimal);
                        }
                        createTens2 = true;
                    }
                }
            }

            intHays1 = 0;
            intHays2 = 0;

            this.ActiveHays_2(1);
            this.ActiveHays_2(2);
        }
        else if (version == 3)
        {
            AnimalSizeControl(data.area1Data, 1);
            AnimalSizeControl(data.area2Data, 2);

            lineOfNumbers.SetActive(true);

            this.SetPositionsHays_2_3(data);

            foreach (GameObject c in activeAnimals)
            {
                if (c.GetComponent<Animals>().area.name == "Area1")
                {
                    gameObject.GetComponent<DragManager>().draggableAnimals1.Add(c);
                    c.GetComponent<Animals>().setAnimalError(0, c.GetComponent<Animals>().positionFinal, sizeAnimals1);

                }
                else if (c.GetComponent<Animals>().area.name == "Area2")
                {
                    gameObject.GetComponent<DragManager>().draggableAnimals2.Add(c);
                    c.GetComponent<Animals>().setAnimalError(0, c.GetComponent<Animals>().positionFinal, sizeAnimals2);
                }
            }

            this.ActiveHays_1_3(1);
            this.ActiveHays_1_3(2);
        }

        gameObject.GetComponent<DragManager>().active = true;
        startError = true;
    }

    private void AnimalSizeControl(AreaTrialData atd, int a)
    {
        float maxSizeHays = 0.042f;
        float actualSizeHays = atd.getSizeOfAnimal() * 0.007f;

        if(actualSizeHays > maxSizeHays)
        {
            if (a == 1) sizeAnimals1 = maxSizeHays / 0.007f;
            else if (a == 2) sizeAnimals2 = maxSizeHays / 0.007f;
        }
        else
        {
            if (a == 1) sizeAnimals1 = atd.getSizeOfAnimal();
            else if (a == 2) sizeAnimals2 = atd.getSizeOfAnimal();

        }

        float newScaleText1 = sizeAnimals1 / 6;
        float newScaleText2 = sizeAnimals2 / 6;

        foreach (GameObject tu1 in textUnitArea1) tu1.transform.localScale = new Vector3(newScaleText1, newScaleText1, newScaleText1);
        foreach (GameObject tt1 in textTensArea1) tt1.transform.localScale = new Vector3(newScaleText1, newScaleText1, newScaleText1);
        foreach (GameObject tu2 in textUnitArea2) tu2.transform.localScale = new Vector3(newScaleText2, newScaleText2, newScaleText2);
        foreach (GameObject tt2 in textTensArea2) tt2.transform.localScale = new Vector3(newScaleText2, newScaleText2, newScaleText2);

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
        countSlider++;
    }

    public void Reset()
    {
        foreach (GameObject p1 in pointsOfHays1) Destroy(p1);
        foreach (GameObject p2 in pointsOfHays2) Destroy(p2);
        foreach (GameObject t1 in tensAnimals1) Destroy(t1);
        foreach (GameObject t2 in tensAnimals2) Destroy(t2);
        foreach (GameObject a1 in positionedAnimals1) Destroy(a1);
        foreach (GameObject a2 in positionedAnimals2) Destroy(a2);
        foreach (GameObject h in activeHays) Destroy(h);
        foreach (GameObject s in refSlidersAnimals) Destroy(s);
        foreach (GameObject tu1 in textUnitArea1) tu1.SetActive(false);
        foreach (GameObject tt1 in textTensArea1) tt1.SetActive(false);
        foreach (GameObject tu2 in textUnitArea2) tu2.SetActive(false);
        foreach (GameObject tt2 in textTensArea2) tt2.SetActive(false);
        foreach (GameObject i in UIImage) i.SetActive(false);

        pointsOfHays1.Clear();
        pointsOfHays2.Clear();
        tensAnimals1.Clear();
        tensAnimals2.Clear();
        positionedAnimals1.Clear();
        positionedAnimals2.Clear();
        activeHays.Clear();
        refSlidersAnimals.Clear();

        fences.SetActive(false);
        startError = false;
        version = 0;
        countSlider = 0;
        sliderStep = 0.00f;
        skipButton.SetActive(false);
        isCoroutine = false;
        canvasSliders.SetActive(false);
        lineOfNumbers.SetActive(false);
        setHays_noSliders = false;

        if (changeOccurred)
        {
            List<GameObject> listUnit = new List<GameObject>();
            List<GameObject> listTens = new List<GameObject>();

            foreach (GameObject u in textUnitArea2) listUnit.Add(u);
            foreach (GameObject t in textTensArea2) listTens.Add(t);

            textUnitArea2.Clear();
            textTensArea2.Clear();

            foreach (GameObject u in listUnit)
            {
                u.GetComponent<Text>().color = Color.white;
                textTensArea2.Add(u);
            }

            foreach (GameObject t in listTens)
            {
                t.GetComponent<Text>().color = Color.black;
                textUnitArea2.Add(t);
            }

            changeOccurred = false;
        }

        if (positionedAnimals1.Count() == gameObject.GetComponent<TrialsManager>().area1Value) textUnitArea1[0].GetComponent<Text>().text = "1";
        if (positionedAnimals2.Count() == gameObject.GetComponent<TrialsManager>().area2Value) textUnitArea2[0].GetComponent<Text>().text = "1";
    }

    private void SetPositionsHays_1(TrialData data)
    {
        List<Vector3> positionsArea1 = new List<Vector3>();
        List<Vector3> positionsArea2 = new List<Vector3>();

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

        if (positionsArea1.Count == 0) positionsArea1.Add(new Vector3(-1.2f, -4.1f, 0f));
        if (positionsArea2.Count == 0) positionsArea2.Add(new Vector3(1.2f, -4.1f, 0f));

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
                setHays_noSliders = true;
            }
        }

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
        }
    }

    private void SetPositionsHays_2_3(TrialData data)
    {
        List<Vector3> positionsArea1 = new List<Vector3>();
        List<Vector3> positionsArea2 = new List<Vector3>();

        if (positionsArea1.Count == 0) positionsArea1.Add(new Vector3(-1.1f, -4.5f, 0f));
        if (positionsArea2.Count == 0) positionsArea2.Add(new Vector3(1.1f, -4.5f, 0f));
        
        for (int i = 1; i < 10; i++)
        {
            Vector3 v_i_1 = new Vector3(positionsArea1[0].x, positionsArea1[0].y + i, 0);
            positionsArea1.Add(v_i_1);

            Vector3 v_i_2 = new Vector3(positionsArea2[0].x, positionsArea2[0].y + i, 0);
            positionsArea2.Add(v_i_2);
        }

        if (version == 2)
        {
            int numAnimals_1 = data.area1Data.getNumberOfAnimals();
            int numAnimals_2 = data.area2Data.getNumberOfAnimals();

            if (data.area1Data.getNumberOfAnimals() > 10) numAnimals_1 = 10;
            if (data.area2Data.getNumberOfAnimals() > 10) numAnimals_2 = 10;

            foreach (Vector3 v in positionsArea1.OrderByDescending(p => p.x).ThenBy(p => p.y))
            {
                if (pointsOfHays1.Count < numAnimals_1)
                {
                    GameObject newHay = Instantiate(hay);
                    newHay.transform.localScale = new Vector3(sizeAnimals1 * 0.007f, sizeAnimals1 * 0.007f, 0);
                    newHay.transform.position = v;
                    newHay.SetActive(false);
                    pointsOfHays1.Add(newHay);
                }
            }

            foreach (Vector3 v in positionsArea2.OrderBy(p => p.x).ThenBy(p => p.y))
            {
                if (pointsOfHays2.Count < numAnimals_2)
                {
                    GameObject newHay = Instantiate(hay);
                    newHay.transform.localScale = new Vector3(sizeAnimals2 * 0.007f, sizeAnimals2 * 0.007f, 0);
                    newHay.transform.position = v;
                    newHay.SetActive(false);
                    pointsOfHays2.Add(newHay);
                }
            }
        }

        if (version == 3)
        {
            if (data.area1Data.getNumberOfAnimals() > 10)
            {
                int div = (int)(data.area1Data.getNumberOfAnimals()/10);
                float avg_1 = sizeAnimals1 * 0.007f * 30f;

                for (int i = 1; i <= div; i++)
                {
                    for(int j = 1; j <= 10; j++)
                    {
                        Vector3 v_j_1 = new Vector3(positionsArea1[j-1].x - (i * avg_1), positionsArea1[j-1].y, 0);
                        positionsArea1.Add(v_j_1);
                    }
                }
            }

            if (data.area2Data.getNumberOfAnimals() > 10)
            {
                int div = (int)(data.area2Data.getNumberOfAnimals() / 10);
                float avg_2 = sizeAnimals2 * 0.007f * 30f;

                for (int i = 1; i <= div; i++)
                {
                    for (int j = 1; j <= 10; j++)
                    {
                        Vector3 v_j_2 = new Vector3(positionsArea2[j - 1].x + (i * avg_2), positionsArea2[j - 1].y, 0);
                        positionsArea2.Add(v_j_2);
                    }
                }
            }

            foreach (Vector3 v in positionsArea1.OrderByDescending(p => p.x).ThenBy(p => p.y))
            {
                if (pointsOfHays1.Count < data.area1Data.getNumberOfAnimals())
                {
                    GameObject newHay = Instantiate(hay);
                    newHay.transform.localScale = new Vector3(sizeAnimals1 * 0.007f, sizeAnimals1 * 0.007f, 0);
                    newHay.transform.position = v;
                    newHay.SetActive(false);
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
                    newHay.SetActive(false);
                    pointsOfHays2.Add(newHay);
                }
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


/* OLD METHODS
private void ControllSize(TrialData data, int num1, int num2)
{
    float d = 8.7f;
    float avg_1 = (data.area1Data.getSizeOfAnimal() * 0.007f * 25f);
    int div_1 = (int)(d / avg_1);
    float avg_2 = (data.area2Data.getSizeOfAnimal() * 0.007f * 25f);
    int div_2 = (int)(d / avg_2);

    sizeAnimals1 = data.area1Data.getSizeOfAnimal();
    sizeAnimals2 = data.area2Data.getSizeOfAnimal();
    Debug.Log(div_2+ " "+ avg_2);

    if (div_1 >= (num1 - 1))
    {
        div_1 = num1 - 1;
        avg_1 = d / div_1;

    }

    if(div_2 >= (num2 - 1))
    {
        div_2 = num2 - 1;
        avg_2 = d / div_2;
        Debug.Log(div_2 + " " + avg_2);
    }

    if (div_1 >= div_2)
    {
        if (div_1 < num2-1) 
        {
            SetNewSize(div_1, avg_1, 2);
        }
        else
        {
            SetNewSize(div_1, avg_1, 0);
        }
    }
    else if (div_2 >= div_1)
    {
        if (div_2 < num1 - 1)
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
    int div = d;
    float avg = a;

    float newsize = (8.8f / 0.175f) / d;

    if (num_area == 1)
    {
        sizeAnimals1 = newsize;
    }
    else if (num_area == 2)
    {
        sizeAnimals2 = newsize;
    }
}
*/

