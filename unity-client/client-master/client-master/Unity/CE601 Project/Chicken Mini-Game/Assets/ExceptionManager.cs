using System.IO;
using UnityEngine;
public class ExceptionManager : MonoBehaviour
{
    void Awake()
    {
        Application.logMessageReceived += HandleException;
        DontDestroyOnLoad(gameObject);
    }

    void HandleException(string logString, string stackTrace, LogType type)
    {
        if (type == LogType.Exception)
        {
            string[] lines ={logString, stackTrace};
            File.WriteAllLines("Exception.txt", lines);
        }
    }
}