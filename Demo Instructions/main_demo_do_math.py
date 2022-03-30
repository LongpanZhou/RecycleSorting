import random

from rcplant import *
import numpy as np
import pandas as pd
import os

spectrum_addition = 0
spectrum = 0
average_spectrum = 0

def user_sorting_function(sensors_output):
    global spectrum_addition
    global spectrum
    global average_spectrum

    # random identification
    sensor_id = 1
    decision = {sensor_id: random.choice(list(Plastic)) for (sensor_id, value) in sensors_output.items()}
   
    if sensors_output[1]['spectrum'].iloc[0] == 0:  
        decision = {sensor_id: Plastic.Blank}
    else:   # Only do math on containers' spectra

        # Get pandas.Series spectrum
        spectrum = sensors_output[sensor_id]['spectrum']

        # Get external average spectrum in pandas.Series
        average_value = spectrum.mean()
        wavenumber_list = list(spectrum.keys())
        average_value_list = [average_value for i in range(len(wavenumber_list))]
        average_spectrum = pd.Series(data=average_value_list, index=wavenumber_list)

        # exponentials
        spectrum_exp = np.exp(spectrum)
        #print(spectrum_exp)

        # addition
        spectrum_addition = spectrum + average_spectrum

        # subtraction
        spectrum_subtraction = spectrum - average_spectrum
        #print(spectrum_subtraction)

        # sum/subtract/squares 
        # e.g. sum of squares error (difference between sensor read and average spectrum)
        spectrum_sse = np.sum(np.square(spectrum - average_spectrum))
        #print(spectrum_sse)

        # greater than, less than, greater than or equal to, less than or equal to
        # print(spectrum.gt(average_spectrum))
        # print(spectrum.lt(average_spectrum))
        # print(spectrum.ge(average_spectrum))
        # print(spectrum.le(average_spectrum))
        # print(pd.concat([average_spectrum, spectrum]))
    
    return decision


def main():

    # simulation parameters
    conveyor_length = 1000  # cm
    conveyor_width = 100  # cm
    conveyor_speed = 10  # cm per second
    num_containers = 100
    sensing_zone_location_1 = 500  # cm
    sensors_sampling_frequency = 1  # Hz
    simulation_mode = 'training'

    sensors = [
        Sensor.create(SpectrumType.FTIR, sensing_zone_location_1),
    ]

    conveyor = Conveyor.create(conveyor_speed, conveyor_length, conveyor_width)

    simulator = RPSimulation(
        sorting_function=user_sorting_function,
        num_containers=num_containers,
        sensors=sensors,
        sampling_frequency=sensors_sampling_frequency,
        conveyor=conveyor,
        mode=simulation_mode
    )

    elapsed_time = simulator.run()

    print(f"spectrum is \n {spectrum} \naverage spectrum is \n{average_spectrum}")
    print(f"sum of the spectrum is \n{spectrum_addition}")

    #print(f'\nResults for running the simulation in "{simulation_mode}" mode:')

    # for item_id, result in simulator.identification_result.items():
    #     print(result)

    # print(f'Total missed containers = {simulator.total_missed}')
    # print(f'Total sorted containers = {simulator.total_classified}')
    # print(f'Total mistyped containers = {simulator.total_mistyped}')

    print(f'\n{num_containers} containers are processed in {elapsed_time:.2f} seconds')


if __name__ == '__main__':
    main()
