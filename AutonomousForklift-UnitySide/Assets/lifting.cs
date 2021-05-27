using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class lifting : MonoBehaviour
{
    public GameObject x;
    public KeyCode giris_1_tus;
    public KeyCode birakma_1_tus;
    public KeyCode giris_2_tus;
    public KeyCode birakma_2_tus;
    public KeyCode giris_3_tus;
    public KeyCode birakma_3_tus;
    public KeyCode default_level_tus;
    public KeyCode picking_from_second_tus;
    public float speed = 0.1f;
    public bool giris_1 = false;
    public bool birakma_1 = false;
    public bool giris_2 = false;
    public bool birakma_2 = false;
    public bool giris_3 = false;
    public bool birakma_3 = false;
    public bool default_level = false;
    public bool picking_from_second_level = false;
    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        /*
                
        0.1 = en alt girişi
        0.0 = en alt bırakma

        2.0 = 1. raf girişi
        1.83 = 1. raf bırakma

        3.70 = 2. raf girişi
        3.50 = 2. raf bırakma
        
        1.50 = Default
        1.20 = 2 kutu üst üste üstten alma
        */
        
        //kamera icin lift seviyesi
        if (Input.GetKeyDown(default_level_tus))
        {
            default_level = true;

        }
        if (default_level == true){
            if (x.transform.position.y >= 1.5 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,-1f,0f))*speed;
                if (x.transform.position.y <= 1.5 + 1.638359){
                    default_level = false;
                }
            }
            if (x.transform.position.y <= 1.5 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,1f,0f))*speed;
                if (x.transform.position.y >= 1.5 + 1.638359){
                    default_level = false;
                }
            }
        }

        //2. kutu icin lift seviyesi
        if (Input.GetKeyDown(picking_from_second_tus))
        {
            picking_from_second_level = true;

        }
        if (picking_from_second_level == true){
            if (x.transform.position.y >= 1.18 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,-1f,0f))*speed;
                if (x.transform.position.y <= 1.18 + 1.638359){
                    picking_from_second_level = false;
                }
            }
            if (x.transform.position.y <= 1.18 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,1f,0f))*speed;
                if (x.transform.position.y >= 1.18 + 1.638359){
                    picking_from_second_level = false;
                }
            }
        }


        //en alt giriş
        if (Input.GetKeyDown(giris_1_tus))
        {
            giris_1 = true;

        }
        if (giris_1 == true){
            if (x.transform.position.y >= 0.1 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,-1f,0f))*speed;
                if (x.transform.position.y <= 0.1 + 1.638359){
                    giris_1 = false;
                }
            }
            if (x.transform.position.y <= 0.1 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,1f,0f))*speed;
                if (x.transform.position.y >= 0.1 + 1.638359){
                    giris_1 = false;
                }
            }
        }
        //en alt bırakma
        if (Input.GetKeyDown(birakma_1_tus))
        {
            birakma_1 = true;

        }
        if (birakma_1 == true){
            if (x.transform.position.y >= 0 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,-1f,0f))*speed;
                if (x.transform.position.y <= 0 + 1.638359){
                    birakma_1 = false;
                }
            }
            if (x.transform.position.y <= 0 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,1,0f))*speed;
                if (x.transform.position.y >= 0 + 1.638359){
                    birakma_1 = false;
                }
            }
        }

        //orta kat giriş
        if (Input.GetKeyDown(giris_2_tus))
        {
            giris_2 = true;

        }
        if (giris_2 == true){
            if (x.transform.position.y >= 2 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,-1f,0f))*speed;
                if (x.transform.position.y <= 2 + 1.638359){
                    giris_2 = false;
                }
            }
            if (x.transform.position.y <= 2 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,1f,0f))*speed;
                if (x.transform.position.y >= 2 + 1.638359){
                    giris_2 = false;
                }
            }
        }
        //orta kat bırakma
        if (Input.GetKeyDown(birakma_2_tus))
        {
            birakma_2 = true;

        }
        if (birakma_2 == true){
            if (x.transform.position.y >= 1.83 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,-1f,0f))*speed;
                if (x.transform.position.y <= 1.83 + 1.638359){
                    birakma_2 = false;
                }
            }
            if (x.transform.position.y <= 1.83 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,1,0f))*speed;
                if (x.transform.position.y >= 1.83 + 1.638359){
                    birakma_2 = false;
                }
            }
        }

        //üst kat giriş
        if (Input.GetKeyDown(giris_3_tus))
        {
            giris_3 = true;

        }
        if (giris_3 == true){
            if (x.transform.position.y >= 3.70 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,-1f,0f))*speed;
                if (x.transform.position.y <= 3.70 + 1.638359){
                    giris_3 = false;
                }
            }
            if (x.transform.position.y <= 3.70 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,1f,0f))*speed;
                if (x.transform.position.y >= 3.70 + 1.638359){
                    giris_3 = false;
                }
            }
        }
        //üst kat bırakma
        if (Input.GetKeyDown(birakma_3_tus))
        {
            birakma_3 = true;

        }
        if (birakma_3 == true){
            if (x.transform.position.y >= 3.50 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,-1f,0f))*speed;
                if (x.transform.position.y <= 3.50 + 1.638359){
                    birakma_3 = false;
                }
            }
            if (x.transform.position.y <= 3.50 + 1.638359){
                x.transform.position = x.transform.position + (new Vector3(0f,1f,0f))*speed;
                if (x.transform.position.y >= 3.50 + 1.638359){
                    birakma_3 = false;
                }
            }
        }

    }
}
