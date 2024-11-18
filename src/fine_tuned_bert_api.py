import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

def analyze_fine_tuned_bert_sentiment(text):
	try:
		tokenizer = RobertaTokenizer.from_pretrained("./fine_tuned_bert")
		fine_tuned_bert_model = RobertaForSequenceClassification.from_pretrained("./fine_tuned_bert")

		inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
		outputs = fine_tuned_bert_model(**inputs)
		logits = outputs.logits
		sentiment = torch.argmax(logits, dim=1).item()

		if sentiment == 0:
			return -1
		elif sentiment == 1:
			return 0
		else:
			return 1
	except Exception as e:
		print(f"Error using model: {e}")
		return 0


print(analyze_fine_tuned_bert_sentiment("fuck this shit im out"))
print(analyze_fine_tuned_bert_sentiment("buzz yeah"))
print(analyze_fine_tuned_bert_sentiment("I have class today"))
print(analyze_fine_tuned_bert_sentiment("sting em! go jackets"))
print(analyze_fine_tuned_bert_sentiment("I am not a helluva engineer"))
