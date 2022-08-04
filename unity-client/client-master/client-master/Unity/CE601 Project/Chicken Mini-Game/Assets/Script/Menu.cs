using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;
using UnityEngine.SceneManagement;

public class Menu : MonoBehaviour
{
    public GameObject pauseMenu;
    public GameObject settingsMenu;
    public GameObject videoTutorial;
    public AudioMixer audioMixer;

    private void Start()
    {
        pauseMenu.SetActive(false);
        settingsMenu.SetActive(false);
        videoTutorial.SetActive(false);
    }

    public void SetVolume(float volume)
    {
        audioMixer.SetFloat("volume", volume);
    }

    public void SetActiveSettingsMenu(bool active)
    {
        pauseMenu.SetActive(!active);
        settingsMenu.SetActive(active);
    }

    public void EnableVideo(bool active)
    {
        
        this.GetComponent<Video>().enabled = active;
        videoTutorial.SetActive(active);
    }

    public void MainMenu()
    {
        SceneManager.LoadScene(0);
    }

}
