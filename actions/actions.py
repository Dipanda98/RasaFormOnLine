# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
import re
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
#
#
class ActionHelloWorld(Action):
#
    def name(self) -> Text:
        return "action_devis"
#
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
        language = tracker.get_slot("language")
        scenario = tracker.get_slot("scenario")
        solution_payement = tracker.get_slot("solution_payement")
        formulaire = tracker.get_slot("formulaire")
        secteur = tracker.get_slot("secteur")
        support = tracker.get_slot("support")
        internationalisation = tracker.get_slot("internationalisation")
        plateforme_gestion = tracker.get_slot("plateforme_gestion")
        nombre_utilisateur = tracker.get_slot("nombre_utilisateur")

        dico_scenario = {
            "-10" : "1000|9000",
            "10...30" : "10000|30000",
            "30...60" : "30000|60000",
            "60+" : "60000|200000",
            "---" : "1000|200000"
        }
        dico_solution_payement = {
            "oui" : "15000|30000",
            "non" : "0|0"
        }
        dico_formulaire = {
            "oui" : "1000|2000",
            "non" : "0|0"
        }
        dico_secteur = {
            "vente" : "200000|900000",
            "service_client" : "400000|1500000",
            "hotellerie" : "700000|3000000",
            "medecine" : "400000|1500000",
            "marketing" : "50000|100000",
            "autre" : "200000|3000000"
        }
        dico_support = {
            "1" : "2000", #Whatsapp
            "2" : "2000", #Telegram
            "3" : "2000", #Messenger
            "4" : "2000", #Instagram
            "5" : "2000", #Mobile app
            "6" : "2000", #Website
            "7" : "4000" #Autre
        }
        dico_internationalisation = {
            "1" : "0|0",
            "2" : "10000|20000",
            "3" : "20000|40000",
            "4" : "30000|60000",
            "5" : "40000|80000",
            "+5" : "50000|100000"
        }
        dico_nombre_utilisateur = {
            "-50" : "5000|5000",
            "50...400" : "5000|5000",
            "400...800" : "17000|17000",
            "---" : "17000|17000"
         }
        dico_plateforme_gestion = {
            "oui": "100000|700000",
            "non" : "0|0"
         }
        try:
            plage_scenario = dico_scenario[scenario].split("|")
            prix_scenario_min = plage_scenario[0]
            prix_scenario_max = plage_scenario[1]

            plage_solution_payement = dico_solution_payement[solution_payement].split("|")
            prix_solution_payement_min = plage_solution_payement[0]
            prix_solution_payement_max = plage_solution_payement[1]

            plage_formulaire = dico_formulaire[formulaire].split("|")
            prix_formulaire_min = plage_formulaire[0]
            prix_formulaire_max = plage_formulaire[1]

            plage_secteur = dico_secteur[secteur].split("|")
            prix_secteur_min = plage_secteur[0]
            prix_secteur_max = plage_secteur[1]

            plage_internationalisation = dico_internationalisation[internationalisation].split("|")
            prix_internationalisation_min = plage_internationalisation[0]
            prix_internationalisation_max = plage_internationalisation[1]

            plage_nombre_utilisateur = dico_nombre_utilisateur[nombre_utilisateur].split("|")
            prix_nombre_utilisateur_min = plage_nombre_utilisateur[0]
            prix_nombre_utilisateur_max = plage_nombre_utilisateur[1]

            plage_plateforme_gestion = dico_plateforme_gestion[plateforme_gestion].split("|")
            prix_plateforme_gestion_min = plage_plateforme_gestion[0]
            prix_plateforme_gestion_max = plage_plateforme_gestion[1]

            prix_support = 0

            for i in support:
                prix_support = prix_support + int(dico_support[i])

            prix_total_min = prix_support + int(prix_scenario_min) + int(prix_solution_payement_min) + int(prix_formulaire_min) + int(prix_secteur_min) + int(prix_internationalisation_min) + int(prix_nombre_utilisateur_min) + int(prix_plateforme_gestion_min)
            prix_total_max = prix_support + int(prix_scenario_max) + int(prix_solution_payement_max) + int(prix_formulaire_max) + int(prix_secteur_max) + int(prix_internationalisation_max) + int(prix_nombre_utilisateur_max) + int(prix_plateforme_gestion_max)

            if (language == "en"):
                dispatcher.utter_message(text="The purchase price of your chatbot is between {} and {} FCFA.".format(prix_total_min,prix_total_max))
            else:
                dispatcher.utter_message(text="Le prix d'acquisition de votre chatbot est compris entre {} et {} FCFA.".format(prix_total_min,prix_total_max))
    #
            return [SlotSet("total_min",prix_total_min),SlotSet("total_max",prix_total_max),SlotSet("execute_action","normal")]
        except(RuntimeError, TypeError, NameError,OSError,ValueError,BaseException):
            date = datetime.today().strftime('%d-%B-%Y %H:%M:%S')
            contenu = ""
            entete = "Une erreur est survenu lors du calcul du devis"
            contenu = contenu + entete + "  "+date+"\n\n"
            with open("logs.txt", "a") as fichier:
                fichier.write(contenu)
            if (language == "en"):
                dispatcher.utter_message(text="An error occurred when calculating the quote for your chatbot. We apologize for this inconvenience. Please try again later!!")
            else:
                dispatcher.utter_message(text="Une erreur est survenu lors du calcul du devis de votre chatbot. Nous nous excusons de ce désagrément. Veuillez reessayer plutard !!")
            return [SlotSet("execute_action","retour")]

