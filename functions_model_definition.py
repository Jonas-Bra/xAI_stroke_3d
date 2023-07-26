import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_probability as tfp
from tensorflow.keras.models import Sequential, Model


# NN Definition
def stroke_binary_3d(input_dim = (128, 128, 28,1), 
                     output_dim = 1,
                     layer_connection = "globalAveragePooling",
                     last_activation = "sigmoid"):
    valid_layer_connection = ["flatten", "globalAveragePooling"]
    if layer_connection not in valid_layer_connection:
        raise ValueError("stroke_binary_3d: layer_connection must be one of %r." % valid_layer_connection)
    valid_activation = ["sigmoid", "linear", "softmax"]
    if last_activation not in valid_activation:
        raise ValueError("stroke_binary_3d: last_activation must be one of %r." % valid_activation)
        
        
#     initializer = keras.initializers.he_normal(seed = 2202)
    
    #input
    inputs = keras.Input(input_dim)
    
    # conv block 0
    x = layers.Convolution3D(32, kernel_size=(3, 3, 3), padding = 'same', activation = 'relu')(inputs)
    x = layers.MaxPooling3D(pool_size=(2, 2, 2))(x)
    
    # conv block 1
    x = layers.Convolution3D(32, kernel_size=(3, 3, 3), padding = 'same', activation = 'relu')(x)
    x = layers.MaxPooling3D(pool_size=(2, 2, 2))(x)
    
    # conv block 2
    x = layers.Convolution3D(64, kernel_size=(3, 3, 3), padding = 'same', activation = 'relu')(x)
    x = layers.MaxPooling3D(pool_size=(2, 2, 2))(x)
    
    # conv block 3
    x = layers.Convolution3D(64, kernel_size=(3, 3, 3), padding = 'same',activation = 'relu')(x)
    x = layers.MaxPooling3D(pool_size=(2, 2, 2))(x)
    
    ## conv block 4
    #x = layers.Convolution3D(256, kernel_size=(3, 3, 3), padding = 'same',activation = 'relu', kernel_initializer = initializer)(x)
    #x = layers.BatchNormalization(center=True, scale=True)(x)
    #x = layers.Convolution3D(256, kernel_size=(3, 3, 3), padding = 'same',activation = 'relu', kernel_initializer = initializer)(x)
    #x = layers.BatchNormalization(center=True, scale=True)(x)
    #x = layers.MaxPooling3D(pool_size=(2, 2, 2), padding='same')(x)
    #x = layers.Dropout(0.3)(x)
    
    
    # cnn to flat connection
    if layer_connection == list(valid_layer_connection)[0]:
        x = layers.Flatten()(x)
    elif layer_connection == list(valid_layer_connection)[1]:
        x = layers.GlobalAveragePooling3D()(x) 
    
    # flat block
    x = layers.Dense(128, activation = 'relu')(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation = 'relu')(x)
    x = layers.Dropout(0.3)(x)
    
    if last_activation == list(valid_activation)[0]:
        out = layers.Dense(units=output_dim, activation = last_activation)(x) # sigmoid
    elif last_activation == list(valid_activation)[1]:
        out = layers.Dense(units=output_dim, activation = last_activation, use_bias = False)(x) # linear
    elif last_activation == list(valid_activation)[2]:
        out = layers.Dense(units=output_dim, activation = last_activation)(x) # softmax (output_dim must be at least 2)
    
    
    # Define the model.
    model_3d = Model(inputs=inputs, outputs=out, name = "cnn_3d_")
    
    return model_3d

def model_setup(version, input_dim = (128, 128, 28, 1)):

    if "sigmoid" in version or "andrea_split" in version:
        last_activation = "sigmoid"
        output_dim = 1
        LOSS = "binary_crossentropy"
    elif "softmax" in version:
        last_activation = "softmax"
        output_dim = 2
        LOSS = tf.keras.losses.categorical_crossentropy
        
    if version.endswith("f"):
        layer_connection = "flatten"
    else:
        layer_connection = "globalAveragePooling"
        
    return input_dim, output_dim, LOSS, layer_connection, last_activation

def set_generate_model_name(model_version, layer_connection, last_activation, path):
    def generate_model_name(which_split, model_nr):
        if layer_connection == "globalAveragePooling":
            return (path + "3d_cnn_binary_model_split" + str(which_split) + 
                    "_unnormalized_avg_layer_paper_model_" + last_activation + 
                    "_activation_"  + str(model_version) + str(model_nr) + ".h5")
        elif layer_connection == "flatten":
            return (path + "3d_cnn_binary_model_split" + str(which_split) + 
                    "_unnormalized_flat_layer_paper_model_" + last_activation + 
                    "_activation_" + str(model_version) + str(model_nr) + ".h5")
            
    return generate_model_name

# def define_model(input_dim = (128, 128, 28,1), 
#                  layer_connection = "globalAveragePooling",
#                  activation = "ontram"):
#     valid_layer_connection = ["flatten", "globalAveragePooling"]
#     if status not in valid_layer_connection:
#         raise ValueError("stroke_binary_3d: layer_connection must be one of %r." % valid_layer_connection)
#     valid_activation = ["sigmoid", "ontram"]
#     if status not in valid_activation:
#         raise ValueError("stroke_binary_3d: ontram must be one of %r." % valid_activation)
