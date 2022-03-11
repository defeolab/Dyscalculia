using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using System.Collections.Generic;

public class Client : IDisposable
{
    const int port = 65432;

    private readonly StreamReader reader;
    private readonly StreamWriter writer;

    public Client()
    {
        // Connecting to the server and creating objects for communications
        TcpClient tcpClient = new TcpClient("localhost", port);
        NetworkStream stream = tcpClient.GetStream();
        reader = new StreamReader(stream);
        writer = new StreamWriter(stream);
        writer.AutoFlush = true;
    }

    public GameTrialData GetTrial()
    {
        // Sending command
        writer.WriteLine("TRIAL");

        string line = reader.ReadLine();
        GameTrialData trial = JsonUtility.FromJson<GameTrialData>(line);
        return trial;
    }

    public Stack<GameTrialData> GetTrials()
    {
        // Sending command
        writer.WriteLine("TRIALS:5");

        string line = reader.ReadLine();
        Debug.Log(line);
        try
        {
            GameTrialData[] trials = JsonUtility.FromJson<GameTrials>("{\"trials\":" + line + "}").trials;
            return new Stack<GameTrialData>(trials);
        } catch (Exception e)
        {
            Debug.Log(e);
        }
        return new Stack<GameTrialData>();
    }

    public void CompleteTrials()
    {
        GameTrialResults results = new GameTrialResults(GameManager.instance.completedTrialResults);
        String resultsJson = JsonUtility.ToJson(results);
        writer.WriteLine("COMPLETE:" + resultsJson);

        string line = reader.ReadLine();
        GameManager.instance.clearResults();
        if (line != "SUCCESS")
        {
            Debug.Log("Unable to complete trials on server");
        }
    }
    public void SaveSettings(GameSettingsData settings)
    {
        String settingsJson = JsonUtility.ToJson(settings);
        writer.WriteLine("SETTINGS:" + settingsJson);

        string line = reader.ReadLine();
        if (line != "SUCCESS")
        {
            Debug.Log("Unable to save settings to server");
        }
    }

    public void Dispose()
    {
        reader.Close();
        writer.Close();
    }
}
