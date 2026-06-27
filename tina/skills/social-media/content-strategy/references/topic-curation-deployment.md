# 选题推送系统部署记录

## Cron Job

- **Job ID**: c9827903fedd
- **名称**: AI选题推送
- **调度**: 每天 8:00 AM
- **投递**: QQ
- **状态**: active

## 网络注意事项

- pip 安装需使用 `uv + 清华镜像源`（见 `devops/install-python-packages-cn` skill）
- RSS 直连国内源（36kr/虎嗅）可能超时，优先使用 web_search

## 管理命令

```
cronjob action=list | grep 选题
cronjob action=run job_id=c9827903fedd
cronjob action=pause job_id=c9827903fedd
```
