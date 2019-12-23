import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ConfigClass import *


class RenderScene:
    def __init__(self):
        # self.config = None
        self.blender_path = "/home/zhaoc/blender/blender_2.81/blender"
        self.background_render = True
        self.config_path = "./config.json"
        self.batch = None

    def read_json(self):
        with open(self.config_path, 'r') as load_f:
            load_dict = json.load(load_f)
        config = Config()
        # update
        config.__dict__ = load_dict
        return config

    def render(self):
        cmd = self.blender_path + " --python ../../Lib/BlenderBridge.py"
        cmd += " -noaudio"
        if self.background_render:
            cmd += " --background"
        cmd += " -- -c " + str(self.config_path)
        print("start rendering...")
        os.system(cmd)
        print("done!")

    def renderBatch(self):
        config = self.read_json()
        # Two layers rendering
        scene_number = 0
        scene_name_list = []
        cell_start_time = datetime.datetime.now()
        model_dir = config.input_prefix
        f_list = os.listdir(model_dir)

        if self.batch == "LayerTwo":
            for index, dirname in enumerate(f_list):
                output = config.output_prefix + "Output/Models/" + config.task_name + \
                         "/" + config.cell_name + "/" + dirname + "/"
                if not os.path.exists(output):
                    os.makedirs(output)
                file_dir = model_dir + dirname + "/"
                file_list = os.listdir(file_dir)
                scene_number += len(file_list)
                scene_name_list += file_list
                for index, filename in enumerate(file_list):
                    config.scene_path = model_dir + dirname + "/" + filename + "/"
                    config.output_path = output + filename + ".png"
                    config.save_config(config.config_save_path)
                    self.render()
        if self.batch == "LayerOne":
            for index, filename in enumerate(f_list):
                output = config.output_prefix + "Output/Models/" + config.task_name + \
                         "/" + config.cell_name + "/" + filename + ".png"
                scene_name_list += f_list
                config.scene_path = model_dir + filename + "/"
                config.output_path = output
                config.save_config(config.config_save_path)
                self.render()
        if self.batch == "Models":
            config.show_singularities = False
            config.cut_mode = "None"
            config.show_loops = False
            for index, filename in enumerate(f_list):
                if ".obj" in filename:
                    output = config.output_prefix + "Output/Models/" + config.task_name + \
                             "/" + config.cell_name + "/" + filename.split(".")[0] + ".png"
                    config.scene_path = model_dir
                    config.output_path = output
                    config.material = "model_only"
                    config.object_name = filename
                    config.save_config(config.config_save_path)
                    self.render()
        cell_end_time = datetime.datetime.now()
        config.time_cost_total = str(cell_end_time - start_time).split('.')[0]
        config.time_cost_cell = str(cell_end_time - cell_start_time).split('.')[0]
        config.save_config(config.config_save_path)