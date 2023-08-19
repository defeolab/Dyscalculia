using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;
using System;
using UnityEngine.SceneManagement;

public class InitialMenu : MonoBehaviour
{
    public GameObject videoTutorial, menu, menuIP,GameMenu;        

    public void EnableVideo(bool active)
    {
        videoTutorial.GetComponent<InitialVideo>().enabled = active;
        videoTutorial.SetActive(active);
        menu.SetActive(!active);
    }

    public void ExitGame()
    {
       SceneManager.LoadScene("Start");
    }

    public void switchMenu(bool flag)
    {
        menu.SetActive(!flag);
        menuIP.SetActive(flag);
    }
    public void GameMenufun()
    {
        GameMenu.SetActive(true);
    }

}


