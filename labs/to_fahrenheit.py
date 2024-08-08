import random
import os
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt


def to_farenheit(celsius):
    return celsius * 9 / 5 + 32


def generate_data(n):
    data = []
    for i in range(-n, n):
        c = i / 7
        data.append((c, to_farenheit(c)))
    # randomize the array
    random.shuffle(data)
    return data


if __name__ == "__main__":
    # if data.csv does not exist, generate the data
    if not tf.io.gfile.exists("data.csv"):
        print("GENERATING DATA FILE")
        data = generate_data(100000)
        df = pd.DataFrame(data, columns=["c", "f"])
        # save the data to a csv file
        df.to_csv("data.csv", index=False)
    else:
        df = pd.read_csv("data.csv")

    print(df.head())
    # layer = tf.keras.layers.Dense(units=1, input_shape=[1])
    # model = tf.keras.Sequential([layer])
    hidden1 = tf.keras.layers.Dense(units=3, input_shape=[1])
    hidden2 = tf.keras.layers.Dense(units=3)
    out = tf.keras.layers.Dense(units=1)
    model = tf.keras.Sequential([hidden1, hidden2, out])
    model.compile(loss="mean_squared_error", optimizer=tf.keras.optimizers.Adam(0.1))
    checkpoint_path = "./training/cf.weights.h5"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    if not tf.io.gfile.exists(checkpoint_path):
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_path, save_weights_only=True, verbose=1
        )
        print("STRARTING TRAINING...")
        hist = model.fit(
            df["c"], df["f"], epochs=100, verbose=True, callbacks=[cp_callback]
        )
        print("TRAINING FINISHED")

        plt.xlabel("Epoch Number")
        plt.ylabel("Loss Magnitude")
        plt.plot(hist.history["loss"])
        plt.show()
    else:
        print("LOADING MODEL WEIGHTS...")
        model.load_weights(checkpoint_path)

    print("PREDICTING VALUES!!")
    input_data = pd.DataFrame([100.0])
    predicted_value = model.predict(input_data)
    print("{:0.2f}C is {:1.2f}F".format(100.0, predicted_value[0][0]))
