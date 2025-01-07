from pynput import keyboard
from time import sleep


def on_press(controller, toggles):
    def callback(key):
        if not isinstance(key, keyboard.KeyCode):
            return

        keycode = str(key).strip("''")

        if keycode not in ["3", "v"] or not key.vk:
            return

        match keycode:
            case "3":
                if toggles["bl"]:
                    return

                toggles["bl"] = True
                sleep(0.300)
                controller.tap("3")
            case "v":
                if toggles["eq"]:
                    return

                toggles["eq"] = True

                controller.press("3")
                sleep(0.900)
                controller.release("3")

    return callback


def on_release(toggles):
    def callback(key):
        if not isinstance(key, keyboard.KeyCode):
            return

        keycode = str(key).strip("''")

        if keycode == "3":
            if key.vk and toggles["bl"]:
                toggles["bl"] = False
            elif not key.vk and toggles["eq"]:
                toggles["eq"] = False

    return callback


def main() -> None:
    controller = keyboard.Controller()

    toggles = {
        "bl": False,  # blackflash
        "eq": False,  # mahoraga's earthquake
    }

    with keyboard.Listener(
        on_press=on_press(controller, toggles), on_release=on_release(toggles)
    ) as listener:
        listener.join()


if __name__ == "__main__":
    main()
