
class Boy:
    def __init__(self, name, age, fav_color):
        self.__name = name
        self.__age = age
        self.__fav_color = fav_color

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def get_fav_color(self):
        return self.__fav_color

    def set_name(self, name):
        self.__name = name

    def set_age(self, age):
        self.__age = age

    def set_fav_color(self, fav_color):
        self.__fav_color = fav_color


if __name__ == "__main__":
    archie = Boy("Archie", 21, "blue")
    simon = archie
    simon.set_name("Simon")
    print("My name is " + archie.get_name() + " and I am " + str(archie.get_age()) + " years old."
          + "My favourite color is " + archie.get_fav_color())
    print("My name is " + simon.get_name() + " and I am " + str(simon.get_age()) + " years old."
          + "My favourite color is " + simon.get_fav_color())

    if isinstance(archie, Boy):
        print(True)
