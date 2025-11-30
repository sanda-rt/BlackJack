import socket
import threading
import json

class GameClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_state = {} # Stockera le dernier état reçu du serveur

    def connect(self):
        """Tente de se connecter au serveur."""
        try:
            self.socket.connect((self.host, self.port))
            print("Connecté au serveur de jeu.")
            # Démarrer un thread pour écouter les mises à jour du serveur
            threading.Thread(target=self._listen_for_state).start()
            return True
        except ConnectionRefusedError:
            print(f"Erreur : Impossible de se connecter au serveur à {self.host}:{self.port}")
            return False

    def _listen_for_state(self):
        """Boucle d'écoute pour recevoir l'état du jeu."""
        while True:
            try:
                # Recevoir les données d'état du jeu
                data = self.socket.recv(4096) 
                if data:
                    # Mettre à jour l'état local du client
                    self.game_state = json.loads(data.decode('utf-8'))
                    self._display_state()
            except:
                print("Déconnexion du serveur.")
                self.socket.close()
                break

    def _display_state(self):
        """Affiche l'état du jeu reçu (À remplacer par l'interface graphique)."""
        print("\n--- MISE À JOUR DU JEU ---")
        if self.game_state.get('board'):
             for row in self.game_state['board']:
                 print(" ".join(row))
        print(f"Statut : {self.game_state.get('message')}")
        print("--------------------------")

    def send_action(self, action_dict):
        """Envoie une action (mouvement) au serveur."""
        try:
            message = json.dumps(action_dict).encode('utf-8')
            self.socket.sendall(message)
        except:
            print("Erreur lors de l'envoi de l'action. Serveur déconnecté ?")

class GameServer:
    """
    Gère la connexion réseau, l'écoute des clients, 
    la réception/l'envoi des données et la liaison avec la logique du jeu.
    """
    def __init__(self, host, port, game_logic):
        self.host = host                          
        self.port = port                          
        self.game = game_logic                    
        self.connections = []                     
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.socket.bind((self.host, self.port)) 
        
    def start(self):
        """
        Démarre le processus d'écoute dans un thread séparé.
        Le thread principal du programme peut continuer son travail.
        """
        print(f"Serveur démarré sur {self.host}:{self.port}. En attente de connexions...")
        
        threading.Thread(target=self._listen_for_clients).start()

    def _listen_for_clients(self):
        """
        La boucle principale qui attend et accepte de nouvelles connexions clients.
        """
        self.socket.listen(5) 
        while True:
           
            conn, addr = self.socket.accept() 
            print(f"Nouvelle connexion de {addr}")
            
            self.connections.append(conn)
            
            threading.Thread(target=self._handle_client, args=(conn, addr)).start()

    def _handle_client(self, conn, addr):
        """
        Gère la boucle de réception des données pour un client spécifique.
        Chaque client a sa propre instance de cette méthode (via un thread).
        """
        while True:
            try:
                
                data = conn.recv(1024).decode('utf-8') 
                
                if data:
                    
                    action = json.loads(data) 
                    

                    self.game.apply_move(action) 
                    
                    
                    self.broadcast_state() 
                    
            except:
                
                print(f"Déconnexion de {addr}")
                conn.close() 
                self.connections.remove(conn) 
                break 
                
    def broadcast_state(self):
        """
        Envoie l'état actuel du jeu à TOUS les clients connectés.
        """
        state_data = json.dumps(self.game.get_state()).encode('utf-8') 
        
        for conn in self.connections:
            try:
                
                conn.sendall(state_data) 
            except:
                
                print("Erreur d'envoi à un client, connexion ignorée.")
                pass