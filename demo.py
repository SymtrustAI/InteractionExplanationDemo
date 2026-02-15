import argparse
from src.Function1 import run_interaction


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # general settings
    parser.add_argument('--gpu_id', type=int, default=2)
    parser.add_argument("--cal_batch_size", default=128, type=int,
                        help="batch size for computing forward passes on masked input samples")
    parser.add_argument("--model_size", type=str, default='large',
                        help="small: 1.5B model, large: 7B model")
    
    args = parser.parse_args()

    run_interaction(args)
