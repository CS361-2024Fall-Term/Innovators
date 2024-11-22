# dynamic sizing functions
# modulize the dynamic sizing found in calendar

class DynamicSizing:
    @staticmethod
    def get_screen_size(root):
        return root.winfo_screenwidth(), root.winfo_screenheight()

    @staticmethod
    def set_window_size(root, width_factor=0.5, height_factor=0.5):
        screen_width, screen_height = DynamicSizing.get_screen_size(root)
        
        window_width = int(screen_width * width_factor)
        window_height = int(screen_height * height_factor)
        
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        
        root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")