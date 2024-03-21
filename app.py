import streamlit as st
import pandas as pd
from time import sleep

st.header('Woordjes')


if 'woordjes' not in  st.session_state:
    st.session_state['woordjes'] = None
    
if 'history' not in  st.session_state:
    st.session_state['history'] = None
    
if 'index' not in  st.session_state:
    st.session_state['index'] = 0
    
if 'finished' not in  st.session_state:
    st.session_state['finished'] = False


df = pd.DataFrame(
    [
       {"Nederlands": "Hallo", "Spaans":'Hola'},

   ]
)

tabs = st.tabs(['Woordenlijst','Oefenen'])

with tabs[0]:
    edited_df = st.data_editor(df, num_rows='dynamic')

    st.write()
    if st.button('Sla op'):
        st.session_state['woordjes'] = dict(edited_df)
        st.session_state['history'] = {'goed':0,'fout':0, 'te gaan':len(st.session_state['woordjes']['Nederlands'])}
        st.session_state['index'] = 0
        st.succes('er staat er in maatj')
        st.rerun()
    

with tabs[1]:
    
    if st.session_state['woordjes']:
    
    

    
  
        dic = dict(edited_df)

        #if starter:
            
        cols = st.columns(2)
        
        with cols[0]:
            
            if not st.session_state['finished']:
                with st.container(border=True):
                    
                    index = st.session_state['index']
                    
                    invoer = st.text_input(label=dic['Nederlands'][index])

                    check = st.button('check')
                    
                    if check:
                        
                        is_goed = invoer==dic['Spaans'][index]
                        nu_de_laatste = index + 1  == len(dic['Spaans'])
                        
                        if nu_de_laatste:
                            st.session_state['finished'] = True
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
                                st.error(f"Het was {dic['Spaans'][index]}, ben je dom?")
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
                            st.error(f"Het was {dic['Spaans'][index]}, ben je dom?")
                            sleep(3)
                            st.rerun()
          
           
            # wel klaar
            else:
                st.info('Het zit erop gap')
                if st.button('Again :)'):
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
            
