import csv
import time

from transformers import pipeline

read_file = '../data/reddit_posts_3_years.csv'
write_file = '../data/labels.txt'

def load_csv():
	entries = []
	with open(read_file, newline='') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',')
		for row in csv_reader:
			title = row[1]
			self_text = row[2]
			post_text = title + " " + self_text
			post_text = post_text[:100]
			entries.append(post_text)
	return entries[1:]  # disregard the attribute names


def write_labels(generated_sentiment_labels):
	f = open(write_file, "a")
	for label in generated_sentiment_labels:
		assigned_label = label['label']
		score = label['score']
		final_label = 0  # let default assumption be neutral
		if assigned_label == 'NEU':
			final_label = 0
		elif assigned_label == 'POS':
			final_label = 1
		elif assigned_label == 'NEG':
			final_label = -1
		f.write(str(final_label))
		f.write("\n")
	f.close()


def main():
	"""
	Provide labels for all posts gathered in reddit_posts_3_years.csv
	Write generated labels to labels.txt
	:return: None
	"""
	entries = load_csv()
	print(f"found {len(entries)} posts")

	start = time.time()
	sentiment_analysis_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
	end = time.time()
	print(f"Loaded sentiment analysis pipeline in {end - start} seconds")
	labels = sentiment_analysis_model(entries)
	new_end = time.time()
	print(f"generated {len(labels)} labels in {new_end - end} seconds")
	write_labels(labels)

main()

