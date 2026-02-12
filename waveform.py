'''
Compony: NUC
Date: 2026-02-11 20:07:15
LastEditors: Loong2525
LastEditTime: 2026-02-11 20:56:34
'''
"@induce: 基于numpy,提供三个方法，生成正弦，锯齿，矩形波"
import numpy as np
import matplotlib.pyplot as plt
'''
@function 产生正弦波
@param:
    A 信号幅度
    f 信号频率(Hz) : [0,100K],生成高频信号时请增大采样率
    T 信号长度(s)
@return:
    t:时间向量
    wave:波形向量
'''
def sin_waveform(A,f,T,fs):
    t = np.linspace(0, T, int(fs * T), endpoint=False)    # 时间向量,从0-T，分为fs*T个点
    wave = A * np.sin(2 * np.pi * f * t)
    return t,wave

'''
@function 产生锯齿波
@param:
    A 信号幅度
    f 信号频率(Hz) : [0,100K],生成高频信号时请增大采样率
    T 信号长度(s)
    duty [0,1):     上升段站整个周期的百分比，建议取{0.2}这样的一位小数而非{0.23}，否则可能会出现倒数是无限小数而导致波形的错误
@return:
    t:时间向量
    wave:波形向量
'''
def triangle_waveform(A,f,T,fs,duty):
    t = np.linspace(0, T, int(fs * T), endpoint=False)
    period = 1.0 / f
    # 将时间映射到单个周期内
    phase = (t / period) % 1.0
    # 相位在[0, duty)时上升，在[duty, 1)时下降
    wave = np.where(phase < duty, 
                    2 * A * phase * (1/duty),                # 上升段：从0上升到2A
                    2 * A * (1 - phase) *(1/(1-duty)) )      # 下降段：从2A下降到0
    # 平移波，使其对称于时间轴
    wave = wave - A
    return t,wave
'''
@function 产生矩形波
@param:
    A 信号幅度
    f 信号频率(Hz) : 小于100K,生成高频信号时请增大采样率
    T 信号长度(s)
    duty [0,1):     上升段站整个周期的百分比
@return:
    t:时间向量
    wave:波形向量
'''
def square_waveform(A,f,T,fs,duty):
    t = np.linspace(0, T, int(fs * T), endpoint=False)
    period = 1.0 / f
    # 将时间映射到单个周期内
    phase = (t / period) % 1.0
    # 相位在[0, duty)时上升，在[duty, 1)时下降
    wave = np.where(phase < duty, 
                    A,       # 高电平
                    -A)      # 低电平
    return t,wave

if __name__=='__main__':
    x,sin = sin_waveform(0.5,30,0.5,10000)
    x,tri = triangle_waveform(0.5,30,0.5,10000,0.5)
    x,squ = square_waveform(0.5,30,0.5,10000,0.5)
    plt.figure()

    plt.subplot(3, 1, 1)
    plt.xlabel('time(s)')
    plt.plot(x, sin, 'b-', linewidth=1.5,label='sin')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)

    plt.subplot(3, 1, 2)
    plt.xlabel('time(s)')
    plt.plot(x, tri, 'r-', linewidth=1.5,label='triangle')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)

    plt.subplot(3, 1, 3)
    plt.xlabel('time(s)')
    plt.plot(x, squ, 'y-', linewidth=1.5,label='square')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()