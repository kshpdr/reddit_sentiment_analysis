## reddit sentiment analysis

To reproduce the results for any given subreddit do the following.

First, rename `.env.example` to a normal `.env` file and put their your OpenAI API key for data labeling.

Collect data with a python script specify subreddit, number of years to get data for and output file:
```
python src/fetch_dataset.py gatech 3 data/reddit_posts_3_years.csv
```

Then open `src/label_data.ipynb` notebook to perform data labeling and save the sentiment to use them as a ground truth.