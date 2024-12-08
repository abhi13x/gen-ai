from sentence_transformers import SentenceTransformer
from diffusers import StableDiffusionPipeline, FluxPipeline
import torch

class GenerateImage:
    input_text: str

    def __init__(self, input_text: str):
        self.input_text = input_text

    def embedding_text_prompt(self):
        # Load the sentence transformer model for text embedding
        sentence_model_name = ["sentence-transformers/sentence-t5-large", 'sentence-transformers/roberta-large-nli-stsb-mean-tokens']
        sentence_model = SentenceTransformer(sentence_model_name[0])
        # Generate text embeddings (if the text-to-image pipeline accepts embeddings)
        text_embedding = sentence_model.encode(self.input_text)
        return text_embedding

    def generate_image(self):
        try:
            # Check if GPU is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            # Print the device being used
            print(f"Using device: {device.upper()}")
            torch_dtype = torch.bfloat16 if device == "cuda" else torch.float32
            print(f"Using torch_dtype: {torch_dtype}")
            diffusion_model: str = ["nelant098/jewelry", "ivankap/vvs-jewelry-hf", "buhofausto/baguette-collection-jewelry-rafael", "black-forest-labs/FLUX.1-dev" ]
            # Load the text-to-image model
            pipe = StableDiffusionPipeline.from_pretrained(
                        diffusion_model[1],
                        torch_dtype=torch_dtype
                    )
            # FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.float16)

            # Move the pipeline to the appropriate device
            pipe = pipe.to(device)

            # Generate an image from the text prompt
            image = pipe(prompt=self.input_text).images[0]
            # Save or display the generated image
            image_name = (self.input_text[0:10]).replace(" ","_")+'.png'
            image.save(image_name)
            image.show()
        except Exception as err:
            return err