def main():
    import input_parser
    
    parser = input_parser.InputParser()
    import win_low_level_hook
    keyboard_hook = win_low_level_hook.WinLowLevelHook(parser.process_keyboard_event, mouse_hook_callback)
    keyboard_hook.start()
    

def mouse_hook_callback(event):
    # print(event)
    return True


if __name__ == '__main__':
    main()