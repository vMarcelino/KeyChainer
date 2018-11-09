class InputParser:
    def __init__(self):
        self.keys_down=set()
    
    def process_keyboard_event(self, event):
        # print(event)
        nCode, e = event
        key_code = e[1] & 0xFFFFFFFF
        key_code_special = 0
        key_name = hex(e[1])[2:]
        key_code_special = int((e[1] & 0xFF00000000) / 0x100000000)
        
        special = False
        import key_map
        try:
            key_name = key_map.key_code_map[key_code]
        except KeyError:
            try:
                key_name = key_map.key_code_map[e[1] & 0xFFFFFFFFF]
            except KeyError:
                try:
                    key_name = key_map.key_code_special_map[key_code_special]
                    special = True
                except KeyError:
                    pass
        
        if e[0] == 'key down':
            return self.on_key_down(key_name, special)
        else:
            return self.on_key_up(key_name)
              
        
    def on_key_down(self, key_name, is_special_key):
        print(key_name, end='', flush=True)
        if key_name == 'F12':
            return False
            
        self.keys_down.add(key_name)

        if 'F1' in self.keys_down and 'LControlKey' in self.keys_down:
            import ui_spawner
            ui_spawner.show_window()
        
        return True
        
        
    def on_key_up(self, key_name):
        if key_name == 'F1':
            exit()
            
        try:
            self.keys_down.remove(key_name)
        except KeyError as ke:
            print('\nkey error:', ke)
        except Exception as ex:
            import exception_handler
            exception_handler.print_traceback(ex)
        
        return True