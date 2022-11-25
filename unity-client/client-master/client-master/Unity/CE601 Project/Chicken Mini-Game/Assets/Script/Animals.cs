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

public class Animals : MonoBehaviour
{
    public GameObject area;
    public GameObject animalModel;
    public Material[] newMaterialRef;
    public AreaTrialData areaData;
    public Animator animator;
    public DragManager dragManager;
    public Vector3 positionFinal, positionFinalError;
    public int number;
    public bool findFinalPos,startWalk,arrived,errorStarted, setPostionError;

    void Start()
    {
        animator = gameObject.GetComponent<Animator>();
        newMaterialRef = new Material[4];
        startWalk = false;
        arrived = false;
        setPostionError=false;
        newMaterialRef = Resources.LoadAll("Materials", typeof(Material)).Cast<Material>().ToArray();
    }

    void Update()
    {
        if (!arrived)
        {
            if (startWalk)
            {
                animator.SetBool("walk", true);
                this.transform.position = Vector2.MoveTowards(this.transform.position, this.positionFinal, 5f * Time.deltaTime); //move animal to Final Position
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

        if (errorStarted)
        {
            if (area.name == "Area1")
            {
                var distanceBetween = Vector2.Distance(dragManager.worldPosition, this.transform.position);

                if (distanceBetween < 1f)
                {
                    dragManager.findDrag1 = true;
                    dragManager.draggedArea1 = gameObject;
                }
            }
            else if (area.name == "Area2")
            {
                var distanceBetween = Vector2.Distance(dragManager.worldPosition, this.transform.position);

                if (distanceBetween < 1f)
                {
                    dragManager.findDrag2 = true;
                    dragManager.draggedArea2 = gameObject;
                }
            }
        }

        if (setPostionError)
        {
            this.transform.position = positionFinalError;
            animator.SetBool("eat", false);
        }

    }

    public void SetAnimal(GameObject area, int number, AreaTrialData areaData)
    {
        transform.localScale = new Vector3(areaData.getSizeOfAnimal(), areaData.getSizeOfAnimal(), areaData.getSizeOfAnimal());
        this.area = area;
        this.areaData = areaData;
        this.number = number;

        //Random prototype for scene on distraction with materials
        if (SceneManager.GetActiveScene().name == "TwoFences_DifferentColors")
        {
            animalModel.GetComponent<SkinnedMeshRenderer>().material = newMaterialRef[Random.Range(0, newMaterialRef.Length)];
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

    public void setAnimalError(int a, Vector3 position, float size)
    {
        if (a == 1)
        {
            this.transform.position = position;
            GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(0f, 270f, 90f));
            this.transform.localScale = new Vector3(size, size, size);
            animator.SetBool("eat", false);
            this.errorStarted = false;
            this.setPostionError = true;
            positionFinalError = position;


        }
        else if(a == 2)
        {
            this.transform.position = position;
            GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(180f, 270f, 90f));
            this.transform.localScale = new Vector3(size, size, size);
            animator.SetBool("eat", false);
            this.errorStarted = false;
            this.setPostionError = true;
            positionFinalError = position;
        }
        else if (a == 0)
        {
            errorStarted = true;
            animator.SetBool("walk", false);
        }
    }

    public void setTensAnimal(int a, float size)
    {
        if (a == 1) 
        {
            transform.position = new Vector3(-4, 7, 0);
            GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(0f, 270f, 90f));
        }
        else if (a == 2)
        {
            transform.position = new Vector3(4, 7, 0);
            GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(180f, 270f, 90f));
        }

        animator.SetBool("walk", false);
        animator.SetBool("eat", false);
        animalModel.GetComponent<SkinnedMeshRenderer>().material = newMaterialRef[0];
        this.transform.localScale = new Vector3(size, size, size);
    }

    public void setSliderAnimal(int a)
    {
        if (a == 1)
        {
            transform.position = new Vector3(-1.21f, -4.25f, 0f);
            transform.rotation = Quaternion.Euler(new Vector3(-90f, 270f, 90f));
            animator.SetBool("walk", true);
            errorStarted = false;
        }
        else if(a == 2)
        {
            transform.position = new Vector3(1.21f, -4.25f, 0f);
            transform.rotation = Quaternion.Euler(new Vector3(-90f, 270f, 90f));
            animator.SetBool("walk", true);
            errorStarted = false;
        }
    }
}
