import streamlit as st
import pandas as pd
import os

# Nome do arquivo CSV onde as reservas serão salvas
CSV_FILE = 'reservations.csv'

# Função para carregar as reservas do arquivo CSV
def load_reservations():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=['Nome', 'Bandejas'])

# Função para salvar as reservas no arquivo CSV
def save_reservations(reservations):
    reservations.to_csv(CSV_FILE, index=False)

# Função principal do aplicativo
def main():
    st.title('Reserva de Bandejas de Ovos')
    st.write('Escolha quantas bandejas de ovos você deseja reservar (1, 2 ou 3). Limite total de 12 bandejas.')

    # Carregar reservas existentes
    reservations = load_reservations()
    total_reserved = reservations['Bandejas'].sum()

    # Formulário de reserva
    with st.form(key='reservation_form'):
        name = st.text_input('Digite seu nome')
        trays = st.selectbox('Escolha o número de bandejas', [1, 2, 3])
        submit_button = st.form_submit_button(label='Reservar')

        if submit_button:
            if total_reserved + trays > 12:
                st.error('Não é possível reservar. Limite de 12 bandejas excedido.')
            else:
                new_reservation = pd.DataFrame({'Nome': [name], 'Bandejas': [trays]})
                reservations = pd.concat([reservations, new_reservation], ignore_index=True)
                save_reservations(reservations)
                st.success('Reserva feita com sucesso!')
                total_reserved = reservations['Bandejas'].sum()

    # Mostrar reservas atuais
    st.write('Reservas atuais:')
    st.table(reservations)

    # Mostrar bandejas restantes
    remaining_trays = 12 - total_reserved
    st.write(f'Bandejas restantes: {remaining_trays}')

if __name__ == '__main__':
    main()
