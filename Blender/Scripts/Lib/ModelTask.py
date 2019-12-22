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

    def runModels(self):
        # load json
        with open(self.config_path, 'r') as load_f:
            load_dict = json.load(load_f)
        config = Config()
        config.__dict__ = load_dict
        renderscene = RenderScene()
        renderscene.config_path = self.config_path
        if self.blender_path != None:
            renderscene.blender_path = self.blender_path
        email = Email()
        renderscene.renderModels()

        model_dir = config.input_prefix + config.scene_name + "/"
        f_list = os.listdir(model_dir)
        output = config.output_prefix + "Output/Models/" + config.task_name + \
                 "/" + config.cell_name + "/" + config.scene_name + "/"
        task = TaskImageVideo()
        task.framerate = config.framerate
        task.ImageInput = output
        task.Rename()
        task.PreProcessing()
        task.CropImage()
        task.ProduceVideo()

        email.send_email()
        os.remove(config.config_save_path)

    def runLayerOne(self):
        # load json
        with open(self.config_path, 'r') as load_f:
            load_dict = json.load(load_f)
        config = Config()
        config.__dict__ = load_dict
        renderscene = RenderScene()
        renderscene.config_path = self.config_path
        if self.blender_path != None:
            renderscene.blender_path = self.blender_path
        email = Email()
        renderscene.renderLayerOne()

        model_dir = config.input_prefix + config.scene_name + "/"
        f_list = os.listdir(model_dir)
        output = config.output_prefix + "Output/Models/" + config.task_name + \
                 "/" + config.cell_name + "/" + config.scene_name + "/"
        task = TaskImageVideo()
        task.framerate = config.framerate
        task.ImageInput = output
        task.Rename()
        task.PreProcessing()
        task.CropImage()
        task.ProduceVideo()

        email.send_email()
        os.remove(config.config_save_path)

    def runLayerTwo(self):
        # load json
        with open(self.config_path, 'r') as load_f:
            load_dict = json.load(load_f)
        config = Config()
        config.__dict__ = load_dict
        renderscene = RenderScene()
        renderscene.config_path = self.config_path
        if self.blender_path != None:
            renderscene.blender_path = self.blender_path
        email = Email()
        renderscene.renderLayerTwo()

        model_dir = config.input_prefix + config.scene_name + "/"
        f_list = os.listdir(model_dir)
        for index, dirname in enumerate(f_list):
            output = config.output_prefix + "Output/Models/" + config.task_name + \
                     "/" + config.cell_name + "/" + config.scene_name + "/" + dirname + "/"
            task = TaskImageVideo()
            task.framerate = config.framerate
            task.ImageInput = output
            task.Rename()
            task.PreProcessing()
            task.CropImage()
            task.ProduceVideo()

        email.send_email()
        os.remove(config.config_save_path)
