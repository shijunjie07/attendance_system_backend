# --------------------------
# utils
# @author: Shi Junjie
# Fri 7 June 2024
# --------------------------

import torch
import numpy as np

class Utils:
    
    # h5
    def check_append(dict_to_append:dict) -> tuple[bool, dict]:
        
        keys = ['id', 'embeddings']
        # check if all keys are in the dictionary
        if not all(key in dict_to_append for key in list(dict_to_append.keys())):
            raise ValueError("\'dict_to_append\' should contain keys: \'{}\'".format(keys))

        # check the shapes
        num_entries = None
        for key in keys:
            value = dict_to_append[key]
            if num_entries is None:
                num_entries = value.shape[0]
            else:
                if value.shape[0] == num_entries:
                    continue
                else:
                    raise ValueError(
                        "\'dict_to_append\' key, {}, doest not match shape {}, shape input: {}".format(
                            key, num_entries, value.shape[0]
                        )
                    )

        # filter unwanted keys
        filtered_dict = {key: dict_to_append[key] for key in keys}
        
        return filtered_dict

    # embedding tensor to binary
    def convert_tensor_to_binary(embedding_tensor:torch.Tensor):
        return embedding_tensor.numpy().tobytes()

    # binary to embedding tensor
    def convert_binary_to_tensor(embedding_binary):
        embedding_array = np.frombuffer(embedding_binary, dtype=np.float32)
        embedding_tensor = torch.tensor(embedding_array).view(1, -1)
        return embedding_tensor

# # Example usage
# dict_to_append = {
#     'embeddings': np.ones((3, 4)),
#     'images': np.zeros((3, 4)),
#     'extra_key': np.random.random((4, 4))
# }

# updated_dict = Utils.check_append(dict_to_append)
# print("All keys exist and have the same dimensions:", updated_dict)