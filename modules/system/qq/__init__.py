# from multiprocessing import Process
# import time
#
#
# def two_task():
#     while True:
#         print("this")
#         time.sleep(0.1)  # 添加间隔降低CPU占用
#
#
# def background_task():
#     pp = Process(target=two_task)
#     pp.daemon = True
#     pp.start()
#
#     while True:
#         print("Daemon is working...")
#         time.sleep(5)
#


# def background_task():
#     while True:
#         print("Daemon is working...")
#         time.sleep(5)
# pp = Process(target=background_task())
# pp.daemon = True
# pp.start()




#
# if __name__ == '__main__':
#     p = Process(target=background_task)
#     p.daemon = True
#     p.start()
#
#     try:
#         while True:  # 添加退出机制
#             time.sleep(10)
#     except KeyboardInterrupt:
#         print("\nMain process terminated")