class ActionSendEmail(Action):
    def name(self) -> Text:
        return "action_send_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("language")
        prix_total_max = tracker.get_slot("total_max")
        prix_total_min = tracker.get_slot("total_min")
        fromaddr = "testvs@sparterobotics.com"
        password = "TestV355.00"
        toaddr = tracker.get_slot("email")
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        #body = "<h2> BONJOUR <font color=\"green\">OK</font></h2>"
        if (language == "en"):
            subject = "Quote for the acquisition of the Chatbot"
            f = open("C:/Users/EMPEROR/Desktop/Perso/rasa/rasa_form_devis/email_chatbot_en.html", "r",encoding='utf-8')
        else:
            subject = "Devis d'acquisition du Chatbot"
            f = open("C:/Users/EMPEROR/Desktop/Perso/rasa/rasa_form_devis/email_chatbot.html", "r",encoding='utf-8')
        
        msg['Subject'] = subject
        body = "{}".format(f.read())
        body = body.format(prix_total_min,prix_total_max)
        f.close()
        msg.attach(MIMEText(body,'html'))

        s = smtplib.SMTP('mail.sparterobotics.com', 587)
        s.starttls()
        try:
            s.login(fromaddr, password)
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
        except(RuntimeError, TypeError, NameError,OSError,ValueError,BaseException):
            date = datetime.today().strftime('%d-%B-%Y %H:%M:%S')
            contenu = ""
            entete = "Une erreur est survenue lors de l'envoi de la requête"
            contenu = contenu + entete + "  "+date+"\n\n"
            with open("logs.txt", "a") as fichier:
                fichier.write(contenu)
            print("Une erreur est survenue lors de l'envoi de la requête")
        finally:
            s.quit()
        try:
            contenu = ""
            email = tracker.get_slot("email")
            phone = tracker.get_slot("telephone")
            date = datetime.today().strftime('%d-%B-%Y %H:%M:%S')
            total_min = tracker.get_slot("total_min")
            total_max= tracker.get_slot("total_max")
            contenu = contenu + "Données Client: \nRaison: Demande de devis\nEmail: {}\nTéléphone: {}\nDate de prise de contact: {}\nPrix minimum : {}\nPrix maximum: {}\n\n\n".format(email,phone,date,total_min,total_max)
            with open("customer_data.txt","a") as fichier:
                fichier.write(contenu)
        except(RuntimeError, TypeError, NameError,OSError,ValueError,BaseException):
            date = datetime.today().strftime('%d-%B-%Y %H:%M:%S')
            contenu = ""
            entete = "Une erreur est survenue lors de l'envoi de la requête"
            contenu = contenu + entete + "  "+date+"\n\n"
            with open("logs.txt", "a") as fichier:
                fichier.write(contenu)
            print("Une erreur est survenue lors de l'envoi de la requête")

        return []

