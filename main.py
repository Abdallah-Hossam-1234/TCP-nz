## this program on "https://github.com/Abdallah-Hossam-1234/TCP-nz"
import socket
import tkinter as tk
from tkinter import messagebox
import threading

# Global configuration
proxy_host = '127.0.0.1'
proxy_port = 8888
destination_host = "google.com"
destination_port = 80

# Flags and objects to control the proxy server
proxy_running = False
proxy_socket = None

def forward_data(source, destination):
    """helper function to continuously forward data from source to destination."""
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    except Exception:
        pass  # Connection closed or error occurred

def handle_client(client_socket):
    """Handles a single client connection by forwarding data bidirectionally."""
    try:
        # 1. Create connection to destination server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((destination_host, destination_port))

        # 2. Start two threads: one for client->server, one for server->client
        t1 = threading.Thread(target=forward_data, args=(client_socket, server_socket), daemon=True)
        t2 = threading.Thread(target=forward_data, args=(server_socket, client_socket), daemon=True)
        
        t1.start()
        t2.start()
        
        # Wait for both directions to finish
        t1.join()
        t2.join()
        print("Data transfer completed successfully.")

    except Exception as e:
        print(f"An error occurred while processing the connection: {e}")
    finally:
        # 3. Clean up sockets
        client_socket.close()
        server_socket.close()

def start_proxy():
    """The main loop for the proxy server, runs in a background thread."""
    global proxy_running, proxy_socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        proxy_socket.bind((proxy_host, proxy_port))
        proxy_socket.listen(5)
        print(f"Proxy server is listening on {proxy_host}:{proxy_port}")
        
        proxy_running = True
        while proxy_running:
            proxy_socket.settimeout(1.0)  # Allows the loop to check the proxy_running flag
            try:
                client_socket, addr = proxy_socket.accept()
                print(f"New connection accepted from {addr[0]}:{addr[1]}")
                
                # Handle each client in a separate daemon thread
                client_thread = threading.Thread(target=handle_client, args=(client_socket,), daemon=True)
                client_thread.start()
            except socket.timeout:
                continue  # Timeout is expected, just check if proxy_running is still True
            except OSError:
                break  # Socket was closed, exit loop
                
    except Exception as e:
        print(f"Failed to start proxy: {e}")
    finally:
        proxy_running = False
        if proxy_socket:
            proxy_socket.close()
        print("Proxy server stopped.")

def start_proxy_from_gui():
    """Validates GUI input, updates globals, and starts the proxy thread."""
    global proxy_host, proxy_port, destination_host, destination_port
    
    # 1. Validate inputs
    if not all([E1.get(), E2.get(), E3.get(), E4.get()]):
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        p_port = int(E2.get())
        d_port = int(E4.get())
    except ValueError:
        messagebox.showerror("Input Error", "Ports must be valid numbers.")
        return

    # 2. Update global configuration with GUI string values
    proxy_host = E1.get()
    proxy_port = p_port
    destination_host = E3.get()
    destination_port = d_port

    # 3. Start proxy in a separate thread to avoid blocking the GUI
    threading.Thread(target=start_proxy, daemon=True).start()
    messagebox.showinfo("success", f"proxy started on {proxy_host}:{proxy_port}")

def stop_proxy_from_gui():
    """stops the proxy server gracefully."""
    global proxy_running, proxy_socket
    proxy_running = False
    if proxy_socket:
        try:
            proxy_socket.close()
        except Exception:
            pass

def Auto_proxy_from_gui():
    """Auto."""
    global proxy_host, proxy_port, destination_host, destination_port
    
    # 1. Validate inputs
    if not all([E3.get()]):
        messagebox.showerror("Input Error", "Please fill the destination_host.")
        return

    p_port = 8888
    d_port = 90

    # 2. Update global configuration with GUI string values
    proxy_host = get_ip_by_hostname()
    proxy_port = p_port
    destination_host = E3.get()
    destination_port = d_port

    # 3. Start proxy in a separate thread to avoid blocking the GUI
    threading.Thread(target=start_proxy, daemon=True).start()
    messagebox.showinfo("success", f"proxy started on {proxy_host}:{proxy_port}")
def get_ip_by_hostname():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))  # Dummy connection, no data is sent
        local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    finally:
        if s is not None:
            s.close()
    
# ================= GUI SETUP =================
root = tk.Tk()
root.title("TCP nz")
root.geometry("400x550") 
root.resizable(False, False)

L1 = tk.Label(root, text="proxy ip", font=("Arial", 12))
E1 = tk.Entry(root, width=40, font=("Arial", 12), justify="center")
E1.insert(0, "XXX.XXX.XXX.XXX")

L2 = tk.Label(root, text="proxy port", font=("Arial", 12))
E2 = tk.Entry(root, width=40, font=("Arial", 12), justify="center")
E2.insert(0, "8888")

L3 = tk.Label(root, text="destination Host", font=("Arial", 12))
E3 = tk.Entry(root, width=40, font=("Arial", 12), justify="center")
E3.insert(0, "github.com")

L4 = tk.Label(root, text="destination Port", font=("Arial", 12))
E4 = tk.Entry(root, width=40, font=("Arial", 12), justify="center")
E4.insert(0, "80")

B1 = tk.Button(root, text="start Proxy", command=start_proxy_from_gui, font=("Arial", 15))
B2 = tk.Button(root, text="stop Proxy", command=stop_proxy_from_gui, font=("Arial", 15))
B3 = tk.Button(root, text="Auto", command=Auto_proxy_from_gui, font=("Arial", 15))
# Layout
L1.pack(pady=(15, 0))
E1.pack(pady=5)
L2.pack(pady=(10, 0))
E2.pack(pady=5)
L3.pack(pady=(10, 0))
E3.pack(pady=5)
L4.pack(pady=(10, 0))
E4.pack(pady=5)

B1.pack(pady=20)
B2.pack(pady=5)
B3.pack()

get_ip_by_hostname()
root.mainloop()
