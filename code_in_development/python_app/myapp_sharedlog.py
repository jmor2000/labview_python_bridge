import queue, json, time
from modules.pyQserver import start_server, connect_to_server, terminate_server, SharedLog, gen_msg_template
import sys, traceback

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
        labview_log = SharedLog(app_name,q_out)
        labview_log.info("System ready. Waiting for LabVIEW data...")

        # 3. Processing Loop -----------------------------------------
        flag_loop_exit = False
        while True:
            try:
            # Operation...........
                flag_process_data = True

                try:
                    # A.Read DATA
                    raw_data = q_in.get(timeout=0.1)  
                    idata = json.loads(raw_data)
                    ivalue = idata['msg']
                    xref = idata['xref']

                # Catch Errors............
                except queue.Empty:
                    # No data received within timeout, just loop again
                    flag_process_data = False
                except json.JSONDecodeError:
                    # failed to load json from message
                    labview_log.error(f" Received malformed data: {raw_data}")
                    flag_process_data = False

                # B. Process Data -------------------------------------------------
                if flag_process_data == True:
                    
                    # convert msg val to float
                    # note: this value can be anything you want, for example another JSON
                    val = float(ivalue)
                    # log the action
                    labview_log.info(f'Processing: {val}',iref="step-b",xref=xref)
                    # note: I am updating the send data JSON with a new value
                    newval = val + 10.0
                
                    # C. Return data -------------------------------------------------
                    data_msg = gen_msg_template(timestamp=True)
                    data_msg['id']   = "data"
                    data_msg['type']   = "data"
                    data_msg['msg']  = str(newval)
                    data_msg['iref'] = "123"
                    data_msg['xref'] = xref

                    q_out.put(json.dumps(data_msg))

                    # --------------------------------------------------------------
                    time.sleep(0.005) #<<<< for testing purposes only, can remove
                
            # Handle errors
            except KeyboardInterrupt:
                # Exit the loop
                labview_log.warn(f'loop ending...',iref=app_name)
                flag_loop_exit = True
            except Exception as e:
                labview_log.error(f"❌ Error in loop",iref=app_name)
                tb = traceback.format_exc()
                print(tb)
                flag_loop_exit = True

            # Exit loop
            if flag_loop_exit == True:
                terminate_server(py_que_server)
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