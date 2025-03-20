from svc.utils.dataset import todos

def get_todos():
    result = []
    for todo in todos:
        if todo['current_step'] < len(todo['steps']):
            result.append(todo)
    return result

def check_todo(id: int):
    for index, todo in enumerate(todos):
        if todo['id'] == id:
            todos[index]['current_step'] = todos[index]['current_step'] + 1
    return get_todos()