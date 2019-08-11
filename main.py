from bot import Admin, Bot, IQPark, VkMessenger

if __name__ == '__main__':
    Bot(
        Admin(IQPark()),
        VkMessenger()
    ).listen()
