import os,sys,platform

if platform.system() == "Linux":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
else:
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])

sys.path.append(BASE_DIR)



if __name__ == '__main__':
    from core import HouseStark
    HouseStark.ArgvHandler(sys.argv)