class ActionResetSlot(Action):

    def name(self) -> Text:
        return "action_reset_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            language = tracker.get_slot("language")
            email = tracker.get_slot("email")

            return [SlotSet("email",email),SlotSet("language",language),AllSlotsReset(),SlotSet("email",email),SlotSet("language",language)]

class ActionMerci(Action):

    def name(self) -> Text:
        return "action_merci"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            language = tracker.get_slot("language")
            url_contact_page = "https://test.com"
            if (language == "en"):
                dispatcher.utter_message(text="Thank you for your time. We hope we were able to help you.\n\
You can contact us to discuss the realization of your chatbot via this number: XXXXX, or by mail at: test@test.com You can also write to us directly by visiting our page  {}".format(url_contact_page))
            else:
                dispatcher.utter_message(text="Merci pour le temps que vous nous avez accordé. Nous espérons que nous avons pu vous aider.\n\
Vous pouvez nous contacter discuter de la réalisation de votre chatbot via ce numéro: XXXXX, ou par mail à l'adresse: test@test.com\nVous pouvez aussi directement nous écrire en visitant notre page  {}".format(url_contact_page))

            return []


class ValidateDemandeEmailDebutForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_demande_email_form"

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        language = tracker.get_slot("language")
        try:
            email = tracker.get_slot("email")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if(re.fullmatch(regex, email)):
                return {"email": slot_value}
            else:
                if (language == "en"):
                    dispatcher.utter_message(text="Error!! Please enter a valid email")
                    return {"email": None}
                else:
                    dispatcher.utter_message(text="Erreur !! Veuillez entrer un email valide")
                    return {"email": None}
        except(RuntimeError, TypeError, NameError,OSError,ValueError,BaseException):
            if (language == "en"):
                dispatcher.utter_message(text="Error!! Please enter a valid email")
            else:
                dispatcher.utter_message(text="Erreur !! Veuillez entrer un email valide")
            return {"email": None}

        
        

class ValidateDemandeSupportDebutForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_demande_support_form"

    def validate_support(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        language = tracker.get_slot("language")
        try:
            support = tracker.get_slot("support")
            support = support.rstrip(",")
            support_list = support.split(",")
            support_autorise = ["1","2","3","4","5","6","7"]
            present = True

            for i in support_list:
                if i not in support_autorise:
                    present = False
                    if (language == "en"):
                        dispatcher.utter_message(text="Wrong choice! Please enter only numbers corresponding to the media in the list, separated by commas.\nExemple: 1,2,3")
                    else:
                        dispatcher.utter_message(text="Erreur de choix !! Veuillez n'entrer que des chiffres correspondant aux supports se trouvant dans la liste en les séparant par des virgules.\nExemple: 1,2,3")
                    return {"support": None}

            if (present == True):
                return {"support": support_list}
            else:
                dispatcher.utter_message(text="Erreur de choix !! Veuillez n'entrer que des chiffres correspondant aux supports se trouvant dans la liste en les séparant par des virgules.\nExemple: 1,2,3")
                return {"support": None} 
                
        except(RuntimeError, TypeError, NameError,OSError,ValueError,BaseException):
            if (language == "en"):
                dispatcher.utter_message(text="Syntax error! Please send the numbers, separated by commas, corresponding to the communication media.\nExample: 1,2,3")
            else:
                dispatcher.utter_message(text="Erreur de syntaxe!! Veuillez envoyer les chiffres, séparés par des virgules, correspondant aux support de communication.\nExemple: 1,2,3")
            return {"support": None}