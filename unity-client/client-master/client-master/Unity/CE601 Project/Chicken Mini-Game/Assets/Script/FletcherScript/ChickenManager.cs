using System;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using Debug = UnityEngine.Debug;

/*
 @Author: Fletcher Hurn (1806938)
 */
public class ChickenManager : MonoBehaviour
{
    public Chicken chicken;
    public float defaultFenceRadius;
    public GameObject area1Fence;
    public GameObject area2Fence;

    public Transform area1Centre;
    public Transform area2Centre;

    private List<Chicken> activeChickens;

    private List<Vector3> createdPositions;

    private AreaTrialData area1Data;
    private AreaTrialData area2Data;

    private Stopwatch stopwatch;

    // Start is called before the first frame update
    void Start()
    {
        stopwatch = new Stopwatch();
        GameTrialData trialData = GameManager.instance.getNextTrial();

        area1Data = trialData.area1Data;
        area2Data = trialData.area2Data;

        float newScaleArea1 = (area1Data.getCircleRadius() / defaultFenceRadius) + 0.2f;
        area1Fence.transform.localScale = new Vector3(newScaleArea1, newScaleArea1);
        float newScaleArea2 = (area2Data.getCircleRadius() / defaultFenceRadius) + 0.2f;
        area2Fence.transform.localScale = new Vector3(newScaleArea2, newScaleArea2);

        activeChickens = new List<Chicken>();

        Debug.Log(area1Data.getNumberOfAnimals());
        Debug.Log(area2Data.getNumberOfAnimals());
        createdPositions = new List<Vector3>();
        initializeChicken(chicken, area1Data, 1, 1);
        for (int i = 1; i < area1Data.getNumberOfAnimals(); i++)
        {
            Chicken newChicken = Instantiate(chicken);
            initializeChicken(newChicken, area1Data, 1, i+1);
        }
        createdPositions = new List<Vector3>();
        for (int i = 0; i < area2Data.getNumberOfAnimals(); i++)
        {
            Chicken newChicken = Instantiate(chicken);
            initializeChicken(newChicken, area2Data, 2, i+1);
        }
        GameManager.instance.area1Chickens = area1Data.getNumberOfAnimals();
        GameManager.instance.area2Chickens = area2Data.getNumberOfAnimals();
        adjustChickenSizes();
    }

    void adjustChickenSizes()
    {
        foreach (Chicken activeChicken in activeChickens)
        {
            AreaTrialData areaData = activeChicken.getArea() == 1 ? area1Data : area2Data;
            activeChicken.transform.localScale = new Vector3(areaData.getSizeOfAnimal(), areaData.getSizeOfAnimal());
        }
    }

    void initializeChicken(Chicken newChicken, AreaTrialData areaData ,int area, int chickenNumber)
    {
        Transform centre = area == 1 ? area1Centre : area2Centre;
        float minCircleX = centre.position.x - areaData.getCircleRadius();
        float maxCircleX = centre.position.x + areaData.getCircleRadius();
        float minCircleY = centre.position.y - areaData.getCircleRadius();
        float maxCircleY = centre.position.y + areaData.getCircleRadius();
        float x;
        float y;
        Vector3 lastCreatedPosition;
        Vector3 secondLastCreatedPosition;
        GameObject temp = new GameObject();
        if (createdPositions.Count > 1)
        {
            int lastPositionIndex = createdPositions.Count - 1;
            int secondLastPositionIndex = createdPositions.Count - 2;
            lastCreatedPosition = createdPositions[lastPositionIndex--];
            secondLastCreatedPosition = createdPositions[secondLastPositionIndex--];
            Vector3 position = GetNextPosition(areaData.getAverageSpaceBetween(), lastCreatedPosition, secondLastCreatedPosition, maxCircleX, minCircleX, maxCircleY, minCircleY);
            while (!CheckValidPosition(position))
            {
                if (secondLastPositionIndex < 0 || lastPositionIndex < 0 || lastPositionIndex == secondLastPositionIndex)
                {
                    if (lastPositionIndex < 0) lastPositionIndex = UnityEngine.Random.Range(0, createdPositions.Count - 1);
                    if (secondLastPositionIndex < 0) secondLastPositionIndex = UnityEngine.Random.Range(0, createdPositions.Count - 1);
                }
                if (secondLastPositionIndex == lastPositionIndex)
                {
                    lastPositionIndex--;
                } else
                {
                    lastCreatedPosition = createdPositions[lastPositionIndex--];
                    secondLastCreatedPosition = createdPositions[secondLastPositionIndex--];
                    position = GetNextPosition(areaData.getAverageSpaceBetween(), lastCreatedPosition, secondLastCreatedPosition, maxCircleX, minCircleX, maxCircleY, minCircleY);
                }
            }
            temp.transform.position = position;
        } else if (createdPositions.Count == 1)
        {
            lastCreatedPosition = createdPositions[createdPositions.Count - 1];
            Vector2 point = RandomPointOnUnitCircle(areaData.getAverageSpaceBetween());
            x = lastCreatedPosition.x + point.x;
            y = lastCreatedPosition.y + point.y;
            while (x > maxCircleX || x < minCircleX || y > maxCircleY || y < minCircleY)
            {
                point = RandomPointOnUnitCircle(areaData.getAverageSpaceBetween());
                x = lastCreatedPosition.x + point.x;
                y = lastCreatedPosition.y + point.y;
            }
            temp.transform.position = new Vector3(RoundFloat(x), RoundFloat(y));
        } else
        {
            x = RoundFloat(UnityEngine.Random.Range(centre.position.x - 0.2f, centre.position.x + 0.2f));
            y = RoundFloat(UnityEngine.Random.Range(centre.position.y - 0.2f, centre.position.y + 0.2f));
            temp.transform.position = new Vector3(x, y);
        }
        print("Chicken " + chickenNumber + " for area " + area + " is being placed at: " + temp.transform.position);
        createdPositions.Add(temp.transform.position);
        newChicken.setLastWaypoint(temp.transform);
        activeChickens.Add(newChicken);
    }

