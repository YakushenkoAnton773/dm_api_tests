def attempt(
        n=5
):
    def decorator(
            func
    ):
        def wraps(
                *args,
                **kwargs
        ):
            print("------------")
            print(n)
            func(*args, **kwargs)
            print("------------")

        return wraps


    return decorator


@attempt(n=3)
def my_print(
        name
):
    print(f"Hello, {name}")


@attempt(n=4)
def my_print1(
        name
):
    print(f"Hello, {name}")


@attempt(n=2)
def my_print2(
        name
):
    print(f"Hello, {name}")


@attempt(n=1)
def my_print3(
        name
):
    print(f"Hello, {name}")


my_print(name="test1")
my_print1(name="test2")
my_print2(name="test3")
my_print3(name="test4")