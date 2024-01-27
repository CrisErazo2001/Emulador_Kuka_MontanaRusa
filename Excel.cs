using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Http;
using System;
using System.IO;
using System.Threading;
using UnityEngine.SceneManagement;


public class Excel : MonoBehaviour
{
    Rigidbody rb;
    int entero;
    float currentTime;
    double lastTime = 0f;
    double lastTimeF = 0f;
    double lastTimeF2 = 0f;
    public Timer timer1second;
    string docPath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        print(rb.name);
        Invoke("WaitToEnd", 77);
    }

    // Update is called once per frame
    void Update()
    {
        currentTime = Time.time;
    
        entero = (int)lastTime;
        lastTimeF = (double)entero + 0.333;
        lastTimeF2 = (double)entero + 0.666;

        if (Math.Round(currentTime, 2) == entero)
        {
            using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "Velocidad7.txt"), true))
            {
                outputFile.WriteLine(currentTime.ToString() + "=> " + rb.velocity);
            }
            using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "Posicion7.txt"), true))
            {
                outputFile.WriteLine(currentTime.ToString() + "=> " + rb.position);
            }
            using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "Rotacion7.txt"), true))
            {
                outputFile.WriteLine(currentTime.ToString() + "=> " + rb.rotation.eulerAngles);
            }
        }

        if (Math.Round(currentTime,2) == Math.Round(lastTimeF, 2)) 
        {
            using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "Velocidad7.txt"), true))
            {
                outputFile.WriteLine(currentTime.ToString() + "=> " + rb.velocity);
            }
            using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "Posicion7.txt"), true))
            {
                outputFile.WriteLine(currentTime.ToString() + "=> " + rb.position);
            }
            using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "Rotacion7.txt"), true))
            {
                outputFile.WriteLine(currentTime.ToString() + "=> " + rb.rotation.eulerAngles);
            }
        }

        if (Math.Round(currentTime, 2) == Math.Round(lastTimeF2, 2))
        {
            using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "Velocidad7.txt"), true))
            {
                outputFile.WriteLine(currentTime.ToString() + "=> " + rb.velocity);
            }
            using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "Posicion7.txt"), true))
            {
                outputFile.WriteLine(currentTime.ToString() + "=> " + rb.position);
            }
            using (StreamWriter outputFile = new StreamWriter(Path.Combine(docPath, "Rotacion7.txt"), true))
            {
                outputFile.WriteLine(currentTime.ToString() + "=> " + rb.rotation.eulerAngles);
            }
        }

        lastTime = currentTime;
    }
    public void WaitToEnd()
    {
        SceneManager.LoadScene("Fin"); 
    }

}
