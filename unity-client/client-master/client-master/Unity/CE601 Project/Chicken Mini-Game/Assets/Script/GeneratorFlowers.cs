using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GeneratorFlowers : MonoBehaviour
{

    public GameObject flowers;
    public GameObject eggs;
    public List<GameObject> activeDisctractions = new List<GameObject>();
    private List<Vector3> createdPositionsInside = new List<Vector3>();
    private List<Vector3> createdPositionsOutside = new List<Vector3>();

    public void DistractionGenerator()
    {
        Random.InitState((int)System.DateTime.Now.Ticks); Random.InitState((int)System.DateTime.Now.Ticks);
        GridInside1();
        GridInside2();
        GridOutside();

        if (activeDisctractions.Count != 0)
        {
            foreach (GameObject f in activeDisctractions)
            {
                Destroy(f);
            }
        }

        /*for (int i = 0; i < Random.Range(2, 15); i++)
        {
            GameObject newFlowers = Instantiate(flowers);
            newFlowers.transform.position = new Vector3(Random.Range(-8.0f, 8.0f), Random.Range(-4.3f, 4.3f), 0.2f);
            newFlowers.transform.rotation = Quaternion.Euler(new Vector3(0, 0, Random.Range(0f, 360f)) * 1);
            activeDisctractions.Add(newFlowers);
        }*/

        for (int i = 0; i < Random.Range(2, 15); i++)
        {
            GameObject newFlowers = Instantiate(flowers);
            int j = Random.Range(0, createdPositionsOutside.Count);
            newFlowers.transform.position = createdPositionsOutside[j];
            newFlowers.transform.rotation = Quaternion.Euler(new Vector3(0, 0, Random.Range(0f, 360f)) * 1);
            activeDisctractions.Add(newFlowers);
        }

        for (int i = 0; i < Random.Range(2, 15); i++)
        {
            GameObject newEggs = Instantiate(eggs);
            int j = Random.Range(0, createdPositionsInside.Count);
            newEggs.transform.position = createdPositionsInside[j];
            newEggs.transform.rotation = Quaternion.Euler(new Vector3(0, 0, Random.Range(0f, 360f)) * 1);
            activeDisctractions.Add(newEggs);
        }

    }

    private void GridOutside()
    {
        float radius_area_x = 8f;
        float radius_area_y = 4.3f;
        int div_x = (int)(radius_area_x / 0.6f);
        int div_y = (int)(radius_area_y/ 0.6f);
        Vector3 centre_area = new Vector3(0, 0, 0);
        List<Vector3> vectors = new List<Vector3>();

        if (vectors.Count == 0)
        {
            vectors.Add(new Vector3((centre_area.x - radius_area_x), (centre_area.y + radius_area_y), 0));
        }

        for (int i = 1; i <= div_y; i++)
        {
            //calculate the horrizontal points
            for (int j = 1; j <= div_x; j++)
            {
                Vector3 v_j = new Vector3((vectors[vectors.Count - 1].x + 0.6f), vectors[vectors.Count - 1].y, 0);
                vectors.Add(v_j);
            }

            Vector3 v_i = new Vector3(vectors[0].x, vectors[0].y - (i * 0.6f), 0);
            vectors.Add(v_i);
        }

        //Take only the points that are outside the circle
        foreach (Vector3 v in vectors)
        {
            Vector3 ca = new Vector3(-4.2f, 0.03f, 0);
            float d_x = (v.x - ca.x) * (v.x - ca.x);
            float d_y = (v.y - ca.y) * (v.y - ca.y);

            Vector3 ac = new Vector3(-4.2f, 0.03f, 0);
            float d_xx = (v.x - ac.x) * (v.x - ac.x);
            float d_yy = (v.y - ac.y) * (v.y - ac.y);

            if ((System.Math.Sqrt(d_x + d_y) > 4.2f))
            {
                if ((System.Math.Sqrt(d_xx + d_yy) > 4.2f))
                {
                    if (!createdPositionsOutside.Contains(v)) createdPositionsOutside.Add(v);
                }
            }
        }
    }

    private void GridInside2()
    {
        float radius_area = 3.5f;
        int div = (int)(radius_area / 0.6f);
        Vector3 centre_area = new Vector3(4.2f, 0.03f, 0);
        List<Vector3> vectors = new List<Vector3>();

        if (vectors.Count == 0)
        {
            vectors.Add(new Vector3(centre_area.x, centre_area.y, 0));
        }

        //calculation all the point usable in the grid
        for (int i = 0; i < div + 1; i++)
        {
            //calculation of points around the center
            for (int j = 1; j <= div; j++)
            {
                float x_plus = vectors[0].x + (j * 0.6f);
                float x_minus = vectors[0].x - (j * 0.6f);
                float y_plus = vectors[0].y + (i * 0.6f);
                float y_minus = vectors[0].y - (i * 0.6f);

                vectors.Add(new Vector3(x_plus, y_plus, 0));
                vectors.Add(new Vector3(x_minus, y_plus, 0));
                vectors.Add(new Vector3(x_plus, y_minus, 0));
                vectors.Add(new Vector3(x_minus, y_minus, 0));
            }

            if (i != 0)
            {
                Vector3 v_i_plus = new Vector3(vectors[0].x, vectors[0].y + (i * 0.6f), 0);
                vectors.Add(v_i_plus);

                Vector3 v_i_minus = new Vector3(vectors[0].x, vectors[0].y - (i * 0.6f), 0);
                vectors.Add(v_i_minus);
            }
        }

        //Take only the points that are inside the circle
        foreach (Vector3 v in vectors)
        {
            float d_x = (v.x - centre_area.x) * (v.x - centre_area.x);
            float d_y = (v.y - centre_area.y) * (v.y - centre_area.y);

            if ((System.Math.Sqrt(d_x + d_y) <= radius_area))
            {
                if (!createdPositionsInside.Contains(v)) createdPositionsInside.Add(v);
            }
        }
    }

    private void GridInside1()
    {
        float radius_area = 3.5f;
        int div = (int)(radius_area / 0.6f);
        Vector3 centre_area = new Vector3(-4.2f, 0.03f, 0);
        List<Vector3> vectors = new List<Vector3>();

        if (vectors.Count == 0)
        {
            vectors.Add(new Vector3(centre_area.x, centre_area.y, 0));
        }

        //calculation all the point usable in the grid
        for (int i = 0; i < div + 1; i++)
        {
            //calculation of points around the center
            for (int j = 1; j <= div; j++)
            {
                float x_plus = vectors[0].x + (j * 0.6f);
                float x_minus = vectors[0].x - (j * 0.6f);
                float y_plus = vectors[0].y + (i * 0.6f);
                float y_minus = vectors[0].y - (i * 0.6f);

                vectors.Add(new Vector3(x_plus, y_plus, 0));
                vectors.Add(new Vector3(x_minus, y_plus, 0));
                vectors.Add(new Vector3(x_plus, y_minus, 0));
                vectors.Add(new Vector3(x_minus, y_minus, 0));
            }

            if (i != 0)
            {
                Vector3 v_i_plus = new Vector3(vectors[0].x, vectors[0].y + (i * 0.6f), 0);
                vectors.Add(v_i_plus);

                Vector3 v_i_minus = new Vector3(vectors[0].x, vectors[0].y - (i * 0.6f), 0);
                vectors.Add(v_i_minus);
            }
        }

        //Take only the points that are inside the circle
        foreach (Vector3 v in vectors)
        {
            float d_x = (v.x - centre_area.x) * (v.x - centre_area.x);
            float d_y = (v.y - centre_area.y) * (v.y - centre_area.y);

            if ((System.Math.Sqrt(d_x + d_y) <= radius_area))
            {
                if (!createdPositionsInside.Contains(v)) createdPositionsInside.Add(v);
            }
        }
    }
}
