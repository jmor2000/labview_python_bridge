# Created by Jeff Morgan 2026
# Brought to you by Awaken IoT
# https://awakeniot.com/
#..........................................................................
# This code is to be used by labview to interact with the python data ques.
#..........................................................................
from multiprocessing.managers import BaseManager
import queue, json

# Python Class
# used to interact with the Lbv_Global_Que object

class QueueManager(BaseManager): 
    """Custom manager to register shared queues."""
    pass

# Register the queue accessors
QueueManager.register('lv_que_in')
QueueManager.register('lv_que_out')

# meq = queue.Queue()
# meq.put(block=False)
# meq.get()

class Lbv_Global_Que:
    """
    Client object to interface LabVIEW with a remote Python Queue Manager.
    """
    def __init__(self,ip: str, port: int, authkey: str):
        self.ip = ip
        self.port = port
        self.auth = authkey.encode('ascii')
        self.manager = QueueManager
        self.queues = [queue,queue]    

    def connect(self)-> bool:
        """Establishes connection to the Queue Manager."""
        try:
            """connect to the global queue manager hosting the data que"""
            self.manager = QueueManager(address=(self.ip, self.port), authkey=self.auth)
            self.manager.connect()
            self.queues = [self.manager.lv_que_in(), self.manager.lv_que_out()]
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def count_items_in_que(self,qid=0):
        """count how many items are in the que"""
        try:
            return self.queues[qid].qsize()
        except (IndexError, AttributeError):
            return -1

    def en_que(self, qid:int, data:str, timeout:float):
        """Class method to safely push data into the que"""
        try:
            self.queues[qid].put(data,block=False,timeout=timeout)
            return True, ""
        except queue.Full:
            return False, "Error: Queue is full."
        except Exception as e:
            return False, str(e)

    def de_que(self, qid:int, timeout:float):
        """Safely retrieves data from the queue."""
        try:
            data = self.queues[qid].get(block=False,timeout=timeout)
            return data, True, ""
        except queue.Empty:
            return "", False, "Error: Timeout reached."
        except Exception as e:
            return "", False, str(e)

# PY-LABVIEW-FUNCTIONS
# used by LABVIEW to interact with the Lbv_Global_Que object

def ObjInitialize(ip: str, port: int, password: str):
    """Create a Lbv_Global_Que object, and connect to the global queue and return the object"""
    client_obj = Lbv_Global_Que(ip,port,password)
    client_obj.connect()
    return client_obj

def Add_data(client_obj, que_id:int, task:str, timeout:float):
    """Wraps put_data in a JSON string for LabVIEW consumption."""
    # 0 is queue in
    # 1 is queue out
    flag_ok, error_msg = client_obj.en_que(que_id,task,timeout)
    result = {
        "value":"",
        "ok":flag_ok,
        "error_msg":error_msg,
    }
    return_str = json.dumps(result)
    return return_str

def Get_data(client_obj, que_id:int, timeout:float):
    """Get data from the que"""
    # 0 is queue in
    # 1 is queue out
    data, flag_ok, error_msg = client_obj.de_que(que_id,timeout)
    result = {
        "value":data,
        "ok":flag_ok,
        "error_msg":error_msg,
    }
    return_str = json.dumps(result)
    return return_str

def Flush(client_obj: Lbv_Global_Que, que_id:int):
    """Rapidly clears all items from a queue."""
    q = client_obj.queues[que_id]
    try:
        while not q.empty():
            q.get_nowait()
    except (queue.Empty, AttributeError):
        pass

def Q_size(client_obj: Lbv_Global_Que,que_id:int):
    """Count how much data is in the que"""
    data = client_obj.count_items_in_que(que_id)
    return data