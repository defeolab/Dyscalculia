using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class StoreIPAddress : MonoBehaviour
{
    public GameObject inputField_IP, inputField_Trials;
    public static StoreIPAddress instance = null;
    public string ipAddress = "10.10.10";
    public int numTrials = 1;

    // Update is called once per frame

    void Start()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Return))
        {
            Store();
        }
    }

    public void Store()
    {
        ipAddress = inputField_IP.GetComponent<Text>().text;
        int.TryParse(inputField_Trials.GetComponent<Text>().text, out numTrials);
    }
}
