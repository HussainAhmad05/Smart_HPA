#*********************************************************** Importing Micorservice Managers and Adaptive Resource Manager ***********************************************************************

import time
import os
import subprocess
import multiprocessing
from multiprocessing import Pool
from functools import partial
from frontend import *
from adservice import *
from checkoutservice import *
from currencyservice import *
from emailservice import *
from paymentservice import *
from productcatalogservice import *
from cartservice import *
from recommendationservice import *
from shippingservice import *
from rediscart import *
from Adaptive_Resource_Manager import *




#***************************************************************************** Execute Component *****************************************************************************************

def Execute (microservice_name, desired_replicas):
    execute_command = f"kubectl scale deployment {microservice_name} --replicas={desired_replicas}"
    os.system(execute_command)
    return



def run_function(func):
    return func()




# ********************************************************************** Starting the Smart HPA operation ************************************************************************


#   Initializing Test Time

desired_time = 900     #Total_Test_Time (sec)
start_time = time.time()

if __name__ == '__main__':

    ARM_saved_decision = [[]]         # Adaptive Resource Manager scaling decision and updated maxR details of previous interation

    row_number = 2                    # for storing maximum replicas and desired replicas values in Knowledge Base


    while (time.time() - start_time) < desired_time:

        Test_Time = time.time() - start_time

        # ********************************************************************** Running Microservice Managers Parallely in fully Decentralized manner ************************************************************************

        functions = [partial(frontend, Test_Time), partial(adservice, Test_Time), partial(cartservice, Test_Time), partial(currencyservice, Test_Time), partial(checkoutservice, Test_Time), partial(emailservice, Test_Time), partial(paymentservice, Test_Time), partial(shippingservice, Test_Time), partial(productcatalogservice, Test_Time), partial(recommendationservice, Test_Time), partial(rediscart, Test_Time)]
        with multiprocessing.Pool(processes=len(functions)) as pool:
            microservices_data = pool.map(run_function, functions)              #Getting data from all microservice managers for Microservice Capacity Analyzer


        ARM_decision = []                 # ARM = Adaptive Resource Manager, ARM current scaling decision and maxR details will be saved here
       
        
        
        # **********************************************************************  Microservice Capacity Analyzer ********************************************************************** 

        for i in range(len(microservices_data)):
            if (microservices_data[i][2]>microservices_data[i][5]):        # desirsed replica count > max. replica count, for microservice i;  this represents Resource Constrained Situation

                for i in range(len(microservices_data)):
                    for j in range(len(ARM_saved_decision)):
                        if microservices_data[i][0] == ARM_saved_decision[j][0]:
                            microservices_data[i][5] = ARM_saved_decision[j][3]          # Changing SLA-defined maxR to the ResourceWise maxR of previous ARM decision for each microservice
                    
                ARM_decision = Adaptive_Resource_Manager(microservices_data)                     # Calling Adaptive Resource Manager
                ARM_saved_decision = ARM_decision
                
                break
        
        #When all microservices operate within their resource capacity (i.e., resource-rich environment) -> desirsed replica count < max. replica count
        
        processes = []
        if len(ARM_decision) == 0:                                       

            ARM_saved_decision = microservices_data                          #to equalize the length
            for i in range(len(microservices_data)):
                for j in range(len(ARM_saved_decision)):
                    if microservices_data[i][0] == ARM_saved_decision[j][0]:
                        ARM_saved_decision[j][3] = microservices_data[i][5]
            
            
            for i in range(len(microservices_data)):
                filename = microservices_data[i][0]
                workbook = load_workbook(f'./Knowledge Base/{filename}.xlsx')
                sheet = workbook.active
                sheet.cell(row=row_number, column=5, value=microservices_data[i][5])                            # storing maximum replicas
                sheet.cell(row=row_number, column=6, value=microservices_data[i][1])                            # storing scaling decision
                workbook.save(f'./Knowledge Base/{filename}.xlsx')


                # ************************************************** Executing Scaling Decisions made by Microservice Managers **********************************************************************

                if microservices_data[i][1] != "no scale":
                    process = multiprocessing.Process(target=Execute, args=(microservices_data[i][0], microservices_data[i][2]))
                    processes.append(process)
                    process.start()
            for process in processes:            # Wait for all processes to finish
                process.join()


        # for Resource Constrained Situation, when Adaptive Resource Manager makes changes to max_Replicas and desired replicas 

        else:
            for i in range(len(ARM_decision)):
                filename = ARM_decision[i][0]
                workbook = load_workbook(f'./Knowledge Base/{filename}.xlsx')
                sheet = workbook.active
                sheet.cell(row=row_number, column=5, value=ARM_decision[i][3])                           #storing resource-wise updated maximum replicas in knowledge base
                sheet.cell(row=row_number, column=6, value=ARM_decision[i][1])                           #storing resource-wise scaling decision in knowledge base
                workbook.save(f'./Knowledge Base/{filename}.xlsx')



                # ************************************************** Executing ResourceWise Scaling Decisions made by Adaptive Resource Managers **********************************************************************

                if ARM_decision[i][1] != "no scale":
                    process = multiprocessing.Process(target=Execute, args=(ARM_decision[i][0], ARM_decision[i][2]))
                    processes.append(process)
                    process.start()
            for process in processes:            # Wait for all processes to finish
                process.join()

        row_number = row_number+1

        
        print ("ARM_decision", ARM_decision)
