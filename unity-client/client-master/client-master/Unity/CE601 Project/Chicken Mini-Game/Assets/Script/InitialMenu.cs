using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;
using System;

public class InitialMenu : MonoBehaviour
{
    public GameObject videoTutorial, menu, menuIP;        

    public void EnableVideo(bool active)
    {
        videoTutorial.GetComponent<InitialVideo>().enabled = active;
        videoTutorial.SetActive(active);
        menu.SetActive(!active);
    }

    public void ExitGame()
    {
        Application.Quit();
    }

    public void switchMenu(bool flag)
    {
        menu.SetActive(!flag);
        menuIP.SetActive(flag);
    }
}


