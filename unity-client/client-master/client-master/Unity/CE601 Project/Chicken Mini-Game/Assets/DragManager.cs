using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DragManager : MonoBehaviour
{
    public bool isDragActive_area1 = false;
    public bool isDragActive_area2 = false;
    public bool active = false;
    public bool findDrag1 = false;
    public bool findDrag2 = false;
    private Vector3 screenPosition;
    public Vector3 worldPosition;
    public List<GameObject> draggableChickens1 = new List<GameObject>();
    public List<GameObject> draggableChickens2 = new List<GameObject>();
    public GameObject lastDragged_area1;
    public GameObject lastDragged_area2;
    public GameObject fences;

    void Awake()
    {
        DragManager[] controllers = FindObjectsOfType<DragManager>();
        if (controllers.Length > 1)
        {
            Destroy(gameObject);
        }
    }

    void Update()
    {
        Vector3 mouse = new Vector3(Input.mousePosition.x, Screen.height - Input.mousePosition.y,0);
        Vector2 touch = new Vector2(Screen.width / 2, 0);

        if (Input.touchCount > 0)
        {
            touch = new Vector2(Input.GetTouch(0).position.x, Screen.height - Input.GetTouch(0).position.y);
        }
        
        if (active && (mouse.x < Screen.width / 2 || touch.x < Screen.width / 2))
        {
            //Debug.Log("Mouse is on left side of screen.");

            if (lastDragged_area2 != null)
            {
                foreach(GameObject d_g in draggableChickens2)
                {
                    d_g.transform.position = d_g.GetComponent<Chickens>().positionFinal;
                    d_g.GetComponent<Animator>().SetBool("eat", true);
                }
            }

            if (isDragActive_area1 && (Input.GetMouseButtonUp(0) || (Input.touchCount == 1 && Input.GetTouch(0).phase == TouchPhase.Ended)))
            {
                Drop(1);
                return;
            }

            if (Input.GetMouseButton(0))
            {
                Vector3 mousePos = Input.mousePosition;
                screenPosition = new Vector3(mousePos.x, mousePos.y, 0);
            }
            else if (Input.touchCount > 0)
            {
                screenPosition = Input.GetTouch(0).position;
            }
            else
            {
                return;
            }

            worldPosition = Camera.main.ScreenToWorldPoint(screenPosition);

            if (isDragActive_area1)
            {
                Drag(1);
            }
            else
            {
                if (findDrag1)
                {
                    InitDrag(1);
                }
            }
        }

        if (active && (mouse.x > Screen.width / 2 || touch.x > Screen.width / 2))
        {
            //Debug.Log("Mouse is on right side of screen.");

            if (lastDragged_area1 != null)
            {
                foreach (GameObject d_g in draggableChickens1)
                {
                    d_g.transform.position = d_g.GetComponent<Chickens>().positionFinal;
                    d_g.GetComponent<Animator>().SetBool("eat", true);
                }
            }

            if (isDragActive_area2 && (Input.GetMouseButtonUp(0) || (Input.touchCount == 1 && Input.GetTouch(0).phase == TouchPhase.Ended)))
            {
                Drop(2);
                return;
            }

            if (Input.GetMouseButton(0))
            {
                Vector3 mousePos = Input.mousePosition;
                screenPosition = new Vector3(mousePos.x, mousePos.y, 0);

            }
            else if (Input.touchCount > 0)
            {
                screenPosition = Input.GetTouch(0).position;
            }
            else
            {
                return;
            }

            worldPosition = Camera.main.ScreenToWorldPoint(screenPosition);

            if (isDragActive_area2)
            {
                Drag(2);
            }
            else
            {
                if (findDrag2)
                {
                    InitDrag(2);
                }
            }
        }
    }

    void InitDrag(int a)
    {
        if (a == 1)
        {
            isDragActive_area1 = true;
        }
        else if (a == 2)
        {
            isDragActive_area2 = true;
        }
    }

    void Drag(int a)
    {
        if (a == 1)
        {
            lastDragged_area1.transform.position = new Vector3(worldPosition.x, worldPosition.y, 0);
            lastDragged_area1.GetComponent<Animator>().SetBool("eat", false);
        }
        else if (a == 2)
        {
            lastDragged_area2.transform.position = new Vector3(worldPosition.x, worldPosition.y, 0);
            lastDragged_area2.GetComponent<Animator>().SetBool("eat", false);
        }      
    }

    void Drop(int a)
    {
        if(a == 1)
        {
            isDragActive_area1 = false;
            findDrag1 = false;
            CheckPositionHay(1);
        }
        else if (a == 2)
        {
            isDragActive_area2 = false;
            findDrag2 = false;
            CheckPositionHay(2);
        }
    }

    private void CheckPositionHay(int a)
    {

        if (a == 1)
        {
            if (draggableChickens1.Count > 0)
            {
                if (Vector3.Distance(lastDragged_area1.transform.position, gameObject.GetComponent<ErrorTrialManager>().hay_area1_pos) < 0.5f)
                {
                    lastDragged_area1.transform.position = gameObject.GetComponent<ErrorTrialManager>().hay_area1_pos;
                    lastDragged_area1.GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(180f, 270f, 90f));
                    lastDragged_area1.GetComponent<Chickens>().errorStarted = false;
                    draggableChickens1.Remove(lastDragged_area1);

                    if (draggableChickens1.Count != 0) gameObject.GetComponent<ErrorTrialManager>().ActiveHays(a);
                }
                else
                {
                    lastDragged_area1.transform.position = lastDragged_area1.GetComponent<Chickens>().positionFinal;
                    lastDragged_area1.GetComponent<Animator>().SetBool("eat", true);
                }
            }

        }
        else if (a == 2)
        {
            if (draggableChickens2.Count > 0)
            {
                if (Vector3.Distance(lastDragged_area2.transform.position, gameObject.GetComponent<ErrorTrialManager>().hay_area2_pos) < 0.5f)
                {
                    lastDragged_area2.transform.position = gameObject.GetComponent<ErrorTrialManager>().hay_area2_pos;
                    lastDragged_area2.GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(0f, 270f, 90f));
                    lastDragged_area2.GetComponent<Chickens>().errorStarted = false;
                    draggableChickens2.Remove(lastDragged_area2);

                    if (draggableChickens2.Count != 0) gameObject.GetComponent<ErrorTrialManager>().ActiveHays(a);
                }
                else
                {
                    lastDragged_area2.transform.position = lastDragged_area2.GetComponent<Chickens>().positionFinal;
                    lastDragged_area2.GetComponent<Animator>().SetBool("eat", true);
                }
            }
        }
    }
}
