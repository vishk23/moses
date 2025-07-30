import argparse
import src.train_model as train_model
import src.predict as predict
from src._version import __version__

def main(production_flag: bool=False) -> None:

    """
    Parses arguments to determine whether to run training or predict pipelines.
    """

    parser = argparse.ArgumentParser(description="Logistic Regression CLI")
    parser.add_argument("mode", choices=["train", "predict"], help="Run mode")

    args = parser.parse_args()

    if args.mode == "train":
        train_model.train_model()
    elif args.mode == "predict":
        predict.predict()



if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    main(production_flag=True)