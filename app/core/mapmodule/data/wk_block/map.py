import plotly.graph_objects as go


mapboxt = open(".mapbox_token").read().rstrip() #my mapbox_access_token 
lats = [52.370216, 53.2191696,  50.851368, 51.8125626]
lons = [4.895168,  6.5666699, 5.690973, 5.8372264 ]
scatt = go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode='markers',
            hovertext=['Amsterdam', 'Groningen',  'Maastricht', 'Nijmegen'],  
            hoverinfo='text',                 
            below='',                 
            marker=dict(symbol ='marker', size=15, color='blue'))
layout = go.Layout(title_text ='Pin location at a few cities in Netherlands', 
                   title_x =0.5, width=750, height=700,
                   mapbox = dict(center= dict(lat=52.370216, lon=4.895168),            
                                 accesstoken= mapboxt,
                                 zoom=6,
                                 style="light"
                               ))

fig=go.Figure(data=[ scatt], layout =layout)

fig.show()