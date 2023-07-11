import platform

def get_system_type():
    if platform.system() == "Windows":
        import wombat
        print('windows')
    elif platform.system() == "Linux":
        import wbashir
        return "Linux"
    else:
        return "Unknown"

if __name__=="__main__":
    get_system_type()