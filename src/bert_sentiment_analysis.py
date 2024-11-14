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
			entries.append(post_text)
	return entries[1:]  # disregard the attribute names


def write_labels(generated_sentiment_labels):
	f = open(write_file, "a")
	for label in generated_sentiment_labels:
		assigned_label = label['label']
		final_label = 0  # let default assumption be neutral
		if assigned_label == 'LABEL_1':
			final_label = 0
		elif assigned_label == 'LABEL_2':
			final_label = 1
		elif assigned_label == 'LABEL_0':
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
	# sentiment_analysis_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
	sentiment_analysis_model = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment", truncation=True, max_length=512)   # Truncate inputs over the limit
	end = time.time()
	print(f"Loaded sentiment analysis pipeline in {end - start} seconds")
	labels = sentiment_analysis_model(entries)
	new_end = time.time()
	print(f"generated {len(labels)} labels in {new_end - end} seconds")
	write_labels(labels)

main()

