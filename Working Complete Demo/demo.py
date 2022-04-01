from pprint import pp
from matplotlib import pyplot as plt
import numpy
from rcplant import *
import pandas as pd
import numpy as np
import random
import os
#checking functions

#PVC has max index between 1250 and 1275 (Unique)
def is_PVC(spectrum):
    decision = False
    if 1250 < spectrum.idxmax() < 1275:
        decision = True
    return decision

#PVC has max index between 1400 and 1500 (Unique)
def is_PS(spectrum):
    decision = False
    if 1400 < spectrum.idxmax() < 1500:
        decision = True
    return decision

#PP HPDE LDPE has max index between 2850 and 2950
def is_PP_HPDE_LDPE(spectrum):
    decision = False
    if 2850 < spectrum.idxmax() < 2950:
        decision = True
    return decision

#PC PU PET Polyester has max index between 1700 and 1800 or at 1250
def is_PC_PU_PET_Polyester(spectrum):
    decision = False
    if 1700 < spectrum.idxmax() < 1800 or spectrum.idxmax() == 1250:
        decision = True
    return decision

#PU has a local max between 3300 and 3400 (Unique)
def is_PU(spectrum):
    decision = False
    spectrum_zoomin = spectrum.loc[3500:3050]
    if 3300 < spectrum_zoomin.idxmax() < 3400:
        decision = True
    return decision

#PET Polyester has a local max between 1250 - 1300
def is_PET_Polyester(spectrum):
    decision = False
    spectrum_zoomin = spectrum.loc[1700:1250]
    if spectrum_zoomin.idxmax() < 1300:
        decision = True
    return decision

#import data base from excel sheet
#Note:I calculated the avg of different material
def import_excel(x):
    data_file = os.path.join(os.path.dirname(__file__), 'FTIR Plastic Database.xlsx')
    data_table = pd.read_excel(data_file, sheet_name=0, index_col=0)
    raw_spectrum = data_table.loc[x]
    return raw_spectrum;

#import data
Data = [import_excel('HDPE'),import_excel('LDPE'),import_excel('PP'),import_excel('LDPE'),import_excel('PC'),import_excel('PVC'),import_excel('Polyester'),import_excel('PET'),import_excel('PU')]
spectra_lst = []

def plot_spectra():
    plt.figure()

    # retrieve 9 types of plastic and plot them seperately
    for spectrum in spectra_lst:
        plastic = spectrum.name
        if plastic == Plastic.PET.value:
            plt.subplot(331)
            spectrum.plot(title= plastic, xlabel='Wavenumber', ylabel='Transmittance')
        elif plastic == Plastic.HDPE.value:
            plt.subplot(332)
            spectrum.plot(title= plastic, xlabel='Wavenumber', ylabel='Transmittance')
        elif plastic == Plastic.PVC.value:
            plt.subplot(333)
            spectrum.plot(title= plastic, xlabel='Wavenumber', ylabel='Transmittance')
        elif plastic == Plastic.LDPE.value:
            plt.subplot(334)
            spectrum.plot(title= plastic, xlabel='Wavenumber', ylabel='Transmittance')
        elif plastic == Plastic.PP.value:
            plt.subplot(335)
            spectrum.plot(title= plastic, xlabel='Wavenumber', ylabel='Transmittance')
        elif plastic == Plastic.PS.value:
            plt.subplot(336)
            spectrum.plot(title= plastic, xlabel='Wavenumber', ylabel='Transmittance')
        elif plastic == Plastic.Polyester.value:
            plt.subplot(337)
            spectrum.plot(title= plastic, xlabel='Wavenumber', ylabel='Transmittance')
        elif plastic == Plastic.PC.value:
            plt.subplot(338)
            spectrum.plot(title= plastic, xlabel='Wavenumber', ylabel='Transmittance')
        elif plastic == Plastic.PU.value:
            plt.subplot(339)
            spectrum.plot(title= plastic, xlabel='Wavenumber', ylabel='Transmittance')
        else:
            pass
            #spectrum.plot(title= 'Blank in testing 5Hz', xlabel='Wavenumber', ylabel='Transmittance')
    plt.show()

