import numpy as np
from tensorflow.keras.layers import Flatten, Dense, Conv2D, Input, Add, Dense, Activation, BatchNormalization, LeakyReLU
from tensorflow.keras.models import Model
from tensorflow.keras.backend import shape


def residual_layer(x):   # channels last
    x_shortcut = x

    x = Conv2D(filters=256, kernel_size=3, strides=1, padding='same')(x)
    x = BatchNormalization(axis=3)(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = Conv2D(filters=256, kernel_size=3, strides=1, padding='same')(x)
    x = BatchNormalization(axis=3)(x)
    x = LeakyReLU(alpha=0.1)(x)

    x = Add()([x, x_shortcut])

    x = LeakyReLU(alpha=0.1)(x)

    return x

def value_head(x):
    x = Conv2D(filters=1, kernel_size=1, strides=1)(x)
    x = BatchNormalization(axis=3)(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = Flatten()(x)
    x = Dense(256)(x)
    x = Dense(1, activation='tanh')(x)

    return x


def policy_head(x):
    x = Conv2D(filters=2, kernel_size=1, strides=1)(x)
    x = BatchNormalization(axis=3)(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = Flatten()(x)
    x = Dense(6)(x)  # number of possible moves that can be played. Connect four: 6, Chess: 4,672


def build_model():  # TODO: should take input shape as an argument
    a_initial = Input((8,8,45))  # this is arbitrary, input shape is decided by the game
    a = a_initial

    # ====== Initial Convolutional block =======
    a = Conv2D(filters=256, kernel_size=3, strides=1, padding='same')(a)
    a = BatchNormalization(axis=3)(a)
    a = LeakyReLU(alpha=0.1)(a)

    # ======= 5 residual layers =======
    for _ in range(0, 5):
        a = residual_layer(a)

    # ========= Value head ==========
    valueHead = value_head(a)

    # ========= Policy head ==========
    policyHead = policy_head(a)

    model = Model(inputs = a_initial, outputs = [valueHead, policyHead])
    return model
