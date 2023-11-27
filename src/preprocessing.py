import torch
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Sample stock data 
data = pd.DataFrame({'Date': [...], 
                     'Close': [100, 102, 106, 110, 105, 102]})  

# Calculate average closing price
data['Avg_Close'] = data['Close'].rolling(5).mean()

# Normalize between 0 and 1  
scaler = MinMaxScaler(feature_range=(0, 1))
data['Normalized_Close'] = scaler.fit_transform(data[['Avg_Close']])

# Final input data
inputs = data[['Normalized_Close']].to_numpy()
targets = data[['Close']].to_numpy()

# Convert to Tensors    
X = torch.Tensor(inputs) 
y = torch.Tensor(targets)

# Define dataset
dataset = Dataset(X, y)
dataloader = DataLoader(dataset, batch_size=64, shuffle=False) 

model = NeuralNetwork()
opt = torch.optim.Adam(model.parameters())

# Train model
for epoch in range(100):
    for batch in dataloader:
        opt.zero_grad()
        
        X_batch, y_batch = batch  
        y_pred = model(X_batch)
        
        loss = loss_fn(y_pred, y_batch)
        loss.backward()
        opt.step()