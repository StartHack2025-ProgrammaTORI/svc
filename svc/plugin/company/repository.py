from svc.utils.dataset import questions, answers

def get_question(index: int = None):
    if (index == None):
        index = 0
    if (index > len(questions)):
        raise Exception("Index out of range")
    return {
        **questions[index],
        'index': index + 1
    }
    
def answer_question(index_question: int, index_answer: str):
    if (index_question > len(questions)):
        raise Exception("Index out of range")
    if index_question >= len(answers):
        answers.append(
            {
                'question': questions[index_question]['question'],
                'answer': questions[index_question]['options'][index_answer]
            }
        )
    else:
        if len(questions[index_question]['options']) <= index_answer:
            raise Exception("index out of range")
        answers[index_question] = {
            'question': questions[index_question]['question'],
            'answer': questions[index_question]['options'][index_answer]
        }
    return {
        **questions[index_question],
        'index': index_question + 1
    }