class Interaction:

    def isOver(self,lemmingList,floor):
        for lemming in lemmingList.getList():
            if lemming.getPos()[0] > floor.getInit()[0] and lemming.getPos()[0] < floor.getEnd()[0] and \
                            lemming.getPos()[1] > floor.getInit()[1]*0.95 and lemming.getPos()[1] < floor.getInit()[1]*1.05:
                    lemming.isFloor(True)
            else:
                lemming.isFloor(False)

