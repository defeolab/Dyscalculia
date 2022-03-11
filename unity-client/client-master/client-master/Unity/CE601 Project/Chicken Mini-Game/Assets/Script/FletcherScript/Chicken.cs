using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*
 @Author: Fletcher Hurn (1806938)
 */
public class Chicken : MonoBehaviour
{

    public Transform[] waypoints;
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
        if (this.waypointIndex != waypoints.Length && Time.realtimeSinceStartup > waitTime && GameManager.instance.gameStarted)
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
        } else if (transform.position.x > waypoints[waypointIndex].transform.position.x)
        {
            movement.x = -1;
        } else
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
    }
}
