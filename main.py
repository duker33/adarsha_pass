from bot import drivers, Admin, Bot, VkMessenger

if __name__ == '__main__':
    # @todo #1:60m  Implement server for bot.
    #  It should receive stop/start signals and restart correctly.
    while True:
        try:
            Bot(
                Admin(drivers.HTTP()),
                VkMessenger()
            ).listen()
        except Exception as e:
            # @todo #1:30m  Response to user with error message.
            #  Make bot to clearly response to user in case of error message.
            print(str(e))
