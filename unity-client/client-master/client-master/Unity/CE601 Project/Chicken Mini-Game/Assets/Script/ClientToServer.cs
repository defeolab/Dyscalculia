using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using System.Collections.Generic;

public class ClientToServer : MonoBehaviour
{
    const int port = 65432;

    const String remote_host = "87.19.52.63";
    const int remote_port = 51831;
    public string lan_host = ""; //REPLACE HERE WITH THE LOCAL IP OF THE LAB PC
    
    private readonly StreamReader reader;
    private readonly StreamWriter writer;

    public ClientToServer(bool remote, bool use_lan, string ip)
    {
        // Connecting to the server and creating objects for communications

        if (use_lan) lan_host = ip; 
        
        TcpClient tcpClient = remote ? new TcpClient(remote_host, remote_port) : use_lan ? new TcpClient(ip, port) : new TcpClient("localhost", port);
        NetworkStream stream = tcpClient.GetStream();
        reader = new StreamReader(stream);
        writer = new StreamWriter(stream);
        writer.AutoFlush = true;
    }

    public void AskTrials()
    {
        // Sending command
        writer.WriteLine("TRIALS:");
    }

    public Stack<TrialData> GetTrials()
    {
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



