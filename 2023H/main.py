'''
Compony: NUC
Date: 2026-02-11 09:27:46
LastEditors: Loong2525
LastEditTime: 2026-02-12 19:39:17
'''
'''
@induce:
    main完成主要处理流程算法
    方法：
        buffle_sort()冒泡排序算法
        get_integration()获取正弦波，方波，三角波的特征值用于区分三者
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签SimHei
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

import waveform as wf #import 自定义模块生成波形

#*******************************冒泡排序 - O(n²)*************************
def bubble_sort(arr):
    array = arr.copy()
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array

def get_integration(arr,threshold):
    cnt = 0
    array = arr.copy()
    for i in range(len(array)):
        if array[i] > threshold:
            cnt+=1
    cnt=cnt/len(array)
    return cnt
    

#*************************** 设置信号参数**************************************
fs = 512000           # 采样频率 (Hz)    1024K可以分开95K和100K

T = 0.1               # 信号时长 (秒)

f1 = 20000          # 第一个波频率 (Hz)
f2 = 60000         # 第二个波频率 (Hz)
A1 = 0.5            # 第一个信号幅值
A2 = 0.5            # 第二个信号幅值

N = 1024             #分辨率fs/N

# 生成两个正弦波
t,signal1 = wf.sin_waveform(A1,f1,T,fs) 
t,signal2 = wf.sin_waveform(A2,f2,T,fs)
# 合成信号
combined_signal = signal1 + signal2


#***************************** 分离合成信号 *****************************************
# 执行FFT
yf = fft(combined_signal,N)       # 计算FFT
xf = fftfreq(N, 1.0/fs)           # 计算频率轴
# 计算幅度谱
amplitude_spectrum = 2.0/N * np.abs(yf)

# 正幅度谱
positive_freq = xf[:N//2]
positive_amplitude = amplitude_spectrum[:N//2]

#****************************排序算法反推正弦频率**********************************
array = []
array = bubble_sort(positive_amplitude.copy())
Am2=array[-1]
Am1=array[-2]
# for i in range(len(array)):
#     print(f"第{i}个{array[i]}\n")
print(f"第一个信号幅值幅值{Am1}\n第二个信号幅值{Am2}")
Am1_index = None
Am2_index = None
for i in range(len(positive_amplitude)):
    if Am1_index is None and np.isclose(positive_amplitude[i], Am1, rtol=1e-10):
        Am1_index = i
    # 跳过已经分配给 Am1 的索引
    if i != Am1_index and Am2_index is None and np.isclose(positive_amplitude[i], Am2, rtol=1e-10):
        Am2_index = i
    if Am1_index is not None and Am2_index is not None:
        break
dpi = fs/N
print(f"第一个频率为{Am1_index*dpi}Hz")
print(f"第二个频率为{Am2_index*dpi}Hz")
#***********************************判断A，B信号波形*************************************
#求出基波频率
f1 = Am1_index*dpi
f2 = Am2_index*dpi

if positive_amplitude[3*Am1_index] > positive_amplitude[Am1_index]/4              \
    and positive_amplitude[5*Am1_index] > positive_amplitude[Am1_index]/6:
    print("A为方波")
elif positive_amplitude[3*Am1_index] > positive_amplitude[Am1_index]/20          \
    and positive_amplitude[5*Am1_index] >positive_amplitude[Am1_index]/50:
    print("A为三角波")
else:
    print("A为正弦波")
if positive_amplitude[3*Am2_index] > (positive_amplitude[Am2_index]-positive_amplitude[Am1_index]/3)/5 :
    print("B为方波")
elif positive_amplitude[3*Am2_index] > 0.01 :
    print("B为三角波")
else:
    print("B为正弦波")

#*******************************绘制图谱******************************************
plt.figure() # 创建figure画布，指定长和高

plt.subplot(2, 2, 1)# 画布分成二行二列，在第一个位置创建并选中子图（subplot）
plt.xlabel('时间 (s)')
plt.ylabel('幅度')
plt.title('时域信号 ')
plt.plot(t, combined_signal, 'b-', linewidth=1.5, label='C信号')
plt.plot(t, signal1, 'r--', linewidth=0.8, alpha=0.7, label='A信号')
plt.plot(t, signal2, 'g--', linewidth=0.8, alpha=0.7, label='B信号')
plt.legend(loc='upper right')#在指定位置显示图例
plt.grid(True, alpha=0.3)#显示网格线， 设置透明度

plt.subplot(2,2,2)
plt.plot(xf, amplitude_spectrum, 'b-', linewidth=1.5)
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.title('FFT幅度双边谱')
plt.grid(True, alpha=0.3)
plt.xlim(-fs/2, fs/2) 

plt.subplot(2,2,3)
plt.plot(positive_freq, positive_amplitude, 'b-', linewidth=1.5)
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.title('FFT幅度单边谱')
plt.grid(True, alpha=0.3)
plt.xlim(0, fs/2) 


# 绘制对数幅度谱（以分贝为单位）
plt.subplot(2,2,4)
log_amplitude = 20 * np.log10(positive_amplitude + 1e-10)  # 加小值避免log(0)
plt.plot(positive_freq, log_amplitude, 'b-', linewidth=1.5)
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度 (dB)')
plt.title('FFT对数幅度谱')
plt.grid(True, alpha=0.3)
plt.xlim(0, fs/2)

# 显示图形
plt.tight_layout()
plt.show()
