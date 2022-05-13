from js import console

todo_text = Element("todo-text")
add_btn = Element("add-btn")
todo_list_group = Element("todo-list-group")
delete_all_button = Element("delete-all")

def add_todo(*args):
    #console.log("add button clicked")
    text = todo_text.element.value
    todo_item = create("li", classes="list-group-item")
    todo_item.element.innerText = text
    todo_list_group.element.appendChild(todo_item.element)

    todo_text.clear()

    todo_item.element.onclick = lambda event: todo_item.element.classList.add("todo-completed")

def delete_all_todos(*args):
    for todo_item in todo_list_group.element.childNodes:
        todo_item.remove()


add_btn.element.onclick = add_todo
delete_all_button.element.onclick = delete_all_todos