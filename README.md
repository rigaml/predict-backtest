## SETUP

Strip out Jupyter Notebooks cells execution output
C:\Users\User\AAAMio\Projects\riga-stock-nn\.git\hooks\pre-commit.bat



### Training

Open Jupyter Notebook:
In Windows open Anaconda Prompt:

```powershell
cd C:\Users\User\AAAMio\Projects\PyTorch
conda activate pytorch
python -m jupyter notebook
```

In web browser open the right Jupyter notebook

### Test

Run app:
In Windows open Anaconda Prompt:

````powershell
cd C:\Users\User\AAAMio\Projects\riga-stock-backpy-run\src
conda activate pytorch
python single-run-nn.py
```powershell

Unit tests: In Powershell window
```
pytest
```

## TODO

Create simple NN with data
+Execute PyTorch program locally - without Notebook
+How to calculate data series
load data from SQL
calculate other input parameters
normalize
iterate until training finish
iterate until buy/sell signal
if buy then find point of sell and calculate benefit
if sell then find point of buy and calculate benefit
(once found store point of sell/buy and only change if over the date)
(later: use Kelly formula depending on probability from NN to decide how much to invest/bet sizing)
update network weights

-STOCK: Classification: Focus in 1 buy/sell decision, don't follow the stock
Make simple version work with your own CPU
Instead of buy/sell a percent just decide if buy/sell everything.
Set a random date start and a random investment period.
If decide to buy/sell at the start then has all the period to sell/buy. Once sold/bought stop and try another buy/sell period. If don't sell before end date force sell at the end. If don't buy at the end of the period leave it like that, as maybe company going down and should not buy more
+Only decide if buy first point of the period if don't buy go for another period. Not going further in the period so no problem that we buy too late and no time to sell
Inputs:
+Open, close, min, max, volume:
difference between last tick and the mean with the last fibonnaci numbers ticks
for Fibonacci=[1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584] -> len=17 \* 1 / 3 = 5.6 -> 6 fibonacci = 13
Example: 2584 / 26 = 99 days (if 15min) -> predict day then window 26
+Time in the period
0..1 day seconds 0..86400
0..1 week day 1..5
0..1 month day 1..31
0..1 year month 1..12
0..1 century year 2010..2030
+Close and Volume most important ?
+ARK as index: Open, close, min, max, volume
+ArkBoughtSUM(Fibonacci numbers)
+Comapre results using StdDev or entropy for Close: which one works better?
+Use Tiingo feed to get Fundamental Data
https://www.tiingo.com/documentation/fundamentals
+What have in the Excel with parameters you created
+What have when calculating Ark totals?
+Want to build a pytorch classification model to predict if should buy, sell or hold a stock. what input parameters should I use to increase the likelyhood of the prediction
-> See 0000-CORD\Projects\0001-2020-10-15-Python-stock\classification-model-predict-stocks.txt
TODO:
-Test if network can learn circles dummy data
-Shuffle the data
-Normalize input
-Add RSI

\*(STOCK:Classification problem
-Signals
+Buy20 if reaches +20% in the period
+Buy30 if reaches +30% in the period (if reaches this don't set Buy20)
...
-Signals2
+Buy15 if over +15% in 60% of the points in the period to predict
+Buy20 if over +20% in 60% of the points in the period to predict
-Calculate the distribution of 10, 20, 30 percent over
+Categoties Buy20, Buy30...Sell20, Sell30... should be equally represented, otherwise remove if never reached
-What if something is over 10% of the time and down 60% time
-How many days in the future can we predict? Should be short as using ticks
3/4 of the observations should be at the same distance of the period we want to predict
-Can shuffle the observations in training as not dependant of time
-Add stop for over fitting when test goes down

\*)STOCK:Classification problem

### 2023-11-28 Experiment 1:

#### SETUP:

2 days after a point predict if % price is doing down or up the amounts percentage
classes_window= 52
down_pcts= [5, 10, 20, 30]
up_pcts= [5, 10, 20, 30]

Classes are not very well distributed as very few cases over 10% or below 10%
0% change (4): 5013 times 28.83%
-5% change (3): 4273 times 24.57%
10% change (6): 2049 times 11.78%
5% change (5): 3258 times 18.74%
20% change (7): 426 times 2.45%
-10% change (2): 2029 times 11.67%
-20% change (1): 175 times 1.01%
-30% change (0): 17 times 0.10%
30% change (8): 97 times 0.56%
0% change (nan): 52 times 0.30%

Using 15min data from 2021-01-01 to 2023-11-11
Stock ticks: 17389

Follow percentages between fibonacci progression and last value observed
signal_windows= [2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]

#### RESULT: Network can't predict on test cases more than 20%

### 2023-11-28 Experiment 2:

#### SETUP:

2 days after a point predict if % price is doing down or up the amounts percentage
classes_window= 52
down_pcts= [5, 10, 15]
up_pcts= [5, 10, 15]

Classes are better distributed as class with minimum values has 4% of the cases
0% change (3): 5013 times 28.83%
-5% change (2): 4273 times 24.57%
10% change (5): 1455 times 8.37%
15% change (6): 1117 times 6.42%
5% change (4): 3258 times 18.74%
-10% change (1): 1511 times 8.69%
-15% change (0): 710 times 4.08%
0% change (nan): 52 times 0.30%

Follow percentages between fibonacci progression and last value observed
signal_windows= [2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]

#### RESULT: Network can't predict on test cases more than 20%

### 2023-11-28 Experiment 3:

Tried with multiple network configuration. Last network configuration
self.linear_layer_stack = nn.Sequential(
nn.Linear(in_features=input_features, out_features=hidden_units*3),
nn.ReLU(),
nn.Linear(in_features=hidden_units*3, out_features=hidden_units\*2),
nn.ReLU(),
nn.Linear(in_features=hidden_units\*2, out_features=hidden_units),
nn.ReLU(),
nn.Linear(in_features=hidden_units, out_features=hidden_units),
nn.ReLU(),
nn.Linear(in_features=hidden_units, out_features=output_features)
)

Never arrived more than
Epoch: 1800 | Loss: 1.74498 Acc: 29.47% | Test loss: 1.84765 Test acc: 29.14%
and the end of the training was worst
Epoch: 9900 | Loss: 0.90309 Acc: 64.75% | Test loss: 4.28144 Test acc: 14.84%

### 2023-11-28 Experiment 4:

Using 15min data for DNA from 2021-01-01 to 2023-11-11
classes_window= 52
down_pcts= [7]
up_pcts= [7]
Stock ticks: 17389

Network:
self.linear_layer_stack = nn.Sequential(
nn.Linear(in_features=input_features, out_features=hidden_units*3),
nn.ReLU(),
nn.Linear(in_features=hidden_units*3, out_features=hidden_units*2),
nn.ReLU(),
nn.Linear(in_features=hidden_units*2, out_features=hidden_units),
nn.ReLU(),
nn.Linear(in_features=hidden_units, out_features=output_features)
)

def forward(self, x): # print("forward x: ",", ".join([str(num) for num in x.tolist()])) # Layers are defined inside the Sequencial NN and will be applied here.
return self.linear_layer_stack(x)

Create an instance of the model

model_0 = StockModelV0(
input_features=len(signal_windows),
output_features=len(down_pcts)+ 1 + len(up_pcts),
hidden_units=10).to(device)

If results are better than 33% is better than random as have 3 classes
Epoch: 8000 | Loss: 0.70446 Acc: 68.65% | Test loss: 1.62542 Test acc: 33.82%
Epoch: 8100 | Loss: 0.69133 Acc: 69.08% | Test loss: 1.72108 Test acc: 39.11%
Epoch: 8200 | Loss: 0.78392 Acc: 63.95% | Test loss: 1.37342 Test acc: 40.26%
Epoch: 8300 | Loss: 0.75909 Acc: 65.67% | Test loss: 1.49493 Test acc: 42.60%
Epoch: 8400 | Loss: 0.74101 Acc: 66.32% | Test loss: 1.49026 Test acc: 44.80%
Epoch: 8500 | Loss: 0.75523 Acc: 65.70% | Test loss: 1.51375 Test acc: 41.95%
Epoch: 8600 | Loss: 0.68539 Acc: 68.69% | Test loss: 1.73102 Test acc: 36.63%
Epoch: 8700 | Loss: 0.71132 Acc: 68.19% | Test loss: 1.73028 Test acc: 38.46%
Epoch: 8800 | Loss: 0.74169 Acc: 66.49% | Test loss: 1.82253 Test acc: 38.22%
Epoch: 8900 | Loss: 0.72336 Acc: 67.32% | Test loss: 1.52088 Test acc: 44.49%
Epoch: 9000 | Loss: 0.73710 Acc: 66.02% | Test loss: 1.75515 Test acc: 42.36%
Epoch: 9100 | Loss: 0.72732 Acc: 66.81% | Test loss: 1.64465 Test acc: 41.51%
Epoch: 9200 | Loss: 0.71473 Acc: 67.24% | Test loss: 1.53813 Test acc: 42.93%
Epoch: 9300 | Loss: 0.64843 Acc: 71.04% | Test loss: 1.51958 Test acc: 38.97%
Epoch: 9400 | Loss: 0.67889 Acc: 69.40% | Test loss: 1.75680 Test acc: 41.38%
Epoch: 9500 | Loss: 0.65562 Acc: 70.78% | Test loss: 1.85222 Test acc: 41.04%
Epoch: 9600 | Loss: 0.63777 Acc: 73.12% | Test loss: 1.73177 Test acc: 41.27%
Epoch: 9700 | Loss: 0.68250 Acc: 70.90% | Test loss: 1.67650 Test acc: 40.05%
Epoch: 9800 | Loss: 0.72190 Acc: 66.28% | Test loss: 1.80084 Test acc: 39.04%
Epoch: 9900 | Loss: 0.68861 Acc: 68.91% | Test loss: 1.82891 Test acc: 38.60%

+Claude: Epoch 9300 has the lowest test loss value of 1.51958 amongst all epochs. Lower test loss implies better generalization.
+Copilot: From the data you’ve provided, it seems that the model performs best on the test set at epoch 8400, where the test accuracy is highest at 44.80%. However, it’s important to note that the model’s performance on the training set is still improving beyond this point, suggesting that the model may continue to learn useful representations if trained for more epochs. However, the increasing gap between the training accuracy and the test accuracy, as well as the increasing test loss, suggest that the model may be overfitting to the training data. Therefore, based on this information, epoch 8400 might be a good point to stop training and use the network configuration, as it offers a good balance between underfitting and overfitting.

### 2023-11-29 Experiment 5:

self.linear_layer_stack = nn.Sequential(
nn.Linear(in_features=input_features, out_features=hidden_units*8),
nn.Tanh(),
nn.Linear(in_features=hidden_units*8, out_features=hidden_units*4),
nn.Tanh(),
nn.Linear(in_features=hidden_units*4, out_features=hidden_units*2),
nn.Tanh(),
nn.Linear(in_features=hidden_units*2, out_features=hidden_units),
nn.Tanh(),
nn.Linear(in_features=hidden_units, out_features=1)
)

Epoch: 9900 | Loss: 0.68638 Acc: 54.93% | Test loss: 0.68470 Test acc: 57.97%

2023-12-01 Experiment 6:
Getting 15 min ticks for DNA from 2021-04-01 to 2023-11-11
classes_window= 52
down_pcts= [7]
up_pcts= [7]
signal_windows= [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
After 600 iterations with randomly shuffle samples and using batches:
Epoch: 420 | Loss: 0.66522 Acc: 58.00% | Test loss: 0.68317 Test acc: 58.69%

2023-12-01 Experiment 7:
Getting 5 min ticks for DNA from 2022-01-01 to 2023-11-30
classes_window= 80
down_pcts= [5]
up_pcts= [7]
Total: 38688
47.31% 18303 times 0% change (1)
18.92% 7318 times 7% change (2)
33.57% 12987 times -5% change (0)
0.21% 80 times 0% change (nan)

signal_windows= [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]

After cutting ends and make classes even
Total: 14631
25.00% 3658 times -5% change (0)
25.00% 3658 times 0% change (1)
50.00% 7315 times 7% change (2)

self.linear_layer_stack = nn.Sequential(
nn.Linear(in_features=input_features, out_features=hidden_units*8),
nn.Tanh(),
nn.Linear(in_features=hidden_units*8, out_features=hidden_units*4),
nn.Tanh(),
nn.Linear(in_features=hidden_units*4, out_features=hidden_units*2),
nn.Tanh(),
nn.Linear(in_features=hidden_units*2, out_features=hidden_units),
nn.Tanh(),
nn.Linear(in_features=hidden_units, out_features=1)

loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(params=model_0.parameters(), lr=0.07)
accuracy_fn= Accuracy(task='binary').to(device)

After 600 iterations with randomly shuffle samples and using batches:
Last Loss: 0.69126 Acc: 51.44% | Test loss: 0.70031 Test acc: 51.67%
After another 600 iterations maximum achieved
Epoch: 540 | Loss: 0.69090 Acc: 51.66% | Test loss: 0.70022 Test acc: 51.98%

### 2023-12-11 Experiment 8:

#### SETUP:

2 days after a point predict if % price is doing down or up the amounts percentage
classes_window= 52
down_pcts= [7]
up_pcts= [7]

Using 15min data for DNA from 2021-01-01 to 2023-11-11

Total: 17389
46.63% 8109 times 0% change (1)
27.36% 4757 times -7% change (0)
25.71% 4471 times 7% change (2)
0.30% 52 times 0% change (nan)

signal_windows= [2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]
signals_calculator = signals_calc.SignalsCalc(signal_windows)

Network:
self.linear_layer_stack = nn.Sequential(
nn.Linear(in_features=input_features, out_features=hidden_units*16),
nn.LeakyReLU(negative_slope=0.1),
nn.Linear(in_features=hidden_units*16, out_features=hidden_units*8),
nn.LeakyReLU(negative_slope=0.1),
nn.Linear(in_features=hidden_units*8, out_features=hidden_units*4),
nn.LeakyReLU(negative_slope=0.1),
nn.Linear(in_features=hidden_units*4, out_features=hidden_units),
nn.LeakyReLU(negative_slope=0.1),
nn.Linear(in_features=hidden_units, out_features=1)
)
model_0 = StockModelBinaryV0(
input_features=len(signal_windows),
hidden_units=12).to(device)

loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(params=model_0.parameters(), lr=0.1)
accuracy_fn= Accuracy(task='binary').to(device)

#### RESULTS:

2023-12-11-DNA-from20210101-to20231111-in16-hid12-result9361pct.pth
Epoch: 590 | Loss: 0.07311 Acc: 96.95% | Test loss: 0.23384 Test acc: 95.48%
Last Loss: 0.06744 Acc: 97.29% | Test loss: 0.24610 Test acc: 93.61%

## TODO:

-How to use transforms
-How to use the DataLoader and batches
-Use the RSI see if it works
-Check which don't match. ie. says positive but is negative or the opposite without counting as a failure the positive to neutral and negative to neutral
-Reload and save network with higher test acc

### Run PyTests

-In PowerShell add current folder to PYTHONPATH
Doc: Mio\Learn\Computers\Tutorials\python-tutorial.txt

```bash
pytest
pytest path/to/test_file.py::test_name
pytest -k <matching-test-function-name>
````

If getting: ModuleNotFoundError: No module named 'modules'

```powershell
$Env:PYTHONPATH = ".\"
Echo $Env:PYTHONPATH
```
