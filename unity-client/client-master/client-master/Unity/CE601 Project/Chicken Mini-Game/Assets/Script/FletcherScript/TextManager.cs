using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

/*
 @Author: Fletcher Hurn (1806938)
 */
public class TextManager : MonoBehaviour
{
    private bool chickensReady = false;

    public Text gameText;
    public Text correctText;
    public Text incorrectText;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (GameManager.instance.chickensReady && !chickensReady)
        {
            chickensReady = true;
            gameText.text = "Please now select the area which has the most chickens";
        }
        correctText.text = "Correct: " + GameManager.instance.correctCount;
        incorrectText.text = "Incorrect: " + GameManager.instance.incorrectCount;
    }
}
