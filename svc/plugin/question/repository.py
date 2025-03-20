from svc.utils.dataset import questions, answers
from svc.utils.userRecomendation import userRec
from svc.utils.database import db
from .schema import Question, QuestionAnswer
from bson import ObjectId  # Add this import for ObjectId
from datetime import datetime

def get_questions(uid: str):
    db_results = db.question.find({'uid': uid})
    return [Question(**item).dict() for item in db_results]

def save_question(question: dict):
    db.question.insert_one(question)
  
async def get_question(index: int = None, uid: str = None):
    questions = get_questions(uid)
    if (index == None):
        index = 0
    if index >= len(questions):
        question = userRec.get_next_question(answers)
        save_question(
            {
                "question": question['question'],
                "options": [{'text': option, 'id': str(ObjectId())} for option in question['options']],
                "uid": uid,
                "answer": None,
                "created_at": datetime.now()
            }
        )
        questions = get_questions(uid)
    return {
        **questions[index],
        'index': index + 1
    }

def save_answer(answer: dict):
    return db.question.update_one(
        {'_id': ObjectId(answer['question'])},
        {'$set': {'answer': answer['answer']}}
    )

def answer_question(index_question: int, index_answer: str, uid: str):
    questions = get_questions(uid)
    if (index_question > len(questions)):
        raise Exception("Index out of range")
    question = questions[index_question]
    save_answer(
        {
            'question': question['id'],
            'answer': index_answer
        }
    )
    questions = get_questions(uid)
    return {
        **questions[index_question],
        'index': index_question + 1
    }
    
def get_questions_and_answers(uid: str):
    print("uid: ", uid)
    data = db.question.aggregate([
        {
            '$match':
            {
                'uid': uid
            }
        },
        {
            "$set": {
            "answer": {
                "$arrayElemAt": [
                {
                    "$filter": {
                    "input": "$options",
                    "as": "option",
                    "cond": {
                        "$eq": ["$$option.id", "$answer"]
                    }
                    }
                },
                0
                ]
            }
            }
        },
        {
            "$project": {
                "_id": 0,
                "question": 1,
                "answer": "$answer.text"
            }
        }
    ])
    data = [QuestionAnswer(**item).dict() for item in data]
    return data