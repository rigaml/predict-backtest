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
for Fibonacci=[1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]
Example: 2584 / 26 = 99 days (if 15min)
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

### Run PyTests

-In PowerShell add current folder to PYTHONPATH
Doc: Mio\Learn\Computers\Tutorials\python-tutorial.txt

```bash
pytest
pytest path/to/test_file.py::test_name
pytest -k <matching-test-function-name>
```

If getting: ModuleNotFoundError: No module named 'modules'

```powershell
$Env:PYTHONPATH = ".\"
Echo $Env:PYTHONPATH
```
