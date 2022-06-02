using System;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using Debug = UnityEngine.Debug;
using Random = UnityEngine.Random;
using System.Collections;
using UnityEngine.UI;
using System.Linq;
using UnityEngine.SceneManagement;

public class Chickens : MonoBehaviour
{
    public GameObject area;
    public GameObject chicken_model;
    public Material[] newMaterialRef;
    public AreaTrialData areaData;
    public Animator animator;
    public Vector3 positionFinal;
    public int number;
    public bool findFinalPos;
    public bool startWalk;
    public bool arrived;

    void Start()
    {
        animator = gameObject.GetComponent<Animator>();
        newMaterialRef = new Material[4];
        startWalk = false;
        arrived = false;

        newMaterialRef = Resources.LoadAll("Materials", typeof(Material)).Cast<Material>().ToArray();
    }

    void Update()
    {
        if (!arrived)
        {
            if (startWalk)
            {
                animator.SetBool("walk", true);
                this.transform.position = Vector2.MoveTowards(this.transform.position, this.positionFinal, 5f * Time.deltaTime); //move chicken to Final Position
            }

            this.NoCollisionInsideCircle();

            if (Vector3.Distance(this.transform.position, this.positionFinal) < 0.01f)
            {
                arrived = true;

                //Set Random Rotation
                GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(Random.Range(0f, 360f), 270f, 90f) * 1);

                animator.SetBool("eat", true);
            }
        }
    }

    public void SetChicken(GameObject area, int number, AreaTrialData areaData)
    {
        transform.localScale = new Vector3(areaData.getSizeOfChicken(), areaData.getSizeOfChicken(), areaData.getSizeOfChicken());
        this.area = area;
        this.areaData = areaData;
        this.number = number;

        if (SceneManager.GetActiveScene().name == "ChickenGame_DifferentColors")
        {
            chicken_model.GetComponent<SkinnedMeshRenderer>().material = newMaterialRef[Random.Range(0, newMaterialRef.Length)];
        }

        
    }

    private void NoCollisionInsideCircle()
    {
        float d_x = (this.transform.position.x - area.transform.position.x) * (this.transform.position.x - area.transform.position.x);
        float d_y = (this.transform.position.y - area.transform.position.y) * (this.transform.position.y - area.transform.position.y);

        if (Math.Sqrt(d_x + d_y) <= areaData.getCircleRadius() * 3f)
        {
            GetComponent<Rigidbody>().constraints = RigidbodyConstraints.FreezeAll;
        }
    }
}
