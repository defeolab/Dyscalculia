using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;
using System.Threading;

public class DragDropEasy0_1 : MonoBehaviour
{
    //correct answer
    public GameObject correct_answer;
    public GameObject incorrect_answer;
    public GameObject incorrect_answer_time;
     public GameObject pause_Button;
    public GameObject pause;
    //time....
    public float timeRemaining=0;
    public bool timeIsRunning=true;
    public TMP_Text timeText;
    public GameObject retry_btn;
    public GameObject next_btn;
    //....slider
    public Slider timeSlider;
    public GameObject game_panel;

    Vector3 offset;
    public string destinationTg1 = "Area_left";
    public string destinationTg2 = "area_right";
    List<string> values = new List<string> {"symbolicWithAnimationEasy", "symbolicWithAnimationEasy0_1", "symbolicWithAnimationEasy0_2", "symbolicWithAnimationEasy0_3", "symbolicWithAnimationEasy0_4","symbolicWitDiffSizeEasy"};

    void Start() 
    {
        timeIsRunning=true ;          
        timeSlider.maxValue=timeRemaining;
        timeSlider.value=timeRemaining;
        game_panel.GetComponent<AudioSource>().Play();
    }
    void Update() 
    {
        if(timeIsRunning)
        {
            if(timeRemaining>=0) 
            {
                timeRemaining-=Time.deltaTime;  
                DisplayTime(timeRemaining); 
            }
        }    
    }
    void DisplayTime(float timeToDisplay)
    {
        timeToDisplay-=1;
        float munutes=Mathf.FloorToInt(timeToDisplay / 60);
        float seconds=Mathf.FloorToInt(timeToDisplay % 60);
        if (seconds>=0)
        {
            timeSlider.value=seconds;
            timeText.text = string.Format("{0:00} : {1:00}", munutes, seconds);
            if (seconds==0)
            {
                incorrect_answer_time.SetActive(true);
                incorrect_answer_time.GetComponent<AudioSource>().Play();
            }
        }
    }
    public void Pause()
    {
        pause.SetActive(true);
    }
    void OnMouseDown() 
    {
        offset = transform.position-GetMouseWorldPosition(); 
        transform.GetComponent<Collider>().enabled=false;   
    }
    void OnMouseDrag() 
    {
        transform.position=GetMouseWorldPosition() + offset;   
    }
    void OnMouseUp()
    {
        var rayOrigin = Camera.main.transform.position;
        var rarDirection =GetMouseWorldPosition()-Camera.main.transform.position;
        RaycastHit hitInfo;
        if(Physics.Raycast(rayOrigin,rarDirection,out hitInfo))
        {
            if(timeRemaining>2){
            if (hitInfo.transform.tag==destinationTg1)
            {
                transform.position=hitInfo.transform.position;
               
                timeIsRunning=false ;
                incorrect_answer.SetActive(true);
                incorrect_answer.GetComponent<AudioSource>().Play();
            }else if(hitInfo.transform.tag==destinationTg2) {
                transform.position=hitInfo.transform.position;

                timeIsRunning=false ;
                correct_answer.SetActive(true);
                correct_answer.GetComponent<AudioSource>().Play();
                
            } else {
                
            }
        }
        transform.GetComponent<Collider>().enabled=true;   
        }
    }
    private Vector3 GetMouseWorldPosition()
    {
        Vector3 mouseScreenPos = Input.mousePosition;
        mouseScreenPos.z = Camera.main.WorldToScreenPoint(transform.position).z;
        return Camera.main.ScreenToWorldPoint(mouseScreenPos);
    }
    public void Retry () {
        SceneManager.LoadScene("symbolicWithAnimationEasy0_1");
    }
        public void Next () {
        int randomNumber = Random.Range(0, 4);
        string nxt_pg = values[randomNumber];
        SceneManager.LoadScene(nxt_pg);
    }
    public void Exit () {
        SceneManager.LoadScene("Start");
    }
}
