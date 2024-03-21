import streamlit as st
import pandas as pd
from time import sleep
import random

st.title('📖 Woordjes')





if 'woordjes' not in  st.session_state:
    st.session_state['woordjes'] = None
    
if 'placeholder' not in  st.session_state:
    st.session_state['placeholder'] = True    
    
if 'history' not in  st.session_state:
    st.session_state['history'] = None
    
if 'index' not in  st.session_state:
    st.session_state['index'] = 0
    
if 'finished' not in  st.session_state:
    st.session_state['finished'] = False


tabs = st.tabs(['Woordenlijst','Oefenen'])

with tabs[0]:
    
    st.subheader('Woordenlijst')
    
    with st.container(border=True):
        collies = st.tabs(['Kant en klaar','Uploaden','Handmatig'])
    
    with collies[0]:
        if st.button('Spaans'):
            df = pd.read_csv('nl-sp.csv')
            st.session_state['woordjes'] = df.sample(frac = 1).reset_index(drop=True)
            
            st.session_state['history'] = {'goed':0,'fout':0, 'te gaan':len(st.session_state['woordjes']['Nederlands'])}
            st.session_state['index'] = 0
            st.session_state['placeholder'] = False
            st.success('het staat er in maatj')
            sleep(2)
            st.rerun()
        if st.button('Engels'):
            df = pd.read_csv('nl-eng.csv')
            st.session_state['woordjes'] = df.sample(frac = 1).reset_index(drop=True)

            st.session_state['history'] = {'goed':0,'fout':0, 'te gaan':len(st.session_state['woordjes']['Nederlands'])}
            st.session_state['index'] = 0
            st.session_state['placeholder'] = False
            st.success('het staat er in maatj')
            sleep(2)
            st.rerun()
        
        if st.button('Portugees'):
            df = pd.read_csv('nl-port.csv')
            st.session_state['woordjes'] = df.sample(frac = 1).reset_index(drop=True)

            st.session_state['history'] = {'goed':0,'fout':0, 'te gaan':len(st.session_state['woordjes']['Nederlands'])}
            st.session_state['index'] = 0
            st.session_state['placeholder'] = False
            st.success('het staat er in maatj')
            sleep(2)
            st.rerun()
       
    with collies[1]:
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.DataFrame([{"Nederlands": "Hallo", "Spaans":'Hola'}])
            
        if st.button('Sla op'):
            st.session_state['woordjes'] = df.sample(frac = 1).reset_index(drop=True)
            st.session_state['history'] = {'goed':0,'fout':0, 'te gaan':len(st.session_state['woordjes']['Nederlands'])}
            st.session_state['index'] = 0
            st.session_state['placeholder'] = False
            st.success('het staat er in maatj')
            
            sleep(2)
            st.rerun()       
        
        
        
    with collies[2]:  
        edited_df = st.data_editor(df, num_rows='dynamic')
        df = edited_df.sample(frac = 1).reset_index(drop=True)
    
    
    
        if st.button('Sla op', key=3):
            st.session_state['woordjes'] = df
            st.session_state['history'] = {'goed':0,'fout':0, 'te gaan':len(st.session_state['woordjes']['Nederlands'])}
            st.session_state['index'] = 0
            st.session_state['placeholder'] = False
            st.success('het staat er in maatj')
            
            sleep(2)
            st.rerun()
        
        


with tabs[1]:
    
    
    
    if not st.session_state['placeholder']:
    
        dic = st.session_state['woordjes']

        vanuit = st.radio('Vanuit',options=['Nederlands',st.session_state['woordjes'].columns[1]], horizontal=True)
        
        index = st.session_state['index']
        
        if vanuit=='Nederlands':
            woord_van = dic['Nederlands'][index]
            woord_naar =  dic[st.session_state['woordjes'].columns[1]][index]
        elif vanuit==st.session_state['woordjes'].columns[1]:
            woord_van = dic[st.session_state['woordjes'].columns[1]][index]
            woord_naar =  dic['Nederlands'][index]

        

        cols = st.columns(2)
        
        with cols[0]:
            
            # Het is nog niet afgerond
            if not st.session_state['finished']:
                with st.container(border=True):
                    
                    invoer = st.text_input(label=woord_van)

                    # De knop is ingedrukt
                    if st.button('check'):
                        
                        is_goed = invoer.lower()==woord_naar.lower()
                        nu_de_laatste = st.session_state['index'] + 1 == len(dic['Nederlands'])
                        
                        # Dit moet sws
                        st.session_state['history']['te gaan'] -= 1
                        
                        # Is het goed?
                        if is_goed:
                            st.session_state['history']['goed'] += 1
                            st.success('Nice')
                            sleep(1)
                        else:
                            st.session_state['history']['fout'] += 1
                            st.error(woord_naar)
                            sleep(2)
                        
                        # De laatste?    
                        if not nu_de_laatste:
                            st.session_state['index'] += 1
                        else:
                            st.session_state['finished'] = True
                        
                        # Alles gedaan, dan refreshen
                        st.rerun()    
                        

            # wel klaar
            else:
                st.info('Het zit erop gap')
                if st.button('Again :)'):
                    st.session_state['woordjes'] = st.session_state['woordjes'].sample(frac = 1).reset_index(drop=True)
                    st.session_state['history'] = {'goed':0,'fout':0, 'te gaan':len(st.session_state['woordjes']['Nederlands'])}
                    st.session_state['index'] = 0
                    st.session_state['finished'] = False
                    sleep(1)

                    st.rerun()
                    
                
            
        with cols[1]:    
            with st.container(border=True):
                st.write('Verhouding')

                his =  st.session_state['history']
                
                df2 = pd.DataFrame({0:{'Goed':his['goed'], 'Fout':his['fout']}}).T
                
                
                bar_goed = st.progress(0, text='voortgang')
                bar_fout = st.progress(0, text='voortgang')
                
                if st.session_state['index'] == 0:
                    bar_goed.progress(his['goed']/ (st.session_state['index']+1), f"{his['goed']} goed")
                    bar_fout.progress(his['fout']/ (st.session_state['index']+1), f"{his['fout']} fout")
                    pass
                else:
                    bar_goed.progress(his['goed']/ (st.session_state['index']), f"{his['goed']} goed")
                    bar_fout.progress(his['fout']/ (st.session_state['index']), f"{his['fout']} fout")
                
                
                #st.dataframe(df2, hide_index=True)
 
 
        my_bar = st.progress(0, text='voortgang')
        index = st.session_state['index']
        hoeveelheid = len(st.session_state['woordjes']['Nederlands'])
        my_bar.progress(index/hoeveelheid, text=f"{index+1}e van de {hoeveelheid}")                
                
    else:
        st.error('Sla eerst je woordjes op')
            
