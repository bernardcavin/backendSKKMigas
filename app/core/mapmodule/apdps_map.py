import dash_mantine_components as dmc
import dash_leaflet as dl
from dash import dcc, html, no_update, callback
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from dash_pydantic_form import ModelForm, fields
from pydantic import BaseModel, Field
import os
from typing import Union, Literal, Optional
import json
import geopandas as gpd
import random
from dash_extensions.javascript import assign

DIR_PREFIX = 'app/core/mapmodule'

def folder_file_list_without_extension(directory):
    filenames_without_extension = []
    for filename in os.listdir(directory):
        base_name, _ = os.path.splitext(filename)
        filenames_without_extension.append(base_name)
    return filenames_without_extension

def read_map_batch_to_dl_geojson(type: Literal['wilayah_kerja', 'lapangan', 'cekungan'], names: list[str]) -> dl.GeoJSON:
    
    gdf = gpd.read_file(f'{DIR_PREFIX}/data/{type}/{names[0]}.json')
    gdf["color_value"] = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    
    if len(names) > 1:
        
        for name in names[1:]:
            
            temp_gdf = gpd.read_file(f'{DIR_PREFIX}/data/{type}/{name}.json')
            temp_gdf["color_value"] = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

            gdf = gdf._append(temp_gdf)
        
    return dl.GeoJSON(data=json.loads(gdf.to_json()), style=render_color, id={'type':'geojson','layer':type}, )

def read_geojson_to_dl_geojson(name: str, color: str = None) -> dl.GeoJSON:
    
    return dl.GeoJSON(data=json.loads(gpd.read_file(f'{DIR_PREFIX}/data/{name}.json').to_json()), style={'color':color} if color is not None else {}, id={'type':'geojson','layer':name})

render_color =  assign("""
    function(feature) {
        return {color: feature.properties.color_value};
    }
""")

class MapScene(BaseModel):
    wilayah_kerja: Optional[list[str]] = Field(default_factory=list) # type: ignore
    lapangan: Optional[list[str]] = Field(default_factory=list) # type: ignore
    basin: Optional[list[str]] = Field(default_factory=list) # type: ignore
    batas_landas_kontinen: bool = Field(default=False)
    batas_laut: bool = Field(default=False)
    zona_ekonomi_ekslusif: bool = Field(default=False)
    
wilayah_kerja_list = folder_file_list_without_extension(
    f'{DIR_PREFIX}/data/wilayah_kerja'
)

lapangan = folder_file_list_without_extension(
    f'{DIR_PREFIX}/data/lapangan'
)

cekungan = folder_file_list_without_extension(
    f'{DIR_PREFIX}/data/cekungan'
)

scene_form = dmc.Stack(
    [
        dmc.MultiSelect(
            data=wilayah_kerja_list,
            label='Wilayah Kerja',
            placeholder='Pilih Wilayah Kerja',
            searchable=True,
            clearable=True,
            comboboxProps={"zIndex": 1200},
            id='wilayah-kerja',
            value=[]
        ),
        dmc.MultiSelect(
            data=lapangan,
            label='Lapangan',
            placeholder='Pilih Lapangan',
            searchable=True,
            clearable=True,
            comboboxProps={"zIndex": 1200},
            id='lapangan',
            value=[]
        ),
        dmc.MultiSelect(
            data=cekungan,
            label='Cekungan',
            placeholder='Pilih Cekungan',
            searchable=True,
            clearable=True,
            comboboxProps={"zIndex": 1200},
            id='cekungan',
            value=[]
        ),
        dmc.Checkbox(
            label='Batas Landas Kontinen',
            checked=False,
            description=dmc.ColorInput(id='color-batas-landas-kontinen',popoverProps={'zIndex': 1200}, value='#FF0000'),
            id='checkbox-batas-landas-kontinen',
        ),
        dmc.Checkbox(
            label='Batas Laut',
            checked=False,
            description=dmc.ColorInput(id='color-batas-laut',popoverProps={'zIndex': 1200}, value='#FFFF00'),
            id='checkbox-batas-laut',
        ),
        dmc.Checkbox(
            label='Zona Ekonomi Ekslusif',
            checked=False,
            description=dmc.ColorInput(id='color-zona-ekonomi-ekslusif',popoverProps={'zIndex': 1200}, value='#0000FF'),
            id='checkbox-zona-ekonomi-ekslusif',
        ),
    ]
)