    private float RoundFloat(float number)
    {
        return (float)Math.Round(number, 5);
    }
    private bool CheckValidPosition(Vector3 position)
    {
        if (float.IsNaN(position.x) || float.IsNaN(position.y))
        {
            return false;
        }
        foreach (Vector3 existingPosition in createdPositions)
        {
            if (Vector3.Distance(position, existingPosition) < 0.05f)
            {
                return false;
            }
        }
        return true;
    }

    private Vector3 GetNextPosition(float averageSpaceBetween,Vector3 lastCreatedPosition, Vector3 secondLastCreatedPosition, float maxCircleX, float minCircleX, float maxCircleY, float minCircleY) 
    {
        double intersection1x;
        double intersection1y;
        double intersection2x;
        double intersection2y;
        intersectionTwoCircles(lastCreatedPosition.x, lastCreatedPosition.y, averageSpaceBetween, secondLastCreatedPosition.x,
            secondLastCreatedPosition.y, averageSpaceBetween, out intersection1x, out intersection1y, out intersection2x, out intersection2y);
        Vector3 position = new Vector3(RoundFloat((float)intersection1x), RoundFloat((float)intersection1y));
        if (position.x > maxCircleX || position.x < minCircleX || position.y > maxCircleY || position.y < minCircleY || createdPositions.Contains(position))
        {
            position = new Vector3(RoundFloat((float)intersection2x), RoundFloat((float)intersection2y));
        }
        return position;
    }

    // Method from https://answers.unity.com/questions/33193/randomonunitcircle-.html
    private Vector2 RandomPointOnUnitCircle(float radius)
    {
        float angle = UnityEngine.Random.Range(0f, Mathf.PI * 2);
        float x = Mathf.Sin(angle) * radius;
        float y = Mathf.Cos(angle) * radius;

        return new Vector2(x, y);

    }

    // Code taken from https://stackoverflow.com/questions/33520698/getting-the-intersection-points-of-2-circles
    private void intersectionTwoCircles(double c1x, double c1y, double r1, double c2x, double c2y, double r2,
        out double a1x, out double a1y, out double a2x, out double a2y)
    {
        /* error handling is missing completely

              A1
             /| \
         r1 / |  \ r2
           /  |   \
          /   |h   \
         /g1  |     \          (g1 means angle gamma1)
        C1----P-----C2
           d1   d2
        */
        double dx = c1x - c2x;
        double dy = c1y - c2y;
        double d = Math.Sqrt(dx * dx + dy * dy); // d = |C1-C2|
        double gamma1 = Math.Acos((r2 * r2 + d * d - r1 * r1) / (2 * r2 * d)); // law of cosines
        double d1 = r1 * Math.Cos(gamma1); // basic math in right triangle
        double h = r1 * Math.Sin(gamma1);
        double px = c1x + (c2x - c1x) / d * d1;
        double py = c1y + (c2y - c1y) / d * d1;
        // (-dy, dx)/d is (C2-C1) normalized and rotated by 90 degrees
        a1x = px + (-dy) / d * h;
        a1y = py + (+dx) / d * h;
        a2x = px - (-dy) / d * h;
        a2y = py - (+dx) / d * h;
    }

    // Update is called once per frame
    void Update()
    {
        if (!GameManager.instance.chickensReady && GameManager.instance.gameStarted)
        {
            bool ready = true;
            foreach (Chicken chicken in activeChickens)
            {
                if (!chicken.isReady())
                {
                    ready = false;
                    break;
                }
            }
            if (ready)
            {
                GameManager.instance.chickensReady = true;
                stopwatch.Start();
            }
        } else
        {
            if (stopwatch.ElapsedMilliseconds > (GameManager.instance.chickenShowTime * 1000)) {
                stopwatch.Stop();
                foreach (Chicken chicken in activeChickens)
                {
                    chicken.gameObject.SetActive(false);
                }
            }
        }
    }
}
