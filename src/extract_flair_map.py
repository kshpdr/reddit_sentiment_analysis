import csv

read_file = '../data/reddit_posts_3_years.csv'
write_file = '../data/labels.txt'

def load_csv():
	entries = []
	with open(read_file, newline='') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',')
		for row in csv_reader:
			title = row[8]
			entries.append(title)
	return entries[1:]  # disregard the attribute names

def build_map(data):
	flair_set = list(set(data))
	flair_map = {}
	for i, elt in enumerate(flair_set):
		flair_map[elt] = i
	print(flair_map)

def main():
	"""
	Provide labels for all posts gathered in reddit_posts_3_years.csv
	Write generated labels to labels.txt
	:return: None
	"""
	entries = load_csv()
	print(f"found {len(entries)} posts")
	build_map(entries)

main()
