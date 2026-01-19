#train NER model
import pickle
import pathlib
import spacy
from spacy.util import minibatch
from spacy.training.example import Example
import random

#load training data
project_root = pathlib.Path(__file__).parent.parent
data_path = project_root / "training_data.pkl"
with open(data_path, 'rb') as f:
    training_data = pickle.load(f)

#create blank nlp model
nlp = spacy.blank("en")

if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

#add labels to ner
for _, annotations in training_data:
    for ent in annotations.get("entities"):
        if ent[2] not in ner.labels:
            ner.add_label(ent[2])

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    epochs = 50
    for epoch in range(epochs):
        random.shuffle(training_data)
        losses = {}
        batches = minibatch(training_data, size=2)
        for batch in batches:
            examples = []
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)
            nlp.update(examples, drop=0.5, sgd=optimizer, losses=losses)
        print(f'Epoch {epoch+1}/{epochs}, Losses: {losses}')

nlp.to_disk(project_root / "ner_model")
print(f"Model saved to {project_root / 'ner_model'}")

