
from pathlib import Path

import torch

import candle
import candle_improve_utils as improve_utils

file_path = Path(__file__).resolve().parent

additional_definitions = [
    {"name": "pred_col_name_suffix",
     "type": str,
     "default": "_pred",
     "help": "Tag to add to predictions when storing the data frame."},
    {"name": "y_col_name",
     "type": str,
     "default": "auc",
     "help": "Drug sensitivity score to use as the target variable (e.g., IC50, AUC)."},
    {"name": "model_arch",
     "default": "GINConvNet",
     "choices": ["GINConvNet", "GATNet", "GAT_GCN", "GCNNet"],
     "type": str,
     "help": "Model architecture to run.", },
    # Preprocessing
    {"name": "download",
     "type": candle.str2bool,
     "default": False,
     "help": "Flag to indicate if downloading from FTP site.",},
    {"name": "set",
     "default": "mixed",
     "choices": ["mixed", "cell", "drug"],
     "type": str,
     "help": "Validation scheme (data splitting strategy).", },
    {"name": "train_split",
        "nargs": "+",
        "type": str,
        "help": "path to the file that contains the split ids (e.g., 'split_0_tr_id',  'split_0_vl_id').", },
    # Training / Inference
    {"name": "log_interval",
     "action": "store",
     "type": int,
     "help": "Interval for saving o/p", },
    {"name": "cuda_name",
     "action": "store",
     "type": str,
     "help": "Cuda device (e.g.: cuda:0, cuda:1."},
    {"name": "train_ml_data_dir",
     "action": "store",
     "type": str,
     "help": "Datadir where train data is stored."},
    {"name": "val_ml_data_dir",
     "action": "store",
     "type": str,
     "help": "Datadir where val data is stored."},
    {"name": "test_ml_data_dir",
     "action": "store",
     "type": str,
     "help": "Datadir where test data is stored."},
    {"name": "model_outdir",
     "action": "store",
     "type": str,
     "help": "Datadir to store trained model."},
    {"name": "model_params",
     "type": str,
     "default": "model.pt",
     "help": "Filename to store trained model."},
    {"name": "pred_fname",
     "type": str,
     "default": "test_preds.csv",
     "help": "Name of file to store inference results."},
    {"name": "response_data",
     "type": str,
     "default": "test_response.csv",
     "help": "Name of file to store inference results."},
    {"name": "out_json",
     "type": str,
     "default": "test_scores.json",
     "help": "Name of file to store scores."},
]

required = [
    "train_data",
    "val_data",
    "test_data",
    # "train_split",
]


class BenchmarkFRM(candle.Benchmark):
    """ Benchmark for FRM. """

    def set_locals(self):
        """ Set parameters for the benchmark.

        Parameters
        ----------
        required: set of required parameters for the benchmark.
        additional_definitions: list of dictionaries describing the additional parameters for the
            benchmark.
        """
        improve_definitions = improve_utils.parser_from_json("candle_improve.json")
        if required is not None:
            self.required = set(required)
        if additional_definitions is not None:
            self.additional_definitions = additional_definitions + improve_definitions


def initialize_parameters(default_model="frm_default_model.txt"):
    """Parse execution parameters from file or command line.

    Parameters
    ----------
    default_model : string
        File containing the default parameter definition.

    Returns
    -------
    gParameters: python dictionary
        A dictionary of Candle keywords and parsed values.
    """

    # Build benchmark object
    frm = BenchmarkFRM(
        file_path,
        default_model,
        "python",
        prog="frm",
        desc="frm functionality",
    )

    # Initialize parameters
    gParameters = candle.finalize_parameters(frm)
    gParameters = improve_utils.build_improve_paths(gParameters)

    return gParameters


def predicting(model, device, loader):
    """ Method to run predictions/inference.
    The same method is in frm_train.py
    TODO: put this in some utils script. --> graphdrp?

    Parameters
    ----------
    model : pytorch model
        Model to evaluate.
    device : string
        Identifier for hardware that will be used to evaluate model.
    loader : pytorch data loader.
        Object to load data to evaluate.

    Returns
    -------
    total_labels: numpy array
        Array with ground truth.
    total_preds: numpy array
        Array with inferred outputs.
    """
    model.eval()
    total_preds = torch.Tensor()
    total_labels = torch.Tensor()
    print("Make prediction for {} samples...".format(len(loader.dataset)))
    with torch.no_grad():
        for data in loader:
            data = data.to(device)
            output, _ = model(data)
            # Is this computationally efficient?
            total_preds = torch.cat((total_preds, output.cpu()), 0)  # preds to tensor
            total_labels = torch.cat((total_labels, data.y.view(-1, 1).cpu()), 0)  # labels to tensor
    return total_labels.numpy().flatten(), total_preds.numpy().flatten()
