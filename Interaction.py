class Interaction:

    def isOver(self,lemming,floor):
        if lemming.getPos()[0] > floor.getInit()[0] and lemming.getPos()[0] < floor.getEnd()[0] and \
                        lemming.getPos()[1] > floor.getInit()[1]*0.9 and lemming.getPos()[1] < floor.getInit()[1]*1.1:
                lemming.isFloor(True)
        else:
            lemming.isFloor(False)

