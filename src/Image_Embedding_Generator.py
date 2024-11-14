import pandas as pd
import requests
from io import BytesIO
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

read_file = '../data/reddit_posts_3_years.csv'


def is_image_url(url):
	try:
		response = requests.get(url, timeout=5)
		if response.status_code == 200 and response.headers['Content-Type'].startswith('image'):
			return Image.open(BytesIO(response.content))
	except Exception as e:
		print(f"URL check failed: {e}")
	return None

def main():
	df = pd.read_csv(read_file)

	# Initialize CLIP model and processor
	model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
	processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

	# Define image size and zero tensor for missing/invalid images
	embedding_dim = model.config.hidden_size  # get embedding dimension
	blank_embedding = torch.zeros(embedding_dim)  # tensor for invalid images

	# Process each URL and create embeddings
	embeddings = []
	for url in df['url']:
		# ensure URL is not NaN
		if pd.notna(url):
			img = is_image_url(url)
			if img is not None:
				# Process and transform the image for CLIP
				inputs = processor(images=img, return_tensors="pt")
				with torch.no_grad():
					embedding = model.get_image_features(**inputs).squeeze()
			else:
				# no valid image case
				embedding = blank_embedding
		else:
			# no valid url case
			embedding = blank_embedding

		embeddings.append(embedding)

	# Convert list of embeddings to a single tensor
	embeddings_tensor = torch.stack(embeddings)
	print("Embeddings generated:", embeddings_tensor.shape)


main()
