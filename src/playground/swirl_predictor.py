import torch

from torch import nn
from torchmetrics import Accuracy

import classificators.data_gen as data_gen

RANDOM_SEED = 42
NUM_CLASSES = 4

X, y = data_gen.generate_spiral(RANDOM_SEED)

# Turn data into tensors
X = torch.from_numpy(X).type(torch.float) # features as float32
y = torch.from_numpy(y).type(torch.LongTensor) # labels need to be of type long

# Create train and test splits
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
  X,
  y,
  test_size=0.2,
  random_state=RANDOM_SEED)

device = "cuda" if torch.cuda.is_available() else "cpu"

acc_fn = Accuracy(task="multiclass", num_classes=NUM_CLASSES).to(device)

# Create model by subclassing nn.Module
class SwirlModel(nn.Module):
  def __init__(self, input_features, output_features, hidden_units=8):
    """Initializes multi-class classification model"""
    super().__init__()
    self.linear_layer_stack = nn.Sequential(
      nn.Linear(in_features=input_features, out_features=hidden_units),
      nn.ReLU(),
      nn.Linear(in_features=hidden_units, out_features=hidden_units),
      nn.ReLU(),
      nn.Linear(in_features=hidden_units, out_features=output_features)
    )

  def forward(self, x):
    # Layers are defined inside the Sequencial NN and will be applied here.
    return self.linear_layer_stack(x)

# Instantiate model and send it to device
model_swirl = SwirlModel(
  input_features=2,
  output_features=NUM_CLASSES,
  hidden_units=8).to(device)

loss_fn= nn.CrossEntropyLoss()
optimizer= torch.optim.SGD(params=model_swirl.parameters(), lr=0.1)

# Build a training loop for the model
X_train, X_test, y_train, y_test = X_train.to(device), X_test.to(device), y_train.to(device), y_test.to(device)
epochs= 10000

# Loop over data
for epoch in range(epochs):
  # Training
  model_swirl.train()

  # 1. Forward pass
  y_logits= model_swirl(X_train)
  y_pred_labels= torch.argmax(torch.softmax(y_logits, dim=1), dim=1)

  # 2. Calculate the loss
  loss= loss_fn(y_logits, y_train)
  acc= acc_fn(y_pred_labels, y_train)
  
  # 3. Optimizer zero grad
  optimizer.zero_grad()

  # 4. Loss backward
  loss.backward()

  # 5. Optimizer step
  optimizer.step()

  ## Testing
  model_swirl.eval()
  with torch.inference_mode():
    # 1. Forward pass
    test_logits= model_swirl(X_test)
    test_pred_probs= torch.softmax(test_logits, dim=1)
    test_pred_labels= torch.argmax(test_pred_probs, dim=1)
      
    # 2. Caculate loss and acc
    test_loss= loss_fn(test_logits, y_test)    
    test_acc= acc_fn(test_pred_labels, y_test)
    
  # Print out what's happening every 100 epochs
  if epoch % 100 == 0: 
    print(f"Epoch: {epoch} | Loss: {loss:.5f} Acc: {acc:.2f}% | Test loss: {test_loss:.5f} Test acc: {test_acc:.2f}%")
  