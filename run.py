from window import Window, World


if __name__ == "__main__":
    window = Window()
    world = World(window)
    world.execute()
