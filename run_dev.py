#!/usr/bin/env python3
"""
开发环境启动脚本
演示如何在不同的运行环境中正确导入和使用配置模块
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入项目模块
from conf import logger
from src.inf.env.env_conf import get_settings


def main():
    """主函数 - 演示配置和日志的使用"""

    logger.info("=" * 50)
    logger.info("hc-mem 开发环境启动")
    logger.info("=" * 50)

    try:
        # 加载配置
        settings = get_settings()
        logger.info(f"应用名称: {settings.app_name}")
        logger.info(f"应用版本: {settings.app_version}")
        logger.info(f"调试模式: {settings.debug}")

        # 测试不同级别的日志
        logger.debug("这是一条调试信息")
        logger.info("配置加载成功")
        logger.warning("这是一条警告信息")
        logger.error("这是一条错误信息")

        logger.info("开发环境启动完成")

    except Exception as e:
        logger.error(f"启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()