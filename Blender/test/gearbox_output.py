# encoding: utf-8
from numpy import ndarray
import numpy as np
from base import VibrationSignal
from Blender.measure_points import BD_Gearbox_Output


def chlorinecompressor_gearbox_outputshaft(xdata: ndarray, teeth_num: ndarray,
                                           fs: int, R: float, bearing_ratio: ndarray,
                                           cur: float, th1: ndarray, th2: ndarray,
                                           ):
    th = th1 if (cur > 150) else th2

    x = VibrationSignal(data=xdata, fs=fs, type=2)

    mp_instance = BD_Gearbox_Output(x=x, y=x, r=R, teeth_num=teeth_num, bearing_ratio=bearing_ratio,
                                    gf_threshold=th[0:3],
                                    ma_threshold=th[3:6],
                                    bw_threshold=th[6:9],
                                    al_threshold=th[9:12],
                                    bl_threshold=th[12:15],
                                    kurtosis_threshold=th[15],
                                    harmonic_threshold=th[16:26])
    mp_instance.diagnosis()
    return mp_instance.fault_num, \
           np.vstack((mp_instance.x_vel.freq, mp_instance.x_vel.spec)), \
           np.vstack((mp_instance.x.freq, mp_instance.x.spec)), \
           np.vstack((mp_instance.x_env.freq, mp_instance.x_env.spec)), \
           np.hstack((mp_instance.bl_indicator, mp_instance.x_vel.harmonics)), \
           mp_instance.x_env.bearing_amp, \
           mp_instance.gf_indicator, \
           mp_instance.x.kurtosis, \
           mp_instance.harmonic_number, \
           mp_instance.ma_indicator, \
           np.hstack((mp_instance.x_vel.half_fr_indexes, mp_instance.x_vel.harmonics_index)), \
           np.transpose(np.reshape(mp_instance.x_env.bearing_index,(4,3)))  , \
           mp_instance.x.sideband_indexes, \
           {'gear': mp_instance.gf_threshold,
            'misalignment': mp_instance.ma_threshold,
            'bearing': mp_instance.bw_threshold,
            'atype_loosen': mp_instance.al_threshold,
            'btype_loosen': mp_instance.bl_threshold
            }


if __name__ == '__main__':
    data = np.loadtxt('Prepolymerizer.csv', delimiter=',', usecols=(5))  # m/s2

    res = chlorinecompressor_gearbox_outputshaft(xdata=1000 * data,  # mm/s2
                                                 fs=25600, cur=200,
                                                 R=1486,
                                                 bearing_ratio=np.array([0.42, 2.99, 4.19, 5.81]),
                                                 teeth_num=np.array([28, 69, 12.5]),
                                                 th1=np.array([
                                                     3000, 4000, 5000,
                                                     10, 20, 30,
                                                     200, 300, 400,
                                                     10, 20, 30,
                                                     30, 40, 50,
                                                     6.0,
                                                     10, 10, 10, 10, 10, 10, 10, 10, 10, 10
                                                 ]),
                                                 th2=np.array([
                                                     10, 20, 30,
                                                     10, 20, 30,
                                                     4, 6, 10,
                                                     10, 20, 30,
                                                     10, 20, 30,
                                                     6.0,
                                                     10, 10, 10, 10, 10, 10, 10, 10, 10, 10
                                                 ]),
                                                 )

    import matplotlib.pyplot as plt

    plt.plot(res[3][0,:], res[3][1,:],)
    plt.xlim(0, 50)
    plt.xlabel('Frequency Hz')
    plt.ylabel('Amplitude mm/s2')
    # plt.axvline(x=res[1][0,:][res[10][1]], color='#000000', linewidth=0.3)
    for item in res[11].flatten():
        plt.axvline(x=res[1][0,:][item], color='#000000', linewidth=0.3)
    plt.show()

    np.savetxt('tmp.csv', res[12]*0.05,delimiter=',')

    np.savetxt('tmp_value.csv', res[11] * 0.05, delimiter=',')
    np.savetxt('tmp_index.csv', np.transpose(np.reshape(res[5],(4,3))) , delimiter=',')