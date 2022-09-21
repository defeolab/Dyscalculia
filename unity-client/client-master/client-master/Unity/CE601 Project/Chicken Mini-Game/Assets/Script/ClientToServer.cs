using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using System.Collections.Generic;

public class ClientToServer : MonoBehaviour
{
    const int port = 65432;

    private readonly StreamReader reader;
    private readonly StreamWriter writer;

    public ClientToServer()
    {
        // Connecting to the server and creating objects for communications
        TcpClient tcpClient = new TcpClient("localhost", port);
        NetworkStream stream = tcpClient.GetStream();
        reader = new StreamReader(stream);
        writer = new StreamWriter(stream);
        writer.AutoFlush = true;
    }

    public Stack<TrialData> GetTrials()
    {
        // Sending command
        writer.WriteLine("TRIALS:");

        string line = reader.ReadLine();
        Debug.Log("GET TRIALS: " + line);

        try
        {
            TrialData[] trials = JsonUtility.FromJson<TrialsArray>("{\"trials\":" + line + "}").trials;
            return new Stack<TrialData>(trials);
        }
        catch (Exception e)
        {
            Debug.Log(e);
        }
        return new Stack<TrialData>();
    }

    public void CompleteTrials()
    {
        TrialsResults results = new TrialsResults(TrialsManager.instance.completedTrialResults);
        String resultsJson = JsonUtility.ToJson(results);

        writer.WriteLine("COMPLETE:" + resultsJson);

        string line = reader.ReadLine();
        TrialsManager.instance.ClearResults();
        if (line != "SUCCESS")
        {
            Debug.Log("Unable to complete trials on server");
        }     
    }

    //Close Connection
    public void Dispose()
    {
        reader.Close();
        writer.Close();
    }  
}



