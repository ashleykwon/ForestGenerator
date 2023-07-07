using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using System.IO;
using System.Text;
using System.Linq;
using System;
using TMPro;

public class TreeSubPrefabGenerator : MonoBehaviour
{


    public GameObject stem;
	public GameObject branch;
	public Transform spawnPos;
	public TextMeshProUGUI paperName;
	
	private readonly string url = "your url here";

	public int numPublications = 5;

	// Start is called before the first frame update
    void Start()
    {
		Instantiate(stem, stem.transform.position, spawnPos.rotation);
        GenerateTrees();
    }

	//get the number of publication for an author
	//make a spawnee and get its position
	//make the spawnee's branch
	//copy the branch for the number of publication times and rotate the copied branch around the spawnee

	private void GenerateTrees(){
		float radius = 0.5f;
		// radius *= 40;
		for (int i = 0; i < numPublications; i++)
		{
			float angle = i * 360 / numPublications; //numTrees*100 is added to prevent trees from overlapping too much
			// Debug.Log(angle);
			float newX = stem.transform.position.x + Mathf.Cos(angle)*radius;
			float newZ = stem.transform.position.z + Mathf.Sin(angle)*radius;
			
			float rotationY = spawnPos.rotation.y + i * 360 / numPublications;
			paperName.text = "hello";
			// Debug.Log("Radius test - many level tree");
			// Debug.Log(Math.Pow(radius, 2));
			// Debug.Log(Math.Pow(Mathf.Sin(angle)*radius,2) + Math.Pow(Mathf.Sin(angle)*radius, 2));
			Vector3 newPos = new Vector3(newX, 0, newZ);
			Quaternion newRot =  Quaternion.Euler(spawnPos.rotation.x, rotationY, spawnPos.rotation.z);
			Instantiate(branch, newPos, newRot);
		}
	}        
	
}
