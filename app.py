import streamlit as st
import pandas as pd
from time import sleep
import random

st.header('Woordjes')


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

with st.sidebar:
    st.write(st.session_state)

df = pd.DataFrame(
    [
       {"Nederlands": "Hallo", "Spaans":'Hola'},

   ]
)

tabs = st.tabs(['Woordenlijst','Oefenen'])

with tabs[0]:
    edited_df = st.data_editor(df, num_rows='dynamic')


    df = edited_df.sample(frac = 1).reset_index(drop=True)
    
    if st.button('Sla op'):

       
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

        vanuit = st.radio('Vanuit',options=['Nederlands','Spaans'])
        
        index = st.session_state['index']
        
        if vanuit=='Nederlands':
            woord_van = dic['Nederlands'][index]
            woord_naar =  dic['Spaans'][index]
        elif vanuit=='Spaans':
            woord_van = dic['Spaans'][index]
            woord_naar =  dic['Nederlands'][index]

        

        cols = st.columns(2)
        
        with cols[0]:
            
            if not st.session_state['finished']:
                with st.container(border=True):
                    
                    index = st.session_state['index']
                    
                    invoer = st.text_input(label=woord_van)

                    check = st.button('check')
                    
                    if check:
                        
                        is_goed = invoer==woord_naar
                        nu_de_laatste = index + 1  == len(dic['Spaans'])
                        
                        if nu_de_laatste:
                            st.session_state['finished'] = True
                            if is_goed:
                                st.session_state['history']['goed'] += 1
                                st.session_state['history']['te gaan'] -= 1
                                
                                st.success('Nice')
                                sleep(1)
                                st.rerun()
                            else:
                                st.session_state['history']['fout'] += 1
                                st.session_state['history']['te gaan'] -= 1
                                st.session_state['index'] += 1
                                st.error(f"Het was {woord_naar}, ben je dom?")
                                sleep(3)
                                st.rerun()

                        # Niet de laatste                            
                        else:
                            pass
                            print(3)
                            
                        
                        if is_goed:
                            st.session_state['history']['goed'] += 1
                            st.session_state['history']['te gaan'] -= 1
                            st.session_state['index'] += 1
                            st.success('Nice')
                            sleep(1)
                            st.rerun()
                        else:
                            st.session_state['history']['fout'] += 1
                            st.session_state['history']['te gaan'] -= 1
                            st.session_state['index'] += 1
                            st.error(f"Het was {woord_naar}, ben je dom?")
                            sleep(3)
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
                st.write('Stats')

                his =  st.session_state['history']
                
                df2 = pd.DataFrame({0:{'Goed':his['goed'], 'Fout':his['fout'], 'Te gaan':his['te gaan']}}).T
                
                st.dataframe(df2, hide_index=True)
 
                
                
    else:
        st.error('Sla eerst je woordjes op')
            

