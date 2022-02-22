using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using UnityEngine.Video;
using UnityEngine.Audio;

public class Video : MonoBehaviour
{
    public VideoPlayer vid;
    private bool isplaying;
    public AudioMixer audioMixer;

    // Start is called before the first frame update
    void Start()
    {
        vid.time = 0;
        vid.Play();
        isplaying = true;
    }

    // Update is called once per frame
    void Update()
    {
        if (isplaying)
        {
            vid.loopPointReached += EndReached;
        }
        else
        {
            vid.time = 0;
            vid.Play();
            isplaying = true;
        }

        this.SetLevelAudio();
    }

    void EndReached(UnityEngine.Video.VideoPlayer vp)
    {
        isplaying = false;
        this.GetComponent<Menu>().EnableVideo(false);
        this.GetComponent<Menu>().SetActiveSettingsMenu(true);
    }

    public void SetLevelAudio()
    {
        float valueMixer;
        float valueVideo;
        bool result = audioMixer.GetFloat("volume", out valueMixer);
        if (result)
        {
            valueVideo = (valueMixer + 80) / 80;
            vid.SetDirectAudioVolume(0, valueVideo);
        }
        else
        {
            vid.SetDirectAudioVolume(0, 1);
        }
    }

}
