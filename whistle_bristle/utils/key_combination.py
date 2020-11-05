from pynput import keyboard

MAIN_KEYS = {'ctrl': keyboard.Key.ctrl,
             'shift': keyboard.Key.shift,
             'alt': keyboard.Key.alt}


class KeyComboError(BaseException):
    pass


class KeyCombinationListener:

    def __init__(self, key_combo=None, on_press=None, on_release=None):
        self.key_combo = check_key(key_combo)

        self.combination = {*keyboard.HotKey.parse(self.key_combo)}
        self.currently_pressed = set()
        self.is_pressed = False
        self.on_press = on_press
        self.on_release = on_release


    def _on_press(self, key):
        ''' Launches function on pressing hotkey'''
        if key in self.combination:
            self.currently_pressed.add(key)

        if self.currently_pressed == self.combination:
            self.is_pressed = True
            self.on_press()

    def _on_release(self, key):
        ''' Launches function on release hotkey'''
        try:
            self.currently_pressed.remove(key)
            if self.is_pressed and len(self.currently_pressed) == 0:
                self.is_pressed = False
                self.on_release()

        except KeyError:
            pass

    def start_listening(self):
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release)
        self.listener.start()


def check_key(key_combo):
    try:
        key_combo = key_combo.lower().strip()
        key_combo = key_combo.replace(' ', '+')
        key_combo = key_combo.replace('-', '+')
        key_combo = key_combo.replace('_', '+')
        key_combo = key_combo.replace(' ', '+')
        for word in key_combo.split('+'):
            if len(word) > 1 and '<' not in word and '>' not in word:
                if word[0] != '<' and word[-1] != '>':
                    key_combo = key_combo.replace(word, f'<{word}>')

        keyboard.HotKey.parse(key_combo)
    except KeyError as ke:  # KeyEror, ValueError, ValueError
        raise ValueError('Not correct name of keys') from ke
    except AttributeError as ae:
        raise TypeError('Not given a key combination') from ae
    except TypeError as te:
        raise TypeError('Key combination must be string') from te
    except ValueError as ve:
        raise ValueError('Wrong syntax for key combination') from ve
    return key_combo


if __name__ == '__main__':
    pass
    key0 = '<ctRl>-<alt>-b'
    key1 = '<ctrl>+<Shift>+<Alt>+"'
    key2 = 'ctRl-alt-b'
    key3 = 'ctRl alt b'

    print(check_key(key0))
    print(check_key(key1))
    print(check_key(key2))
    print(check_key(key3))

    key_com0 = KeyCombinationListener(key3, lambda: print('pressed!'),
                              lambda: print('released!'))

    key_com0.start_listening()

    input()
