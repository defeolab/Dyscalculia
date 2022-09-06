using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InitialMenu : MonoBehaviour
{
    public GameObject videoTutorial;
    public GameObject menu;

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
}


