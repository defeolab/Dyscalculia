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
        if (this.startWalk)
        {
            animator.SetBool("walk", true);
            this.transform.position = Vector2.MoveTowards(this.transform.position, this.positionFinal, 5f * Time.deltaTime);
            
            //GetComponent<Rigidbody>().MovePosition((this.positionFinal + transform.position) * 0.5f * Time.deltaTime);
        }

        if (Vector3.Distance(this.transform.position, this.positionFinal) < 0.001f)
        {
            startWalk = false;
            arrived = true;
            animator.SetBool("eat", true);
        }
        /*if (this.startWalk)
        {
            float step = 5.0f * Time.deltaTime; // calculate distance to move
            this.transform.position = Vector2.MoveTowards(this.transform.position, this.positionFinal, step);

            if (Vector3.Distance(this.transform.position, this.positionFinal) < 0.01f)
            {
                startWalk = false;
                arrived = true;
                //gameObject.GetComponent<Rigidbody>().constraints = RigidbodyConstraints.FreezeAll;

            //fare rigidybody solo su fence e poi dopo su polli
            }
        }*/
    }

        public void SetChicken(GameObject area, int number, AreaTrialData areaData)
    {
        transform.localScale = new Vector3(
                areaData.getSizeOfChicken(),
                areaData.getSizeOfChicken(),
                areaData.getSizeOfChicken());
        this.area = area;
        this.areaData = areaData;
        this.number = number;        
    }

    IEnumerator FreezAll()
    {
        yield return new WaitForSeconds(1f);
        GetComponent<Rigidbody>().constraints = RigidbodyConstraints.FreezeAll;
        

    }

   /* void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.tag == "Chicken")
        {
            Physics.IgnoreCollision(collision.collider, this.GetComponent<Collision>().collider);
        }
    }*/

        /*public Transform[] waypoints;
        public float moveSpeed = 2f;
        public Animator animator;

        public int waypointIndex = 0;

        private float waitTime;
        private int area;

        Vector2 movement;

        // Start is called before the first frame update
        void Start()
        {
            waitTime = Random.Range(0, 5);
        }

        // Update is called once per frame
        void Update()
        {
            animator.SetFloat("Horizontal", movement.x);
            animator.SetFloat("Vertical", movement.y);
            animator.SetFloat("Speed", movement.sqrMagnitude);
        }

        //Executed 50 time per second independant of frame rate
        void FixedUpdate()
        {
            if (this.waypointIndex != waypoints.Length && Time.realtimeSinceStartup > waitTime && TrialsManager.instance.gameStarted)
            {
                Move();
            }
        }

        public bool isReady()
        {
            return transform.position == waypoints[waypoints.Length - 1].transform.position;
        }

        public void setLastWaypoint(Transform waypoint)
        {
            waypoints[waypoints.Length - 1] = waypoint;
            area = waypoint.position.x < 0 ? 1 : 2;
        }

        private void Move()
        {
            transform.position = Vector2.MoveTowards(transform.position, waypoints[waypointIndex].transform.position, moveSpeed * Time.deltaTime);

            if (transform.position.x < waypoints[waypointIndex].transform.position.x)
            {
                movement.x = 1;
            }
            else if (transform.position.x > waypoints[waypointIndex].transform.position.x)
            {
                movement.x = -1;
            }
            else
            {
                movement.x = 0;
            }

            if (transform.position.y < waypoints[waypointIndex].transform.position.y)
            {
                movement.y = 1;
            }
            else if (transform.position.y > waypoints[waypointIndex].transform.position.y)
            {
                movement.y = -1;
            }
            else
            {
                movement.y = 0;
            }

            if (transform.position == waypoints[waypointIndex].transform.position)
            {
                waypointIndex += 1;
                movement.x = 0;
                movement.y = 0;
            }
        }

        public int getArea()
        {
            return area;
        }

        public void Reset()
        {
            transform.position = new Vector3(-0.6577309f, 4.202539f);
        }*/
    }
