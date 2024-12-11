from transformers import AutoModel, AutoProcessor
from PIL import Image
import os
from typing import List

class Generate3DModel:
    image_name: str
    def __init__(self, image_name:str):
        self.image_name = image_name
    
    def loadModelAndPreProcessor(self):
        model_name: List[str] = ["jadechoghari/vfusion3d", "nvidia/3d-mesh-gen"]
        model = AutoModel.from_pretrained(model_name[0], trust_remote_code=True)
        processor = AutoProcessor.from_pretrained(model_name[0], trust_remote_code=True)

        return model, processor
    
    def generateModel(self):
        image_path = os.path.join(self.image_name)
        # image_path = os.path.join('..', 'src', "temp_9.png")
        print('image path: ' + image_path)
        # Load the image from the local path
        image = Image.open(image_path)
        # preprocess the image and get the source camera
        print("preprocess the image and get the source camera") 
        model, processor = self.loadModelAndPreProcessor()
        image, source_camera = processor(image)

        # generate planes (default output)
        print("generate planes (default output)")
        output_planes = model(image, source_camera)
        print("Planes shape:", output_planes.shape)

        # generate a 3D mesh
        print("generate a 3D mesh")
        output_planes, mesh_path = model(image, source_camera, export_mesh=True)
        print("Planes shape:", output_planes.shape)
        print("Mesh saved at:", mesh_path)
        
        # Generate a video
        print("Generate a video")
        output_planes, video_path = model(image, source_camera, export_video=True)
        print("Planes shape:", output_planes.shape)
        print("Video saved at:", video_path)
