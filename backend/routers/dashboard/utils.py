import json
import plotly.graph_objects as go
import plotly.express as px

COLOR_SEQUENCE = px.colors.qualitative.Pastel

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
            t=0,
            b=0
        ),
        plot_bgcolor='white',
    )
    
    fig.update_traces(marker=dict(colors=COLOR_SEQUENCE))

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
            t=0,
            b=0
        ),
        plot_bgcolor='white',
    )
    
    fig.update_traces(marker=dict(color=COLOR_SEQUENCE))

    fig_json = fig.to_json(pretty=True, engine="json")
    fig_data = json.loads(fig_json)
    
    return fig_data

def generate_stimulation_graph(stimulation_data: dict):
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Oil', 'Gas'],
        y=[stimulation_data['current_onstream_oil'], stimulation_data['current_onstream_gas']],
        name='Current',
        marker_color=COLOR_SEQUENCE[0]
    ))
    fig.add_trace(go.Bar(
        x=['Oil', 'Gas'],
        y=[stimulation_data['final_onstream_oil'], stimulation_data['final_onstream_gas']],
        name='Final',
        marker_color=COLOR_SEQUENCE[1]
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
            t=0,
            b=0
        ),
        plot_bgcolor='white',
    )

    fig_json = fig.to_json(pretty=True, engine="json")
    fig_data = json.loads(fig_json)
    
    return fig_data

