# todo: add toggle key

from pynput.keyboard import Controller, Listener
from vgamepad import VX360Gamepad, XUSB_BUTTON
from time import sleep


class Macro:
    toggle = True

    lock_on = "c"
    blackflash = False
    earthquake = False


def on_press(controller: Controller, gamepad: VX360Gamepad, macro: Macro):
    def callback(key):

        keycode = str(key).strip("''")

        if keycode not in ["3", "v", macro.lock_on] or not key.vk:
            return

        match keycode:

            case "3":
                if macro.blackflash:
                    return

                macro.blackflash = True
                sleep(0.300)
                controller.tap("3")
            case "v":
                if macro.earthquake:
                    return

                macro.earthquake = True

                controller.press("3")
                sleep(0.900)
                controller.release("3")

            case macro.lock_on:
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)

                gamepad.update()

                gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
                gamepad.update()

    return callback


def on_release(macro: Macro):
    def callback(key):
        keycode = str(key).strip("''")

        if keycode == "3":
            if key.vk and macro.blackflash:
                macro.blackflash = False
            elif not key.vk and macro.earthquake:
                macro.earthquake = False

    return callback


def main() -> None:
    controller = Controller()
    gamepad = VX360Gamepad()
    macro = Macro()

    with Listener(
        on_press=on_press(controller, gamepad, macro),
        on_release=on_release(macro),
    ) as listener:
        listener.join()


if __name__ == "__main__":
    main()
