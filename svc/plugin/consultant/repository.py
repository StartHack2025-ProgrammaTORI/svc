from svc.utils.dataset import read_csv, answers
import os

dataset = read_csv(os.environ["DB"])

def list():
    print(answers)
    return dataset.to_dict(orient="records")
