import pandas as pd
import numpy as np
import plotly.express as px
from plotly import graph_objects as go
from plotly.subplots import make_subplots
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

def create_operation_plot(
    plan_events: list,
    plan_days: list,
    plan_start_depths: list,
    plan_end_depths: list,
    plan_costs: list,
    actual_events: list = [],
    actual_days: list = [],
    actual_start_depths: list = [],
    actual_end_depths: list = [],
    actual_costs: list = [],
):

    plan_cumulative_days_start = np.cumsum([0] + plan_days[:-1])
    plan_cumulative_days_end = np.cumsum(plan_days)

    actual_cumulative_days_start = np.cumsum([0] + actual_days[:-1])
    actual_cumulative_days_end = np.cumsum(actual_days)

    fig = make_subplots(
    # rows=2, cols=1,
    # shared_xaxes=True,
    # vertical_spacing=0.12,
    specs=[[{"secondary_y": True}],
            #  [{"type": "table"}]
            ]
    )

    for i in range(len(plan_events)):

        o = 'left'

        days = [plan_cumulative_days_start[i], plan_cumulative_days_end[i]]
        depths = [plan_start_depths[i], plan_end_depths[i]]
        fig.add_trace(
            go.Scatter(
                x=days,
                y=depths,
                line=dict(width=2),
                name='Planned Operation',
                showlegend=False if i!= len(plan_events)-1 else True,
                marker_color = colors[0]
                ),
            # row=1, col=1
            )

        center_days = ((days[1]-days[0])/2)+days[0]
        center_depths = ((depths[1]-depths[0])/2)+depths[0]

        fig.add_annotation(
            x=center_days,
            y=center_depths,
            xshift=2,
            text=i+1,
            showarrow=True,
            ax=-30,
            ay=25,
            font=dict(
                family="Arial",
                size=16,
                color='black'
            ),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            opacity=0.8
            )

    for i in range(len(actual_events)):

        o = 'right'

        days = [actual_cumulative_days_start[i], actual_cumulative_days_end[i]]
        depths = [actual_start_depths[i], actual_end_depths[i]]
        fig.add_trace(
            go.Scatter(
                x=days,
                y=depths,
                line=dict(width=2),
                name='Actual Operation',
                showlegend=False if i!= len(actual_events)-1 else True,
                marker_color = colors[1]
                ),
            # row=1, col=1
            )

        center_days = ((days[1]-days[0])/2)+days[0]
        center_depths = ((depths[1]-depths[0])/2)+depths[0]

        fig.add_annotation(
            x=center_days,
            y=center_depths,
            xshift=2,
            text=i+1,
            showarrow=True,
            ax=25,
            ay=-30,
            font=dict(
                family="Arial",
                size=16,
                color='black'
            ),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            opacity=0.8
            )

    fig.add_trace(
        go.Scatter(
            x=plan_cumulative_days_end,
            y=np.cumsum(plan_costs),
            line=dict(width=2, dash='dash'),
            name='Planned Cost',
            marker_color=colors[5],
            xaxis='x1',
            yaxis='y2',
            ),
        secondary_y=True,
        # row=1, col=1
        )

    fig.add_trace(
        go.Scatter(
            x=actual_cumulative_days_end,
            y=np.cumsum(actual_costs),
            line=dict(width=2, dash='dash'),
            name='Actual Cost',
            marker_color=colors[6],
            xaxis='x1',
            yaxis='y2',
            ),
        secondary_y=True,
        # row=1, col=1
        )


    table_data = pd.DataFrame({
        'Event': plan_events,
        'Days': plan_days,
        'Start Depth': plan_start_depths,
        'End Depth': plan_end_depths,
        'Cost': plan_costs
    })

    # fig.add_trace(
    #     go.Table(
    #         header=dict(
    #             values=['Event','Days','Start Depth','End Depth','Cost'],
    #             line_color='darkslategray',
    #             fill_color='royalblue',
    #             align=['left','center'],
    #             font=dict(color='white', size=12),
    #             height=40
    #         ),
    #         cells=dict(
    #             values=[plan_events,
    #                     plan_days,
    #                     plan_start_depths,
    #                     plan_end_depths,
    #                     plan_costs],
    #             line_color='darkslategray',
    #   fill=dict(color=['paleturquoise', 'white']),
    #   align=['left', 'center'],
    #   font_size=12,
    #   height=30)
    #     ),
    #     row=2, col=1
    # )

    fig.update_yaxes(autorange="reversed", secondary_y=False)
    fig.update_layout(template='plotly_white')
    fig.update_layout(
        height=600,
    )
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
            autorange='reversed',
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
        xaxis_title="Days",
        yaxis_title="Depth",
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        ),
        plot_bgcolor='white',
    )
    
    fig_json = fig.to_json(pretty=True, engine="json")
    fig_data = json.loads(fig_json)

    return {
        'table': table_data,
        'plot': fig_data
    }

def create_well_path(
    df_planned_well: pd.DataFrame,
    planned_casing_end_depths: list,
    df_actual_well: pd.DataFrame = pd.DataFrame(),
    actual_casing_end_depths: list = [],
    ):

    fig = go.Figure()

    # Plot planned well trajectory
    x = df_planned_well['east']
    y = df_planned_well['md']

    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Planned Well Trajectory'))

    # Add planned casings
    for i, end_depth in enumerate(planned_casing_end_depths):
        index = (y - end_depth).abs().idxmin()

        x_image = x[index]
        y_casing = y[index]

        fig.add_trace(go.Scatter(
            x=[x_image], y=[y_casing],
            mode='markers',
            marker=dict(size=10, color='blue'),
            showlegend=False
        ))

        fig.add_annotation(
            x=x_image,
            y=y_casing,
            xshift=2,
            text=f'P-{i+1}',
            showarrow=True,
            ax=-100,
            ay=0,
            font=dict(
                family="Arial",
                size=16,
                color='black'
            ),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            opacity=0.8
        )

    # Plot actual well trajectory if available
    if not df_actual_well.empty:
        x = df_actual_well['east']
        y = df_actual_well['md']

        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Actual Well Trajectory'))

        # Add actual casings
        for i, end_depth in enumerate(actual_casing_end_depths):
            index = (y - end_depth).abs().idxmin()

            x_image = x[index]
            y_casing = y[index]

            fig.add_trace(go.Scatter(
                x=[x_image], y=[y_casing],
                mode='markers',
                marker=dict(size=10, color='red'),
                showlegend=False
            ))

            fig.add_annotation(
                x=x_image,
                y=y_casing,
                xshift=2,
                text=f'A-{i+1}',
                showarrow=True,
                ax=100,
                ay=0,
                font=dict(
                    family="Arial",
                    size=16,
                    color='black'
                ),
                align="center",
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                opacity=0.8
            )

    fig.update_yaxes(autorange="reversed")

    fig.update_layout(
        xaxis_title='East',
        yaxis_title='MD',
    )

    fig.update_layout(template='plotly_white')
    fig.update_layout(
        height=800,
        width=600
    )
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

    fig_json = fig.to_json(pretty=True, engine="json")
    fig_data = json.loads(fig_json)

    return {
        'plot': fig_data
    }

