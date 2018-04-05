import pandas as pd


def make_tidy_albums_df(albums_df, songs_df):
    # make `wide_df` where each song gets a column
    frames = [
        albums_df,
        pd.DataFrame(albums_df['track_list'].tolist())]
    wide_df = pd.concat(frames, axis=1)

    # "melt" wide_df into tidy format
    song_cols = [x for x in wide_df.columns if isinstance(x, int)]
    tidy_albums = wide_df.melt(
        id_vars=['title', 'year'], var_name='track_num',
        value_vars=song_cols, value_name='song')

    # Merge with songs_df
    _df = songs_df[['title', 'author']].rename(columns={'title': 'song'})
    full_df = pd.merge(
        left=tidy_albums, right=_df, on='song')

    # sort by title then track number
    return (full_df.sort_values(['title', 'track_num'])
            .dropna()
            .reset_index(drop=True))


def get_album_data(albums_df, songs_df, attr):
    """attr should be 'author' or 'album' """
    full_df = make_tidy_albums_df(albums_df, songs_df)
    if attr == 'author':
        return get_data_author(full_df)
    elif attr == 'album':
        return get_data_album(full_df, albums_df)


def get_counts(df, col):
    _counts = df[col].value_counts()
    return (_counts.to_frame(name='count')
            .reset_index()
            .rename(columns={'index': col}))


def get_data_author(full_df):
    df = pd.merge(
        get_counts(full_df.query("author == 'Bob Dylan'"), 'year'),
        get_counts(full_df.query("author != 'Bob Dylan'"), 'year'),
        on='year', suffixes=('_bob', '_other'))

    return (df.sort_values('year')
            .reset_index(drop=True)
            .rename({'count_bob': 'original', 'count_other': 'cover'},
                    axis='columns'))


def get_data_album(full_df, albums_df):
    alb_counts = get_counts(full_df, 'title')
    merge_df = pd.merge(alb_counts, albums_df)
    pivot_df = (merge_df
                .pivot(index='year', columns='title', values='count')
                .reset_index()
                .fillna(0))
    pivot_df.columns.name = None
    return pivot_df


def resize_list(lst, target_len):
    lst = lst[:target_len]
    if len(lst) == target_len:
        return lst
    else:
        return resize_list(lst * 2, target_len)
