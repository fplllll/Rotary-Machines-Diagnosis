# encoding: utf-8
from numpy import ndarray
from base import VibrationSignal
from Compressor.measure_points import CP_Gearbox_Output_Horizontal
import numpy as np


def chlorinecompressor_gearbox_outputshaft_horizontal(xdata: ndarray, teeth_num: ndarray,
                                                      fs: int, R: ndarray, th: ndarray):
    x = VibrationSignal(data=xdata, fs=fs, type=2)
    mp_instance = CP_Gearbox_Output_Horizontal(x=x, y=x, r=R[1], teeth_num=teeth_num,
                                               gf_threshold=th[0:3],
                                               ma_threshold=th[3:6],
                                               wd_threshold=th[6:9],
                                               kurtosis_threshold=th[9]
                                               )
    mp_instance.diagnosis()
    return mp_instance.fault_num, \
           np.vstack((mp_instance.x_lp.freq, mp_instance.x_lp.spec)), \
           np.vstack((mp_instance.x_hp.freq, mp_instance.x_hp.spec)), \
           mp_instance.ma_indicator, \
           np.hstack((0, mp_instance.x_lp.harmonics)), \
           mp_instance.x_lp.ow_amp, \
           mp_instance.gf_indicator, \
           mp_instance.x.kurtosis, \
           np.hstack((0, mp_instance.x_lp.harmonics_index)), \
           mp_instance.x_lp.ow_index, \
           mp_instance.x_hp.sideband_indexes, \
           {'gear': mp_instance.gf_threshold,
            'misalignment': mp_instance.ma_threshold,
            'bearing': mp_instance.wd_threshold,
            }


if __name__ == '__main__':
    data = np.loadtxt('Chlorine.csv', delimiter=',', usecols=(9))  # m/s2

    res = chlorinecompressor_gearbox_outputshaft_horizontal(xdata=data,
                                                            fs=25600,
                                                            R=np.array([1491.0, 10384.0]),
                                                            teeth_num=np.array([167, 28, 69]),
                                                            th=np.array([
                                                                10, 20, 30,
                                                                10, 20, 30,
                                                                10, 20, 30,
                                                                6.0,
                                                            ])
                                                            )

    # import matplotlib.pyplot as plt
    #
    # plt.plot(res[2][0,:], res[2][1,:],)
    # # plt.xlim(0, 2000)
    # plt.xlabel('Frequency Hz')
    # plt.ylabel('Amplitude mm/s2')
    # # plt.axvline(x=res[1][0,:][res[9]], color='#000000', linewidth=0.3)
    # for item in res[10].flatten():
    #     plt.axvline(x=res[1][0,:][item], color='#000000', linewidth=0.3)
    # plt.show()
    #
    # np.savetxt('tmp.csv', res[10]*0.05,delimiter=',')