using System;
using System.Collections;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using UnityEngine.Networking;

public class BeatSaberBlockSpawner : MonoBehaviour
{
    public GameObject redBlockPrefab;
    public GameObject blueBlockPrefab;
    public GameObject bombBlockPrefab;
    public Transform spawnPoint;

    public float horizontalSpacing = 2.0f;
    public float verticalSpacing = 2.0f;

    public string beatMapFilePath;

    public float bpm = 105;

    public float noteJumpMovementSpeed = 10f;
    public float noteJumpStartBeatOffset = 1f;

    // C:\Users\Sam\Documents\Beat Saber\Beat Saber\Assets\Beat Saber_Regular Intervals(slow)_Aespa Dreams Come True_PANNED.wav
    public string filePath;

    private void Start()
    {
        // initialize tcp connection (this is the server/sender)
        // send start packet to client - client begins playing music
        // StartCoroutine(TCP());
        // TCP();

        StartCoroutine(Initialize());
    }
// 2021.3.16
    // private IEnumerator TCP()
    // {
    //     string serverIp = "127.0.0.1"; 
    //     int serverPort = 8080; 
    //     TcpClient client = null;
    //     NetworkStream stream = null;


    //     client = new TcpClient(serverIp, serverPort);
    //     stream = client.GetStream();
    //     // Convert the string message to bytes
    //     byte[] data = Encoding.UTF8.GetBytes(filePath);

    //     // Send the data over the network stream
    //     stream.Write(data, 0, data.Length);

    //     Debug.Log($"Sent: {filePath}");
    //     yield return StartCoroutine(Initialize(stream));

    
    //     // Ensure that we properly close the client and stream, even if an exception occurs
    //     stream?.Close();
    //     client?.Close();
        


    //     // using (TcpClient client = new TcpClient(serverIp, serverPort))
    //     // {
    //     //     using (NetworkStream stream = client.GetStream())
    //     //     {
    //     //         // Convert the string message to bytes
    //     //         byte[] data = Encoding.UTF8.GetBytes(filePath);

    //     //         // Send the data over the network stream
    //     //         stream.Write(data, 0, data.Length);

    //     //         Debug.Log($"Sent: {filePath}");
    //     //         StartCoroutine(Initialize(stream));

    //     //     }
    //     // }

    // }

    private IEnumerator Initialize()
    {
        string path = Path.Combine(Application.streamingAssetsPath, beatMapFilePath);
        yield return StartCoroutine(ReadFileFromStreamingAssets(path, (jsonString) =>
        {
            if (!string.IsNullOrEmpty(jsonString))
            {
                BeatSaberMapData mapData = JsonUtility.FromJson<BeatSaberMapData>(jsonString);
                StartCoroutine(SpawnBlocks(mapData));
            }
        }));
    }

    private IEnumerator ReadFileFromStreamingAssets(string filePath, System.Action<string> onComplete)
    {
        if (string.IsNullOrEmpty(filePath))
        {
            Debug.LogError("File path is empty or null.");
            onComplete?.Invoke(null);
            yield break;
        }

        using (UnityWebRequest www = UnityWebRequest.Get(filePath))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error reading file: " + www.error);
                onComplete?.Invoke(null);
            }
            else
            {
                onComplete?.Invoke(www.downloadHandler.text);
            }
        }
    }

    private IEnumerator SpawnBlocks(BeatSaberMapData mapData)
    {
        string serverIp = "127.0.0.1"; 
        int serverPort = 8080; 
        TcpClient client = null;
        NetworkStream stream = null;


        client = new TcpClient(serverIp, serverPort);
        stream = client.GetStream();

        float startTime = Time.time;

        foreach (BeatSaberBlockData blockData in mapData._notes)
        {
            float targetTime = (blockData._time / bpm) * 60;


            float timeToWait = targetTime - (Time.time - startTime)+ noteJumpStartBeatOffset;

            if (timeToWait > 0)
            {
                yield return new WaitForSeconds(timeToWait);
            }
            
            byte[] data = Encoding.UTF8.GetBytes($"targetTime: {targetTime}");
            stream.Write(data, 0, data.Length);
            Debug.Log($"Sent: {filePath}");

            SpawnBlock(blockData);
        }
        // Ensure that we properly close the client and stream, even if an exception occurs
        stream?.Close();
        client?.Close();
    }

    private void SpawnBlock(BeatSaberBlockData blockData)
    {
        Debug.Log("SPAWN " + blockData._time + "-" + blockData._type);

        GameObject blockPrefab = null;

        switch (blockData._type)
        {
            case (int)BeatSaberBlockType.Red:
                blockPrefab = redBlockPrefab;
                break;
            case (int)BeatSaberBlockType.Blue:
                blockPrefab = blueBlockPrefab;
                break;
            case (int)BeatSaberBlockType.Bomb:
                blockPrefab = bombBlockPrefab;
                break;
            default:
                Debug.LogError("Unknown block type: " + blockData._type);
                return;
        }

        Vector3 spawnPosition = spawnPoint.position;
        spawnPosition.x += blockData._lineIndex * horizontalSpacing;
        spawnPosition.y += blockData._lineLayer * verticalSpacing;
        spawnPosition.z = 15;

        Debug.Log("spawnposition:" + spawnPosition);

        GameObject blockInstance = Instantiate(blockPrefab, spawnPosition, Quaternion.identity);

        BlockController blockController = blockInstance.GetComponent<BlockController>();
        blockController.Initialize(blockData);
    }

    [System.Serializable]
    public class BeatSaberMapData
    {
        public BeatSaberBlockData[] _notes;
    }

    [System.Serializable]
    public class BeatSaberBlockData
    {
        public float _time;
        public int _lineIndex;
        public int _lineLayer;
        public int _type;
        public int _cutDirection;
    }


    public enum BeatSaberBlockType
    {
        Red, Blue, Bomb
    };
}

