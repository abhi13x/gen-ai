from sentence_transformers import SentenceTransformer
from diffusers import StableDiffusionPipeline
import torch

class GenerateImage:
    input_text: str

    def __init__(self, input_text: str):
        self.input_text = input_text

    def embedding_text_prompt(self):
        # Load the sentence transformer model for text embedding
        sentence_model = SentenceTransformer("sentence-transformers/sentence-t5-large")  # Example model
        # text_prompt = self.input_text
        # Generate text embeddings (if the text-to-image pipeline accepts embeddings)
        text_embedding = sentence_model.encode(self.input_text)
        return text_embedding

    def generate_image(self):
        # Check if GPU is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if device == "cuda" else torch.float32
        
        # Load the text-to-image model (fine-tuned for Chinese jewelry)
        pipe = StableDiffusionPipeline.from_pretrained(
                    "ivankap/vvs-jewelry-hf",
                    torch_dtype=torch_dtype
                )

        # Move the pipeline to the appropriate device
        pipe = pipe.to(device)

        # Generate an image from the text prompt
        image = pipe(prompt=self.input_text).images[0]

        # Save or display the generated image
        image_name = (self.input_text[0:10]).replace(" ","_")+'.png'
        image.save(image_name)
        image.show()
