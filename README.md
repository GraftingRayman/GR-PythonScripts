# GR-PythonScripts
A repository for every scripts that I use


## GRLoraTrainer
Using Kohya SS scripts (SD3 Branch), these scripts train a lora with the most minimal of information from the user. 

You will need to edit the paths to fit your requirements.

Launch using loramenu.py

Option 1 creates the dataset and captions for your images

Option 2 trains a lora for flux

Option 3 resumes training a lora for flux

Option 4 merges two loras together to create a new one

### Edit the following in both the resume.py and trainlora.py

    # Define fixed paths
    repo_path = "H:\\sd-scripts" #this points to the kohya ss scripts folder
    flux_train_script = os.path.join(repo_path, "flux_train_network.py")
    base_model_path = "E:\\models\\flux1-dev.safetensors" # change this to the flux model of your choice
    ae_path = "E:\\models\\ae.safetensors" # this is the vae
    clip_model_path = "E:\\models\\clip_l.safetensors" # the clip l
    t5_model_path = "E:\\models\\t5xxl_fp16.safetensors" # the clip text encoder

