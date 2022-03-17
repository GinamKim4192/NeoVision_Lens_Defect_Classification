from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Concatenate, Dense, AveragePooling2D, BatchNormalization, Flatten, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.resnet import ResNet50

def vgg19(shape, classes):
    model = VGG19(include_top=False, weights=None, input_shape=shape)
    x = model.output
    x = Flatten()(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(256, activation='relu')(x)

    output = Dense(classes, activation='softmax')(x)
    model = Model(model.input, output)
    return model

def resnet(shape, classes):
    model = ResNet50(include_top=False, weights=None, input_shape=shape)
    x = model.output
    x = Flatten()(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(256, activation='relu')(x)

    output = Dense(classes, activation='softmax')(x)
    model = Model(model.input, output)
    return model



def create_poweradeNet(shape, classes):
    input_ = Input(shape=shape)

    before_layer = Conv2D(filters=64, kernel_size=(3, 3), strides=1, activation='relu')(input_)
    before_layer = Conv2D(filters=64, kernel_size=(5, 5), strides=1, activation='relu')(before_layer)
    before_layer = MaxPooling2D(pool_size=2)(before_layer)
    before_layer = BatchNormalization()(before_layer)


    # right_layers
    low_layer = Conv2D(filters=128, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(before_layer)
    low_layer = BatchNormalization()(low_layer)
    low_layer = MaxPooling2D(pool_size=4)(low_layer)


    # left_layers
    deep_layer = Conv2D(filters=128, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(before_layer)
    deep_layer = Conv2D(filters=128, kernel_size=(5, 5), strides=1, activation='relu', padding='same')(deep_layer)
    deep_layer = BatchNormalization()(deep_layer)
    deep_layer = MaxPooling2D(pool_size=2)(deep_layer)

    deep_layer_1 = Conv2D(filters=128, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(deep_layer)
    deep_layer_1 = BatchNormalization()(deep_layer_1)
    deep_layer_1 = MaxPooling2D(pool_size=2)(deep_layer_1)

    deep_layer_2 = Conv2D(filters=128, kernel_size=(5, 5), strides=1, activation='relu', padding='same')(deep_layer)
    deep_layer_2 = BatchNormalization()(deep_layer_2)
    deep_layer_2 = MaxPooling2D(pool_size=2)(deep_layer_2)

    deep_layer_3 = Conv2D(filters=128, kernel_size=(7, 7), strides=1, activation='relu', padding='same')(deep_layer)
    deep_layer_3 = BatchNormalization()(deep_layer_3)
    deep_layer_3 = MaxPooling2D(pool_size=2)(deep_layer_3)

    deep_layer_4 = Conv2D(filters=128, kernel_size=(9, 9), strides=1, activation='relu', padding='same')(deep_layer)
    deep_layer_4 = BatchNormalization()(deep_layer_4)
    deep_layer_4 = MaxPooling2D(pool_size=2)(deep_layer_4)

    deep_concat = Concatenate()([deep_layer_1, deep_layer_2, deep_layer_3, deep_layer_4])

    # right, left concat & Conv
    last_concat = Concatenate()([deep_concat, low_layer])
    last_layer = AveragePooling2D(pool_size=(2, 2), name='last_feature_map')(last_concat)
    flatten_layer = Flatten()(last_layer)
    # Fully Connection
    fc1 = Dense(units=512, activation='relu')(flatten_layer)
    fc2 = Dense(units=256, activation='relu')(fc1)
    output = Dense(units=classes, activation='softmax')(fc2)
    model = Model(inputs=[input_], outputs=[output])

    return model

def create_parisbaguetteNet(shape, classes):
    input_ = Input(shape=shape)

    #start layer
    start_layer = Conv2D(filters=32, kernel_size=(3, 3), strides=1, activation='relu')(input_)
    start_layer = MaxPooling2D(pool_size=(2, 2))(start_layer)
    start_layer = Conv2D(filters=64, kernel_size=(3, 3), strides=1, activation='relu')(start_layer)
    start_layer = MaxPooling2D(pool_size=(2, 2))(start_layer)
    start_layer = Conv2D(filters=128, kernel_size=(3, 3), strides=1, activation='relu')(start_layer)
    start_layer = MaxPooling2D(pool_size=(2, 2))(start_layer)


    #low layer
    low_layer = Conv2D(filters=128, kernel_size=(2, 2), strides=1, activation='relu')(start_layer)
    low_layer = BatchNormalization()(low_layer)
    low_layer = MaxPooling2D(pool_size=(2, 2))(low_layer)




    #dilation layer
    dilation_layer_1 = Conv2D(filters=128, kernel_size = (1, 1), strides=1, activation='relu', dilation_rate=2, padding='same')(start_layer)
    dilation_layer_1 = BatchNormalization()(dilation_layer_1)
    dilation_layer_1 = MaxPooling2D(pool_size=(2, 2))(dilation_layer_1)

    dilation_layer_2 = Conv2D(filters=128, kernel_size = (1, 1), strides=1, activation='relu', dilation_rate=5, padding='same')(start_layer)
    dilation_layer_2 = BatchNormalization()(dilation_layer_2)
    dilation_layer_2 = MaxPooling2D(pool_size=(2, 2))(dilation_layer_2)

    dilation_layer_3 = Conv2D(filters=128, kernel_size = (6, 6), strides=1, activation='relu', dilation_rate=3, padding='same')(start_layer)
    dilation_layer_3 = BatchNormalization()(dilation_layer_3)
    dilation_layer_3 = MaxPooling2D(pool_size=(2, 2))(dilation_layer_3)

    dilation_layer_4 = Conv2D(filters=128, kernel_size = (8, 8), strides=1, activation='relu', dilation_rate=2, padding='same')(start_layer)
    dilation_layer_4 = BatchNormalization()(dilation_layer_4)
    dilation_layer_4 = MaxPooling2D(pool_size=(2, 2))(dilation_layer_4)

    dilation_concat = Concatenate()([dilation_layer_1, dilation_layer_2, dilation_layer_3, dilation_layer_4])
    dilation_concat = BatchNormalization()(dilation_concat)


    #deep_layer
    deep_layer_1 = Conv2D(filters=128, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(start_layer)
    deep_layer_1 = BatchNormalization()(deep_layer_1)
    deep_layer_1 = MaxPooling2D(pool_size=(2, 2))(deep_layer_1)

    deep_layer_2 = Conv2D(filters=128, kernel_size=(5, 5), strides=1, activation='relu', padding='same')(start_layer)
    deep_layer_2 = BatchNormalization()(deep_layer_2)
    deep_layer_2 = MaxPooling2D(pool_size=(2, 2))(deep_layer_2)

    deep_layer_3 = Conv2D(filters=128, kernel_size=(7, 7), strides=1, activation='relu', padding='same')(start_layer)
    deep_layer_3 = BatchNormalization()(deep_layer_3)
    deep_layer_3 = MaxPooling2D(pool_size=(2, 2))(deep_layer_3)

    deep_layer_4 = Conv2D(filters=128, kernel_size=(9, 9), strides=1, activation='relu', padding='same')(start_layer)
    deep_layer_4 = BatchNormalization()(deep_layer_4)
    deep_layer_4 = MaxPooling2D(pool_size=(2, 2))(deep_layer_4)

    deep_concat = Concatenate()([deep_layer_1, deep_layer_2, deep_layer_3, deep_layer_4])
    deep_concat = BatchNormalization()(deep_concat)

    final_concat = Concatenate()([low_layer, dilation_concat, deep_concat])
    final_concat = Conv2D(filter=128, kernel_size=(3, 3), strides=1, activation='relu', padding='valid')(final_concat)
    final_concat = BatchNormalization()(final_concat)
    final_concat = AveragePooling2D(2, name='final_concat')(final_concat)

    flatten_layer = Flatten()(final_concat)
    fc1 = Dense(512, activation='relu')(flatten_layer)
    fc2 = Dense(256, activation='relu')(fc1)
    output = Dense(classes, activation='softmax')(fc2)
    model = Model(inputs=[input_], outputs=[output])

    return model

def create_MangoNet(shape, classes):
    input_ = Input(shape=shape)
    start_layer = Conv2D(filters=32, kernel_size=(3, 3), activation='relu', strides=1)(input_)
    start_layer = MaxPooling2D(pool_size=(2, 2))(start_layer)
    start_layer = BatchNormalization()(start_layer)

    #first_deeplayer
    first_deep_layer1 = Conv2D(filters=64, kernel_size=(3, 3), activation='relu', strides=1, padding='same')(start_layer)
    first_deep_layer1 = MaxPooling2D()(first_deep_layer1)

    first_deep_layer2 = Conv2D(filters=64, kernel_size=(5, 5), activation='relu', strides=1, padding='same')(start_layer)
    first_deep_layer2 = MaxPooling2D()(first_deep_layer2)

    first_deep_layer3 = Conv2D(filters=64, kernel_size=(7, 7), activation='relu', strides=1, padding='same')(start_layer)
    first_deep_layer3 = MaxPooling2D()(first_deep_layer3)

    first_deep_layer4 = MaxPooling2D(pool_size=(2, 2), padding='valid')(start_layer)

    first_deep_concat = Concatenate()([first_deep_layer1, first_deep_layer2, first_deep_layer3, first_deep_layer4])
    first_deep_concat = BatchNormalization()(first_deep_concat)

    #first_dilation_layer
    first_dilation_layer1 = Conv2D(filters=64, kernel_size=(3, 3), activation='relu', strides=1, dilation_rate=2, padding='same')(start_layer)
    first_dilation_layer2 = Conv2D(filters=64, kernel_size=(5, 5), activation='relu', strides=1, dilation_rate=3, padding='same')(start_layer)
    first_dilation_layer3 = Conv2D(filters=64, kernel_size=(7, 7), activation='relu', strides=1, dilation_rate=4, padding='same')(start_layer)
    first_dilation_layer4 = Conv2D(filters=64, kernel_size=(9, 9), activation='relu', strides=1, dilation_rate=5, padding='same')(start_layer)
    first_dilation_concat = Concatenate()([first_dilation_layer1, first_dilation_layer2, first_dilation_layer3, first_dilation_layer4])
    first_dilation_concat = BatchNormalization()(first_dilation_concat)
    first_dilation_concat = MaxPooling2D(pool_size=2)(first_dilation_concat)

    #first_concat
    first_concat = Concatenate()([first_deep_concat, first_dilation_concat])
    first_concat = Conv2D(filters=64, kernel_size=(3, 3), activation='relu', strides=1)(first_concat)
    first_concat = AveragePooling2D(pool_size=(2, 2))(first_concat)

    #second_deep_layer
    second_deep_layer1 = Conv2D(filters=128, kernel_size=(3, 3), activation='relu', strides=1, padding='same')(first_concat)
    second_deep_layer2 = Conv2D(filters=128, kernel_size=(5, 5), activation='relu', strides=1, padding='same')(first_concat)
    second_deep_concat = Concatenate()([second_deep_layer1, second_deep_layer2])
    second_deep_concat = BatchNormalization()(second_deep_concat)

    #second_dilation_layer
    second_dilation_layer1 = Conv2D(filters=128, kernel_size=(3, 3), activation='relu', strides=1, dilation_rate=2, padding='same')(first_concat)
    second_dilation_layer2 = Conv2D(filters=128, kernel_size=(3, 3), activation='relu', strides=1, dilation_rate=4, padding='same')(first_concat)
    second_dilation_concat = Concatenate()([second_dilation_layer1, second_dilation_layer2])
    second_dilation_concat = BatchNormalization()(second_dilation_concat)

    #poolings_layer
    poolings_layer = Conv2D(filters=256, kernel_size=(1, 1), activation='relu', strides=1, padding='same')(start_layer)
    poolings_layer = MaxPooling2D(pool_size=8)(poolings_layer)
    poolings_layer = BatchNormalization()(poolings_layer)

    #second_concat
    second_concat = Concatenate()([second_deep_concat, second_dilation_concat])
    second_concat = Conv2D(filters=256, kernel_size=(1, 1), activation='relu', strides=1)(second_concat)
    second_concat = AveragePooling2D(pool_size=2)(second_concat)

    #third_concat
    third_concat = Concatenate()([second_concat, poolings_layer])
    third_concat = Conv2D(filters=256, kernel_size=(1, 1), strides=(1, 1), activation='relu')(third_concat)

    #fc
    fc = Flatten()(third_concat)
    fc = Dense(512, activation='relu')(fc)
    fc = Dense(256, activation='relu')(fc)

    output = Dense(classes, activation='softmax')(fc)
    model = Model(inputs=[input_], outputs=[output])

    return model

def create_americano(shape, classes):

    input_ = Input(shape=shape)

    start_layer = Conv2D(filters=64, kernel_size=(3, 3), strides=1, activation='relu')(input_)
    start_layer = Conv2D(filters=64, kernel_size=(5, 5), strides=1, activation='relu')(start_layer)
    start_layer = MaxPooling2D(pool_size=2)(start_layer)
    start_layer = BatchNormalization()(start_layer)


    # low_layers
    low_layer = Conv2D(filters=128, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(start_layer)
    low_layer = BatchNormalization()(low_layer)
    low_layer = MaxPooling2D(pool_size=4)(low_layer)


    # dilation_layers
    dilation_layer = Conv2D(filters=128, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(start_layer)
    dilation_layer = Conv2D(filters=128, kernel_size=(5, 5), strides=1, activation='relu', padding='same')(dilation_layer)
    dilation_layer = BatchNormalization()(dilation_layer)
    dilation_layer = MaxPooling2D(pool_size=2)(dilation_layer)

    dilation_layer_1 = Conv2D(filters=128, kernel_size=(3, 3), strides=1, dilation_rate=2, activation='relu', padding='same')(dilation_layer)
    dilation_layer_1 = BatchNormalization()(dilation_layer_1)
    dilation_layer_1 = MaxPooling2D(pool_size=2)(dilation_layer_1)

    dilation_layer_2 = Conv2D(filters=128, kernel_size=(5, 5), strides=1, dilation_rate=2, activation='relu', padding='same')(dilation_layer)
    dilation_layer_2 = BatchNormalization()(dilation_layer_2)
    dilation_layer_2 = MaxPooling2D(pool_size=2)(dilation_layer_2)

    dilation_layer_3 = Conv2D(filters=128, kernel_size=(7, 7), strides=1, dilation_rate=2, activation='relu', padding='same')(dilation_layer)
    dilation_layer_3 = BatchNormalization()(dilation_layer_3)
    dilation_layer_3 = MaxPooling2D(pool_size=2)(dilation_layer_3)

    dilation_layer_4 = Conv2D(filters=128, kernel_size=(9, 9), strides=1, dilation_rate=2, activation='relu', padding='same')(dilation_layer)
    dilation_layer_4 = BatchNormalization()(dilation_layer_4)
    dilation_layer_4 = MaxPooling2D(pool_size=2)(dilation_layer_4)

    dilation_concat = Concatenate()([dilation_layer_1, dilation_layer_2, dilation_layer_3, dilation_layer_4])

    # right, left concat & Conv
    last_concat = Concatenate(name='concat')([dilation_concat, low_layer])
    last_layer = AveragePooling2D(pool_size=(2, 2))(last_concat)
    flatten_layer = Flatten()(last_layer)
    # Fully Connection
    fc1 = Dense(units=512, activation='relu')(flatten_layer)
    fc2 = Dense(units=256, activation='relu')(fc1)
    output = Dense(units=classes, activation='softmax')(fc2)
    model = Model(inputs=[input_], outputs=[output])

    return model



