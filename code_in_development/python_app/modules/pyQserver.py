# Created by Jeff Morgan 2026
# Brought to you by Awaken IoT
# https://awakeniot.com/
#..........................................................................
# This code is to be used by python to host shared python data ques
#..........................................................................
import multiprocessing
from multiprocessing.managers import BaseManager
from datetime import datetime
import json

class QueueManager(BaseManager): pass

def shared_q_server(ip:str, port:int, key:str, que_size:int):
    """
    Starts a multiprocessing server to host shared python queues
    """
    queue_1 = multiprocessing.Queue(maxsize=que_size)
    queue_2 = multiprocessing.Queue(maxsize=que_size)
    auth_key_b = key.encode('ASCII')
    QueueManager.register('lv_que_in', callable=lambda:queue_1)
    QueueManager.register('lv_que_out', callable=lambda:queue_2)
    m = QueueManager(address=(ip, port), authkey=auth_key_b)
    s = m.get_server()
    print(f"Queue Server starting on {ip}:{port}...")
    s.serve_forever()

def start_server(ip:str, port:int, key:str, que_size:int):
    """
    Launches the python queue server to run asynchronously
    """
    # Start the server in a separate process (Call and Forget)
    server_process = multiprocessing.Process(target=shared_q_server, daemon=True,args=(ip,port,key,que_size))
    server_process.start()
    return server_process

def connect_to_server(ip:str, port:int, key:str):
    """
    Connects to an existing queue server and returns the shared queues to input data and get data back out.
    """

    QueueManager.register('lv_que_in')
    QueueManager.register('lv_que_out')

    try:
        m2 = QueueManager(address=(ip, port), authkey=key.encode('utf-8'))
        m2.connect()
        thequeuein = m2.lv_que_in()
        thequeueout = m2.lv_que_out()
        
        return True, thequeuein,thequeueout
    except ConnectionRefusedError:
        print(f"Connection refused. Is the server running at {ip}:{port}?")
        return False, None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False, None, None

def terminate_server(server_process:multiprocessing.Process):  
    """
    Connects to an existing queue server and returns the shared queues to input data and get data back out.
    """        
    if server_process:
        server_process.terminate()
        server_process.join()

def gen_timestamp():
    """
    Generate a timestamp in a string format
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%ms")
    return ts

def gen_msg_template(timestamp=False):
    """
    This is the default message template to add to data queues

    id       = id of sender   
    type     = type of message, e.g. log, data, cmd, error, sys
    ts       = timestamp string
    msg      = anything (in string format)
    iref     = internal reference, e.g. for log the current step
    xref     = external reference, e.g. your labview app sends a id per message sent

    version 1.0

    """
    msg = {
        "id"  :"",
        "type"  :"",       
        "ts"  :"",
        "msg" :"",
        "iref":"",
        "xref":""
    }
    if timestamp == True:
        gen_timestamp()
    return msg

class SharedLog():
    """
    
    logs information to the terminal via print + sends the info to an external app via a data queue.
    
    """
    def __init__(self, name:str, que_out:multiprocessing.Queue):
        self.logs  = []
        self.count = [0,0,0]
        self.statusque = que_out
        self.name = name

    def _log(self, level: str, message: str, iref="", xref=""):
        """Internal helper to format and store the log."""
        try:
            timestamp = gen_timestamp()
            # Standardizing the level tag to 5 characters for visual alignment
            formatted_entry = f"{timestamp} - {level.upper():<5}"
            if iref != "":
                formatted_entry += f"- {iref}"
            if xref != "":
                formatted_entry += f"- {xref}"
            formatted_entry += f"- {message}"
            send_msg = level.upper() + " - " + message

            # assemble message            
            log_msg = gen_msg_template()
            log_msg['id']   = self.name            
            log_msg['type'] = "log"
            log_msg['msg']  = send_msg
            log_msg['ts']   = timestamp
            log_msg['iref'] = iref
            log_msg['xref'] = xref
            #output
            print(formatted_entry)
            self.statusque.put(json.dumps(log_msg), block=False)
            return True
        except Exception:
            # do fail and ignore, not critical operation
            return False

    def info(self, message: str, iref="", xref=""):
        """
        logging level 0 = INFO
        """
        self._log("INFO", message,iref,xref)
        self.count[0] += 1

    def warn(self, message: str, iref="", xref=""):
        """
        logging level 1 = WARNING
        """
        self._log("WARN", message,iref,xref)
        self.count[1] += 1

    def error(self, message: str, iref="", xref=""):
        """
        logging level 2 = ERROR
        """
        self._log("ERROR", message,iref,xref)
        self.count[2] += 1

    