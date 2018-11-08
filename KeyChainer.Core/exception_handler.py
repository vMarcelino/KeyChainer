def print_traceback(exception):
    import traceback
    print('Exception:', str(exception))
    print('Traceback:', '\n'.join(traceback.format_list(traceback.extract_tb(exception.__traceback__))))
            