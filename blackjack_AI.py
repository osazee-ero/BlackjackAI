#%%
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
import os

# os.chdir("C:/Users/Ero/Desktop/ErosAIPortfolio/QLearning")

#%% create sequential model
def sequential_model(data_shape):
    model = keras.models.Sequential()
    model.add(keras.layers.Flatten(input_shape = [data_shape[1]]))
    model.add(keras.layers.Dense(units = 128, activation = "sigmoid"))
    model.add(keras.layers.Dense(units = 128, activation = "sigmoid"))
    model.add(keras.layers.Dropout(0))
    model.add(keras.layers.Dense(units = 2, activation="softmax"))
    return model


#%% run sequential model
def Sequential_model_search(X_train, X_test, y_train, y_test):
    optimizer_ = keras.optimizers.SGD(lr=0.001)
    loss_ = keras.losses.categorical_crossentropy
    BlackJack_AI = sequential_model(X_train.shape)
    print(BlackJack_AI.summary())
    BlackJack_AI.compile(optimizer=optimizer_, loss =loss_ , metrics=["accuracy"])
    calls_back1 = keras.callbacks.ModelCheckpoint('BlackJack_Model.h',save_best_only=True)
    calls_back2 = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    hist = BlackJack_AI.fit(X_train, y_train, batch_size=32, epochs=1000, validation_split=0.2, callbacks=[calls_back1,calls_back2])
    return BlackJack_AI, hist

#%% randomized search model
def build_search_model(n_hidden=1, n_neurons=30, lr = 1e-3, dropout_rate=0.1, activation_="relu", input_shape=[3]):
    model = keras.models.Sequential()
    options = {"input_shape":input_shape}
    for i in range(n_hidden):
        model.add(keras.layers.Dense(units=n_neurons, activation =activation_, **options))
        model.add(keras.layers.Dropout(dropout_rate))
        options={}
    model.add(keras.layers.Dense(units = 2, activation="softmax"))
    loss_ = keras.losses.categorical_crossentropy
    optimizer_ = keras.optimizers.SGD(lr)
    model.compile(optimizer=optimizer_, loss =loss_ , metrics=["accuracy"])
    return model

#%% randomized search model run
def run_search_model(options,model,X_train,y_train):
    sc_model = keras.wrappers.scikit_learn.KerasClassifier(model)
    sc_search = RandomizedSearchCV(sc_model, options, cv=3, n_iter=10)
    calls_back1 = keras.callbacks.ModelCheckpoint('RBlackJack_Model.h',save_best_only=True)
    calls_back2 = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    search = sc_search.fit(X_train,y_train, batch_size=32, epochs=1000, validation_split=0.1, callbacks=[calls_back1,calls_back2])
    results = search.cv_results_
    best_prameters = search.best_params_
    return  results, best_prameters
    

#%% plot of actions in bar chart
def plot_data(data):
    actions = data.iloc[:,-1].values
    rewards = data["reward"]
    total_draws = len(rewards[rewards==0])
    total_wins = len(rewards[rewards==1])
    total_loss = len(rewards[rewards==-1])
    total_hit_actions = len(actions[actions==0])
    total_stand_actions = len(actions[actions==1])
    plt.figure(figsize=(10,10), dpi =100)
    plt.bar(x=[0,1],height=[total_hit_actions,total_stand_actions])
    plt.xticks([0,1],("hit", "stand"))
    plt.xlabel("type of actions")
    plt.ylabel("Number of actions")
    plt.title("Data spread")
    plt.figure(figsize=(10,10), dpi =100)
    plt.bar(x=[0,1,2],height=[total_draws,total_wins,total_loss])
    plt.xticks([0,1,2],("draws", "wins", "loss"))
    plt.xlabel("rewards")
    plt.ylabel("Number of episodes")
    plt.title("Data spread")

#%% model data
def get_train_test_data(data):
    data_label = data[data["reward"]==1]
    actions = data_label.iloc[:,-1].values
    y_label = actions.copy()
    encode = OneHotEncoder()
    y_label = encode.fit_transform(y_label.reshape(-1,1)).toarray()
    X_label = data_label.iloc[:,[0,2,3]].values
    X_train, X_test, y_train, y_test = train_test_split(X_label, y_label, test_size=0.1)
    return X_train, X_test, y_train, y_test
    

#%% predict game
def predict_game(observations):
    AI = keras.models.load_model('BlackJack_Model.h')
    predictions = AI.predict(observations)
    return predictions
    

#%% train model
def train_game():
    data = pd.read_csv("BlackJack_training_data.csv")
    data = data.iloc[:,1:]
    plot_data(data)
    X_train, X_test, y_train, y_test = get_train_test_data(data)
    BlackJack_AI, hist = Sequential_model_search(X_train, X_test, y_train, y_test)
    y_pred_score = BlackJack_AI.evaluate(X_test,y_test)
    print(y_pred_score)
    hist_plot = pd.DataFrame(hist.history).plot(kind='line')
    hist_plot.set_xlabel("epochs")
    hist_plot.set_ylabel("metrics")
    hist_plot.set_title("metrics_plot")   

#%% run random model
# data = pd.read_csv("BlackJack_training_data.csv")
# #plot_data(data)
# data = data.iloc[:,1:]
# X_train, X_test, y_train, y_test = get_train_test_data(data)
# options = {"n_hidden":[1,2,3],
#               "n_neurons":[32,64,128],
#               "lr":[1e-3, 1e-2, 1e-1],
#               "dropout_rate": [0,0.1,0.2],
#               "activation_":['sigmoid', 'relu', 'tanh', 'elu']}

# cv_results, best_prameters = run_search_model(options,build_search_model,X_train,y_train)

#Sequential_model_search(X_train, X_test, y_train, y_test)
# observations = np.array([10, 2, 7]).reshape(1,3)
# action = predict_game(observations)




















