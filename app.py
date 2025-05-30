import streamlit as st
import pandas as pd
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Nome do arquivo CSV onde as reservas serão salvas
CSV_FILE = 'Reservas.csv'

# Função para autenticar e criar uma instância do Google Drive
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

# Função para carregar as reservas do Google Drive
def load_reservations(drive, file_id):
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(CSV_FILE)
    return pd.read_csv(CSV_FILE)

# Função para salvar as reservas no Google Drive
def save_reservations(drive, file_id, reservations):
    reservations.to_csv(CSV_FILE, index=False)
    file = drive.CreateFile({'id': file_id})
    file.SetContentFile(CSV_FILE)
    file.Upload()

# Função principal do aplicativo
def main():
    st.title('Reserva de Bandejas de Ovos')
    st.write('Escolha quantas bandejas de ovos você deseja reservar (1, 2 ou 3). Limite total de 12 bandejas.')

    # Autenticar e criar instância do Google Drive
    drive = authenticate_drive()

    # ID do arquivo CSV no Google Drive (substitua pelo seu)
    file_id = '1KhAY6-Q1HDu3EkHKDtmDsPCmNxlyupjWNk2h5OpXR8o'

    # Carregar reservas existentes
    reservations = load_reservations(drive, file_id)
    total_reserved = reservations['Bandejas'].sum()

    # Formulário de reserva
    with st.form(key='reservation_form'):
        name = st.text_input('Digite seu nome')
        trays = st.selectbox('Escolha o número de bandejas', [1, 2, 3])
        submit_button = st.form_submit_button(label='Reservar')

        if submit_button:
            if not name.strip():
                st.error('Por favor, digite seu nome antes de reservar.')
            elif total_reserved + trays > 12:
                st.error('Não é possível reservar. Limite de 12 bandejas excedido.')
            else:
                new_reservation = pd.DataFrame({'Nome': [name], 'Bandejas': [trays]})
                reservations = pd.concat([reservations, new_reservation], ignore_index=True)
                save_reservations(drive, file_id, reservations)
                st.success(f'Reserva feita com sucesso, {name}!')
                reservations = load_reservations(drive, file_id)
                total_reserved = reservations['Bandejas'].sum()

    # Mostrar reservas atuais
    st.write('Reservas atuais:')
    st.table(reservations)

    # Mostrar bandejas restantes
    remaining_trays = 12 - total_reserved
    st.write(f'Bandejas restantes: {remaining_trays}')

if __name__ == '__main__':
    main()
