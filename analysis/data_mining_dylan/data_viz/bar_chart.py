from bokeh.core.properties import value
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Category20_20
from bokeh.models import HoverTool

from ..data_prep import get_album_data


def make_bar_chart(albums_df, songs_df, cross='author'):
    data = get_album_data(albums_df, songs_df, cross)
    categories = list(data.columns)[1:]
    colors = resize_list(Category20_20, len(categories))

    source = ColumnDataSource(data=data)

    p = figure(
        plot_height=350,
        title="# Songs Released by Year",
        toolbar_location=None, tools="")

    legend = [value(x) for x in categories] if len(categories) < 10 else None
    renderers = p.vbar_stack(
        categories, x='year', width=0.9,
        color=colors, source=source,
        legend=legend, name=categories)

    for r in renderers:
        cat = r.name
        hover = HoverTool(
            tooltips=[("year", '@year'), (cross, cat), ("songs", "@{%s}" % cat)],
            renderers=[r])
        p.add_tools(hover)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    return p


def resize_list(lst, target_len):
    lst = lst[:target_len]
    if len(lst) == target_len:
        return lst
    else:
        return resize_list(lst * 2, target_len)
