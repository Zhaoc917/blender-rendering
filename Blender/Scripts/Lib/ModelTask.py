import os
import sys
sys.path.append("..")
sys.path.append("../../")
from Lib.RenderScene import RenderScene
from Lib.ConfigClass import Config
from Lib.ImageVideo import TaskImageVideo
from Lib.email_sender import Email
from IPython.display import display,Video
import imageio
import datetime
import socket
import json
import getpass
import time


class TaskHub():
    def __init__(self):
        self.config_path = None
        self.blender_path = None
        self.batch_type = "LayerTwo"
        self.material_path = None
        self.texture_path = None
        self.image_input = None
        self.email_reveiver = None

    def run(self):
        # load json
        with open(self.config_path, 'r') as load_f:
            load_dict = json.load(load_f)
        config = Config()
        config.__dict__ = load_dict
        renderscene = RenderScene()
        renderscene.config_path = self.config_path
        renderscene.texture_path = self.texture_path
        renderscene.material_path = self.material_path
        if self.blender_path != None:
            renderscene.blender_path = self.blender_path
        email = Email()
        email.config = config
        renderscene.batch = self.batch_type
        renderscene.renderBatch()
        model_dir = config.input_prefix
        f_list = os.listdir(model_dir)
        if self.batch_type == "LayerTwo":
            for index, dirname in enumerate(f_list):
                output = config.output_prefix + config.task_name + \
                         "/" + config.cell_name + "/" + dirname + "/"
                task = TaskImageVideo()
                task.framerate = config.framerate
                task.ImageInput = output
                task.Rename()
                task.PreProcessing()
                task.CropImage()
                task.ProduceVideo()
        else:
            output = config.output_prefix + config.task_name + \
                     "/" + config.cell_name + "/"
            task = TaskImageVideo()
            task.framerate = config.framerate
            task.ImageInput = output
            task.Rename()
            task.PreProcessing()
            task.CropImage()
            task.ProduceVideo()
        if self.email_reveiver != None:
            email.receiver = self.email_reveiver
        email.send_email()
        os.remove(config.config_save_path)

    def GenerateVideo(self):
        # load json
        with open(self.config_path, 'r') as load_f:
            load_dict = json.load(load_f)
        config = Config()
        config.__dict__ = load_dict
        email = Email()
        email.config = config

        output = config.output_prefix + config.task_name + \
                 "/" + config.cell_name + "/"
        task = TaskImageVideo()
        task.framerate = config.framerate
        if self.image_input == None:
            task.ImageInput = output
        else:
            task.ImageInput = self.image_input
        task.Rename()
        task.PreProcessing()
        task.CropImage()
        task.ProduceVideo()
        if self.email_reveiver != None:
            email.receiver = self.email_reveiver
        email.send_email()

    # def runSingle(self):
    #     # load json
    #     with open(self.config_path, 'r') as load_f:
    #         load_dict = json.load(load_f)
    #     config = Config()
    #     config.__dict__ = load_dict
    #     renderscene = RenderScene()
    #     renderscene.config_path = self.config_path
    #     if self.blender_path != None:
    #         renderscene.blender_path = self.blender_path
    #     email = Email()
    #     renderscene.render()
    #     output = config.output_prefix + config.task_name + \
    #              "/" + config.cell_name + "/"
    #     task = TaskImageVideo()
    #     task.framerate = config.framerate
    #     task.ImageInput = output
    #     task.Rename()
    #     task.PreProcessing()
    #     task.CropImage()
    #     task.ProduceVideo()



    # def runSingle(self):
    #     # load json
    #     with open(self.config_path, 'r') as load_f:
    #         load_dict = json.load(load_f)
    #     config = Config()
    #     config.__dict__ = load_dict
    #     renderscene = RenderScene()
    #     renderscene.config_path = self.config_path
    #     if self.blender_path != None:
    #         renderscene.blender_path = self.blender_path



