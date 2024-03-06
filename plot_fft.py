import customtkinter as ctk
from customtkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import soundfile as sf
import os
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Plot FFT")
        self.geometry("400x830")
        # Impedisci il ridimensionamento della finestra
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)

        self.frame_laterale = ctk.CTkFrame(self)
        self.frame_laterale.grid_configure(row=2, column=0, padx=25, sticky="nswe")

        self.frame_laterale.grid_rowconfigure(0, weight=0)
        self.frame_laterale.grid_rowconfigure(1, weight=0)
        self.frame_laterale.grid_rowconfigure(2, weight=0)
        self.frame_laterale.grid_rowconfigure(3, weight=0)
        self.frame_laterale.grid_columnconfigure(0, weight=1)

        # load images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "Logo_della_Polizia_Scientifica_no_bg.png")), size=(40, 40))

        self.titolo = ctk.CTkLabel(self, text="    POLIZIA SCIENTIFICA", image=self.logo_image, 
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))   
        self.sottotitolo = ctk.CTkLabel(self, text="    Sezione Indagini Elettroniche", font=ctk.CTkFont(size=13, weight="bold")) 
        self.sottotitolo.grid(row=1, column=0, pady=(5,20))                                                 
        self.titolo.grid(row=0, column=0, padx=20, pady=(20,0))

        # Widget in the frame
        #LABEL 1
        self.label1 = ctk.CTkLabel(self.frame_laterale, text="1- Load data file with FFT value")
        self.label1.grid(row=0, columnspan=5, pady=(10, 15), sticky="nwe")
        #BUTTON 1
        self.button_txt = ctk.CTkButton(self.frame_laterale, text="Load_txt", command=self.load_txt)
        self.button_txt.grid(row=1, columnspan=5, padx=20, sticky="nwe")
        #BUTTON LOAD WAVE
        self.button_wave = ctk.CTkButton(self.frame_laterale, text="Load_wave", command=self.load_wave)
        self.button_wave.grid(row=2, columnspan=5, padx=20, pady=(10,15), sticky="nwe")

        #LABEL 2
        self.label2 = ctk.CTkLabel(self.frame_laterale, text="2- Plot entire FFT in dbSPL")
        self.label2.grid(row=3, columnspan=5, pady=(35, 15), sticky="nwe")
        #BUTTON 2
        self.button = ctk.CTkButton(self.frame_laterale, text="Plot_entire_FFT", command=self.plot_entire_fft)
        self.button.grid(row=4, columnspan=5,padx=20, sticky="nwe")
        #BUTTON 3
        self.button = ctk.CTkButton(self.frame_laterale, text="Plot_entire_FFT + audibility curves", command=self.plot_fft_on_audibility_curves)
        self.button.grid(row=5, columnspan=5,padx=20, pady=(10, 15), sticky="nwe")

        #LABEL 3
        self.label3 = ctk.CTkLabel(self.frame_laterale, text="3- Plot selected frequency")
        self.label3.grid(row=6, columnspan=5, pady=(30, 15), sticky="nwe")
        #WIDGET FOR PLOT THE SELECTED FREQUENCY
        #ENTRY 1
        self.entry1 = ctk.CTkEntry(self.frame_laterale, width=60, placeholder_text="FREQ_1")
        self.entry1.grid(row=7, column=0, padx=5, pady=5)
        self.entry1.insert(0, "0")  # Imposta il valore di default
        #ENTRY 2
        self.entry2 = ctk.CTkEntry(self.frame_laterale, width=60, placeholder_text="FREQ_2")
        self.entry2.grid(row=7, column=1, padx=5, pady=5)
        self.entry2.insert(0, "0")  # Imposta il valore di default
        #ENTRY 3
        self.entry3 = ctk.CTkEntry(self.frame_laterale, width=60, placeholder_text="FREQ_3")
        self.entry3.grid(row=7, column=2, padx=5, pady=5)
        self.entry3.insert(0, "0")  # Imposta il valore di default
        #ENTRY 4
        self.entry4 = ctk.CTkEntry(self.frame_laterale, width=60, placeholder_text="FREQ_4")
        self.entry4.grid(row=7, column=3, padx=5, pady=5)
        self.entry4.insert(0, "0")  # Imposta il valore di default
        #ENTRY 5
        self.entry5 = ctk.CTkEntry(self.frame_laterale, width=60, placeholder_text="FREQ_5")
        self.entry5.grid(row=7, column=4, padx=5, pady=5)
        self.entry5.insert(0, "0")  # Imposta il valore di default
        #BUTTON 4
        self.button = ctk.CTkButton(self.frame_laterale, text="Plot selected frequency", command=self.plot_selected_freq)
        self.button.grid(row=8, columnspan=5,padx=20, pady=(10, 15), sticky="nwe")

        #LABEL 4
        self.label4 = ctk.CTkLabel(self.frame_laterale, text="4- Plot given frequencies")
        self.label4.grid(row=9, columnspan=5, pady=(20, 15), sticky="nwe")
        #BUTTON 5
        self.button = ctk.CTkButton(self.frame_laterale, text="Plot given frequencies", command=self.plot_given_frequencies)
        self.button.grid(row=10, columnspan=5, padx=20, sticky="nwe")

        #LABEL 5
        self.label5 = ctk.CTkLabel(self.frame_laterale, text="5- Plot wave file")
        self.label5.grid(row=11, columnspan=5, pady=(50, 15), sticky="nwe")
        #BUTTON 6
        self.button = ctk.CTkButton(self.frame_laterale, text="Plot wave file", command=self.plot_wave_file)
        self.button.grid(row=12, columnspan=5, padx=20, pady=(0, 15), sticky="nwe")
       
    def load_txt(self):
        print("Load_txt button pressed")
        input_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if input_file_path:
            print(f"File loaded: {input_file_path}")
            # Segnalo che il file è stato caricato correttamente
            self.button_txt.configure(fg_color="green")
            with open(input_file_path, 'r') as file:
                lines = file.readlines()
            # Delete first line and put in the same place "FREQUENZA DECIBEL"
            lines[0] = "FREQUENZA   DECIBEL\n"

            # Change coma with decimal point
            lines = [line.replace(',', '.') for line in lines]

            # Write new data in a MODIFIED new file
            global output_file_path
            output_file_path = input_file_path.replace('.txt', '_MODIFIED.txt')
            with open(output_file_path, 'w') as file:
                 file.writelines(lines)
                 print(f"Output path: {output_file_path}")

    def load_wave(self):
        print("Load_wave button pressed")
        global input_file_path_wav
        input_file_path_wav = filedialog.askopenfilename(filetypes=[("Text files", "*.wav")])
        if input_file_path_wav:
            print(f"File loaded: {input_file_path_wav}")
            # Segnalo che il file è stato caricato corettamente
            self.button_wave.configure(fg_color="green")
       
    def plot_entire_fft(self):
        with open(output_file_path, 'r') as file:
            # Salta la prima riga
            next(file)
            # Leggi le colonne di dati
            data = np.loadtxt(file)

        # Estrai le colonne di dati
        frequenze = data[:, 0]
        ampiezze_decibel = data[:, 1]

        # Crea il grafico
        plt.figure(figsize=(10, 6))
        plt.plot(frequenze, ampiezze_decibel, marker='.', label='FFT')
        plt.xscale('log')  # Scala logaritmica per coprire l'intero range di frequenza
        plt.title('FFT [dbSPL]')
        plt.xlabel('Frequenza [Hz]')
        plt.ylabel('Ampiezza [dBSPL]')
        plt.grid(True)
        plt.legend(loc='upper left')
        
        plt.show()

    def plot_fft_on_audibility_curves(self):
        # Leggi i dati dal file di testo
        with open(output_file_path, 'r') as file:
            # Salta la prima riga
            next(file)
            # Leggi le colonne di dati
            data = np.loadtxt(file)

        # Estrai le colonne di dati
        frequenze = data[:, 0]
        ampiezze_decibel = data[:, 1]

        # Leggi il file CSV delle curve isofoniche
        file_path = "C:\\Users\\elpup\\Documents\\progetti\\test_audibilita\\Plot_fft\\Valori_curve_isofoniche.csv"
        data = pd.read_csv(file_path, delimiter=';')

        # Crea il grafico
        plt.figure(figsize=(10, 6))
        # Plot FFT
        plt.plot(frequenze, ampiezze_decibel, marker='.', label='FFT')

        # Plotta le curve isofoniche
        for colonna in data.columns[1:]:
            plt.plot(data['Frequenza (Hz)'], data[colonna], color='black')

            # Etichetta del numero di phon al centro della curva con offset verticale
            x_center = data['Frequenza (Hz)'].iloc[len(data) // 2]
            y_center = data[colonna].iloc[len(data) // 2]
            offset = 5  # Puoi regolare questo valore in base alle tue esigenze
            plt.text(x_center + 14000, y_center + offset, f'{colonna}', fontsize=10, ha='left', va='bottom')

        # Etichetta "Soglia di udibilità" in basso a sinistra
        threshold_label_x = data['Frequenza (Hz)'].iloc[0]
        threshold_label_y = min(data.min()) + 30  # Sposta il testo leggermente sotto il grafico
        plt.text(threshold_label_x, threshold_label_y, 'Soglia di udibilità', fontsize=10, ha='left', va='bottom')
       
        # Freccia che parte dalla scritta "Soglia di udibilità" e va verso l'alto
        arrow_x = threshold_label_x + 17
        arrow_y = threshold_label_y + 25  # Altezza della freccia
        plt.annotate('', xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y - 20),arrowprops=dict(facecolor='black', arrowstyle='->'), ha='center', va='bottom')

        # Configura il grafico
        plt.xscale('log')  # Scala logaritmica per coprire l'intero range di frequenza
        plt.title('FFT [dbSPL]')
        plt.xlabel('Frequenza [Hz]')
        plt.ylabel('Ampiezza [dBSPL]')
        plt.grid(True)
        plt.legend(loc='upper left')

        # Aggiungi griglia orizzontale per facilitare la lettura delle curve
        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
        
        plt.show()
    
    def plot_selected_freq(self):
        # Leggi i dati dal file di testo
        with open(output_file_path, 'r') as file:
            # Salta la prima riga
            next(file)
            # Leggi le colonne di dati
            data_fft = np.loadtxt(file)

        # Estrai le colonne di dati
        frequenze = data_fft[:, 0]
        ampiezze_decibel = data_fft[:, 1]

        # Leggi il file CSV delle curve isofoniche
        file_path = "C:\\Users\\elpup\\Documents\\progetti\\test_audibilita\\Plot_fft\\Valori_curve_isofoniche.csv"
        data = pd.read_csv(file_path, delimiter=';')

        # Crea il grafico
        plt.figure(figsize=(10, 6))

        # Plotta le curve isofoniche
        for colonna in data.columns[1:]:
            plt.plot(data['Frequenza (Hz)'], data[colonna], color='black')

            # Etichetta del numero di phon al centro della curva con offset verticale
            x_center = data['Frequenza (Hz)'].iloc[len(data) // 2]
            y_center = data[colonna].iloc[len(data) // 2]
            offset = 5  # Puoi regolare questo valore in base alle tue esigenze
            plt.text(x_center + 14000, y_center + offset, f'{colonna}', fontsize=10, ha='left', va='bottom')

        # Aggiungi griglia orizzontale per facilitare la lettura delle curve
        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)

        # Leggo i valori messi nelle entry
        frequenze_utente = [
            float(self.entry1.get()),
            float(self.entry2.get()),
            float(self.entry3.get()),
            float(self.entry4.get()),
            float(self.entry5.get()),
        ]

        print("Valori letti:", frequenze_utente)

        # Inizializza le liste per i dati da visualizzare nel grafico a dispersione
        frequenze_vicine = []
        decibel_corrispondenti = []

        # Trova il valore più vicino per ciascuna frequenza inserita
        for frequenza_utente in frequenze_utente:
            # Faccio la differenza tra tutte le frequenze e quella inserita e poi di questo vettore prendo il più piccolo (argmin()) quindi mi avvicino il più possibile al valore inserito
            indice_piu_vicino = np.abs(frequenze - frequenza_utente).argmin()
            valore_piu_vicino_frequenza = data_fft[indice_piu_vicino, 0]
            valore_piu_vicino_decibel = data_fft[indice_piu_vicino, 1]
            
            print(f"Frequenza inserita: {frequenza_utente}, Frequenza più vicina: {valore_piu_vicino_frequenza}, Valore più vicino in decibel: {valore_piu_vicino_decibel}") 

            # Aggiungi i dati alle liste
            frequenze_vicine.append(valore_piu_vicino_frequenza)
            decibel_corrispondenti.append(valore_piu_vicino_decibel)

        # Crea un diagramma a dispersione con simboli diversi per ciascun valore in decibel_corrispondenti
        simboli = ['o', 's', '^', '*', 'D']  # Puoi aggiungere altri simboli se necessario
        for i, (frequenza, decibel) in enumerate(zip(frequenze_vicine, decibel_corrispondenti)):
            #plt.scatter(frequenza, decibel, label=f'Punto {i + 1}', marker=simboli[i], s=100)
            plt.scatter(frequenza, decibel, label=f'{frequenze_vicine[i]} Hz --> {decibel_corrispondenti[i]} dBSPL', marker=simboli[i], s=100)
        
        # Etichetta "Soglia di udibilità" in basso a sinistra
        threshold_label_x = data['Frequenza (Hz)'].iloc[0]
        threshold_label_y = min(data.min()) + 30  # Sposta il testo leggermente sotto il grafico
        plt.text(threshold_label_x, threshold_label_y, 'Soglia di udibilità', fontsize=10, ha='left', va='bottom')
       
        # Freccia che parte dalla scritta "Soglia di udibilità" e va verso l'alto
        arrow_x = threshold_label_x + 17
        arrow_y = threshold_label_y + 25  # Altezza della freccia
        plt.annotate('', xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y - 20),arrowprops=dict(facecolor='black', arrowstyle='->'), ha='center', va='bottom')

        # Configura il grafico
        plt.xscale('log')  # Scala logaritmica per coprire l'intero range di frequenza
        plt.title('FFT [dbSPL]')
        plt.xlabel('Frequenza [Hz]')
        plt.ylabel('Ampiezza [dBSPL]')
        plt.grid(True)
        plt.legend(loc='upper left')
         
        plt.show()

    def plot_given_frequencies(self):
        # Leggi i dati dal file di testo
        with open(output_file_path, 'r') as file:
            # Salta la prima riga
            next(file)
            # Leggi le colonne di dati
            data_fft = np.loadtxt(file)

        # Estrai le colonne di dati
        frequenze = data_fft[:, 0]
        ampiezze_decibel = data_fft[:, 1]

        # Leggi il file CSV delle curve isofoniche
        file_path = "C:\\Users\\elpup\\Documents\\progetti\\test_audibilita\\Plot_fft\\Valori_curve_isofoniche.csv"
        data = pd.read_csv(file_path, delimiter=';')

        # Crea il grafico
        plt.figure(figsize=(10, 6))

        # Plotta le curve isofoniche
        for colonna in data.columns[1:]:
            plt.plot(data['Frequenza (Hz)'], data[colonna], color='black')

            # Etichetta del numero di phon al centro della curva con offset verticale
            x_center = data['Frequenza (Hz)'].iloc[len(data) // 2]
            y_center = data[colonna].iloc[len(data) // 2]
            offset = 5  # Puoi regolare questo valore in base alle tue esigenze
            plt.text(x_center + 14000, y_center + offset, f'{colonna}', fontsize=10, ha='left', va='bottom')

        # Aggiungi griglia orizzontale per facilitare la lettura delle curve
        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)

        #  Frequenze date
        frequenze_date = [100.0, 600.0, 1100.0, 1600.0, 2100.0, 2600.0, 3100.0, 3600.0, 4100.0, 4600.0]
        frequenze_vicine = []
        decibel_corrispondenti = []

        # Trova il valore più vicino per ciascuna frequenza inserita
        for frequenza_data in frequenze_date:
            # Faccio la differenza tra tutte le frequenze e quella inserita e poi di questo vettore prendo il più piccolo (argmin()) quindi mi avvicino il più possibile al valore inserito
            indice_piu_vicino = np.abs(frequenze - frequenza_data).argmin()
            valore_piu_vicino_frequenza = data_fft[indice_piu_vicino, 0]
            valore_piu_vicino_decibel = data_fft[indice_piu_vicino, 1]
            
            print(f"Frequenza inserita: {frequenza_data}, Frequenza più vicina: {valore_piu_vicino_frequenza}, Valore più vicino in decibel: {valore_piu_vicino_decibel}") 

            # Aggiungi i dati alle liste
            frequenze_vicine.append(valore_piu_vicino_frequenza)
            decibel_corrispondenti.append(valore_piu_vicino_decibel)

        # Crea un diagramma a dispersione con simboli diversi per ciascun valore in decibel_corrispondenti
        simboli = ['o', 's', '^', '*', 'D', '.', 'p', 'H', 'X', '2']  # Puoi aggiungere altri simboli se necessario
        for i, (frequenza, decibel) in enumerate(zip(frequenze_vicine, decibel_corrispondenti)):
            #plt.scatter(frequenza, decibel, label=f'Punto {i + 1}', marker=simboli[i], s=100)
            plt.scatter(frequenza, decibel, label=f'{frequenze_vicine[i]} Hz --> {decibel_corrispondenti[i]} dBSPL', marker=simboli[i], s=100)
        
        # Etichetta "Soglia di udibilità" in basso a sinistra
        threshold_label_x = data['Frequenza (Hz)'].iloc[0]
        threshold_label_y = min(data.min()) + 30  # Sposta il testo leggermente sotto il grafico
        plt.text(threshold_label_x, threshold_label_y, 'Soglia di udibilità', fontsize=10, ha='left', va='bottom')
       
        # Freccia che parte dalla scritta "Soglia di udibilità" e va verso l'alto
        arrow_x = threshold_label_x + 17
        arrow_y = threshold_label_y + 25  # Altezza della freccia
        plt.annotate('', xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y - 20),arrowprops=dict(facecolor='black', arrowstyle='->'), ha='center', va='bottom')

        # Configura il grafico
        plt.xscale('log')  # Scala logaritmica per coprire l'intero range di frequenza
        plt.title('FFT [dbSPL]')
        plt.xlabel('Frequenza [Hz]')
        plt.ylabel('Ampiezza [dBSPL]')
        plt.grid(True)
        plt.legend(loc='upper left')
         
        plt.show()

    def plot_wave_file(self):
        # Load wave file
        data, sample_rate = sf.read(input_file_path_wav)

        # Se il file ha più canali, prendi solo uno (ad esempio, il primo)
        if len(data.shape) > 1:
            print("ERROR: Stereo files are not supported. Please use only mono wave files.")
            print("I'LL USE ONLY CHANNEL 0 OF THIS WAV FILE")
            data = data[:, 0]

        # Calcola l'FFT per l'intero segnale
        spectrum = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(spectrum), 1/sample_rate)

        # Normalizzazione lineare
        spectrum /= len(data)

        # Solo frequenze positive e spettro positivo
        positive_frequencies = frequencies[:len(frequencies)//2]
        positive_spectrum = np.abs(spectrum[:len(spectrum)//2])

        # Risolvi il problema di log10(0)
        epsilon = 1e-6
        positive_spectrum_with_epsilon = positive_spectrum + epsilon

        # Calcola lo spettro di magnitudine in dB (scala logaritmica)
        spectrum_dB = 20 * np.log10(positive_spectrum_with_epsilon)

        # Crea il plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

        # Plot del segnale audio nel dominio del tempo
        ax1.plot(np.arange(len(data)) / sample_rate, data)
        ax1.set_title('Segnale Audio nel Dominio del Tempo')
        ax1.set_xlabel('Tempo (s)')
        ax1.set_ylabel('Ampiezza')
        ax1.grid(True)

        # Plot dell'FFT per l'intero segnale
        ax2.plot(positive_frequencies, spectrum_dB, color="red")
        ax2.set_xscale('log')  # Imposta l'asse x in scala logaritmica
        #ax2.set_xticks([30, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])  # Imposta ticks personalizzati
        #ax2.get_xaxis().set_major_formatter(plt.ScalarFormatter())  # Utilizza una formattazione standard
        ax2.set_xlim(30, sample_rate / 2)
              
        ax2.set_title('Spettro di Ampiezza in dB (FFT sull\'intero segnale)')
        ax2.set_xlabel('Frequenza (Hz)')
        ax2.set_ylabel('Ampiezza (dB)')
        ax2.grid(True)

        # Mostra il plot
        plt.tight_layout()
        plt.show()


main_window = App()
ctk.set_appearance_mode("dark")

num_colonne = main_window.grid_size()[0]
print(f"La finestra ha {num_colonne} colonne.")

main_window.mainloop()
