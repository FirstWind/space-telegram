

if __name__ == "__main__":
    select_image_type = int(
        input(
            "Какие картинки будем загружать? Выберите цифру:\n NASA(1)\n NASA EPIC(2)\n SpaceX(3)\n Или не качаем(0)\n >> "
            )
        )
    if select_image_type == 1:
        exec(open('photo_nasa.py').read())
    elif select_image_type == 2:
        exec(open('photo_nasa_epic.py').read())
    elif select_image_type == 3:
        exec(open('photo_space_x.py').read())

    exec(open('photo_bot.py').read())
    print("Закончили")
