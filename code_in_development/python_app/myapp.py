import queue, json
from modules.pyQserver import start_server, connect_to_server, terminate_server

def main():
    # Configuration - In a real project, these could come from a .env file
    CONFIG = {
        "auth": 'abracadabra',
        "ip": "localhost",
        "port": 50000,
        "max_size": 1000
    }
    try:
        # 1. Start Server ---------------------------------------------
        py_que_server = start_server(CONFIG["ip"], CONFIG["port"], CONFIG["auth"], CONFIG["max_size"])
        print(f"🚀 Server started on PID {py_que_server.pid} (Port {CONFIG['port']})")

        # 2. Connect Client ------------------------------------------
        q_in, q_out = connect_to_server(CONFIG["ip"], CONFIG["port"], CONFIG["auth"])
        print("📥 System ready. Waiting for LabVIEW data...")

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
                if 'double' in msg:
                    flag_process_data = True

                # C. Process Data
                if flag_process_data == True:

                    val = float(msg['double'])
                    print(f"📈 Processing: {val}")
                    # note: I am updating the send data JSON with a new value
                    msg['double'] = val + 10.0
                    
                    # D. Send data back =====
                    q_out.put(json.dumps(msg))
                
            # Catch Error............
            except queue.Empty:
                # No data received within timeout, just loop again
                continue
            except KeyboardInterrupt:
                # Exit the loop
                print(f"📥 loop ending...")
                break
            except Exception as e:
                print(f"❌ Error in loop: {e}")
        #<<<-----Processing Loop END
    finally:
        # 4. Cleanup: This runs even if the script crashes or is stopped
        print("Stopping server...")
        terminate_server(py_que_server)
        print("end.")

if __name__ == "__main__":
    main()