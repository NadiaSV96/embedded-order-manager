# gpio_manager.py

import time
import RPi.GPIO as GPIO
from gpiozero import Buzzer
from config_loader import CONFIG

# Fonction pour initialiser les GPIO
def setup_gpio():
    led_pin_rouge = CONFIG["gpio"]["led_pin_rouge"]  # Récupérer le pin LED rouge depuis la configuration
    led_pin_jaune = CONFIG["gpio"]["led_pin_jaune"]  # Récupérer le pin LED jaune depuis la configuration
    led_pin_verte = CONFIG["gpio"]["led_pin_verte"]  # Récupérer le pin LED verte depuis la configuration
    buzzer_pin = CONFIG["gpio"]["buzzer_pin"]  # Récupérer le pin Buzzer depuis la configuration
    quit_button_pin = CONFIG["gpio"]["quit_button_pin"] # Récupérer le pin Button depuis la configuration
    export_button_pin = CONFIG["gpio"]["export_button_pin"] 
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin_rouge, GPIO.OUT)
    GPIO.output(led_pin_rouge, GPIO.LOW)
    GPIO.setup(led_pin_jaune, GPIO.OUT)
    GPIO.output(led_pin_jaune, GPIO.LOW)
    GPIO.setup(led_pin_verte, GPIO.OUT)
    GPIO.output(led_pin_verte, GPIO.LOW)
    GPIO.setup(quit_button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(export_button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)


    
    buzzer = Buzzer(buzzer_pin)
    buzzer.off()
    
    return buzzer, led_pin_rouge, quit_button_pin, led_pin_jaune, led_pin_verte, export_button_pin

def clignoter_led(led_pin_rouge, clignotement_event):
    while not clignotement_event.is_set():  # tant que event pas actif
        GPIO.output(led_pin_rouge, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led_pin_rouge, GPIO.LOW)
        time.sleep(1)
        
# Fonction pour faire sonner le buzzer
def sonner_buzzer(buzzer):
    buzzer.on()
    time.sleep(10)
    buzzer.off()
    
# Fonction pour allumer LED 
def allumer_led(pin):
    GPIO.output(pin, GPIO.HIGH)

# Fonction pour éteindre LED 
def eteindre_led(pin):
    GPIO.output(pin, GPIO.LOW)

# Fonction pour arrêter le buzzer
def arreter_buzzer(buzzer):
    buzzer.off()

# Fonction pour nettoyer les GPIO
def nettoyer_gpio():
    GPIO.cleanup()