map = dl.Map(
    center=[-2.600029, 118.015776], 
    attributionControl=False,
    zoom=4, 
    children=[
        dl.TileLayer(
            url='http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',
            maxZoom=20,
            subdomains=['mt0','mt1','mt2','mt3']
        ),
        dl.ScaleControl(
            position="bottomleft"
        ),
        dl.LayerGroup(
            id='layers-control-container'
        )
    ], 
    style={'height': '100vh','width':'100vw'}, 
    id="map"
)

credit = dmc.Paper(
    dmc.Group(
        [
            dmc.Group(
                [
                    dmc.ThemeIcon(
                        size="lg",
                        color="indigo",
                        variant="outline",
                        radius='xl',
                        children=DashIconify(
                            icon='arcticons:networksurvey',width=20
                        ),
                    ),
                    dmc.Text('APDPS Map',size='md',fw=200),
                ],
                gap='sm'
            ),
        ],
        justify='space-between',
    ),
    withBorder=True,
    p='xs',
    radius='md',
    # w=350
)

# layers = dmc.Paper(
#     dmc.Fieldset(
#         legend=dmc.Group(
#             [
#                 DashIconify(icon='ph:stack-light', width=25),
#                 dmc.Title('Layers',size='xl',fw=600),
#             ],
#             gap='sm'
#         ),
#         children=[
#             dmc.ScrollArea(
#                 dmc.Center(
#                     'No layers present'
#                 ),
#                 h=200, 
#                 w=150, 
#                 id='layers-container',
#             )
#         ]
#     ),
#     withBorder=True,
#     p='xs',
#     radius='md',
# )

modal_choose_layers = dmc.Modal(
    [
        dmc.Stack(
            [
                scene_form,
            ],
            m='md'
        ),
        dmc.Flex(
            dmc.Button(
                'Apply',
                color='blue',
                radius='xl',
                n_clicks=0,
                size='md',
                id='button-apply-modal-choose-layers'
            ),
            justify='end'
        )
    ],
    opened=False,
    zIndex=1100,
    id='modal-choose-layers',
    title=dmc.Group(
        [
            DashIconify(icon='ph:stack-light', width=25),
            dmc.Title('Create Scene',size='xl',fw=600),
        ],
        gap='sm'
    ),
    size='xl'
)

button_show_modal_choose_layers = dmc.ActionIcon(
    DashIconify(icon='ph:stack-light', width=20),
    id='button-show-modal-choose-layers',
    variant='default',
    size=40,
    radius='xl',
    n_clicks=0
)

layout = dmc.Group(
    [
        map,
        dmc.Affix(
            dmc.Stack(
                [
                    credit,
                    modal_choose_layers,
                    dmc.Flex(
                        button_show_modal_choose_layers,
                        justify='end'
                    )
                ],
            ),
            position={'top':20,'right':20},
            zIndex=1000,
            style={'max-height':'90vh'}
        ),
        # dmc.Affix(
        #     layers,
        #     position={'bottom':20,'right':20},
        #     zIndex=1000,
        #     style={'max-height':'90vh'}
        # ),
    ],
    gap=0,
)

@callback(
    Output('modal-choose-layers', 'opened'),
    Input('button-show-modal-choose-layers', 'n_clicks'),
    prevent_initial_call=True
)
def show_modal_choose_layers(n_clicks):
    if n_clicks > 0:
        return True
    else:
        raise PreventUpdate

