FILEPATH = "todos.txt"


def get_todos(filepath="todos.txt"):
    with open(filepath, "r") as file:
        return file.readlines()


def write_todos(todos_arg, filepath="todos.txt"):
    with open(filepath, "w") as file:
        file.writelines(todos_arg)



if __name__ == "__main__":
    print("Hello")
    print(get_todos())
