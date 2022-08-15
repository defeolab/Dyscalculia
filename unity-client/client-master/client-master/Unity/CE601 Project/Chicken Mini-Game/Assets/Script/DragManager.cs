﻿using System;
using System.Collections.Generic;
using UnityEngine;

public class DragManager : MonoBehaviour
{
    public bool isDragActive_area1 = false, isDragActive_area2 = false;
    public bool active = false;
    public bool findDrag1 = false, findDrag2 = false;
    private Vector3 screenPosition;
    public Vector3 worldPosition;
    public List<GameObject> draggableAnimals1 = new List<GameObject>();
    public List<GameObject> draggableAnimals2 = new List<GameObject>();
    public GameObject draggedArea1, draggedArea2;
    public Collider colliderArea1, colliderArea2;

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

            if (draggedArea2 != null)
            {
                foreach(GameObject d_g in draggableAnimals2)
                {
                    d_g.transform.position = d_g.GetComponent<Animals>().positionFinal;
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

            if (draggedArea1 != null)
            {
                foreach (GameObject d_g in draggableAnimals1)
                {
                    d_g.transform.position = d_g.GetComponent<Animals>().positionFinal;
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

    public void Reset()
    {
        draggableAnimals1.Clear();
        draggableAnimals2.Clear();
        isDragActive_area1 = false;
        isDragActive_area2 = false;
        active = false;
        findDrag1 = false;
        findDrag2 = false;
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
            draggedArea1.transform.position = new Vector3(worldPosition.x, worldPosition.y, 0);
            draggedArea1.GetComponent<Animator>().SetBool("eat", false);
        }
        else if (a == 2)
        {
            draggedArea2.transform.position = new Vector3(worldPosition.x, worldPosition.y, 0);
            draggedArea2.GetComponent<Animator>().SetBool("eat", false);
        }      
    }

    void Drop(int a)
    {
        if(a == 1)
        {
            isDragActive_area1 = false;
            findDrag1 = false;
            CheckPosition(1);
        }
        else if (a == 2)
        {
            isDragActive_area2 = false;
            findDrag2 = false;
            CheckPosition(2);
        }
    }

    private void CheckPosition(int a)
    {
        if (a == 1)
        {
            if (colliderArea1.bounds.Contains(draggedArea1.transform.position))
            {
                draggedArea1.transform.position = draggedArea1.GetComponent<Animals>().positionFinal;
                draggedArea1.GetComponent<Animals>().errorStarted = false;
                draggedArea1.SetActive(false);
                draggableAnimals1.Remove(draggedArea1);

                gameObject.GetComponent<ErrorTrialManager>().IncreaseSlider(colliderArea1,1);
            }
            else
            {
                draggedArea1.transform.position = draggedArea1.GetComponent<Animals>().positionFinal;
                draggedArea1.GetComponent<Animator>().SetBool("eat", true);
            }
        }
        else if (a == 2)
        {
            if (colliderArea2.bounds.Contains(draggedArea2.transform.position))
            {
                draggedArea2.transform.position = draggedArea2.GetComponent<Animals>().positionFinal;
                draggedArea2.GetComponent<Animals>().errorStarted = false;
                draggedArea2.SetActive(false);
                draggableAnimals2.Remove(draggedArea1);

                gameObject.GetComponent<ErrorTrialManager>().IncreaseSlider(colliderArea2, 2);
            }
            else
            {
                draggedArea2.transform.position = draggedArea2.GetComponent<Animals>().positionFinal;
                draggedArea2.GetComponent<Animator>().SetBool("eat", true);
            }
        }

    }

    public void CheckPositionHay(int a)
    {

        if (a == 1)
        {
            if (draggableAnimals1.Count > 0)
            {
                if (Vector3.Distance(draggedArea1.transform.position, gameObject.GetComponent<ErrorTrialManager>().hay_area1_pos) < 0.5f)
                {
                    draggedArea1.transform.position = gameObject.GetComponent<ErrorTrialManager>().hay_area1_pos;
                    draggedArea1.GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(180f, 270f, 90f));
                    draggedArea1.GetComponent<Animals>().errorStarted = false;
                    draggableAnimals1.Remove(draggedArea1);

                    if (draggableAnimals1.Count != 0) gameObject.GetComponent<ErrorTrialManager>().ActiveHays(a);
                }
                else
                {
                    draggedArea1.transform.position = draggedArea1.GetComponent<Animals>().positionFinal;
                    draggedArea1.GetComponent<Animator>().SetBool("eat", true);
                }
            }

        }
        else if (a == 2)
        {
            if (draggableAnimals2.Count > 0)
            {
                if (Vector3.Distance(draggedArea2.transform.position, gameObject.GetComponent<ErrorTrialManager>().hay_area2_pos) < 0.5f)
                {
                    draggedArea2.transform.position = gameObject.GetComponent<ErrorTrialManager>().hay_area2_pos;
                    draggedArea2.GetComponent<Rigidbody>().rotation = Quaternion.Euler(new Vector3(0f, 270f, 90f));
                    draggedArea2.GetComponent<Animals>().errorStarted = false;
                    draggableAnimals2.Remove(draggedArea2);

                    if (draggableAnimals2.Count != 0) gameObject.GetComponent<ErrorTrialManager>().ActiveHays(a);
                }
                else
                {
                    draggedArea2.transform.position = draggedArea2.GetComponent<Animals>().positionFinal;
                    draggedArea2.GetComponent<Animator>().SetBool("eat", true);
                }
            }
        }
    }
}