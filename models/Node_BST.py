from datetime import datetime, timedelta


class Node:
    def __init__(self, event: str = "12:30|30|Sam pl E"):
        event = event.split("|")
        start_time, duration_minutes, event_name = event
        start_datetime = datetime.strptime(start_time, "%H:%M")
        end_datetime = (start_datetime + timedelta(minutes=int(duration_minutes)))
        start_time, end_time = start_datetime.time(), end_datetime.time()

        self.start_time_key = start_time
        self.duration_minutes = duration_minutes
        self.end_time = end_time
        self.event_name = event_name.strip()

        self.left_child = None
        self.right_child = None
        self.parent = None

    def __str__(self) -> str:
        return f"Event: {self.event_name}\n" +\
               f"{' ' * len('Event: ')}Start time: {str(self.start_time_key)[:-3]}, Duration: {self.duration_minutes}, End time: {str(self.end_time)[:-3]}"


class BST:
    def __init__(self):
        self.root = None
        self.length = 0

    def insert(self, event: (Node, str), from_file: bool = False):
        if not isinstance(event, Node):
            event = Node(event)

        if self.root is None:
            self.root = event
            self.length += 1
            if not from_file:
                print(f"First {event}\nAdded successfully.")
                return True
        else:
            return self._insert(self.root, event, from_file)

    def _insert(self, curr, event, from_file):
        if event.start_time_key < curr.start_time_key and event.end_time <= curr.end_time:
            if curr.left_child is None:
                event.parent = curr
                curr.left_child = event
                self.length += 1
                if not from_file:
                    print(f"{event}\nAdded successfully.")
                    return True
            else:
                return self._insert(curr.left_child, event, from_file)
        elif event.start_time_key > curr.start_time_key and event.end_time >= curr.end_time:
            if curr.right_child is None:
                event.parent = curr
                curr.right_child = event
                self.length += 1
                if not from_file:
                    print(f"{event}\nAdded successfully.")
                    return True
            else:
                return self._insert(curr.right_child, event, from_file)
        else:
            print(f"Insertion fail:")
            print(f"{event}")
            print(f"Cause: event time overlap with:")
            print(f"{curr}")
            return

    def in_order_event_printer(self):
        if self.root:
            print("Everyday's current schedule is:")
            print("-" * 60)
            self._in_order_event_printer(self.root)
            print("-" * 60)
        else:
            print("Your calendar is empty yet. First, you have to add an event.")
        return True

    def _in_order_event_printer(self, curr):
        if curr:
            self._in_order_event_printer(curr.left_child)
            print(curr)
            self._in_order_event_printer(curr.right_child)

    def in_order_free_time_printer(self):
        if self.root:
            print("Current free time intervals:")
            print("-" * 60)
            intervals = self._in_order_free_time_printer(self.root)
            intervals.append(intervals[0])
            free = []
            for index, time in enumerate(intervals[1:]):
                free.append(time)
                if index % 2 != 0:
                    print(" - ".join(free))
                    free = []
            print("-" * 60)
        else:
            print("Your calendar is empty yet. First, you have to add an event.")
        return True

    def _in_order_free_time_printer(self, curr, intervals=None):
        if intervals is None:
            intervals = []

        if curr:
            self._in_order_free_time_printer(curr.left_child, intervals)
            intervals.append(str(curr.start_time_key))
            intervals.append(str(curr.end_time))
            self._in_order_free_time_printer(curr.right_child, intervals)
            return intervals

    def find(self, event):
        if not isinstance(event, Node):
            event = Node(event)

        if self.root is None:
            print("Your calendar is empty yet. First, you have to add an event.")
        else:
            return self._find(self.root, event)

    def _find(self, curr, event):
        if curr:
            if curr.start_time_key == event.start_time_key:
                if curr.event_name == event.event_name and curr.duration_minutes == event.duration_minutes:
                    return True
                else:
                    print(f"{event}\nParameters does not match.")
                    return
            elif curr.start_time_key > event.start_time_key:
                return self._find(curr.left_child, event)
            else:
                return self._find(curr.right_child, event)
        else:
            print(f"{event}\nDid not find.")
            return

    def remove(self, event):
        if not isinstance(event, Node):
            event = Node(event)

        return self._remove(self.root, None, event)

    def _remove(self, curr, is_right, event):
        if curr:
            if curr.start_time_key == event.start_time_key:
                if curr.left_child is None and curr.right_child is None:
                    if curr.parent:
                        if is_right:
                            curr.parent.right_child = None
                        else:
                            curr.parent.left_child = None
                    else:
                        self.root = None
                elif curr.right_child and curr.left_child:
                    bottom_left_child = self._left_remove_helper(curr.left_child)
                    curr.start_time_key = bottom_left_child.start_time_key
                    self._remove(curr.left_child, False, bottom_left_child)
                elif curr.left_child is None and curr.right_child:
                    if curr.parent:
                        if is_right:
                            curr.parent.right_child = curr.right_child
                        else:
                            curr.parent.left_child = curr.right_child
                    else:
                        self.root = curr.right_child
                else:
                    if curr.parent:
                        if is_right:
                            curr.parent.right_child = curr.left_child
                        else:
                            curr.parent.left_child = curr.left_child
                    else:
                        self.root = curr.left_child
                self.length -= 1
                print(f"{event}\nDeleted successfully.")
                return True
            elif curr.start_time_key > event.start_time_key:
                return self._remove(curr.left_child, False, event)
            else:
                return self._remove(curr.right_child, True, event)
        else:
            print(f"{event}\nDid not find ==> failed to remove.")
            return

    def _left_remove_helper(self, curr):
        if curr.right_child is None:
            return curr
        else:
            return self._left_remove_helper(curr.right_child)
