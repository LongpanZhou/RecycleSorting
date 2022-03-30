import random
from matplotlib import pyplot as plt
from rcplant import *

# For plot
spectra_lst = []

def user_sorting_function(sensors_output):
    
    sensor_id = 1
    if sensors_output[1]['spectrum'].iloc[0] == 0:
        decision = {sensor_id: Plastic.Blank}
    else:
        decision = {sensor_id: random.choice(list(Plastic)[0:-1])}  # random output a plastic type. [0:-1] is to avoid outputting a blank spectrum based on class Plastic
        spectra_lst.append(sensors_output[1]['spectrum']) # append all spectra into a list for plotting

    return decision

def plot_spectra():
    plt.figure()

    # retrieve 9 types of plastic and plot them seperately
    for spectrum in spectra_lst: 
        plastic = spectrum.name  # Plastic.PET.value = 'PET' based on class Plastic
                                 # They are interchangable
        if plastic == 'PET':
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
    

def main():
    
    # simulation parameters
    conveyor_length = 1000  # cm
    conveyor_width = 100  # cm
    conveyor_speed = 10  # cm per second
    num_containers = 200
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
    
    plot_spectra()
    




if __name__ == '__main__':
    main()
