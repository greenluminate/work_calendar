class FileRW:
    def __init__(self, bst, filename="events.txt"):
        self.filename = filename
        self.bst = bst

    def read_insert_to_bst(self):
        with open(self.filename, "r") as to_read:
            for line in to_read:
                if line != "\n":
                    self.bst.insert(line, True)

    def write(self, event):
        with open(self.filename, "r") as f:
            last_line = f.readline(-1)
        with open(self.filename, "a") as f:
            if last_line == "\n":
                f.write(event)
            else:
                f.write("\n"+event)

    def remove(self, event):
        with open(self.filename, "r") as f:
            lines = f.readlines()
        with open(self.filename, "w") as f:
            for line in lines:
                if line.strip("\n") != event and line.strip("\n") != "":
                    f.write(line)
