import queue, json, time
from modules.pyQserver import start_server, connect_to_server, terminate_server, SharedLog

import sys
from datetime import datetime

def main(app_name:str):
    # Configuration - In a real project, these could come from a .env file
    CONFIG = {
        "auth": 'abracadabra',
        "ip": "localhost",
        "port": 50000,
        "max_size": 1000
    }
    # 2. Connect Client ------------------------------------------
    isconnected, q_in, q_out = connect_to_server(CONFIG["ip"], CONFIG["port"], CONFIG["auth"])

    if isconnected == False:
        # Start Server ---------------------------------------------
        py_que_server = start_server(CONFIG["ip"], CONFIG["port"], CONFIG["auth"], CONFIG["max_size"])
        print(f"🚀 Server started on PID {py_que_server.pid} (Port {CONFIG['port']})")

        # retry Connect Client ------------------------------------------
        isconnected, q_in, q_out = connect_to_server(CONFIG["ip"], CONFIG["port"], CONFIG["auth"])   

    if isconnected == True:

        # Feature to share python logs with your labview app
        applog = SharedLog(q_out)
        applog.info("System ready. Waiting for LabVIEW data...",iref=app_name,)

        # 3. Processing Loop -----------------------------------------
        while True:
            try:
            # Operation...........
                flag_process_data = False

                # A.Read DATA
                raw_data = q_in.get(timeout=0.1)  
                # B.Validate - input data is JSON
                try:
                    msg = json.loads(raw_data)
                except json.JSONDecodeError:
                    print(f"⚠️ Received malformed data: {raw_data}")
                    flag_process_data = False
                    
                # B.Validate - input item is present 
                # e.g. double is a json value sent in the message {"double":"0.12345", "ref":"123anything"}
                if 'double' in msg:
                    flag_process_data = True

                # C. Process Data -------------------------------------------------
                if flag_process_data == True:

                    val = float(msg['double'])
                    ref = msg['ref']
                    # log the action
                    applog.info(f'Processing: {val}',iref=app_name,xref=ref)
                    # note: I am updating the send data JSON with a new value
                    newval = val + 10.0
                    
                    # construct return message
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%ms")
                    data_msg = {
                        "id":"data",
                        "ts":timestamp,
                        "msg": str(newval),
                        "iref":"123",
                        "xref":ref,
                    }
                    # D. Send data back =====
                    q_out.put(json.dumps(data_msg))

                    # --------------------------------------------------------------

                    time.sleep(0.005)
                
            # Catch Error............
            except queue.Empty:
                # No data received within timeout, just loop again
                continue
            except KeyboardInterrupt:
                # Exit the loop
                applog.warn(f'loop ending...',iref=app_name)
                break
            except Exception as e:
                applog.warn(f"❌ Error in loop: {e}",iref=app_name)
                break
    else:
        print("count not connect or create")

    #<<<-----Processing Loop END
    print("end.")

if __name__ == "__main__":
    
    # Send a name to your python app
    # py myapp_sharedlog.py "Apple"
    # Apple is the name....
    try:
        app_name= sys.argv[1]
    except Exception:
        app_name= "Your-Python-App"

    main(app_name)