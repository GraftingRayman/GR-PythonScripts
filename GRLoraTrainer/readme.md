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

### Default settings, edit --sample_prompts=e:\\models\\sample_prompts.txt" to point to the right place:

        f"--pretrained_model_name_or_path={base_model_path}",
        f"--ae={ae_path}",
        f"--output_dir={parent_directory}",
        f"--output_name={dataset_folder_name}",
        f"--train_data_dir={parent_directory}",
        f"--dataset_config={config_file_path}",  # Add the dataset_config argument
        f"--learning_rate=8e-4",
        f"--max_train_steps={max_train_steps}",
        f"--save_every_n_steps={save_every_n_steps}",
        f"--save_model_as=safetensors",
        f"--logging_dir=logs",
        f"--clip_l={clip_model_path}",
        f"--t5xxl={t5_model_path}",
        f"--resolution={selected_resolution}",
        f"--sample_every_n_steps={generate_sample_steps}",
        f"--network_module=networks.lora_flux",
        f"--network_dim=4",
        "--cache_text_encoder_outputs",
        "--cache_text_encoder_outputs_to_disk",
        "--fp8_base",
        "--highvram",
        "--max_train_epochs=16",
        "--save_every_n_epochs=1",
        "--cache_latents_to_disk",
        "--sdpa",
        "--persistent_data_loader_workers",
        "--max_data_loader_n_workers=2",
        "--seed=42",
        "--gradient_checkpointing",
        "--mixed_precision=bf16",
        "--save_precision=bf16",
        "--network_train_unet_only",
        "--timestep_sampling=shift",
        "--discrete_flow_shift=3.1582",
