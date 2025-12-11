from conf import GlobalLogger

def main():
    GlobalLogger.info("Hello from hc-mem!")
    GlobalLogger.debug("这是一条调试信息")
    GlobalLogger.warning("这是一条警告信息")
    GlobalLogger.error("这是一条错误信息")
    print("程序运行完成，请检查终端输出和 /hc/logs/hc_server.log 文件")


if __name__ == "__main__":
    main()
