# 录音自检：不用语音识别的定量分析

当网络环境无法使用 Whisper / Google STT 等语音转文字服务时，用 ffmpeg 做定量音频分析同样有效。

## 需要的工具

```bash
ffmpeg  # 系统自带或 apt/brew install
```

无需任何 Python 包，无需网络。

## 分析流水线

### 1. 预处理：转成统一格式

```bash
ffmpeg -y -i 录音.m4a -ar 16000 -ac 1 /tmp/recording.wav
```

### 2. 停顿检测

```bash
ffmpeg -i /tmp/recording.wav -af "silencedetect=noise=-30dB:d=0.8" -f null -
```

- `noise=-30dB`：低于此阈值算静音
- `d=0.8`：持续 0.8 秒以上才算有效停顿
- 输出会标注每段静音的起止时间和持续时长

### 3. 音量分析

```bash
ffmpeg -i /tmp/recording.wav -af "volumedetect" -f null -
```

输出 `mean_volume` 和 `max_volume`。峰值接近 0dB 说明接近破音，均值低于 -30dB 说明太轻。

### 4. 能量曲线（可选）

```bash
ffmpeg -i /tmp/recording.wav -af "astats=metadata=1:reset=1:length=1" -f null -
```

每秒输出一次 RMS 能量，可用于画能量曲线看节奏变化。

## 分析维度

| 指标 | 怎么看 | 目标值 |
|------|--------|--------|
| 停顿数 | 停顿数 / 自然段数 | 每个自然段间应有停顿 |
| 停顿时长 | 关键转折处是否留白 | 重要钩子前 0.5-1s |
| 平均音量 | mean_volume | -20 到 -25 dB |
| 峰值 | max_volume | < -1 dB（不破音） |
| 段落长度 | 最长连续朗读段 | < 30s（超过说明在「赶」） |

## 实际案例（#6 互联网焦虑）

- 时长 103s，5 处停顿
- 前 35s（4 个自然段）节奏好，每段间有停顿
- 后 68s（最后一段）一口气读完，中间无停顿
- 结论：后半段需要拆成 3-4 个自然段，每段间停 1s，结尾问句前留白 0.5s

## 与原文对照

拿到停顿时间点后，对照原文找出每个停顿对应的段落边界。如果某个停顿位置和自然段边界对不上，说明朗读节奏和文字结构脱节。
