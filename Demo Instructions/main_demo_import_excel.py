import random

from rcplant import *
import os
import pandas as pd # pip install pandas -> https://pypi.org/project/pandas/
import numpy as np # pip install numpy -> https://pypi.org/project/numpy/

def import_excel():
    # First need to put excel file under the same folder as main.py
    data_file = os.path.join(os.path.dirname(__file__), 'demo_import.xlsx') 
    # Use pandas to read the entire table
    data_table = pd.read_excel(data_file, sheet_name=0, index_col=0)

    # Use .loc[] the spectra you want to retrieve
    average_spectrum = data_table.loc['PP_AVERAGE']
# OR
    # You could also import raw spectrum and calculate the average by .mean()
    raw_spectrum = data_table.loc['PP']
    # calculate the average value
    average_value = raw_spectrum.mean()
    # retrieve the list of wavenumbers from raw_spectrum
    wavenumbers_list = list(raw_spectrum.keys())
    # then create the corresponding average value (transmittance) list
    average_value_list = [average_value for i in range(len(wavenumbers_list))]
    # Construct the average value list and wavenumber list into a pandas.Series 
    average_spectrum_2 = pd.Series(data=average_value_list, index=wavenumbers_list)
    return average_spectrum_2

def user_sorting_function(sensors_output):
    # random identification
    decision = {sensor_id: random.choice(list(Plastic)) for (sensor_id, value) in sensors_output.items()}
    
    # If you have made some data in excel (e.g. average PP spectrum) 
    # and want to import to sorting function
    average_PP = import_excel()
    print(f'\nImport excel successfully: average_PP is {average_PP}')

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

    print(f'\nResults for running the simulation in "{simulation_mode}" mode:')

    for item_id, result in simulator.identification_result.items():
        print(result)

    print(f'Total missed containers = {simulator.total_missed}')
    print(f'Total sorted containers = {simulator.total_classified}')
    print(f'Total mistyped containers = {simulator.total_mistyped}')

    print(f'\n{num_containers} containers are processed in {elapsed_time:.2f} seconds')


if __name__ == '__main__':
    main()
