/*
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class rotate_forklift : MonoBehaviour
{
    public KeyCode rotateAround;
    public GameObject c;
    // Start is called before the first frame update
    void Start()
    {

    }
    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(rotateAround))
        {
            c.transform.rotation = Quaternion.Euler(0, c.transform.localRotation.eulerAngles.y + 270, 0);
        }

    }
}
*/


using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class rotate_forklift : MonoBehaviour
{
    public KeyCode rotateAround;
    public GameObject Forklift;
    public bool flag = false;
    private float y_value;
    // Start is called before the first frame update
    void Start()
    {
    }
    
    // Update is called once per frame
    void Update()
    {   

        if (Input.GetKeyDown(rotateAround))
        {
            flag = true;
            y_value = this.transform.localRotation.eulerAngles.y;
            if (y_value >= 180 ){
                y_value = ((y_value + 180) % 360);
            }
            else{
                y_value = y_value + 180;
            }
            //Forklift.transform.rotation = Quaternion.Euler(0, Forklift.transform.localRotation.eulerAngles.y + 270, 0);
        }
        
        if (flag == true){
            this.transform.Rotate(new Vector3(0f,0.5f,0f),0.08f); 
            
            if (this.transform.localRotation.eulerAngles.y >= y_value - 2 && this.transform.localRotation.eulerAngles.y < y_value + 2){
                flag = false;
            }
        }

    }
}
