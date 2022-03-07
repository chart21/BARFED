# calculate averaged weight of a model without SMC
import torch
from decimal import Decimal
import shamir_smc as ss

def share_weights(models):
    state_dicts = []
    
    state_dicts = [models[i].state_dict() for i in range(len(models))]
    for key in state_dicts[0]:
        #print(0,state_dicts[0][key])
        for i in range(1,len(models)):
        #for i in range(len(models)):
            #print(i,state_dicts[i][key])
            state_dicts[0][key] += state_dicts[i][key]
            
        state_dicts[0][key] /= len(models)
        #print(0,state_dicts[0][key])
    for i in range(len(models)):
        models[i].load_state_dict(state_dicts[0]) 


def update_main_model(main_model,
                                                                                                       model_dict,                                                                                                       
                                                                                                       device):
    mean_weight_array = get_averaged_weights_without_smc(model_dict, device)
    main_model_param_data_list = list(main_model.parameters())
    with torch.no_grad():
        for j in range(len(main_model_param_data_list)):
            main_model_param_data_list[j].data = mean_weight_array[j]
    return main_model


def get_averaged_weights_without_smc(model_dict, device):
    #chosen_clients = iteration_distance[iteration_distance["include_calculation"] == True].index
    name_of_models = list(model_dict.keys())
    parameters = list(model_dict[name_of_models[0]].named_parameters())

    ### mesela conv 1 için zeros [chosen client kadar, 32, 1, 5, 5] atanıyor bunları doldurup mean alacağız
    weight_dict = dict()
    for k in range(len(parameters)):
        name = parameters[k][0]
        w_shape = list(parameters[k][1].shape)
        w_shape.insert(0, len(name_of_models))
        weight_info = torch.zeros(w_shape, device=device)
        weight_dict.update({name: weight_info})

    weight_names_list = list(weight_dict.keys())
    with torch.no_grad():
        for i in range(len(name_of_models)):
            sample_param_data_list = list(model_dict[name_of_models[name_of_models[i]]].parameters())
            for j in range(len(weight_names_list)):
                weight_dict[weight_names_list[j]][i,] = sample_param_data_list[j].data.clone()

        mean_weight_array = []
        for m in range(len(weight_names_list)):
            mean_weight_array.append(torch.mean(weight_dict[weight_names_list[m]], 0))

    return mean_weight_array


def get_averaged_weights_with_smc(model_dict, device):
    #chosen_clients = iteration_distance[iteration_distance["include_calculation"] == True].index
    name_of_models = list(model_dict.keys())
    num_parties = len(name_of_models)
    parameters = list(model_dict[name_of_models[0]].named_parameters())

    ### mesela conv 1 için zeros [chosen client kadar, 32, 1, 5, 5] atanıyor bunları doldurup mean alacağız
    weight_dict = dict()
    for k in range(len(parameters)):
        name = parameters[k][0]
        w_shape = list(parameters[k][1].shape)
        w_shape.insert(0, len(name_of_models))
        weight_info = torch.zeros(w_shape, device=device)
        weight_dict.update({name: weight_info})

    weight_names_list = list(weight_dict.keys())
    with torch.no_grad():
        for i in range(len(name_of_models)):
            sample_param_data_list = list(model_dict[name_of_models[name_of_models[i]]].parameters())
            for j in range(len(weight_names_list)):
                weight_dict[weight_names_list[j]][i,] = sample_param_data_list[j].data.clone()

        mean_weight_array = []
        for m in range(len(weight_names_list)):
            #mean_weight_array.append(torch.mean(weight_dict[weight_names_list[m]], 0))
            ith_secret_of_all_players = []
            for x in weight_dict[weight_names_list[m]]:
                ith_secret_of_all_players.append(Decimal(x))                   
                    #print(ith_secret_of_all_players)
            sum_of_secret = ss.sum_of_secrets_with_SMC(ith_secret_of_all_players, num_parties)
            sum_of_secret /=  num_parties
            mean_weight_array.append(float(sum_of_secret))


    return mean_weight_array