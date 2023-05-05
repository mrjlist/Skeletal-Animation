import gradio as gr
import subprocess
import os
import imageio
import numpy as np
from gradio.outputs import Image
from PIL import Image, PngImagePlugin
import requests
import json
import io
import base64
import sys
import cv2
import shutil
import time
import math

from modules import shared
from modules import scripts
from modules import script_callbacks
from modules.sd_samplers import samplers
from modules.shared import cmd_opts, demo
import modules.shared as shared

url = "http://127.0.0.1:7860"

class Script(scripts.Script):
    def title(self):
        return "Animate"

    def show(self, is_img2img):
        return scripts.AlwaysVisible
     
    def ui(self, is_img2img):
        return []
        
def run_ar(
        InFF, 
        OuFF):
    return InFF, OuFF


def run_vr(prompt, n_prompt, sampler_index, steps, seed_resize_from_w, seed_resize_from_h, cfg_scale, seed, prompt_styles):
    quest = {
        # "denoising_strength": 0,
        "prompt": prompt,
        "styles": prompt_styles,
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": samplers[sampler_index].name,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": seed_resize_from_w,
        "height": seed_resize_from_h,
        "negative_prompt": n_prompt,
        "sampler_index": samplers[sampler_index].name,
        "save_images": True,
        }
    print(quest)
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=quest)
    r = response.json()
    
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
    
    return image

def add_tab():
    print('LAB')
    with gr.Blocks(analytics_enabled=False) as AnimatedTT:
        with gr.Tabs():
            with gr.Tab("Animation rendering"):
                with gr.Row():
                    with gr.Column():
                        InFF = gr.Textbox(label="Original/reference frames folder", placeholder="RAW frames, or generated ones.")
                        OuFF = gr.Textbox(label="Output skeletal animate frames folder", placeholder="Folder for saving skeletal animation frames.")
                        run_button_ar = gr.Button(value="Run", variant="primary")
                        output_placeholder_ar = gr.Textbox(label="Status", placeholder="LOADING...")

            with gr.Tab("Video rendering"):
                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            with gr.Column(scale=80):
                                with gr.Row():
                                    prompt = gr.Textbox(show_label=False, lines=2, interactive=True, elem_id=f"prompt", placeholder="Enter your prompt here...")
                                with gr.Row():
                                    n_prompt = gr.Textbox(show_label=False, lines=3, interactive=True, elem_id=f"n_prompt", placeholder="Enter your negative prompt here...")
                            with gr.Column():
                                with gr.Row():
                                    run_button_vr = gr.Button(value="Run reference", variant="primary")
                                with gr.Row():
                                    run_button_vr_anim = gr.Button(value="Run frame", variant="stop")
                                with gr.Row():
                                    prompt_styles = gr.Dropdown(label="Styles", show_label=False, elem_id=f"styles", choices=[k for k, v in shared.prompt_styles.styles.items()], value=[], multiselect=True)
                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            sampler_index = gr.Dropdown(label='Sampling method', elem_id=f"sampling", choices=[x.name for x in samplers], value=samplers[0].name, type="index")
                            steps = gr.Slider(minimum=1, maximum=150, step=1, elem_id=f"steps", label="Sampling steps", value=20)
                        with gr.Row():
                            with gr.Column():
                                seed_resize_from_w = gr.Slider(minimum=0, maximum=2048, step=8, label="width", value=512, elem_id='seed_resize_from_w')
                                seed_resize_from_h = gr.Slider(minimum=0, maximum=2048, step=8, label="height", value=512, elem_id='seed_resize_from_h')
                                cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5, label='CFG Scale', value=7.0, elem_id="cfg_scale")
                                seed = (gr.Textbox if cmd_opts.use_textbox_seed else gr.Number)(label='Seed', value=-1, elem_id='seed')
                                InMFF = gr.Textbox(label="Folder skeletal mask frames", placeholder="Mask frames")
                                denoising_strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label='Denoising strength', value=0.7, elem_id="denoising_strength")
                    with gr.Column():
                        ti_gallery = gr.Image(label='Output', show_label=False, elem_id='ti_gallery', type="pil")
                        

            # with gr.Tab("Guide"):
            #     with gr.Column():
            #         gr.Markdown("# What DFI does?")
            #         with gr.Accordion("Info", open=False):
            #             gr.Markdown("DFI processing analyzes the motion of the original video, and attempts to force that information into the generated video. Demo on https://github.com/AbyszOne/Abysz-LAB-Ext")
            #             gr.Markdown("In short, this will reduce flicker in areas of the video that don't need to change, but SD does. For example, for a man smoking, leaning against a pole, it will detect that the pole is static, and will try to prevent it from changing as much as possible.")
            #             gr.Markdown("This is an aggressive process that requires a lot of control for each context. Read the recommended strategies.")
            #             gr.Markdown("Although Video to Video is the most efficient way, a DFI One Shot method is under experimental development as well.")
            #         gr.Markdown("# Usage strategies")
            #         with gr.Accordion("Info", open=False):
            #             gr.Markdown("If you get enough understanding of the tool, you can achieve a much more stable and clean enough rendering. However, this is quite demanding.")
            #             gr.Markdown("Instead, a much friendlier and faster way to use this tool is as an intermediate step. For this, you can allow a reasonable degree of corruption in exchange for more general stability. ")
            #             gr.Markdown("You can then clean up the corruption and recover details with a second step in Stable Diffusion at low denoising (0.2-0.4), using the same parameters and seed.")
            #             gr.Markdown("In this way, the final result will have the stability that we have gained, maintaining final detail. If you find a balanced workflow, you will get something at least much more coherent and stable than the raw AI render.")
            #             gr.Markdown("**OPTIONAL:** Although not ideal, you can use the same AI generated video as the source, instead of the RAW. The trick is to use DFI and denoise to wash out map details so that you reduce low/mid changes between frames. If you only need a soft deflick, it is a valid option.")
        
        # dt_inputs=[ruta_entrada_1, ruta_entrada_2, denoise_blur, dfi_strength, dfi_deghost, test_mode, smooth]
        run_inputs_ar=[
            InFF, 
            OuFF
            ]
        run_inputs_vr=[
            prompt, 
            n_prompt,
            sampler_index,
            steps,
            seed_resize_from_w,
            seed_resize_from_h,
            cfg_scale,
            seed,
            prompt_styles
            ]
        

        run_button_ar.click(fn=run_ar, inputs=run_inputs_ar, outputs=output_placeholder_ar)
        run_button_vr.click(fn=run_vr, inputs=run_inputs_vr, outputs=ti_gallery)
    return [(AnimatedTT, "Animation", "AnimatedTT")]
        
script_callbacks.on_ui_tabs(add_tab)
