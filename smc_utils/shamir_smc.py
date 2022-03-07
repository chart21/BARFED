import random
from math import ceil
from decimal import Decimal
import shamir as s

def generate_shares(n,m,secret,interpolation_points):
    """
    Split given `secret` into `n` shares with minimum threshold
    of `m` shares to recover this `secret`. Use intperolation_points from array.
    """
    coefficients = s.coeff(m, secret)
    shares = []
 
    for i in range(len(interpolation_points)):
        #x = random.randrange(1, FIELD_SIZE)
        # use fixed interpolation points:
        x = interpolation_points[i]    
        shares.append((x, s.polynom(x, coefficients)))
    #print(shares)
    return shares

def sum_of_secrets_with_SMC(secrets, num_parties):
    interpolation_points = [i for i in range(1,num_parties+1)]
    nump = range(len(secrets))
    shares = []    
    for i in nump:
        # generate secret
        shares.append(generate_shares(len(secrets), len(secrets), secrets[i], interpolation_points))
        
        # send all secrets s[][j] to party j
        # ...
        
        #party sums up all secrets
    sums_of_shares = []
    aggreagated_shares = []       
    
    for i in nump:
        sums_of_shares.append(Decimal(0))
        for j in nump:
            sums_of_shares[i] += Decimal(shares[j][i][1])            
        
        # x is the same for all secrets send to party i,y        
        aggreagated_shares.append( (shares[0][i][0] ,Decimal(sums_of_shares[i])))
        
    # reconstruct secrets   
    #print(aggreagated_shares)

    reconstructed_secret = s.reconstruct_secret(aggreagated_shares)
    
    return reconstructed_secret
    

# def share_weights_with_SMC(models,num_parties,threshold, precision):
#     state_dicts = []    
    
#     state_dicts = [models[i].state_dict() for i in range(len(models))]
    
    
#     save all weights and biases as as secrets 
#     for key in state_dicts[0]:
#         iterate over all elements in all tensors
#         secrets = []
#         elements = []
#         for p in pa: # usually performed at each party individually
#             secrets.append([])
                            
#             for x in np.nditer(state_dicts[p][key]):
#                     secrets[p].append(Decimal(x.item()))
                    
#         engage in secret sharing for each value
        
#         tensor = state_dicts[0][key]    
#         with np.nditer(tensor, op_flags=['readwrite']) as it:  
#             print("before", tensor)
#             i = 0
#             for x in it: # do one shamir's secret sharing per secret
#                 ith_secret_of_all_players = []
#                 for p in pa: # usually performed at each party individually
#                     ith_secret_of_all_players.append(Decimal(secrets[p][i]))                   
#                     print(ith_secret_of_all_players)
#                 sum_of_secret = sum_of_secrets_with_SMC(ith_secret_of_all_players, num_parties)
#                 sum_of_secret /=  num_parties
#                 x[...] = float(sum_of_secret)
#                 x[...] = 5.05
#                     print("after", elements)
                    
#                 i+=1   
#         print(i,"tafter", tensor)
#         state_dicts[0][key] = tensor
#         print(i,"after", state_dicts[0][key])
          

#     load averaged weights and biases
#     for i in range(len(models)):
#         models[i].load_state_dict(state_dicts[0]) 