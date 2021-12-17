using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;

public class Menu : MonoBehaviour
{
    public GameObject pauseMenu;
    public GameObject settingsMenu;
    public AudioMixer audioMixer;
            
    public void SetVolume(float volume)
    {
        audioMixer.SetFloat("volume", volume);
    }

    public void SetActiveSettingsMenu(bool active)
    {
        pauseMenu.SetActive(!active);
        settingsMenu.SetActive(active);
    }
}