@callback(
    Output('layers-control-container', 'children'),
    Output('modal-choose-layers', 'opened', allow_duplicate=True),
    # Output('layers-container', 'children'),
    Input('button-apply-modal-choose-layers', 'n_clicks'),
    State('wilayah-kerja', 'value'),
    State('lapangan', 'value'),
    State('cekungan', 'value'),
    State('checkbox-batas-landas-kontinen', 'checked'),
    State('checkbox-batas-laut', 'checked'),
    State('checkbox-zona-ekonomi-ekslusif', 'checked'),
    State('color-batas-landas-kontinen', 'value'),
    State('color-batas-laut', 'value'),
    State('color-zona-ekonomi-ekslusif', 'value'),
    prevent_initial_call=True
)
def apply_modal_choose_layers(
    n_clicks, 
    wilayah_kerja, 
    lapangan, 
    cekungan, 
    batas_landas_kontinen, 
    batas_laut, 
    zona_ekonomi_ekslusif,
    color_batas_landas_kontinen,
    color_batas_laut,
    color_zona_ekonomi_eksklusif
    ):
    if n_clicks > 0:
        
        output = []
        layer_checkbox_labels = []
        layer_checkbox_id = []
        # layer_desc = []
        
        if wilayah_kerja:
            output.append(read_map_batch_to_dl_geojson('wilayah_kerja', wilayah_kerja))
            layer_checkbox_labels.append(f'Wilayah Kerja')
            layer_checkbox_id.append('wilayah_kerja')
            # layer_desc.append(
            #     dmc.List(
            #         [
            #             dmc.ListItem(item) for item in wilayah_kerja
            #         ] 
            #     )
            # )
        
        if lapangan:
            output.append(read_map_batch_to_dl_geojson('lapangan', lapangan))
            layer_checkbox_labels.append(f'Lapangan')
            layer_checkbox_id.append('lapangan')
            # layer_desc.append(
            #     dmc.List(
            #         [
            #             dmc.ListItem(item) for item in lapangan
            #         ]
            #     ) 
            # )
        
        if cekungan:
            output.append(read_map_batch_to_dl_geojson('cekungan', cekungan))
            layer_checkbox_labels.append(f'Cekungan')
            layer_checkbox_id.append('cekungan')
            # layer_desc.append(
            #     dmc.List(
            #         [
            #             dmc.ListItem(item) for item in cekungan
            #         ]
            #     ) 
            # )
            
        if batas_landas_kontinen:
            output.append(read_geojson_to_dl_geojson('batas_landas_kontinen', color_batas_landas_kontinen))
            layer_checkbox_labels.append('Batas Landas Kontinen')
            layer_checkbox_id.append('batas_landas_kontinen')
            # layer_desc.append(None)
        
        if batas_laut:
            output.append(read_geojson_to_dl_geojson('batas_laut', color_batas_laut))
            layer_checkbox_labels.append('Batas Laut')
            layer_checkbox_id.append('batas_laut')
            # layer_desc.append(None)
        
        if zona_ekonomi_ekslusif:
            output.append(read_geojson_to_dl_geojson('zona_ekonomi_ekslusif', color_zona_ekonomi_eksklusif))
            layer_checkbox_labels.append('Zona Ekonomi Ekslusif')
            layer_checkbox_id.append('zona_ekonomi_ekslusif')
            # layer_desc.append(None)
        
        # layer_checkbox_output = dmc.CheckboxGroup(
        #     [
        #         dmc.Checkbox(
        #             label=layer,
        #             value=id,
        #             description=desc
        #         ) for layer, id, desc in zip(layer_checkbox_labels, layer_checkbox_id, layer_desc)
        #     ],
        #     id='layers-checkbox-group',
        #     value=layer_checkbox_id
        # )
        
        # final_output = dl.LayersControl(
        #     [
        #         dl.Overlay(layer, name=name, checked=True) for layer,name in zip(output, layer_checkbox_labels)
        #     ],
        #     position='bottomright',
        # )
         
        return output, False
    
    else:
        
        raise PreventUpdate