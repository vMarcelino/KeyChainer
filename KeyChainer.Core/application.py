def main():
    import input_parser
    
    parser = input_parser.InputParser()

    import win_low_level_hook

    keyboard_hook = win_low_level_hook.WinLowLevelHook(parser.process_keyboard_event, mouse_hook_callback)
    keyboard_hook.start()

    import ui_spawner

    ui_thread = ui_spawner.UIThread()
    ui_thread.start()

    import time
    time.sleep(3)
    ui_thread.show_window()
    

def mouse_hook_callback(event):
    # print(event)
    return True


if __name__ == '__main__':
    main()