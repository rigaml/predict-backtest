# Predict Backtest

This project uses PyTorch to train a neural network on patterns from preprocessed stock data. The trained network is then tested on new, unseen data to validate its accuracy. If the prediction is accurate, a backtesting library is used to simulate the results on future data.

## Installation

Use [Poetry](https://python-poetry.org/), a package dependency manager to install project dependencies:

```bash
poetry install
```

If you want to use your GPU, follow the instructions provided by your computer's GPU vendor to install the corresponding drivers, if not done so before.


Next, create a Jupyter kernel that points to the Poetry environment so you can work with project's installed dependencies in the Jupiter Notebooks in Jupyter later
```bash
poetry run python -m ipykernel install --user --name=<my_pytorch_env>
```

When you run the command to install the kernel (using ipykernel), it registers the kernel with Jupyter by creating a kernel specification file. These kernel spec files are typically stored in a user-specific directory. The exact location depends on your operating system:

On Ubuntu/Linux kernels are in: `~/.local/share/jupyter/kernels/`

You can actually see all the kernels Jupyter knows about by running this command:
```bash
poetry run jupyter kernelspec list
```

### Jupyter Notebook
If you don't have Jupyter Notebook installed in your system, in a separate folder, install it following: 
```bash
python -m venv jupyter_env
source jupyter_env/bin/activate
pip install jupyter
```
Once jupiter environment activated and Jupyter installed open it with:
```bash
jupyter notebook
```
If you created a kernel with this project dependecies as explained in previous steps, you can select it on the top right hand side of the notebook.


## Usage

Create a file `config.json` in the root folder of the project, and add your secret API key got the [Tiingo](https://www.tiingo.com/) API, which is used to download stock data.

```json
{
    "tiingo-key": "your-api-key"
}

```
Open `single_class.ipynb` Jupyter Notebook and follow the instructions to train a neural network. You might need to adjust the download ticker and dates to get your required data. 
After executing the notebook, a file with the resulting neural network will be saved in the `models` folder. Also parameters about training results will be displayed.

The trained network obtained in the previous notebook can be used in `single_class_test.ipynb` to test on unseen data. Adjust the ticker and dates to test on the desired unseen data.  

## Notebooks and Git

Installed [nbstripout](https://github.com/kynan/nbstripout) to clean Jupiter Notebooks output before commiting changes to Git.

Executed command below to setup a Git filter to automatically remove the output cells (such as execution counts, outputs, and other metadata) from Jupyter Notebook files (.ipynb) before they are committed to a Git repository.

```bash
nbstripout --install --attributes .gitattributes
``` 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)