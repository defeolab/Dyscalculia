using System;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using Debug = UnityEngine.Debug;
using Random = UnityEngine.Random;
using System.Collections;
using UnityEngine.UI;

public class ControllGrid : MonoBehaviour
{
    private float radius_area=1.2f;
    private float increment = 0.0001f;
    private int div = 0;
    private float field_area = 0;
    private float asb = 0.9f;
    private List<Vector3> createdPositionsArea;
    private List<GameObject> spheres;
    public GameObject area;
    public GameObject sphere;
    public Text asb_text;
    public Text num_text;
    public Text cr_text;
    public Text fa_text;
    private Stopwatch stopwatch;
    private bool startwatch;
    private List<String> allVariable;
    public bool butt_next;
    public bool butt_back;

    // Start is called before the first frame update
    void Start()
    {
        cr_text.text = radius_area.ToString();
        radius_area = radius_area * 3f;
        field_area = radius_area * radius_area * Mathf.PI;
        fa_text.text = field_area.ToString();
        createdPositionsArea = new List<Vector3>();
        spheres = new List<GameObject>();
        stopwatch = new Stopwatch();
        allVariable= new List<String>();
    }

    // Update is called once per frame
    void Update()
    {
        if (asb <= 3.5f)
        {
            if (!startwatch)
            {
                this.CreateGrid(area, asb);
                asb_text.text = asb.ToString();
                num_text.text = createdPositionsArea.Count.ToString();
                //stopwatch.Start();
                startwatch = true;

                allVariable.Add(GenerateSting(asb, createdPositionsArea.Count));
            }
            else
            {
                //if(stopwatch.IsRunning && stopwatch.ElapsedMilliseconds > 2000)
                //{
                //stopwatch.Stop();
                if (butt_next)
                {
                    startwatch = false;
                    asb += increment;
                    foreach (GameObject s in spheres)
                    {
                        Destroy(s);
                    }
                    spheres.Clear();
                    createdPositionsArea.Clear();
                    butt_next = false;
                    butt_back = false;
                }else if (butt_back)
                {
                    startwatch = false;
                    asb -= increment;
                    foreach (GameObject s in spheres)
                    {
                        Destroy(s);
                    }
                    spheres.Clear();
                    createdPositionsArea.Clear();
                    butt_next = false;
                    butt_back = false;
                }

                //stopwatch.Reset();
                //}
            }

        }
        else
        {
            Debug.Log(allVariable.Count);
            Debug.Log(ToString(0));
            Debug.Log(ToString(1));
            Debug.Log(ToString(2));
        }       
    }

    private void CreateGrid(GameObject area, float asb)
    {
        float div_f = radius_area / asb;
        div = Mathf.RoundToInt(div_f);
        Vector3 centre_area = area.transform.position;
        List<Vector3> vectors = new List<Vector3>();
        List<Vector3> vectors_total = new List<Vector3>();

        if (vectors.Count == 0)
        {
            vectors.Add(new Vector3(centre_area.x, centre_area.y, 0));
        }

        //Calculate all the point usable in the grid
        for (int i = 0; i < div + 1; i++)
        {
            //calculate the horrizontal points
            for (int j = 1; j <= div; j++)
            {
                float x_plus = vectors[0].x + (j * asb);
                float x_minus = vectors[0].x - (j * asb);
                float y_plus = vectors[0].y + (i * asb);
                float y_minus = vectors[0].y - (i * asb);

                vectors.Add(new Vector3(x_plus, y_plus, 0));
                vectors.Add(new Vector3(x_minus, y_plus, 0));
                vectors.Add(new Vector3(x_plus, y_minus, 0));
                vectors.Add(new Vector3(x_minus, y_minus, 0));
            }

            if (i != 0)
            {
                Vector3 v_i_plus = new Vector3(vectors[0].x, vectors[0].y + (i * asb), 0);
                vectors.Add(v_i_plus);

                Vector3 v_i_minus = new Vector3(vectors[0].x, vectors[0].y - (i * asb), 0);
                vectors.Add(v_i_minus);
            }
        }

        foreach (Vector3 v1 in vectors)
        {
            if (!vectors_total.Contains(v1)) vectors_total.Add(v1);
        }
        //Take only the points that are inside the circle
        foreach (Vector3 v in vectors_total)
        {
            GameObject newsphere = Instantiate(sphere);
            newsphere.transform.position = v;
            

            float d_x = (v.x - centre_area.x) * (v.x - centre_area.x);
            float d_y = (v.y - centre_area.y) * (v.y - centre_area.y);

            if ((Math.Sqrt(d_x + d_y) <= radius_area))
            {
                if (!createdPositionsArea.Contains(v)) createdPositionsArea.Add(v);
                newsphere.GetComponent<Renderer>().material.SetColor("_Color", Color.red);
            }

            spheres.Add(newsphere);
        }
    }

    public string GenerateSting(float asb, int num)
    {
        return asb + " - " + num;
    }

    public string ToString(int j)
    {
       int lenght= 927;
        string temp = "";

       for(int i=j*lenght; i< lenght*(j+1); i++)
        {
            temp += allVariable[i];
            temp += '\n';
        }
        /*foreach (string str in allVariable)
        {
            temp += str;
            temp += '\n'; 
        }*/
        return temp;
    }

    public void ButtNext (bool b)
    {
        butt_next = b;
    }
    public void ButtBack(bool b)
    {
        butt_back = b;
    }

}