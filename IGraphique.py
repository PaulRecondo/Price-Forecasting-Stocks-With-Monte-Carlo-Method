import tkinter as tk
from tkinter import ttk, messagebox
import Fonctions as f
import customtkinter as ctk
from tkinter import messagebox
import Fonctions as f

def Pricing():
    global resultat_label, detail_label, btn_calcul
    try:
        # Récupération des paramètres
        ticker = ticker_var.get()
        start = start_var.get()
        end = end_var.get()
        simulations = int(sims_var.get())
        maturite = int(mat_var.get())
        taux_risque = float(rate_var.get()) / 100.0
        type_option = type_var.get()
        strike = float(strike_var.get())

        # Feedback visuel pendant le calcul
        btn_calcul.configure(text="Calcul en cours...", state="disabled")
        app.update()

        # Téléchargement et préparation des données
        df = f.get_data(ticker, start, end)
        if df is None or isinstance(df, str):
            btn_calcul.configure(text="Calculer le prix", state="normal")
            messagebox.showerror("Erreur", "Impossible de télécharger les données.")
            return

        f.transoData(df)

        # Appel des fonctions
        if type_option == "Call Européen":
            prix = f.EuropeanCallPricing(df, strike_price=strike, risk_free_rate=taux_risque,
                                         num_simulations=simulations, forecast_days=maturite)
        else:
            prix = f.AsianCall(df, strike_price=strike, risk_free_rate=taux_risque,
                               num_simulations=simulations, forecast_days=maturite)

        # Affichage du résultat mis en valeur
        resultat_label.configure(text=f"{prix:.4f} $", text_color="#2FA572")
        detail_label.configure(text=f"Prix estimé pour Strike: {strike:.2f} $ | {type_option}")

    except Exception as e:
        messagebox.showerror("Erreur de calcul", f"Une erreur est survenue : {str(e)}")
    finally:
        # Restauration du bouton une fois le calcul terminé
        btn_calcul.configure(text="Lancer la simulation", state="normal")


# ==========================================
# CONFIGURATION DU THEME PRO
# ==========================================
ctk.set_appearance_mode("System")  # S'adapte au thème clair/sombre de Windows/Mac
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pricer d'Options - Monte Carlo")
app.geometry("550x700")

# ==========================================
# CADRE PRINCIPAL (MAIN FRAME)
# ==========================================
main_frame = ctk.CTkFrame(master=app, corner_radius=15)
main_frame.pack(pady=30, padx=30, fill="both", expand=True)

titre_label = ctk.CTkLabel(master=main_frame, text="Paramètres du Modèle", font=ctk.CTkFont(size=24, weight="bold"))
titre_label.grid(row=0, column=0, columnspan=2, pady=(30, 20))

# Définition des variables
ticker_var = ctk.StringVar(value="PREIX")
start_var = ctk.StringVar(value="2015-01-01")
end_var = ctk.StringVar(value="2026-01-01")
sims_var = ctk.StringVar(value="1000")
mat_var = ctk.StringVar(value="252")
rate_var = ctk.StringVar(value="4.0")
strike_var = ctk.StringVar(value="100.0")
type_var = ctk.StringVar(value="Call Européen")

# Centrage des colonnes dans le cadre
main_frame.grid_columnconfigure(0, weight=1, pad=10)
main_frame.grid_columnconfigure(1, weight=1, pad=10)

# ==========================================
# CHAMPS DE SAISIE MODERNES
# ==========================================
ctk.CTkLabel(master=main_frame, text="Ticker de l'action :").grid(row=1, column=0, sticky="e", pady=8, padx=10)
ctk.CTkEntry(master=main_frame, textvariable=ticker_var, width=180).grid(row=1, column=1, sticky="w", pady=8, padx=10)

ctk.CTkLabel(master=main_frame, text="Date de début :").grid(row=2, column=0, sticky="e", pady=8, padx=10)
ctk.CTkEntry(master=main_frame, textvariable=start_var, width=180).grid(row=2, column=1, sticky="w", pady=8, padx=10)

ctk.CTkLabel(master=main_frame, text="Date de fin :").grid(row=3, column=0, sticky="e", pady=8, padx=10)
ctk.CTkEntry(master=main_frame, textvariable=end_var, width=180).grid(row=3, column=1, sticky="w", pady=8, padx=10)

ctk.CTkLabel(master=main_frame, text="Simulations :").grid(row=4, column=0, sticky="e", pady=8, padx=10)
ctk.CTkEntry(master=main_frame, textvariable=sims_var, width=180).grid(row=4, column=1, sticky="w", pady=8, padx=10)

ctk.CTkLabel(master=main_frame, text="Maturité (jours) :").grid(row=5, column=0, sticky="e", pady=8, padx=10)
ctk.CTkEntry(master=main_frame, textvariable=mat_var, width=180).grid(row=5, column=1, sticky="w", pady=8, padx=10)

ctk.CTkLabel(master=main_frame, text="Taux sans risque (%) :").grid(row=6, column=0, sticky="e", pady=8, padx=10)
ctk.CTkEntry(master=main_frame, textvariable=rate_var, width=180).grid(row=6, column=1, sticky="w", pady=8, padx=10)

ctk.CTkLabel(master=main_frame, text="Strike ($) :").grid(row=7, column=0, sticky="e", pady=8, padx=10)
ctk.CTkEntry(master=main_frame, textvariable=strike_var, width=180).grid(row=7, column=1, sticky="w", pady=8, padx=10)

ctk.CTkLabel(master=main_frame, text="Type d'option :").grid(row=8, column=0, sticky="e", pady=8, padx=10)
ctk.CTkComboBox(master=main_frame, variable=type_var, values=["Call Européen", "Call Asiatique"], width=180).grid(row=8, column=1, sticky="w", pady=8, padx=10)

# ==========================================
# BOUTON ET RESULTATS
# ==========================================
btn_calcul = ctk.CTkButton(master=main_frame, text="Lancer la simulation", command=Pricing, font=ctk.CTkFont(weight="bold", size=14), height=45, corner_radius=8)
btn_calcul.grid(row=9, column=0, columnspan=2, pady=(35, 15))

resultat_label = ctk.CTkLabel(master=main_frame, text="-- $", font=ctk.CTkFont(size=38, weight="bold"))
resultat_label.grid(row=10, column=0, columnspan=2, pady=(10, 0))

detail_label = ctk.CTkLabel(master=main_frame, text="En attente de simulation...", font=ctk.CTkFont(size=12), text_color="gray")
detail_label.grid(row=11, column=0, columnspan=2, pady=(0, 20))

app.mainloop()



