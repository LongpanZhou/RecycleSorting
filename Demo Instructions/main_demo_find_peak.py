import random
from turtle import color
from matplotlib import style

from rcplant import *

from scipy.signal import argrelextrema # pip install scipy -> https://pypi.org/project/scipy/
import numpy as np # pip install numpy -> https://pypi.org/project/numpy/
from matplotlib import pyplot as plt  # pip install matplotlib -> https://pypi.org/project/matplotlib/

spectra_lst = []

def user_sorting_function(sensors_output):
    # random identification
    sensor_id = 1
    spectrum = sensors_output[1]['spectrum']
    decision = {sensor_id: random.choice(list(Plastic)[0:-1]) for (sensor_id, value) in sensors_output.items()}
    
    if spectrum.iloc[0] == 0:  
        decision = {sensor_id: Plastic.Blank}
    else:  
        spectra_lst.append(sensors_output[sensor_id]['spectrum'])
#---------------------------------------------------------------------------------------------------------
        # Plot spectrum one by one
        # n = 10
        # # comparator = np.greater or np.less, stand for local maxima or minima
        # # order = n, means how many points on each side to use for the comparison to consider
        # # [0] at the end is to access the entire array of local extrema wavenumbers, based on the structure of return value
        # iloc_max_wavenumbers = argrelextrema(spectrum.values, comparator=np.greater, order=n)[0]

        # # Plot the spectrum
        # spectrum.plot()

        # # Plot the local maximum points
        # spectrum.iloc[iloc_max_wavenumbers].plot(title= spectrum.name, style="v", color="red")
        # plt.show()
#---------------------------------------------------------------------------------------------------------
       
    return decision

def plot_local_extrema(spectra):
    n = 10
    for spectrum in spectra:
        if spectrum.name == Plastic.PVC.value:
            # comparator = np.greater or np.less, stand for local maxima or minima
            # order = n, means how many points on each side to use for the comparison to consider
            iloc_max = argrelextrema(spectrum.values, comparator=np.greater, order=10)[0]
            spectrum.plot()
            spectrum.iloc[iloc_max].plot(title= spectrum.name,style="v", color="red")
    plt.show()

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

    print(f'\nResults for running the simulation in "{simulation_mode}" mode:')

    for item_id, result in simulator.identification_result.items():
        print(result)
    
    plot_local_extrema(spectra_lst)


    print(f'Total missed containers = {simulator.total_missed}')
    print(f'Total sorted containers = {simulator.total_classified}')
    print(f'Total mistyped containers = {simulator.total_mistyped}')

    print(f'\n{num_containers} containers are processed in {elapsed_time:.2f} seconds')


if __name__ == '__main__':
    main()
