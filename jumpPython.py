# -*- coding: UTF-8 -*-
# 音乐频谱跳动
import pygame
import numpy as np
import librosa
from scipy.fft import fft

# 初始化pygame
pygame.init()

# 设置窗口和颜色
screen_width = 800
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("跺脚的python")
text_color = (255, 255, 255)

# 设置音符和其他参数
notes = r"J u m p  P y t h o n"  # 使用音符的名称
base_x = 200
note_spacing = 50
base_y = screen_height - 80
max_jump_height = 800  # 调整最大跳动高度
font = pygame.font.Font(None, 50)   

#设置速度阻尼，值越大，减速越快
velocity_damp = 2.0

# 加载音乐文件
audio_path = 'D:/learn/pycode/demo/music/qmys.mp3'
y, sr = librosa.load(audio_path, sr=None)  # 加载音频，sr=None以使用原始采样率
audio_length = librosa.get_duration(filename=audio_path)  # 获取音频时长

# FFT设置
n_fft = 2048
hop_length = 512
fft_frame = 0

# 播放音频
pygame.mixer.init(frequency=sr, size=-16, channels=2, buffer=4096)
pygame.mixer.music.load(audio_path)
pygame.mixer.music.play()

# 用于同步的时钟
clock = pygame.time.Clock()
last_update = pygame.time.get_ticks()

# 定义字母初始位置
note_positions = {note: base_y for note in notes.split()}
note_velocities = {note: 0 for note in notes.split()}



# 游戏主循环
running = True
while running:
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - last_update) / 1000.0  # 转换为秒

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # 清屏

    # 更新FFT数据
    if fft_frame < len(y) - n_fft:
        fft_result = fft(y[fft_frame:fft_frame + n_fft])
        fft_frame += hop_length
    else:
        fft_frame = 0

    # 绘制音符
    bar_width = (screen_width - base_x - (len(notes) - 1) * note_spacing) / len(notes)
    magnitudes = np.abs(fft_result[:n_fft // 2])  # 获取频谱的振幅值
    for i, note in enumerate(notes.split()):
        x_pos = base_x + i * (bar_width + note_spacing)
        # 根据振幅值调整音符的跳动高度
        jump_value = min(max_jump_height, magnitudes[i] * max_jump_height)
        # 使用速度来平滑跳动
        note_velocities[note] = note_velocities[note] * velocity_damp + (jump_value - note_positions[note] + base_y) * 0.2
        note_positions[note] = max(base_y, note_positions[note])  # 更新字母的位置， 确保字母不会跳到基线以下  
        note_positions[note] = base_y - jump_value  # 更新字母的位置
        y_pos = note_positions[note]
        note_text = font.render(note, True, text_color)
        screen.blit(note_text, (x_pos + bar_width / 2 - note_text.get_width() / 2,
                                y_pos + max_jump_height / 2 - note_text.get_height() / 2))

    # 控制帧率以匹配音频的播放
    clock.tick(24)  # 设置FPS为30，这个值可以根据需要进行调整
    last_update = current_time

    pygame.display.flip()  # 更新屏幕显示

# 清理并退出
pygame.mixer.music.stop()
pygame.quit()
