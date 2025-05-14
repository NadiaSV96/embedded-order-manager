import tkinter as tk
from tkinter import messagebox
from config_loader import CONFIG
from status import status
from logger_manager import get_logger
from gpio_manager import nettoyer_gpio
import sys
import pygame
import threading

# Récupérer le logger
logger = get_logger()

def demander_pin(changer_etat_commande):
    """
    Cette fonction demande un PIN à l'utilisateur pour changer l'état de la commande.
    Si le PIN est correct, l'état est mis à "Expédiée", sinon un message d'erreur est affiché.
    """
    def run_tkinter():
        pin_window = tk.Tk()
        pin_window.title("Authentification")

        label = tk.Label(pin_window, text="Entrez le PIN pour changer l'état de la commande:")
        label.pack(pady=10)

        pin_entry = tk.Entry(pin_window, show="*")
        pin_entry.pack(pady=10)

        def verifier_pin():
            entered_pin = pin_entry.get()
            if entered_pin == CONFIG["pin"]:
                changer_etat_commande()
                pin_window.destroy()
            else:
                messagebox.showerror("Erreur", "PIN incorrect !")

        verify_button = tk.Button(pin_window, text="Vérifier", command=verifier_pin)
        verify_button.pack(pady=20)

        pin_window.mainloop()

    # Démarrer le thread pour la fenêtre Tkinter
    threading.Thread(target=run_tkinter, daemon=True).start()

def changer_etat_commande(data_table, save_to_json):
    """
    Change l'état d'une commande à "Expédiée" dans la table de commandes.
    """
    global logger
    for row in data_table:
        if row[4] == status.ATTENTE.label:  # Si la commande est en attente
            row[4] = status.EXPEDIEE.label  # Changer l'état à "Expédiée"
            save_to_json()  # Sauvegarder dans le fichier JSON
            break

def main():
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Application principale")

    # Fonction pour demander la confirmation de fermeture
    def on_close():
        demander_confirmation_fermeture()

    # Intercepter l'événement de fermeture (clic sur le X)
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Ajouter un bouton pour tester la demande de PIN
    test_button = tk.Button(root, text="Test PIN", command=lambda: demander_pin(changer_etat_commande))
    test_button.pack(pady=20)

    # Lancer la boucle principale de Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()

def demander_confirmation_fermeture():
    """
    Affiche une fenetre Tkinter demandant la confirmation de fermeture de l'application.
    """
    def on_quit():
        # Si l'utilisateur confirme, fermer l'application Pygame
        logger.info("Fermeture de l'application et nettoyage propre des GPIO")
        nettoyer_gpio() # S'assurer de nettoyer les gpio
        pygame.quit()
        sys.exit()

    def on_cancel():
        confirmation_window.destroy()

    confirmation_window = tk.Tk()
    confirmation_window.title("Confirmer la fermeture")

    label = tk.Label(confirmation_window, text="Êtes-vous sûr de vouloir quitter ?")
    label.pack(pady=10)

    quit_button = tk.Button(confirmation_window, text="Quitter", command=on_quit)
    quit_button.pack(side=tk.LEFT, padx=10, pady=10)

    cancel_button = tk.Button(confirmation_window, text="Annuler", command=on_cancel)
    cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

    confirmation_window.protocol("WM_DELETE_WINDOW", on_cancel)

    confirmation_window.mainloop()
