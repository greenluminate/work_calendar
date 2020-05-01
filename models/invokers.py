class Invokers:
    @staticmethod
    def show(bst, *args):
        return bst.in_order_event_printer()

    @staticmethod
    def add(bst, file_rw, event_input):
        event = "|".join(event_input())
        if bst.insert(event):
            file_rw.write(event)
        return True

    @staticmethod
    def rem(bst, file_rw, event_input):
        event = "|".join(event_input())
        if bst.find(event):
            file_rw.remove(event)
            bst.remove(event)
        return True

    @staticmethod
    def free(bst, *args):
        bst.in_order_free_time_printer()
        return True

    @staticmethod
    def esc(*args):
        print("Have a nice day!")
        return
