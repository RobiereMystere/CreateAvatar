from application import Application
from character import Character

if __name__ == "__main__":
    new_character = Character()
    app = Application()
    app.draw_char(new_character)
    app.mainloop()
