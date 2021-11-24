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
        if (startWalk && !arrived)
        {
            animator.SetBool("walk", true);
            this.transform.position = Vector2.MoveTowards(this.transform.position, this.positionFinal, 5f * Time.deltaTime);
        }

        if ((Vector3.Distance(this.transform.position, this.positionFinal) < 0.001f)&&!arrived)
        {
            startWalk = false;
            arrived = true;
            transform.Rotate(Random.Range(0,360), 180, 0, Space.World);
            animator.SetBool("eat", true);
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
