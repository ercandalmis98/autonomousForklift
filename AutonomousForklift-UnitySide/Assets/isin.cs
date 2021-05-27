using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class isin : MonoBehaviour
{
    RaycastHit nesne;
    public KeyCode running;
    public KeyCode not_running;
    public GameObject Forklift;
    public bool Parent31_flag = false;
    public bool Parent32_flag = false;
    public bool Parent33_flag = false;
    public bool Parent21_flag = false;
    public bool Parent22_flag = false;
    public bool Parent23_flag = false;
    public bool Parent11_flag = false;
    public bool Parent12_flag = false;
    public bool Parent13_flag = false;
    private bool loop_flag = false;
    private bool assigned = false;

    void Update()
    {
        if (Input.GetKeyDown(running))
        {
            loop_flag = true;
        }

        if (Input.GetKeyDown(not_running)){
            loop_flag = false;
        }

        if (loop_flag == true){
            if ( Physics.Raycast(transform.position,transform.forward,out nesne,1f) ) {
                if (nesne.collider.gameObject.tag == "P31"){
                    nesne.collider.gameObject.transform.parent.parent = Forklift.transform;
                }

                if (nesne.collider.gameObject.tag == "P32"){
                    nesne.collider.gameObject.transform.parent.parent = Forklift.transform;
                }

                if (nesne.collider.gameObject.tag == "P33"){
                    nesne.collider.gameObject.transform.parent.parent = Forklift.transform;
                }

                if (nesne.collider.gameObject.tag == "P21"){
                    nesne.collider.gameObject.transform.parent.parent = Forklift.transform;
                }

                if (nesne.collider.gameObject.tag == "P22"){
                    nesne.collider.gameObject.transform.parent.parent = Forklift.transform;
                }

                if (nesne.collider.gameObject.tag == "P23"){
                    nesne.collider.gameObject.transform.parent.parent = Forklift.transform;
                }

                if (nesne.collider.gameObject.tag == "P11"){
                    nesne.collider.gameObject.transform.parent.parent = Forklift.transform;
                }

                if (nesne.collider.gameObject.tag == "P12"){
                    nesne.collider.gameObject.transform.parent.parent = Forklift.transform;
                }

                if (nesne.collider.gameObject.tag == "P13"){
                    nesne.collider.gameObject.transform.parent.parent = Forklift.transform;
                }
            }
        }
        else{
            if ( Physics.Raycast(transform.position,transform.forward,out nesne,1f) ) {
                if (nesne.collider.gameObject.tag == "P31"){
                    nesne.collider.gameObject.transform.parent.parent = null;
                }
                if (nesne.collider.gameObject.tag == "P32"){
                    nesne.collider.gameObject.transform.parent.parent = null;
                }

                if (nesne.collider.gameObject.tag == "P33"){
                    nesne.collider.gameObject.transform.parent.parent = null;
                }

                if (nesne.collider.gameObject.tag == "P21"){
                    nesne.collider.gameObject.transform.parent.parent = null;
                }

                if (nesne.collider.gameObject.tag == "P22"){
                    nesne.collider.gameObject.transform.parent.parent = null;
                }

                if (nesne.collider.gameObject.tag == "P23"){
                    nesne.collider.gameObject.transform.parent.parent = null;
                }

                if (nesne.collider.gameObject.tag == "P11"){
                    nesne.collider.gameObject.transform.parent.parent = null;
                }

                if (nesne.collider.gameObject.tag == "P12"){
                    nesne.collider.gameObject.transform.parent.parent = null;
                }

                if (nesne.collider.gameObject.tag == "P13"){
                    nesne.collider.gameObject.transform.parent.parent = null;
                }
            }
        }
    }
}