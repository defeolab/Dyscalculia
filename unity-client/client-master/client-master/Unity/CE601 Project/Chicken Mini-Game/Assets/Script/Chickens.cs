using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Chickens : MonoBehaviour
{
    public GameObject area;
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
        startWalk = false;
        arrived = false;
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

            if (Vector3.Distance(this.transform.position, this.positionFinal) < 0.001f)
            {
                arrived = true;

                //Set Random Rotation
                GetComponent<Rigidbody>().constraints = RigidbodyConstraints.FreezeAll;
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
    }
}
