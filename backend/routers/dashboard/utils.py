import json
import plotly.graph_objects as go

def generate_pie_chart(data: list, labels: list):
    
    import plotly.graph_objects as go
    
    fig = go.Figure(data=[
        go.Pie(labels=labels, values=data)
    ])

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
    
    return fig_data

def generate_vs_bar_graph(x_axis: list, y_axis: list, orientation: str = 'v'):
    
    colors = ['blue','red']

    fig = go.Figure(data=[go.Bar(
        x=x_axis if orientation == 'v' else y_axis,
        y=y_axis if orientation == 'v' else x_axis,
        orientation=orientation,
        marker_color=colors # marker color can be a single color value or an iterable
    )])

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
    
    return fig_data

def generate_stimulation_graph(stimulation_data: dict):
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Oil Before', 'Gas Before'],
        y=[stimulation_data['current_onstream_oil'], stimulation_data['current_onstream_gas']],
    ))
    fig.add_trace(go.Bar(
        x=['Final Oil', 'Final Gas'],
        y=[stimulation_data['final_onstream_oil'], stimulation_data['final_onstream_gas']],
    ))

    fig.update_layout(barmode='group')
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
    
    return fig_data