def user_sorting_function(sensors_output):
    sensor_id = 1
    spectrum = sensors_output[sensor_id]['spectrum']

    decision = {sensor_id: random.choice(list(Plastic)[0:-1])}
    difference = numpy.zeros(9)

    if spectrum.iloc[0] == 0:  # For FTIR, if the first transmittance is 0, it is blank spectra
        decision = {sensor_id: Plastic.Blank}
    else:

        for i, metearial in enumerate(Data):
            difference[i] = sum(abs(spectrum-metearial))
        min_diff = min(difference)

        if min_diff == difference[0]:
            decision = {sensor_id: Plastic.HDPE}
            spectrum.name = 'HDPE'
        elif min_diff == difference[1]:
            decision = {sensor_id: Plastic.LDPE}
            spectrum.name = 'LDPE'
        elif min_diff == difference[2]:
            decision = {sensor_id: Plastic.PP}
            spectrum.name = 'PP'
        elif min_diff == difference[3]:
            decision = {sensor_id: Plastic.PS}
            spectrum.name = 'PS'
        elif min_diff == difference[4]:
            decision = {sensor_id: Plastic.PC}
            spectrum.name = 'PC'
        elif min_diff == difference[5]:
            decision = {sensor_id: Plastic.PVC}
            spectrum.name = 'PVC'
        elif min_diff == difference[6]:
            decision = {sensor_id: Plastic.Polyester}
            spectrum.name = 'Polyester'
        elif min_diff == difference[7]:
            decision = {sensor_id: Plastic.PET}
            spectrum.name = 'PET'
        elif min_diff == difference[8]:
            decision = {sensor_id: Plastic.PU}
            spectrum.name = 'PU'

        if is_PS(spectrum):
            decision = {sensor_id: Plastic.PS}
            spectrum.name = 'PS'
        elif is_PP_HPDE_LDPE(spectrum):
            spectrum_zoomin = spectrum.loc[1500:1250]
            if 1350 < spectrum_zoomin.idxmax() < 1450:
                decision = {sensor_id: Plastic.PP}
                spectrum.name = 'PP'

        #clear PVC and PET mixes
        if decision == {sensor_id: Plastic.PVC}:
            if spectrum.idxmax() > 1550:
                decision = {sensor_id: Plastic.PET}
                spectrum.name = 'PET'

        #Clear Polyester and PET mixes
        if decision == {sensor_id: Plastic.PET} or decision == {sensor_id: Plastic.Polyester}:
            spectrum_zoomin = spectrum.loc[3000:2750]
            if spectrum.idxmax() > 2500:
                decision = {sensor_id: Plastic.HDPE}
                spectrum.name = 'HDPE'
            elif spectrum_zoomin.max() > 0.1125:
                decision = {sensor_id: Plastic.Polyester}
                spectrum.name = 'Polyester'
            elif spectrum_zoomin.max() < 0.0225:
                decision = {sensor_id: Plastic.PET}
                spectrum.name = 'PET'
        #impossible to split LDPE and HDPE

        spectra_lst.append(sensors_output[1]['spectrum'])
    return decision


def main():
    # simulation parameters
    conveyor_length = 1000  # cm
    conveyor_width = 100  # cm
    conveyor_speed = 35  # cm per second
    num_containers = 200
    sensing_zone_location_1 = 500  # cm
    sensors_sampling_frequency = 5  # Hz
    simulation_mode = 'testing'

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

    elapsed_time = simulator.run()  # added last two arguments
    for item_id, result in simulator.identification_result.items():
        if result['actual_type'] != result['identified_type']:
            print(f"Incorrectly identified : {result}")

    print(f'\nResults for running the simulation in "{simulation_mode}" mode:')
    print(f'Total missed containers = {simulator.total_missed}')
    print(f'Total sorted containers = {simulator.total_classified}')
    print(f'Total mistyped containers = {simulator.total_mistyped}')

    print(f'\n{num_containers} containers are processed in {elapsed_time:.2f} seconds')

    plot_spectra()

if __name__ == '__main__':
    main()
