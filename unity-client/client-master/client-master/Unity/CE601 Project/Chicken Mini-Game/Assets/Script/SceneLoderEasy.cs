using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneLoderEasy : MonoBehaviour
{
    // Start is called before the first frame update
    public void LoadSceneEasy()
    {
        SceneManager.LoadScene("symbolicWithAnimationEasy");
    }
}
