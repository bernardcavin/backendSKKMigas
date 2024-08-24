import pandas as pd
import numpy as np
import plotly.express as px
import json

colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

def create_gantt_chart(
    events: list,
    plan_start_dates: list,
    plan_end_dates: list,
    actual_start_dates: list = [],
    actual_end_dates: list = [],
):

  df = [dict(Task=events[i], Start=plan_start_dates[i], Finish=plan_end_dates[i], Type='Planned') for i in range(len(events))] + [dict(Task=events[i], Start=actual_start_dates[i], Finish=actual_end_dates[i], Type='Actual') for i in range(len(actual_start_dates))]
  
  plot_colors = {}
  plot_colors['Planned'] =  colors[0]  #specify the color for the 'planned' schedule bars
  plot_colors['Actual'] = colors[1]  #specify the color for the 'actual' schedule bars

  fig = px.timeline(
      df,
      x_start="Start",
      x_end="Finish",
      y="Task",
      color='Type',
      color_discrete_map = plot_colors,
      hover_name="Task",
      pattern_shape='Type',
      )

  fig.update_yaxes(autorange="reversed")          #if not specified as 'reversed', the tasks will be listed from bottom up

  fig.update_layout(
                  bargap=0.1,
                  width=850,
                  height=500,
                  xaxis_title="",
                  yaxis_title="",
                  title_x=0.5,
                  legend_title="",
                  legend = dict(orientation = 'v', xanchor = "center"), #Adjust legend position
              )


  fig.update_layout(template='plotly_white')
  fig.update_layout(
      xaxis=dict(
          showline=True,
          showgrid=False,
          showticklabels=True,
          linecolor='rgb(204, 204, 204)',
          linewidth=2,
          ticks='outside',
          tickfont=dict(
              family='Arial',
              size=12,
              color='rgb(82, 82, 82)',
          ),
      ),
      yaxis=dict(
          showline=True,
          showgrid=True,
          showticklabels=True,
          linecolor='rgb(204, 204, 204)',
          linewidth=2,
          ticks='outside',
          tickfont=dict(
              family='Arial',
              size=12,
              color='rgb(82, 82, 82)',
          ),
      ),
      margin=dict(
          l=0,
          r=0,
          t=50,
          b=0
      ),
      plot_bgcolor='white',
  )

  fig.update_layout(barmode="group")
  
  fig_json = fig.to_json(pretty=True, engine="json")
  fig_data = json.loads(fig_json)

  return {
      'table': df,
      'plot': fig_data
  }
