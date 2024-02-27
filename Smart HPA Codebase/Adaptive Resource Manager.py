
# This file contains the resource-efficient heuristics of Smart HPA, outlining the functionality of Adaptive Resource Manager

import sys
import os
import fnmatch
import glob, os
import subprocess
import math
import numpy as np
import time
import statistics
import openpyxl
import psutil
import matplotlib.pyplot as plt



def Adaptive_Resource_Manager(microservices_data):

    # microservice_data = [microservice_name, SD, DR, CR, CPU request, maxR], ARM is getting this data for each microservice separately


    # ******************************************************************** Microservice Resource Inspector *************************************************************************************

    Underprovisoned_MS = []                         # Underprovisioned Microservices Details
    Overprovisioned_MS = []                         # Overprovisioned Microservices Details

    for i in range(len(microservices_data)):

        if (microservices_data[i][2] > microservices_data[i][5]):     #desired replica count > max replica count

            Required_Replicas = microservices_data[i][2] - microservices_data[i][5]       # desired - max
            Required_CPU = Required_Replicas * microservices_data[i][4]
            Underprovisoned_MS.append ([microservices_data[i][0], Required_Replicas, Required_CPU, microservices_data[i][4], microservices_data[i][3], microservices_data[i][5]])         #(microservive_name, required_replicas, required cpu, CPU request, CR, maxR)

        else:                                                         #max replica count >= desired replica count

            Residual_Replicas = microservices_data[i][5] - microservices_data[i][2]           # max - desired
            Residual_CPU = Residual_Replicas * microservices_data[i][4]
            Overprovisioned_MS.append([microservices_data[i][0], Residual_CPU, microservices_data[i][1], microservices_data[i][2], microservices_data[i][3], microservices_data[i][4], microservices_data[i][5]])     #(microservive_name, residual cpu, SD, DR, CR, CPU request)



    # ******************************************************************** Microservice Resource Balancer *************************************************************************************


    Total_Residual_CPU = 0                                      # Total_Residual_CPU for addressing the needs of underprovisioned microservices

    for i in range(len(Overprovisioned_MS)):
        Total_Residual_CPU = Total_Residual_CPU + Overprovisioned_MS[i][1]                #calculating Total_Residual_CPU possessed by overprovisioned microservices

    ARM_decision = []                                            # ARM current scaling decision details

    Underprovisoned_MS = sorted (Underprovisoned_MS, key=lambda x: x[2], reverse=True)               # Underprovisioned microservices Sorting in descending order based on required resource value (x[2]) to address heavily underprovisioned microservice first

    for i in range(len(Underprovisoned_MS)):
        possible_RR = Total_Residual_CPU / Underprovisoned_MS[i][3]                            #Total application's residual CPU divided by CPU request value for creating possible replicas for microservice i

        if possible_RR >= Underprovisoned_MS[i][1]:                   #possible replicas >= required replicas
            scaling_action = "scale up"
            Feasible_Replicas = ARM_maxR = Underprovisoned_MS[i][1] + Underprovisoned_MS[i][5]           # required replicas + max replicas = desired replicas 
            ARM_decision.append([Underprovisoned_MS[i][0], scaling_action, Feasible_Replicas, ARM_maxR, Underprovisoned_MS[i][3]])
            Total_Residual_CPU = Total_Residual_CPU - (Underprovisoned_MS[i][1] * Underprovisoned_MS[i][3])

        elif possible_RR >=  1 and possible_RR < Underprovisoned_MS[i][1]:     #if possible replicas are in between 1 and required replicas
            scaling_action = "scale up"
            Feasible_Replicas = ARM_maxR = math.floor (possible_RR) + Underprovisoned_MS[i][5]        # max replicas + possible RR
            ARM_decision.append([Underprovisoned_MS[i][0], scaling_action, Feasible_Replicas, ARM_maxR, Underprovisoned_MS[i][3]])
            Total_Residual_CPU = Total_Residual_CPU - (math.floor(possible_RR) * Underprovisoned_MS[i][3])
        
        else:
            if Underprovisoned_MS[i][4] < Underprovisoned_MS[i][5]:
                scaling_action = "scale up"
                Feasible_Replicas = possible_RR = Underprovisoned_MS[i][5]              #feasible replicas = max replicas
                ARM_maxR = Feasible_Replicas

            else:
                scaling_action = "no scale"
                Feasible_Replicas = possible_RR = Underprovisoned_MS[i][4]               #desired = current
                ARM_maxR = Feasible_Replicas
            ARM_decision.append([Underprovisoned_MS[i][0], scaling_action, Feasible_Replicas, ARM_maxR, Underprovisoned_MS[i][3]])  #  Adaptive Scaler 


    # After addressing the needs of underprovisioned microservices, the remaining residual resource is now distributed back to the overprovisioned microservices


    Overprovisioned_MS = sorted (Overprovisioned_MS, key=lambda x: x[1], reverse=False)                  # Overprovisioned microservices Sorting in ascending order based on residual resource value (x[1]) to return resource back to less overprovisioned first
   

    for i in range(len(Overprovisioned_MS)):

        scaling_action = Overprovisioned_MS[i][2]
        Desired_Replicas = Overprovisioned_MS[i][3]

        Remaining_replicas = math.floor(Total_Residual_CPU / Overprovisioned_MS[i][5])        # Total_Residual_CPU divided by resource request value
        possible_RR = Desired_Replicas + Remaining_replicas

        if (possible_RR >= Overprovisioned_MS[i][6]):                                          # Overprovisioned_MS[i][6] = initial maxR (resource capacity) of microservice i
            ARM_maxR = Overprovisioned_MS[i][6]                                               # ARM_maxR is the updated capacity of the microservice i
        elif Remaining_replicas >= 1 and ARM_maxR < Overprovisioned_MS[i][6]:
            ARM_maxR = possible_RR
        else:
            ARM_maxR = Desired_Replicas
        
        Total_Residual_CPU = Total_Residual_CPU - ((ARM_maxR - Desired_Replicas) * Overprovisioned_MS[i][5])

        ARM_decision.append([Overprovisioned_MS[i][0], scaling_action, Desired_Replicas, ARM_maxR, Overprovisioned_MS[i][5]])  #  Adaptive Scaler 

    return ARM_decision           #  Adaptive Scaler return the ARM decision to Execute component