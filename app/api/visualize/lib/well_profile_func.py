from app.api.visualize.lib.well_profile.well import Well
from plotly.subplots import make_subplots
import json

def render_well_profile(well: Well):
    
    fig_3d = well.plot(
        names=['3D View'],plot_type='3d'
    )
    
    fig_top = well.plot(
        names=['Top View'],plot_type='top'
    )

    fig_vs = well.plot(
        names=['Inclination vs. Depth'],plot_type='vs'
    )
    
    # Create the subplot layout
    fig = make_subplots(
        rows=2, cols=2,
        row_heights=[0.6, 0.4],  # The first row will be larger
        specs=[[{"type": "scene", "colspan": 2}, None],  # The first plot is 3D, spanning both columns
            [{"type": "xy"}, {"type": "xy"}]]  # The second row has 2D plots
)

    # Add traces from fig1 to the first row
    for trace in fig_3d.data:
        fig.add_trace(trace, row=1, col=1)

    # Add traces from fig2 to the second row, first column
    for trace in fig_top.data:
        fig.add_trace(trace, row=2, col=1)

    # Add traces from fig3 to the second row, second column
    for trace in fig_vs.data:
        fig.add_trace(trace, row=2, col=2)

    # Optionally, update layout based on fig1, fig2, or fig3 layout settings
    fig.update_layout(title_text="Well Trajectory")

    # Show the subplot
    fig_json = fig.to_json(pretty=True)
    fig_data = json.loads(fig_json)
    
    return fig_data