import app

def test():
    head, *tail = [1, 2, 3, 4, 5]
    print(head)
    print(tail)
    *head, tail = [1, 2, 3, 4, 5]
    print(head)
    print(tail)


def dictionary_comprehension():
    users = [
        (0, "Bob", "password"),
        (1, "Rolf", "bob123"),
        (2, "Jose", "long4assword"),
        (3, "username", "1234"),
    ]
    username_mapping = {user[1]: user for user in users}
    return username_mapping


def unpacking_keyword_arguments(**kwargs):
    print(kwargs)


if __name__ == '__main__':
    test()
    #print(dictionary_comprehension())
    #unpacking_keyword_arguments(name="Bob", age=25)

class ClassTest:
    def instance_method(self):
        print(f"Called instance_method of {self}")

    @classmethod
    def class_method(cls):
        print(f"Called class_method of {cls}")
        # typically used as factory methods

    @staticmethod
    def static_method():
        print("Called static_method.")
