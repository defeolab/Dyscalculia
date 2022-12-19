using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Video;
using UnityEngine.Audio;
using UnityEngine.SceneManagement;

public class InitialVideo : MonoBehaviour
{
    public VideoPlayer vid;
    private bool isplaying;
    public AudioMixer audioMixer;
    public GameObject loadScene;
    public GameObject skip;

    // Start is called before the first frame update
    void Start()
    {
        vid.url = System.IO.Path.Combine(Application.streamingAssetsPath, "TOTAL.mp4");
        vid.time = 0;
        vid.Play();
        isplaying = true;
        skip.SetActive(true);
    }

    // Update is called once per frame
    void Update()
    {
        if (isplaying)
        {
            vid.loopPointReached += EndReached;
        }

        this.SetLevelAudio();

        if (Input.GetKeyDown(KeyCode.S))
        {
            SkipVideo();
        }
    }

    void EndReached(UnityEngine.Video.VideoPlayer vp)
    {
        isplaying = false;
        this.gameObject.SetActive(false);
        skip.SetActive(false);
        loadScene.SetActive(true);
        loadScene.GetComponent<LoadLevelTwoFences>().enabled = true;
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

    public void SkipVideo()
    {
        isplaying = false;
        this.gameObject.SetActive(false);
        skip.SetActive(false);
        loadScene.SetActive(true);
        loadScene.GetComponent<LoadLevelTwoFences>().enabled = true;
    }
}
