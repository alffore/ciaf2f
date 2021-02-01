import torch
import time


import model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


if __name__ == '__main__':
    start = time.perf_counter()




    print(f'Termino en {round(time.perf_counter() - start, 2)} segundos')